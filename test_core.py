"""
Testy jednostkowe dla modułu core.py — kalkulator wielkości próby.

Pokrywają:
- poprawność stałych,
- wartości krytyczne (z, t),
- dokładność mocy testu t (niecentralny rozkład t),
- klasyczne scenariusze Cohena (d = 0.2, 0.5, 0.8),
- monotoniczność mocy względem n,
- spójność: test nieparametryczny >= test parametryczny,
- korekta ARE,
- hipoteza jednostronna vs dwustronna,
- warunki brzegowe (n < 2, duże efekty).
"""

import math

import pytest
from scipy.stats import norm, t as student_t

from core import (
    ARE_NORMAL,
    effective_parametric_n_for_nonparametric,
    n_independent_t_approx,
    n_independent_t_exact,
    n_mann_whitney,
    n_paired_t_approx,
    n_paired_t_exact,
    n_wilcoxon,
    power_independent_t,
    power_paired_t,
    t_critical,
    z_critical,
)


# ===================================================================
# 1. Stałe
# ===================================================================


class TestConstants:
    def test_are_normal_value(self):
        assert ARE_NORMAL == pytest.approx(3 / math.pi, rel=1e-10)

    def test_are_normal_approximate_value(self):
        assert ARE_NORMAL == pytest.approx(0.9549, rel=1e-3)

    def test_are_less_than_one(self):
        """ARE < 1 oznacza, że test nieparametryczny jest mniej wydajny."""
        assert ARE_NORMAL < 1.0

    def test_are_greater_than_zero(self):
        assert ARE_NORMAL > 0.0


# ===================================================================
# 2. Wartości krytyczne
# ===================================================================


class TestZCritical:
    def test_two_sided_005(self):
        assert z_critical(0.05, two_sided=True) == pytest.approx(1.95996, rel=1e-4)

    def test_two_sided_001(self):
        assert z_critical(0.01, two_sided=True) == pytest.approx(2.57583, rel=1e-4)

    def test_one_sided_005(self):
        assert z_critical(0.05, two_sided=False) == pytest.approx(1.64485, rel=1e-4)

    def test_one_sided_less_than_two_sided(self):
        """Wartość krytyczna jednostronna jest mniejsza od dwustronnej."""
        assert z_critical(0.05, False) < z_critical(0.05, True)

    def test_symmetry(self):
        """z_critical(alpha/2, one-sided) == z_critical(alpha, two-sided)."""
        assert z_critical(0.025, False) == pytest.approx(z_critical(0.05, True), rel=1e-10)


class TestTCritical:
    def test_converges_to_z_for_large_df(self):
        """Dla dużych df rozkład t zbiega do normalnego."""
        t_val = t_critical(0.05, df=10000, two_sided=True)
        z_val = z_critical(0.05, two_sided=True)
        assert t_val == pytest.approx(z_val, rel=1e-3)

    def test_two_sided_greater_than_one_sided(self):
        assert t_critical(0.05, 30, True) > t_critical(0.05, 30, False)

    def test_decreases_with_df(self):
        """Wartość krytyczna maleje ze wzrostem df."""
        assert t_critical(0.05, 10, True) > t_critical(0.05, 100, True)


# ===================================================================
# 3. Moc testu t — warunki brzegowe
# ===================================================================


class TestPowerEdgeCases:
    def test_independent_n_below_2_returns_zero(self):
        assert power_independent_t(0.5, 0.05, 1, True) == 0.0

    def test_paired_n_below_2_returns_zero(self):
        assert power_paired_t(0.5, 0.05, 1, True) == 0.0

    def test_power_between_0_and_1(self):
        p = power_independent_t(0.5, 0.05, 64, True)
        assert 0.0 < p < 1.0

    def test_paired_power_between_0_and_1(self):
        p = power_paired_t(0.5, 0.05, 34, True)
        assert 0.0 < p < 1.0


# ===================================================================
# 4. Moc testu t — monotoniczność
# ===================================================================


