# Kalkulator wielkości próby statystycznej
Narzędzie webowe do planowania liczebności próby dla badań porównujących różnice między dwiema grupami lub między dwoma pomiarami tej samej grupy. Aplikacja została przygotowana jako praktyczny kalkulator analizy mocy dla testów parametrycznych i nieparametrycznych, ze szczególnym naciskiem na sytuację, w której rozkład danych nie jest znany na etapie planowania badania.

## Cel programu
Program odpowiada na pytanie:

**Jaką trzeba mieć liczebność próby, aby analiza statystyczna porównująca różnice była wiarygodna?**

W języku metodologicznym chodzi o wyznaczenie minimalnej liczebności próby zapewniającej zadaną:

- istotność statystyczną (`α`, poziom błędu I rodzaju),
- moc testu (`1 − β`, zdolność wykrycia efektu),
- czułość na określoną wielkość efektu,
- zgodność z planowanym schematem badania (próby niezależne lub zależne).

Program ma charakter **a priori power analysis**, czyli służy do planowania badania **przed** zebraniem danych.

## Zakres funkcjonalny aktualnej wersji
Aktualna wersja aplikacji obsługuje dwa schematy badawcze:

1. **Dwie grupy niezależne**
2. **Pomiary zależne (parowane)**

W ramach tych schematów udostępnione są cztery testy:

### Dwie grupy niezależne
- **Test t-Studenta dla prób niezależnych**  
  Parametryczny test różnicy średnich, stosowany przy założeniu normalności i homogeniczności wariancji.
- **Test Manna-Whitneya (U)**  
  Nieparametryczny odpowiednik dla dwóch grup niezależnych, stosowany wtedy, gdy rozkład jest nieznany, dane są skośne albo zawierają wartości odstające.

### Pomiary zależne
- **Test t-Studenta dla prób zależnych**  
  Parametryczny test średniej różnicy między dwoma pomiarami.
- **Test Wilcoxona (znaków rangowanych)**  
  Nieparametryczny odpowiednik dla danych sparowanych.

## Najważniejsze funkcjonalności aplikacji

### 1. Wybór schematu badania
Użytkownik wybiera, czy analizuje:

- dwie niezależne grupy,
- czy dwa pomiary tych samych osób / obiektów.

Od tego zależy interpretacja liczebności:

- dla prób niezależnych wynik oznacza **liczbę obserwacji na grupę**,
- dla prób zależnych wynik oznacza **liczbę par / osób mierzonych dwukrotnie**.

### 2. Wybór poziomu istotności `α`
Aplikacja umożliwia wybór spośród kilku standardowych wartości poziomu istotności:

- 0.001
- 0.005
- 0.01
- 0.025
- 0.05
- 0.10

Interpretacja:

- `α` to prawdopodobieństwo popełnienia **błędu I rodzaju**,
- czyli odrzucenia hipotezy zerowej `H₀`, mimo że jest prawdziwa.

W badaniach empirycznych najczęściej stosuje się `α = 0.05`.

### 3. Wybór mocy testu `1 − β`
Użytkownik może wybrać żądaną moc testu z przedziału od 0.70 do 0.95.

Interpretacja:

- moc testu to prawdopodobieństwo wykrycia efektu, jeśli efekt rzeczywiście istnieje,
- `β` oznacza **błąd II rodzaju**, czyli niewykrycie istniejącego efektu.

Najczęściej przyjmowaną wartością jest `0.80`.

### 4. Wybór hipotezy jednostronnej lub dwustronnej
Aplikacja wspiera dwa tryby testowania:

- **hipoteza dwustronna** – badacz sprawdza, czy istnieje różnica w dowolnym kierunku,
- **hipoteza jednostronna** – badacz testuje różnicę tylko w jednym, wcześniej określonym kierunku.

Hipoteza jednostronna wymaga silnego uzasadnienia metodologicznego i powinna być wybierana wyłącznie wtedy, gdy kierunek efektu został określony **przed** rozpoczęciem badania.

