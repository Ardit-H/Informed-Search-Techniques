# Informed Search Techniques, SAT, CSP, Local Search (Detyra 2 - AI)

Zgjidhje në Python për katër probleme: kërkim i informuar (A\*), SAT, CSP dhe metaheuristika.

Instalimi: `pip install -r requirements.txt`

| Detyra | Skedari | Ekzekutimi |
|---|---|---|
| 1. Blocked N-Queens (A*, 3 heuristika) | `task1_blocked_queens/blocked_queens.py` | `python task1_blocked_queens/blocked_queens.py` |
| 2. SAT - uljet e mysafirëve | `task2_sat/seating_sat.py` | `python task2_sat/seating_sat.py` |
| 3. Killer Sudoku (CSP, CP-SAT) | `task3_killer_sudoku/killer_sudoku.py` | `python task3_killer_sudoku/killer_sudoku.py` |

## 1. Blocked N-Queens
Vendosen N mbretëresha në tabelën NxN ashtu që asnjëra të mos sulmojë tjetrën (rresht, kolonë, diagonale)
dhe asnjë mbretëreshë të mos qëndrojë në katror të bllokuar. Katrorët e bllokuar vetëm ndalojnë vendosjen,
nuk ndalojnë sulmet.

A\*: gjendja = kolonat e mbretëreshave të vendosura rresht pas rreshti, kosto 1 për mbretëreshë.
- `h1` = N-k (admissible)
- `h2` = N-k, por INF nëse një rresht i mbetur nuk ka katror të sigurt (admissible, dominon h1)
- `h3` = 2(N-k) + INF për rreshta të vdekur (jo admissible)

Nga rezultatet (nyje të zgjeruara), `h2` zgjeron ~2.5x më pak nyje se `h1` dhe gjen zgjidhje optimale,
ndaj propozohet si heuristika admissible. `h3` jep të njëjtin numër nyjesh sepse zgjidhja ka thellësi fikse.

## 2. SAT
Variabla `x[g][t]` (mysafiri g ulet në tavolinën t); klauzola: (1) çdo mysafir të paktën një tavolinë,
(2) më së shumti një, (3) tavolina ≤ 10, (4) çiftet e ndaluara `¬x[a][t] ∨ ¬x[b][t]`, (5) çiftet e detyruara
(ekuivalencë), (6) gjinia: |M−F| ≤ 3 me 10 vende ⇔ 4 ≤ M ≤ 6 (kardinalitet me sequential counter).
Instanca (gjinitë, çiftet e ndaluara dhe të detyruara) gjenerohet me seed fiks. Gjeneron `seating.cnf`
(DIMACS) dhe e zgjidh me Glucose3; zgjidhja verifikohet në kod.

## 3. Killer Sudoku
CP-SAT: `AllDifferent` për rreshta/kolona/blloqe/kafaze + shuma e kafazit. Puzzle (31 kafaze) është gjeneruar
nga ne nga një grid i zgjidhur dhe ka zgjidhje unike (kontrollohet duke kërkuar 2 zgjidhje).
