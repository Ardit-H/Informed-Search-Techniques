# Informed Search Techniques, SAT, CSP, Local Search (Detyra 2 - AI)

Zgjidhje në Python për katër probleme: kërkim i informuar (A\*), SAT, CSP dhe metaheuristika.

| Detyra | Skedari | Ekzekutimi |
|---|---|---|
| 1. Blocked N-Queens (A*, 3 heuristika) | `task1_blocked_queens/blocked_queens.py` | `python task1_blocked_queens/blocked_queens.py` |

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