### 5. Trzy sposoby definiowania wielkości efektu
Aplikacja umożliwia zdefiniowanie efektu na trzy sposoby:

#### a) Konwencja Cohena
Predefiniowane wartości:

- `d = 0.2` – mały efekt
- `d = 0.5` – średni efekt
- `d = 0.8` – duży efekt

#### b) Ręczne podanie `d`
Użytkownik może wprowadzić własną wartość standaryzowanej wielkości efektu.

#### c) Obliczenie `d` z różnicy i odchylenia standardowego
Aplikacja może policzyć:

`d = Δ / σ`

gdzie:

- `Δ` – minimalna różnica, którą badacz chce wykryć,
- `σ` – odchylenie standardowe.

Dla prób zależnych `σ` oznacza odchylenie standardowe **różnic**, a nie surowych wyników.

### 6. Bufor na braki danych
Kalkulator pozwala dodać zapas na:

- brakujące dane,
- wykluczenia,
- rezygnacje uczestników,
- odpadnięcia w badaniach podłużnych.

Wynik prezentowany jest:

- jako liczebność bazowa,
- oraz jako liczebność powiększona o zadany bufor.

### 7. Równoległe wyniki dla testu parametrycznego i nieparametrycznego
Dla każdego scenariusza aplikacja pokazuje:

- wynik dla testu parametrycznego,
- wynik dla testu nieparametrycznego.

To pozwala użytkownikowi zdecydować, czy planować badanie:

- pod kątem scenariusza bardziej optymistycznego (parametrycznego),
- czy bardziej konserwatywnego (nieparametrycznego).

### 8. Rekomendacja testu przy nieznanym rozkładzie
Jeżeli użytkownik deklaruje, że:

- **nie zna rozkładu**,

to aplikacja rekomenduje przyjęcie wyniku dla testu nieparametrycznego jako bezpieczniejszej podstawy planowania.

### 9. Krzywa mocy
Aplikacja generuje wykres zależności:

- liczebność próby → moc testu

osobno dla:

- testu parametrycznego,
- testu nieparametrycznego.

To pozwala zobaczyć:

- gdzie przebiega punkt osiągnięcia żądanej mocy,
- jak szybko rośnie moc wraz ze wzrostem próby,
- i gdzie zaczyna się obszar malejących korzyści.

### 10. Analiza czułości
Program buduje tabelę wymagań liczebności dla różnych:

- wielkości efektu (`d`),
- poziomów mocy.

To ułatwia analizę typu:

- „co się stanie z wymaganą próbą, jeśli efekt okaże się mniejszy, niż zakładam?”

### 11. Wbudowana sekcja metodologiczna
Aplikacja zawiera sekcję objaśniającą:

- czym jest `α`,
- czym jest moc testu,
- czym jest `d`,
- skąd pochodzą wzory,
- i w jaki sposób liczona jest korekta dla testów nieparametrycznych.

## Tło naukowe

## Analiza mocy jako standard planowania badań
Podstawą działania programu jest klasyczna **analiza mocy statystycznej** (*statistical power analysis*), rozwinięta systematycznie przez Jacoba Cohena.

Analiza mocy opisuje zależność między czterema wielkościami:

1. liczebnością próby `n`,
2. poziomem istotności `α`,
3. mocą testu `1 − β`,
4. wielkością efektu `ES` (effect size).

W każdym konkretnym modelu statystycznym jedna z tych wielkości jest funkcją pozostałych trzech. W planowaniu badania interesuje nas najczęściej:

**jakie `n` jest potrzebne, aby przy zadanym `α` i założonym efekcie osiągnąć żądaną moc?**

## Wielkość efektu
W przypadku porównania różnic między dwiema średnimi najczęściej stosowaną miarą jest **Cohen’s d**:

```text
d = Δ / σ
```

gdzie:

- `Δ` to różnica, którą chcemy wykryć,
- `σ` to odchylenie standardowe.

