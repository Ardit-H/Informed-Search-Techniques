"""Problemi i uljes së mysafirëve - formulimi SAT (CNF) dhe zgjidhja me PySAT.

Variablat: x[g][t] = 1  <=>  mysafiri g ulet në tavolinën t   (100 x 10 = 1000 variabla)

Klauzolat:
 1. Çdo mysafir ulet të paktën në një tavolinë:  (x[g][0] v ... v x[g][9])
 2. Çdo mysafir ulet në më së shumti një tavolinë: (-x[g][t] v -x[g][u]) për t<u
 3. Çdo tavolinë ka më së shumti 10 mysafirë (100 mysafirë / 10 tavolina => saktësisht 10).
 4. Çiftet e ndaluara (a,b): për çdo tavolinë t:  (-x[a][t] v -x[b][t])
 5. Çiftet e detyruara (a,b): për çdo tavolinë t: (-x[a][t] v x[b][t]) dhe (x[a][t] v -x[b][t])
 6. Gjinia: |M - F| <= 3 në çdo tavolinë. Me M+F = 10 => 2M-10 in [-3,3] => 4 <= M <= 6.
    Kufizimet kardinaliteti (atmost 6 meshkuj, atmost 6 femra) kodohen në CNF
    me sequential counter (CardEnc.atmost nga PySAT).
"""
import itertools
import random

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose3

N_GUESTS, N_TABLES, CAPACITY, MAX_DIFF = 100, 10, 10, 3


def make_instance(seed=7, n_forbidden=60, n_together=15):
    """Gjeneron një instancë: gjinitë, çiftet e ndaluara dhe çiftet e detyruara.
    Instanca bazohet në një ulje 'e fshehur' që siguron se ka zgjidhje."""
    rnd = random.Random(seed)
    guests = list(range(N_GUESTS))
    rnd.shuffle(guests)
    hidden = {g: i // CAPACITY for i, g in enumerate(guests)}      # tavolina e fshehur
    gender = {}
    for t in range(N_TABLES):                                        # 5 M + 5 F për tavolinë
        members = [g for g in range(N_GUESTS) if hidden[g] == t]
        rnd.shuffle(members)
        for i, g in enumerate(members):
            gender[g] = "M" if i < 5 else "F"
    forbidden, together = set(), set()
    while len(forbidden) < n_forbidden:
        a, b = sorted(rnd.sample(range(N_GUESTS), 2))
        if hidden[a] != hidden[b]:
            forbidden.add((a, b))
    while len(together) < n_together:
        a, b = sorted(rnd.sample(range(N_GUESTS), 2))
        if hidden[a] == hidden[b]:
            together.add((a, b))
    return gender, sorted(forbidden), sorted(together)


def build_cnf(gender, forbidden, together):
    pool = IDPool()
    x = lambda g, t: pool.id(("x", g, t))
    cnf = CNF()
    for g in range(N_GUESTS):
        cnf.append([x(g, t) for t in range(N_TABLES)])                          # (1)
        for t, u in itertools.combinations(range(N_TABLES), 2):
            cnf.append([-x(g, t), -x(g, u)])                                    # (2)
    for t in range(N_TABLES):
        lits = [x(g, t) for g in range(N_GUESTS)]
        cnf.extend(CardEnc.atmost(lits, bound=CAPACITY, vpool=pool,
                                  encoding=EncType.seqcounter).clauses)         # (3)
        males = [x(g, t) for g in range(N_GUESTS) if gender[g] == "M"]
        females = [x(g, t) for g in range(N_GUESTS) if gender[g] == "F"]
        # M <= 6  dhe  F <= 6  (=> M >= 4 sepse M+F = 10)
        for grp in (males, females):
            cnf.extend(CardEnc.atmost(grp, bound=(CAPACITY + MAX_DIFF) // 2,
                                      vpool=pool, encoding=EncType.seqcounter).clauses)  # (6)
        for a, b in forbidden:
            cnf.append([-x(a, t), -x(b, t)])                                    # (4)
        for a, b in together:
            cnf.append([-x(a, t), x(b, t)])                                     # (5)
            cnf.append([x(a, t), -x(b, t)])
    return cnf, x


def main():
    gender, forbidden, together = make_instance()
    cnf, x = build_cnf(gender, forbidden, together)
    print(f"Variabla: {cnf.nv}, klauzola: {len(cnf.clauses)}")
    cnf.to_file("seating.cnf")                         # DIMACS
    with Glucose3(bootstrap_with=cnf.clauses) as s:
        if not s.solve():
            print("UNSAT - nuk ka zgjidhje")
            return
        model = set(l for l in s.get_model() if l > 0)
    tables = {t: [g for g in range(N_GUESTS) if x(g, t) in model] for t in range(N_TABLES)}
    for t, gs in tables.items():
        m = sum(gender[g] == "M" for g in gs)
        print(f"Tavolina {t + 1:2d}: M={m} F={len(gs) - m} -> " + " ".join(f"M{g + 1}" for g in gs))
    # verifikim
    where = {g: t for t, gs in tables.items() for g in gs}
    assert len(where) == N_GUESTS
    assert all(len(gs) == CAPACITY for gs in tables.values())
    assert all(where[a] != where[b] for a, b in forbidden)
    assert all(where[a] == where[b] for a, b in together)
    assert all(abs(sum(gender[g] == "M" for g in gs) * 2 - CAPACITY) <= MAX_DIFF
               for gs in tables.values())
    print("Të gjitha kushtet janë të plotësuara.")


if __name__ == "__main__":
    main()