class TestPowerMonotonicity:
    """Moc powinna rosnąć ze wzrostem n (przy stałym d, alpha)."""

    @pytest.mark.parametrize("n", [10, 20, 40, 80, 160])
    def test_independent_power_increases_with_n(self, n):
        p1 = power_independent_t(0.5, 0.05, n, True)
        p2 = power_independent_t(0.5, 0.05, n + 1, True)
        assert p2 >= p1

    @pytest.mark.parametrize("n", [10, 20, 40, 80])
    def test_paired_power_increases_with_n(self, n):
        p1 = power_paired_t(0.5, 0.05, n, True)
        p2 = power_paired_t(0.5, 0.05, n + 1, True)
        assert p2 >= p1

    def test_independent_power_increases_with_d(self):
        """Moc rośnie ze wzrostem wielkości efektu."""
        p_small = power_independent_t(0.2, 0.05, 50, True)
        p_large = power_independent_t(0.8, 0.05, 50, True)
        assert p_large > p_small

    def test_paired_power_increases_with_d(self):
        p_small = power_paired_t(0.2, 0.05, 50, True)
        p_large = power_paired_t(0.8, 0.05, 50, True)
        assert p_large > p_small


# ===================================================================
# 5. Klasyczne scenariusze Cohena — test t niezależny
# ===================================================================


class TestCohenScenariosIndependent:
    """Weryfikacja z klasycznymi tabelami Cohena (α=0.05, moc=0.80, dwustronny)."""

    def test_medium_effect(self):
        """d=0.5 → n≈64 na grupę (Cohen 1992, Tabela 2)."""
        n = n_independent_t_exact(0.5, 0.05, 0.80, True)
        assert n == 64

    def test_small_effect(self):
        """d=0.2 → n≈394 (Cohen: ~393-395 w zależności od metody)."""
        n = n_independent_t_exact(0.2, 0.05, 0.80, True)
        assert 390 <= n <= 400

    def test_large_effect(self):
        """d=0.8 → n≈26 (Cohen: ~25-26)."""
        n = n_independent_t_exact(0.8, 0.05, 0.80, True)
        assert 25 <= n <= 27


class TestCohenScenariosPaired:
    """Weryfikacja dla testu parowego (α=0.05, moc=0.80, dwustronny)."""

    def test_medium_effect(self):
        """d=0.5 → n≈34 par."""
        n = n_paired_t_exact(0.5, 0.05, 0.80, True)
        assert 33 <= n <= 35

    def test_small_effect(self):
        """d=0.2 → n≈199 par."""
        n = n_paired_t_exact(0.2, 0.05, 0.80, True)
        assert 195 <= n <= 202

    def test_large_effect(self):
        """d=0.8 → n≈15 par."""
        n = n_paired_t_exact(0.8, 0.05, 0.80, True)
        assert 14 <= n <= 16


# ===================================================================
# 6. Dokładność wyników — moc przy obliczonym n
# ===================================================================


class TestExactPowerAtComputedN:
    """Moc przy obliczonym n powinna być >= żądanej, a przy n-1 < żądanej."""

    @pytest.mark.parametrize(
        "d,alpha,target_power",
        [
            (0.2, 0.05, 0.80),
            (0.5, 0.05, 0.80),
            (0.8, 0.05, 0.80),
            (0.5, 0.01, 0.80),
            (0.5, 0.05, 0.90),
            (0.5, 0.05, 0.95),
        ],
    )
    def test_independent_power_at_n(self, d, alpha, target_power):
        n = n_independent_t_exact(d, alpha, target_power, True)
        assert n is not None
        p_at_n = power_independent_t(d, alpha, n, True)
        p_at_n_minus_1 = power_independent_t(d, alpha, n - 1, True)
        assert p_at_n >= target_power
        assert p_at_n_minus_1 < target_power

    @pytest.mark.parametrize(
        "d,alpha,target_power",
        [
            (0.2, 0.05, 0.80),
            (0.5, 0.05, 0.80),
            (0.8, 0.05, 0.80),
            (0.5, 0.01, 0.90),
        ],
    )
    def test_paired_power_at_n(self, d, alpha, target_power):
        n = n_paired_t_exact(d, alpha, target_power, True)
        assert n is not None
        p_at_n = power_paired_t(d, alpha, n, True)
        p_at_n_minus_1 = power_paired_t(d, alpha, n - 1, True)
        assert p_at_n >= target_power
        assert p_at_n_minus_1 < target_power


# ===================================================================
# 7. Przybliżenie vs. wynik dokładny
# ===================================================================


class TestApproxVsExact:
    """Przybliżenie normalne powinno być bliskie wynikowi dokładnemu."""

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_independent_approx_close_to_exact(self, d):
        approx = n_independent_t_approx(d, 0.05, 0.80, True)
        exact = n_independent_t_exact(d, 0.05, 0.80, True)
        assert abs(approx - exact) <= max(5, exact * 0.05)

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_paired_approx_close_to_exact(self, d):
        approx = n_paired_t_approx(d, 0.05, 0.80, True)
        exact = n_paired_t_exact(d, 0.05, 0.80, True)
        assert abs(approx - exact) <= max(5, exact * 0.05)