Wartości konwencyjne zaproponowane przez Cohena:

- `0.2` – mały efekt,
- `0.5` – średni efekt,
- `0.8` – duży efekt.

Wartość `d = 0.5` nie jest wyprowadzona z jednego twierdzenia matematycznego ani z jednej uniwersalnej funkcji. Jest to **konwencja empiryczna**, zaproponowana przez Cohena jako rozsądny punkt startowy wtedy, gdy badacz nie ma wiarygodnych danych pilotażowych ani wcześniejszych estymacji efektu.

## Podstawa obliczeń parametrycznych
Aktualna implementacja nie opiera się wyłącznie na szkolnym przybliżeniu opartym na rozkładzie normalnym.

Program działa dwuetapowo:

1. wyznacza przybliżone `n` z klasycznego wzoru,
2. następnie szuka najmniejszego `n`, dla którego dokładna moc testu t osiąga zadany poziom.

### Wzór przybliżony dla dwóch grup niezależnych

```text
n ≈ 2 * (z_crit + z_power)^2 / d^2
```

gdzie:

- `n` – liczba obserwacji na grupę,
- `z_crit` – wartość krytyczna dla zadanego `α`,
- `z_power` – kwantyl odpowiadający żądanej mocy,
- `d` – Cohen’s d.

### Wzór przybliżony dla prób parowanych

```text
n ≈ (z_crit + z_power)^2 / d^2
```

### Klasyczne uproszczenie Lehra
Dla:

- `α = 0.05`,
- testu dwustronnego,
- mocy `0.80`,

otrzymujemy:

```text
n ≈ 16 / d^2   (dla dwóch grup niezależnych)
n ≈ 8 / d^2    (dla prób parowanych)
```

To uproszczenie zostało opisane przez Lehra (1992) jako praktyczna reguła pamięciowa.

## Dokładniejsza implementacja w aplikacji
Po wyznaczeniu przybliżonego punktu startowego aplikacja liczy moc testu t z wykorzystaniem **niecentralnego rozkładu t**.

Dla prób niezależnych:

- liczba stopni swobody: `df = 2 * (n - 1)`
- parametr niecentralności:

```text
δ = d * sqrt(n / 2)
```

Dla prób zależnych:

- liczba stopni swobody: `df = n - 1`
- parametr niecentralności:

```text
δ = d * sqrt(n)
```

Dla kolejnych kandydatów `n` liczona jest moc:

```text
Power = P(|T| > t_crit | df, δ)
```

Wyniki parametryczne prezentowane w aplikacji są więc **dokładniejsze niż samo przybliżenie z wzoru z**.

## Dlaczego testy nieparametryczne są trudniejsze do planowania?
W przypadku testów nieparametrycznych sytuacja jest metodologicznie bardziej złożona.

Testy takie jak:

- Mann-Whitney,
- Wilcoxon signed-rank,

nie są w ogólności prostymi „testami median”.

### Ważna uwaga interpretacyjna
**Test Manna-Whitneya nie testuje automatycznie różnicy median.**

Formalnie test ten dotyczy różnicy między rozkładami lub prawdopodobieństwa przewagi jednej obserwacji nad drugą:

```text
P(X > Y)
```

Interpretacja jako testu median jest poprawna dopiero przy dodatkowych założeniach, np. gdy oba rozkłady mają podobny kształt i różnią się głównie położeniem.

Analogicznie:

- test Wilcoxona signed-rank jest ściśle związany z rozkładem różnic i najczyściej interpretuje się go jako test przesunięcia lokalizacji przy odpowiednich założeniach o symetrii różnic.

## Jak program planuje próbę dla testów nieparametrycznych?
Aktualna wersja programu stosuje podejście **konserwatywne i intuicyjne**:

1. najpierw wyznacza liczebność dla odpowiadającego testu t,
2. następnie koryguje tę liczebność przez **asymptotyczną względną efektywność** (*Asymptotic Relative Efficiency*, ARE).

