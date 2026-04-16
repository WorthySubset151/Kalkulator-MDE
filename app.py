import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from core import (
    ARE_NORMAL,
    effective_parametric_n_for_nonparametric,
    n_independent_t_exact,
    n_mann_whitney,
    n_paired_t_exact,
    n_wilcoxon,
    power_independent_t,
    power_paired_t,
)


st.set_page_config(
    page_title="Kalkulator Wielkości Próby",
    layout="wide",
    page_icon="📊",
)


COHEN_D = {
    "Mały efekt (d = 0,2)": 0.2,
    "Średni efekt (d = 0,5)": 0.5,
    "Duży efekt (d = 0,8)": 0.8,
}


st.title("📊 Kalkulator wielkości próby")
st.caption(
    "Szacowanie minimalnej liczebności próby dla porównania różnic "
    "testami parametrycznymi i nieparametrycznymi, także gdy rozkład "
    "jest nieznany."
)


with st.sidebar:
    st.header("Parametry badania")

    design = st.radio(
        "Schemat badania",
        [
            "Dwie grupy niezależne",
            "Pomiary zależne (parowane)",
        ],
        help=(
            "Niezależne: dwie osobne grupy.\n"
            "Parowane: te same osoby mierzone dwukrotnie lub pary dopasowane."
        ),
    )

    distribution_knowledge = st.radio(
        "Co wiesz o rozkładzie?",
        [
            "Nie znam rozkładu / chcę wersję bezpieczną",
            "Mogę założyć normalność",
        ],
        help=(
            "Jeśli rozkład jest nieznany, bezpieczniej planować próbę dla testu "
            "nieparametrycznego."
        ),
    )

    alpha = st.select_slider(
        "Poziom istotności α",
        options=[0.001, 0.005, 0.01, 0.025, 0.05, 0.10],
        value=0.05,
        help="Prawdopodobieństwo błędu I rodzaju. Standard naukowy: α = 0,05.",
    )

    power = st.select_slider(
        "Moc testu (1 − β)",
        options=[0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
        value=0.80,
        help="Prawdopodobieństwo wykrycia efektu, jeśli efekt rzeczywiście istnieje.",
    )

    two_sided = (
        st.radio(
            "Rodzaj hipotezy",
            ["Dwustronna", "Jednostronna"],
            help=(
                "Jednostronną wybieraj tylko wtedy, gdy kierunek efektu został "
                "określony przed badaniem."
            ),
        )
        == "Dwustronna"
    )

    st.divider()
    st.subheader("Wielkość efektu")

    effect_mode = st.radio(
        "Jak chcesz podać efekt?",
        ["Konwencja Cohena", "Podaj d ręcznie", "Oblicz d z Δ i σ"],
        help="d = Δ / σ. Dla testów parowanych σ oznacza odchylenie standardowe różnic.",
    )

    if effect_mode == "Konwencja Cohena":
        d = COHEN_D[st.selectbox("Wybierz efekt", list(COHEN_D.keys()), index=1)]
    elif effect_mode == "Podaj d ręcznie":
        d = st.slider("Cohen's d", min_value=0.05, max_value=3.0, value=0.5, step=0.05)
    else:
        if design == "Dwie grupy niezależne":
            delta_label = "Minimalna istotna różnica Δ"
            sigma_label = "Wspólne odchylenie standardowe σ"
        else:
            delta_label = "Średnia różnica Δ"
            sigma_label = "Odchylenie standardowe różnic σ_d"

        col_a, col_b = st.columns(2)
        with col_a:
            delta = st.number_input(delta_label, min_value=0.01, value=10.0, step=0.5)
        with col_b:
            sigma = st.number_input(sigma_label, min_value=0.01, value=20.0, step=0.5)
        d = delta / sigma
        st.info(f"Obliczone **d = Δ / σ = {d:.3f}**")

    buffer_pct = st.slider(
        "Bufor na braki danych (%)",
        min_value=0,
        max_value=30,
        value=10,
        step=5,
        help="Dodatkowy zapas na brakujące dane, wykluczenia i odpadnięcia.",
    )


parametric_test = (
    "Test t-Studenta dla prób niezależnych"
    if design == "Dwie grupy niezależne"
    else "Test t-Studenta dla prób zależnych"
)
nonparametric_test = (
    "Test Manna-Whitneya"
    if design == "Dwie grupy niezależne"
    else "Test Wilcoxona (znaków rangowanych)"
)
unit_label = "na grupę" if design == "Dwie grupy niezależne" else "par"
direction_label = "dwustronna" if two_sided else "jednostronna"
buffer_multiplier = 1 + buffer_pct / 100


if design == "Dwie grupy niezależne":
    n_param = n_independent_t_exact(d, alpha, power, two_sided)
    n_nonparam = n_mann_whitney(d, alpha, power, two_sided)
else:
    n_param = n_paired_t_exact(d, alpha, power, two_sided)
    n_nonparam = n_wilcoxon(d, alpha, power, two_sided)


tabs = st.tabs(
    [
        "Wynik główny",
        "Krzywa mocy",
        "Analiza czułości",
        "Metodologia i referencje",
    ]
)


with tabs[0]:
    if distribution_knowledge == "Nie znam rozkładu / chcę wersję bezpieczną":
        st.success(
            f"Rekomendacja planistyczna: **{nonparametric_test}** — "
            "to bezpieczniejszy punkt odniesienia, gdy rozkład jest nieznany."
        )
    else:
        st.success(
            f"Rekomendacja planistyczna: **{parametric_test}** — "
            "zakładasz normalność, więc test parametryczny jest naturalnym wyborem."
        )

    summary_cols = st.columns(2)

    with summary_cols[0]:
        st.markdown(f"### 🔵 {parametric_test}")
        st.caption("Wynik ścisły oparty na mocy testu i niecentralnym rozkładzie t.")
        if n_param is None:
            st.error("Nie udało się wyznaczyć liczebności w zadanym zakresie.")
        else:
            st.metric(f"Liczebność bazowa {unit_label}", n_param)
            st.metric(
                f"Liczebność z buforem {unit_label}",
                math.ceil(n_param * buffer_multiplier),
            )
            if design == "Dwie grupy niezależne":
                st.metric(
                    "Łączna liczba osób (z buforem)",
                    math.ceil(n_param * buffer_multiplier) * 2,
                )
            else:
                st.metric(
                    "Łączna liczba osób (z buforem)",
                    math.ceil(n_param * buffer_multiplier),
                )

    with summary_cols[1]:
        st.markdown(f"### 🟠 {nonparametric_test}")
        st.caption(
            "Wynik przybliżony naukowo: liczebność testu parametrycznego "
            "skorygowana przez ARE = 3/π ≈ 0,955."
        )
        if n_nonparam is None:
            st.error("Nie udało się wyznaczyć liczebności w zadanym zakresie.")
        else:
            st.metric(f"Liczebność bazowa {unit_label}", n_nonparam)
            st.metric(
                f"Liczebność z buforem {unit_label}",
                math.ceil(n_nonparam * buffer_multiplier),
            )
            if design == "Dwie grupy niezależne":
                st.metric(
                    "Łączna liczba osób (z buforem)",
                    math.ceil(n_nonparam * buffer_multiplier) * 2,
                )
            else:
                st.metric(
                    "Łączna liczba osób (z buforem)",
                    math.ceil(n_nonparam * buffer_multiplier),
                )

    st.divider()
    st.info(
        f"Parametry bieżącego scenariusza: **α = {alpha}**, **moc = {power}**, "
        f"**hipoteza = {direction_label}**, **d = {d:.3f}**, **bufor = {buffer_pct}%**."
    )

    with st.expander("Jak czytać ten wynik?"):
        st.markdown(
            """
- Wynik **parametryczny** jest właściwy, gdy dane spełniają założenia testu t
  lub gdy masz mocne uzasadnienie, że test t będzie wystarczająco odporny.
- Wynik **nieparametryczny** jest bezpieczniejszy, gdy rozkład jest nieznany,
  skośny albo spodziewasz się wartości odstających.
- Wartość **z buforem** to praktyczna liczebność rekrutacyjna.
- Dla schematu parowanego liczebność oznacza liczbę **osób/par**,
  a nie osobne grupy.
"""
        )

    if abs(d - 0.5) < 1e-9 and alpha == 0.05 and power == 0.80 and two_sided:
        st.warning(
            "Dla klasycznego scenariusza Cohena (d = 0,5; α = 0,05; moc = 0,80) "
            f"kalkulator daje około **{n_param} {unit_label}** dla testu t oraz "
            f"**{n_nonparam} {unit_label}** dla testu nieparametrycznego."
        )


with tabs[1]:
    st.subheader("Krzywa mocy")
    st.caption(
        "Wykres pokazuje, jak rośnie moc testu wraz ze wzrostem liczebności próby."
    )

    reference_n = max(
        n for n in [n_param, n_nonparam] if n is not None
    )
    max_n = min(max(reference_n * 3, 60), 3000)
    step = max(1, max_n // 400)
    sample_sizes = np.arange(2, max_n + 1, step)

    if design == "Dwie grupy niezależne":
        power_param_curve = [
            power_independent_t(d, alpha, int(n), two_sided) for n in sample_sizes
        ]
        power_nonparam_curve = [
            power_independent_t(
                d,
                alpha,
                effective_parametric_n_for_nonparametric(int(n)),
                two_sided,
            )
            for n in sample_sizes
        ]
    else:
        power_param_curve = [
            power_paired_t(d, alpha, int(n), two_sided) for n in sample_sizes
        ]
        power_nonparam_curve = [
            power_paired_t(
                d,
                alpha,
                effective_parametric_n_for_nonparametric(int(n)),
                two_sided,
            )
            for n in sample_sizes
        ]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        sample_sizes,
        power_param_curve,
        label=parametric_test,
        color="#1f77b4",
        linewidth=2.2,
    )
    ax.plot(
        sample_sizes,
        power_nonparam_curve,
        label=f"{nonparametric_test} (aproks.)",
        color="#ff7f0e",
        linestyle="--",
        linewidth=2.2,
    )
    ax.axhline(
        power,
        color="#d62728",
        linestyle=":",
        linewidth=1.5,
        label=f"Docelowa moc = {power}",
    )
    ax.set_xlabel(f"Liczebność {unit_label}", fontsize=12)
    ax.set_ylabel("Moc testu", fontsize=12)
    ax.set_ylim(0, 1.02)
    ax.set_xlim(left=0)
    ax.grid(alpha=0.25)
    ax.legend(loc="lower right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Krzywa dla testu nieparametrycznego jest przybliżona przez względną "
        "efektywność ARE przy rozkładzie normalnym."
    )


with tabs[2]:
    st.subheader("Analiza czułości")
    st.caption(
        "Tabela pokazuje, jak zmienia się wymagana liczebność wraz z wielkością efektu i mocą."
    )

    d_values = [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00]
    power_levels = [0.80, 0.90, 0.95]

    param_rows = []
    nonparam_rows = []

    for d_value in d_values:
        if design == "Dwie grupy niezależne":
            param_calc = [
                n_independent_t_exact(d_value, alpha, p_level, two_sided)
                for p_level in power_levels
            ]
            nonparam_calc = [
                n_mann_whitney(d_value, alpha, p_level, two_sided)
                for p_level in power_levels
            ]
        else:
            param_calc = [
                n_paired_t_exact(d_value, alpha, p_level, two_sided)
                for p_level in power_levels
            ]
            nonparam_calc = [
                n_wilcoxon(d_value, alpha, p_level, two_sided)
                for p_level in power_levels
            ]

        param_rows.append(param_calc)
        nonparam_rows.append(nonparam_calc)

    param_df = pd.DataFrame(
        param_rows,
        index=[f"d = {value:.2f}" for value in d_values],
        columns=[f"Moc {int(level * 100)}%" for level in power_levels],
    )
    nonparam_df = pd.DataFrame(
        nonparam_rows,
        index=[f"d = {value:.2f}" for value in d_values],
        columns=[f"Moc {int(level * 100)}%" for level in power_levels],
    )

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(f"#### {parametric_test}")
        st.dataframe(param_df, width="stretch")
    with col_right:
        st.markdown(f"#### {nonparametric_test}")
        st.dataframe(nonparam_df, width="stretch")

    st.caption(
        f"Wszystkie wartości oznaczają liczebność **{unit_label}** i nie zawierają bufora."
    )


with tabs[3]:
    st.subheader("Metodologia")

    with st.expander("1. Co dokładnie liczy to narzędzie?", expanded=True):
        st.markdown(
            """
Kalkulator szacuje **minimalną liczebność próby** potrzebną do wykrycia
zadanej wielkości efektu przy ustalonym:

- poziomie istotności **α**
- poziomie mocy **1 − β**
- schemacie badania (niezależnym lub parowanym)
- rodzaju hipotezy (jednostronnej lub dwustronnej)

W wersji parametrycznej wynik jest liczony na podstawie **mocy testu t**
z użyciem **niecentralnego rozkładu t**. W wersji nieparametrycznej wynik
jest wyznaczany jako konserwatywna korekta testu parametrycznego przez
**ARE = 3/π**.
"""
        )

    with st.expander("2. Skąd bierze się Cohen's d?", expanded=False):
        st.markdown("Dla dwóch średnich używamy standaryzowanej wielkości efektu:")
        st.latex(r"d = \frac{\Delta}{\sigma}")
        st.markdown(
            """
gdzie:

- **Δ** — minimalna różnica, którą chcesz wykryć
- **σ** — odchylenie standardowe

Konwencje Cohena:

- **d = 0,2** — mały efekt
- **d = 0,5** — średni efekt
- **d = 0,8** — duży efekt

Wartość **d = 0,5** nie jest prawem natury ani wynikiem jednego wzoru.
To konwencja zaproponowana przez Cohena jako rozsądny punkt wyjścia,
gdy badacz nie ma wcześniejszych danych.
"""
        )

    with st.expander("3. Wzory bazowe dla testu t", expanded=False):
        st.markdown("Dla dwóch grup niezależnych:")
        st.latex(
            r"n \approx \frac{2\,(z_{1-\alpha^*} + z_{1-\beta})^2}{d^2}"
        )
        st.markdown("Dla testu parowanego:")
        st.latex(
            r"n \approx \frac{(z_{1-\alpha^*} + z_{1-\beta})^2}{d^2}"
        )
        st.markdown(
            """
gdzie:

- dla hipotezy **dwustronnej**: α* = α / 2
- dla hipotezy **jednostronnej**: α* = α

W tym narzędziu nie kończymy jednak na tym przybliżeniu. Używamy go tylko
jako punktu startowego, a potem szukamy najmniejszego **n** dającego
wymaganą moc w dokładniejszym modelu z niecentralnym rozkładem t.
"""
        )

    with st.expander("4. Skąd bierze się korekta dla testów nieparametrycznych?", expanded=False):
        st.markdown(
            """
Dla testu Manna-Whitneya i testu Wilcoxona zastosowano klasyczną
asymptotyczną względną efektywność Pitmana przy rozkładzie normalnym:
"""
        )
        st.latex(r"\mathrm{ARE} = \frac{3}{\pi} \approx 0{,}9549")
        st.markdown(
            """
To oznacza, że przy normalności test nieparametryczny jest nieco mniej
wydajny od parametrycznego i zwykle potrzebuje około:
"""
        )
        st.latex(r"\frac{1}{0{,}9549} - 1 \approx 4{,}7\%")
        st.markdown(
            """
więcej obserwacji. Dlatego stosujemy:
"""
        )
        st.latex(
            r"n_{\mathrm{nieparam}} = \left\lceil \frac{n_{\mathrm{param}}}{3/\pi} \right\rceil"
        )
        st.markdown(
            """
Jest to **konserwatywne** podejście. Przy rozkładach silnie skośnych
lub ciężkoogonowych test nieparametryczny może być nawet korzystniejszy.
"""
        )

    with st.expander("5. Referencje", expanded=False):
        st.markdown(
            """
1. **Cohen, J. (1988).** *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
2. **Cohen, J. (1992).** A power primer. *Psychological Bulletin, 112*(1), 155–159. https://doi.org/10.1037/0033-2909.112.1.155
3. **Noether, G. E. (1987).** Sample size determination for some common nonparametric tests. *Journal of the American Statistical Association, 82*(398), 645–647.
4. **Lehr, R. (1992).** Sixteen S-squared over D-squared: A relation for crude sample size estimates. *Statistics in Medicine, 11*(8), 1099–1102.
5. **Lehmann, E. L. (1975).** *Nonparametrics: Statistical Methods Based on Ranks.* Holden-Day.
"""
        )


st.divider()
st.caption(
    "Uwagi: Aktualna wersja programu jest naukowo poprawnym narzędziem do planowania "
    "liczebności próby dla porównań dwugrupowych, ale jego część nieparametryczna"
    " ma charakter przybliżony i konserwatywny opartym na asymptotycznej względnej efektywności (ARE). "
    "Jeżeli projekt badania ma wysoką wagę kliniczną, regulacyjną lub rejestracyjną,"
    " zalecane jest potwierdzenie liczebności przez dedykowane oprogramowanie lub symulację Monte Carlo."
)
