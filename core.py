"""
Moduł obliczeniowy kalkulatora wielkości próby.

Zawiera funkcje do wyznaczania:
- wartości krytycznych (z, t),
- mocy testu t (niecentralny rozkład t),
- wymaganej liczebności próby dla testów parametrycznych i nieparametrycznych.

Wszystkie funkcje są niezależne od Streamlit i mogą być testowane jednostkowo.
"""

import math
from functools import lru_cache

from scipy.stats import nct, norm, t as student_t

# ---------------------------------------------------------------------------
# Stałe
# ---------------------------------------------------------------------------

ARE_NORMAL = 3 / math.pi  # Pitman ARE testu rangowego vs. testu t przy normalności


# ---------------------------------------------------------------------------
# Wartości krytyczne
# ---------------------------------------------------------------------------


def z_critical(alpha, two_sided):
    """Kwantyl rozkładu normalnego dla zadanego poziomu istotności."""
    if two_sided:
        return norm.ppf(1 - alpha / 2)
    return norm.ppf(1 - alpha)


def t_critical(alpha, df, two_sided):
    """Kwantyl rozkładu t-Studenta dla zadanego alpha i df."""
    if two_sided:
        return student_t.ppf(1 - alpha / 2, df)
    return student_t.ppf(1 - alpha, df)


# ---------------------------------------------------------------------------
# Moc testu t (dokładna, na niecentralnym rozkładzie t)
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def power_independent_t(d, alpha, n_per_group, two_sided):
    """Dokładna moc testu t dla dwóch grup niezależnych."""
    if n_per_group < 2:
        return 0.0
    df = 2 * (n_per_group - 1)
    nc = d * math.sqrt(n_per_group / 2)
    tcrit = t_critical(alpha, df, two_sided)
    if two_sided:
        return float(1 - nct.cdf(tcrit, df, nc) + nct.cdf(-tcrit, df, nc))
    return float(1 - nct.cdf(tcrit, df, nc))


@lru_cache(maxsize=None)
def power_paired_t(d, alpha, n_pairs, two_sided):
    """Dokładna moc testu t dla prób zależnych (parowanych)."""
    if n_pairs < 2:
        return 0.0
    df = n_pairs - 1
    nc = d * math.sqrt(n_pairs)
    tcrit = t_critical(alpha, df, two_sided)
    if two_sided:
        return float(1 - nct.cdf(tcrit, df, nc) + nct.cdf(-tcrit, df, nc))
    return float(1 - nct.cdf(tcrit, df, nc))


# ---------------------------------------------------------------------------
# Przybliżona liczebność (wzór z-normalny)
# ---------------------------------------------------------------------------


def n_independent_t_approx(d, alpha, power, two_sided):
    """Przybliżona n na grupę — test t niezależny (wzór z kwantylami z)."""
    z_alpha = z_critical(alpha, two_sided)
    z_beta = norm.ppf(power)
    return max(2, math.ceil(2 * ((z_alpha + z_beta) / d) ** 2))


def n_paired_t_approx(d, alpha, power, two_sided):
    """Przybliżona n (par) — test t parowy (wzór z kwantylami z)."""
    z_alpha = z_critical(alpha, two_sided)
    z_beta = norm.ppf(power)
    return max(2, math.ceil(((z_alpha + z_beta) / d) ** 2))


# ---------------------------------------------------------------------------
# Dokładna liczebność (iteracyjne szukanie n z niecentralnym t)
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def n_independent_t_exact(d, alpha, power, two_sided):
    """Dokładna n na grupę — test t niezależny."""
    start_n = max(2, n_independent_t_approx(d, alpha, power, two_sided) - 10)
    for n_per_group in range(start_n, 100_000):
        if power_independent_t(d, alpha, n_per_group, two_sided) >= power:
            return n_per_group
    return None


@lru_cache(maxsize=None)
def n_paired_t_exact(d, alpha, power, two_sided):
    """Dokładna n (par) — test t parowy."""
    start_n = max(2, n_paired_t_approx(d, alpha, power, two_sided) - 10)
    for n_pairs in range(start_n, 100_000):
        if power_paired_t(d, alpha, n_pairs, two_sided) >= power:
            return n_pairs
    return None


# ---------------------------------------------------------------------------
# Testy nieparametryczne (korekta ARE)
# ---------------------------------------------------------------------------


def n_mann_whitney(d, alpha, power, two_sided):
    """n na grupę — test Manna-Whitneya (korekta ARE na bazie testu t)."""
    n_param = n_independent_t_exact(d, alpha, power, two_sided)
    if n_param is None:
        return None
    return math.ceil(n_param / ARE_NORMAL)


def n_wilcoxon(d, alpha, power, two_sided):
    """n par — test Wilcoxona signed-rank (korekta ARE na bazie testu t)."""
    n_param = n_paired_t_exact(d, alpha, power, two_sided)
    if n_param is None:
        return None
    return math.ceil(n_param / ARE_NORMAL)


# ---------------------------------------------------------------------------
# Pomocnicze
# ---------------------------------------------------------------------------


def effective_parametric_n_for_nonparametric(n_nonparam):
    """Efektywna n parametryczna odpowiadająca n nieparametrycznej (do krzywej mocy)."""
    return max(2, int(math.floor(n_nonparam * ARE_NORMAL)))