Dla porównania testu rangowego z testem t przy rozkładzie normalnym przyjmuje się klasyczną wartość:

```text
ARE = 3 / π ≈ 0.9549
```

Stąd:

```text
n_nonparam = ceil(n_param / ARE)
```

czyli praktycznie:

- test nieparametryczny potrzebuje około **4.7% więcej obserwacji** niż test parametryczny.

To podejście ma kilka zalet:

- jest proste i intuicyjne,
- dobrze nadaje się do planowania przy nieznanym rozkładzie,
- daje wynik konserwatywny,
- pozostaje zgodne z klasyczną teorią asymptotyczną.

## Co to oznacza naukowo?
Należy jasno podkreślić:

- wyniki dla testów t są w tej aplikacji **dokładne w sensie modelu niecentralnego rozkładu t**,
- wyniki dla testów nieparametrycznych są **przybliżeniem naukowo uzasadnionym**, ale nie są dokładnym wyznaczeniem mocy dla dowolnego rozkładu.

W bardziej zaawansowanych analizach dla testów nieparametrycznych można stosować:

- podejście Noethera (1987),
- dokładniejsze przybliżenia Shieh, Jan i Randles (2006, 2007),
- symulację Monte Carlo dla konkretnego modelu danych.

Aktualna aplikacja świadomie wybiera prostsze i bardziej intuicyjne rozwiązanie, aby zachować użyteczność dla badacza planującego badanie bez pełnej wiedzy o rozkładzie.

## Walidacja liczbowa
W klasycznym scenariuszu:

- `d = 0.5`
- `α = 0.05`
- moc = `0.80`
- test dwustronny

aplikacja zwraca dla dwóch grup niezależnych:

- **test t**: `n = 64` na grupę
- **Mann-Whitney**: `n = 68` na grupę

To jest zgodne z klasycznymi tabelami Cohena oraz z ogólną relacją wynikającą z korekty ARE.

## Co dokładnie opisuje wynik?

### Dla testów parametrycznych
Wynik oznacza minimalną liczbę obserwacji potrzebną do wykrycia różnicy o zadanej wielkości `d` przy:

- ustalonym `α`,
- zadanej mocy,
- zadanym typie hipotezy,
- założeniu odpowiedniego modelu testu t.

### Dla testów nieparametrycznych
Wynik oznacza konserwatywną estymację liczebności potrzebnej do uzyskania podobnej czułości analitycznej bez konieczności przyjmowania normalności.

## Ograniczenia metodologiczne
Poniższe punkty są kluczowe dla poprawnej interpretacji programu:

### 1. Program obsługuje tylko plany z dwiema warstwami porównania
Aktualna wersja nie implementuje:

- ANOVA,
- Kruskala-Wallisa,
- Welch t-test,
- projektów wielopoziomowych,
- modeli mieszanych,
- analiz z nierównym przydziałem do grup.

### 2. Program zakłada zbilansowany projekt
Dla prób niezależnych liczebności grup są równe (`n1 = n2`).

### 3. Wyniki nieparametryczne nie są dokładną analizą mocy dla dowolnego rozkładu
To przybliżenie przez ARE, a nie pełny model oparty na:

- prawdopodobieństwie przewagi,
- dokładnym efekcie rangowym,
- liczbie wiązań,
- konkretnym rozkładzie alternatywnym.

### 4. Program nie służy do retrospektywnej analizy mocy
Nie należy używać go do uzasadniania już zebranej próby po obejrzeniu wyników. Narzędzie jest przeznaczone do **planowania badania przed zebraniem danych**.

### 5. Interpretacja „porównania median” wymaga dodatkowych założeń
Jeśli użytkownik chce mówić ściśle o medianach, musi pamiętać, że:

- Mann-Whitney nie jest w pełni równoważny testowi median bez dodatkowych założeń o kształcie rozkładu,
- Wilcoxon signed-rank wymaga odpowiednich warunków interpretacyjnych dotyczących rozkładu różnic.