# ===================================================================
# 8. Korekta ARE — testy nieparametryczne
# ===================================================================


class TestNonparametricARE:
    """Wyniki nieparametryczne powinny być >= parametrycznych."""

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_mann_whitney_ge_t_independent(self, d):
        n_t = n_independent_t_exact(d, 0.05, 0.80, True)
        n_mw = n_mann_whitney(d, 0.05, 0.80, True)
        assert n_mw >= n_t

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_wilcoxon_ge_t_paired(self, d):
        n_t = n_paired_t_exact(d, 0.05, 0.80, True)
        n_w = n_wilcoxon(d, 0.05, 0.80, True)
        assert n_w >= n_t

    def test_mann_whitney_classic_scenario(self):
        """d=0.5, α=0.05, moc=0.80 → n_MW ≈ 67-68."""
        n = n_mann_whitney(0.5, 0.05, 0.80, True)
        assert 66 <= n <= 70

    def test_wilcoxon_classic_scenario(self):
        """d=0.5, α=0.05, moc=0.80 → n_W ≈ 36."""
        n = n_wilcoxon(0.5, 0.05, 0.80, True)
        assert 35 <= n <= 38

    def test_are_correction_factor(self):
        """n_nonparam ≈ n_param * (π/3), z zaokrągleniem w górę."""
        n_t = n_independent_t_exact(0.5, 0.05, 0.80, True)
        n_mw = n_mann_whitney(0.5, 0.05, 0.80, True)
        expected = math.ceil(n_t / ARE_NORMAL)
        assert n_mw == expected

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_nonparam_overhead_around_5_percent(self, d):
        """Narzut nieparametryczny powinien wynosić ok. 4-6%."""
        n_t = n_independent_t_exact(d, 0.05, 0.80, True)
        n_mw = n_mann_whitney(d, 0.05, 0.80, True)
        overhead = (n_mw - n_t) / n_t
        assert 0.03 <= overhead <= 0.08


# ===================================================================
# 9. Hipoteza jednostronna vs dwustronna
# ===================================================================


class TestOneSidedVsTwoSided:
    """Test jednostronny wymaga mniejszej próby niż dwustronny."""

    @pytest.mark.parametrize("d", [0.3, 0.5, 0.8])
    def test_independent_one_sided_less(self, d):
        n_two = n_independent_t_exact(d, 0.05, 0.80, True)
        n_one = n_independent_t_exact(d, 0.05, 0.80, False)
        assert n_one < n_two

    @pytest.mark.parametrize("d", [0.3, 0.5, 0.8])
    def test_paired_one_sided_less(self, d):
        n_two = n_paired_t_exact(d, 0.05, 0.80, True)
        n_one = n_paired_t_exact(d, 0.05, 0.80, False)
        assert n_one < n_two


# ===================================================================
# 10. Parowany wymaga mniejszej próby niż niezależny
# ===================================================================


class TestPairedVsIndependent:
    """Dla tego samego d, test parowy wymaga mniejszego n niż niezależny."""

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_paired_less_than_independent(self, d):
        n_ind = n_independent_t_exact(d, 0.05, 0.80, True)
        n_pair = n_paired_t_exact(d, 0.05, 0.80, True)
        assert n_pair < n_ind

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_paired_roughly_half_of_independent(self, d):
        """n_parowane ≈ n_niezależne / 2 (przybliżenie)."""
        n_ind = n_independent_t_exact(d, 0.05, 0.80, True)
        n_pair = n_paired_t_exact(d, 0.05, 0.80, True)
        ratio = n_pair / n_ind
        assert 0.40 <= ratio <= 0.60


# ===================================================================
# 11. Wpływ α i mocy na wymaganą próbę
# ===================================================================


class TestAlphaAndPowerEffects:
    def test_stricter_alpha_requires_more(self):
        n_05 = n_independent_t_exact(0.5, 0.05, 0.80, True)
        n_01 = n_independent_t_exact(0.5, 0.01, 0.80, True)
        assert n_01 > n_05

    def test_higher_power_requires_more(self):
        n_80 = n_independent_t_exact(0.5, 0.05, 0.80, True)
        n_90 = n_independent_t_exact(0.5, 0.05, 0.90, True)
        n_95 = n_independent_t_exact(0.5, 0.05, 0.95, True)
        assert n_95 > n_90 > n_80

    def test_smaller_effect_requires_more(self):
        n_small = n_independent_t_exact(0.2, 0.05, 0.80, True)
        n_medium = n_independent_t_exact(0.5, 0.05, 0.80, True)
        n_large = n_independent_t_exact(0.8, 0.05, 0.80, True)
        assert n_small > n_medium > n_large


