"""Killer Sudoku zgjidhur me Constraint Programming (OR-Tools CP-SAT).

Variablat : x[r][c] in 1..9 (81 variabla)
Kufizimet : AllDifferent për çdo rresht, kolonë dhe bllok 3x3;
            për çdo kafaz (cage): shuma e qelizave = shuma e dhënë dhe
            qelizat e kafazit janë të ndryshme (AllDifferent).
"""
from ortools.sat.python import cp_model

# (shuma, [(rreshti, kolona), ...]) - kafazet e një puzzle-i Killer Sudoku
CAGES = [
    (22, [(7, 7), (8, 7), (8, 8), (6, 7)]),
    (32, [(4, 5), (3, 5), (3, 6), (4, 6), (4, 4)]),
    (9, [(4, 2), (4, 1), (4, 3)]),
    (20, [(5, 0), (4, 0), (3, 0), (2, 0)]),
    (26, [(6, 4), (7, 4), (7, 5), (8, 5)]),
    (19, [(0, 3), (1, 3), (1, 4)]),
    (9, [(0, 6), (1, 6)]),
    (17, [(7, 0), (7, 1), (7, 2)]),
    (12, [(3, 2), (2, 2), (1, 2)]),
    (11, [(4, 8), (4, 7), (5, 8)]),
    (20, [(2, 7), (2, 8), (2, 6)]),
    (15, [(0, 7), (1, 7), (0, 8)]),
    (19, [(0, 5), (0, 4), (1, 5), (2, 5), (2, 4)]),
    (6, [(8, 3), (8, 2)]),
    (17, [(3, 3), (3, 4), (2, 3)]),
    (18, [(0, 2), (0, 1), (0, 0)]),
    (8, [(8, 0), (8, 1)]),
    (17, [(6, 2), (5, 2), (5, 1)]),
    (14, [(5, 5), (5, 6)]),
    (9, [(7, 8), (6, 8)]),
    (19, [(2, 1), (3, 1), (1, 1)]),
    (13, [(8, 6), (7, 6)]),
    (16, [(3, 7), (3, 8)]),
    (12, [(6, 0), (6, 1)]),
    (14, [(7, 3), (6, 3), (5, 3)]),
    (3, [(6, 5), (6, 6)]),
    (1, [(1, 8)]),
    (2, [(1, 0)]),
    (3, [(5, 4)]),
    (1, [(5, 7)]),
    (1, [(8, 4)]),
]


def solve(cages, count_limit=2):
    m = cp_model.CpModel()
    x = [[m.NewIntVar(1, 9, f"x_{r}_{c}") for c in range(9)] for r in range(9)]
    for i in range(9):
        m.AddAllDifferent(x[i])                                   # rreshtat
        m.AddAllDifferent([x[r][i] for r in range(9)])            # kolonat
    for br in range(3):
        for bc in range(3):                                       # blloqet 3x3
            m.AddAllDifferent([x[3 * br + i][3 * bc + j] for i in range(3) for j in range(3)])
    for total, cells in cages:                                    # kafazet
        vs = [x[r][c] for r, c in cells]
        m.AddAllDifferent(vs)
        m.Add(sum(vs) == total)
    s = cp_model.CpSolver()
    s.parameters.enumerate_all_solutions = True
    sols = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            sols.append([[self.Value(x[r][c]) for c in range(9)] for r in range(9)])
            if len(sols) >= count_limit:
                self.StopSearch()

    s.Solve(m, CB())
    return sols


if __name__ == "__main__":
    assert sorted(c for _, cg in CAGES for c in cg) == [(r, c) for r in range(9) for c in range(9)]
    sols = solve(CAGES)
    print(f"Zgjidhje të gjetura (max 2 kërkohen për të testuar unicitetin): {len(sols)}")
    for row in sols[0]:
        print(" ".join(map(str, row)))
    # verifikim
    g = sols[0]
    assert all(sorted(row) == list(range(1, 10)) for row in g)
    assert all(sorted(g[r][c] for r in range(9)) == list(range(1, 10)) for c in range(9))
    assert all(sum(g[r][c] for r, c in cg) == t for t, cg in CAGES)
    print("Verifikimi OK; zgjidhja është" + (" unike." if len(sols) == 1 else " jo unike."))