## Kiedy ten program jest szczególnie użyteczny?
Program jest szczególnie przydatny, gdy:

- badacz chce zaplanować badanie porównawcze,
- nie ma jeszcze danych,
- zna `α`, moc i przybliżoną wielkość efektu,
- nie zna rozkładu i chce przyjąć ostrożny wariant planowania,
- chce szybko porównać wariant parametryczny i nieparametryczny.

## Instalacja
Wymagane biblioteki:

- `streamlit`
- `scipy`
- `numpy`
- `pandas`
- `matplotlib`

Instalacja przez `pip`:

```bash
pip install streamlit scipy numpy pandas matplotlib
```

Instalacja przez `conda`:

```bash
conda install streamlit scipy numpy pandas matplotlib
```

## Uruchomienie
Z katalogu projektu:

```bash
streamlit run app.py
```

## Struktura działania aplikacji
Interfejs zawiera cztery główne zakładki:

1. **Wynik główny**  
   Podstawowy wynik liczebności dla wariantu parametrycznego i nieparametrycznego.

2. **Krzywa mocy**  
   Wykres relacji liczebność–moc.

3. **Analiza czułości**  
   Tabela wymaganych prób dla różnych `d` i różnych poziomów mocy.

4. **Metodologia i referencje**  
   Skrócony opis podstaw teoretycznych bezpośrednio w aplikacji.

## Znaczenie praktyczne
Program nie zastępuje pełnej konsultacji biostatystycznej, ale stanowi:

- rzetelne narzędzie do wstępnego planowania,
- intuicyjny kalkulator dla badaczy,
- naukowo uzasadniony kompromis między prostotą a poprawnością metodologiczną.

W praktyce oznacza to, że użytkownik może:

- zaplanować konserwatywną próbę przy nieznanym rozkładzie,
- szybko ocenić koszt badania przy różnych założeniach,
- uzyskać wynik zgodny z klasyczną analizą mocy i literaturą metodyczną.

## Referencje

1. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.

2. Cohen, J. (1992). A power primer. *Psychological Bulletin, 112*(1), 155–159. https://doi.org/10.1037/0033-2909.112.1.155

3. Lehr, R. (1992). Sixteen S-squared over D-squared: A relation for crude sample size estimates. *Statistics in Medicine, 11*(8), 1099–1102. https://doi.org/10.1002/sim.4780110811

4. Noether, G. E. (1987). Sample size determination for some common nonparametric tests. *Journal of the American Statistical Association, 82*(398), 645–647. https://doi.org/10.1080/01621459.1987.10478478

5. Lehmann, E. L. (1975). *Nonparametrics: Statistical Methods Based on Ranks*. Holden-Day.

6. Shieh, G., Jan, S.-L., & Randles, R. H. (2006). On power and sample size determinations for the Wilcoxon-Mann-Whitney test. *Journal of Nonparametric Statistics, 18*(1), 33–43. https://doi.org/10.1080/10485250500473099

7. Shieh, G., Jan, S.-L., & Randles, R. H. (2007). Power and sample size determinations for the Wilcoxon signed-rank test. *Journal of Statistical Computation and Simulation, 77*(8), 717–724. https://doi.org/10.1080/10629360600635245

8. Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*(2), 175–191. https://doi.org/10.3758/BF03193146

9. Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power: The pervasive fallacy of power calculations for data analysis. *The American Statistician, 55*(1), 19–24. https://doi.org/10.1198/000313001300339897

---

**Uwaga końcowa:**  
Aktualna wersja programu jest naukowo poprawnym narzędziem do planowania liczebności próby dla porównań dwugrupowych, ale jego część nieparametryczna ma charakter przybliżony i konserwatywny. Jeżeli projekt badania ma wysoką wagę kliniczną, regulacyjną lub rejestracyjną, zalecane jest potwierdzenie liczebności przez dedykowane oprogramowanie lub symulację Monte Carlo.