# ===================================================================
# 12. effective_parametric_n_for_nonparametric
# ===================================================================


class TestEffectiveParametricN:
    def test_always_at_least_2(self):
        assert effective_parametric_n_for_nonparametric(1) >= 2

    def test_correct_floor(self):
        """Powinno zwracać floor(n * ARE)."""
        result = effective_parametric_n_for_nonparametric(100)
        expected = int(math.floor(100 * ARE_NORMAL))
        assert result == expected

    def test_less_than_input(self):
        """Efektywna n parametryczna < n nieparametryczna (bo ARE < 1)."""
        for n in [10, 50, 100, 500]:
            assert effective_parametric_n_for_nonparametric(n) <= n


# ===================================================================
# 13. Uproszczenie Lehra: n ≈ 16/d² (dla α=0.05, moc=0.80, dwustronny)
# ===================================================================


class TestLehrApproximation:
    """Przybliżenie Lehra: n ≈ 16/d² dla dwóch grup niezależnych."""

    @pytest.mark.parametrize("d", [0.2, 0.3, 0.5, 0.8, 1.0])
    def test_lehr_formula_close(self, d):
        lehr_n = 16 / d**2
        exact_n = n_independent_t_exact(d, 0.05, 0.80, True)
        # Lehr daje przybliżenie — dopuszczamy ±10% lub ±5 obs.
        assert abs(lehr_n - exact_n) <= max(5, exact_n * 0.10)


# ===================================================================
# 14. Wyniki nie powinny być None dla rozsądnych parametrów
# ===================================================================


class TestNoNoneForReasonableInputs:
    @pytest.mark.parametrize(
        "d,alpha,power",
        [
            (0.1, 0.05, 0.80),
            (0.2, 0.01, 0.95),
            (0.5, 0.05, 0.80),
            (1.0, 0.10, 0.70),
            (2.0, 0.05, 0.95),
        ],
    )
    def test_independent_not_none(self, d, alpha, power):
        assert n_independent_t_exact(d, alpha, power, True) is not None

    @pytest.mark.parametrize(
        "d,alpha,power",
        [
            (0.1, 0.05, 0.80),
            (0.2, 0.01, 0.95),
            (0.5, 0.05, 0.80),
            (1.0, 0.10, 0.70),
            (2.0, 0.05, 0.95),
        ],
    )
    def test_paired_not_none(self, d, alpha, power):
        assert n_paired_t_exact(d, alpha, power, True) is not None

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_mann_whitney_not_none(self, d):
        assert n_mann_whitney(d, 0.05, 0.80, True) is not None

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_wilcoxon_not_none(self, d):
        assert n_wilcoxon(d, 0.05, 0.80, True) is not None


# ===================================================================
# 15. Wyniki powinny być liczbami całkowitymi >= 2
# ===================================================================


class TestResultTypes:
    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_independent_returns_int_ge_2(self, d):
        n = n_independent_t_exact(d, 0.05, 0.80, True)
        assert isinstance(n, int)
        assert n >= 2

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_paired_returns_int_ge_2(self, d):
        n = n_paired_t_exact(d, 0.05, 0.80, True)
        assert isinstance(n, int)
        assert n >= 2

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_mann_whitney_returns_int_ge_2(self, d):
        n = n_mann_whitney(d, 0.05, 0.80, True)
        assert isinstance(n, int)
        assert n >= 2

    @pytest.mark.parametrize("d", [0.2, 0.5, 0.8])
    def test_wilcoxon_returns_int_ge_2(self, d):
        n = n_wilcoxon(d, 0.05, 0.80, True)
        assert isinstance(n, int)
        assert n >= 2


# ===================================================================
# 16. Duży efekt — mała próba
# ===================================================================


class TestLargeEffects:
    def test_very_large_d_independent(self):
        """Przy d=2.0, wystarczy kilka osób na grupę."""
        n = n_independent_t_exact(2.0, 0.05, 0.80, True)
        assert n is not None
        assert n <= 10

    def test_very_large_d_paired(self):
        n = n_paired_t_exact(2.0, 0.05, 0.80, True)
        assert n is not None
        assert n <= 8
