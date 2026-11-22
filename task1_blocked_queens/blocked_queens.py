"""Blocked N-Queens zgjidhur me A*.

Problemi: vendosni N mbretëresha në tabelën NxN ashtu që asnjëra të mos sulmojë
tjetrën (rresht, kolonë, diagonale) dhe asnjë mbretëreshë të mos qëndrojë në
katror të bllokuar.

Gjendja   : tuple me kolonat e mbretëreshave të vendosura rresht pas rreshti.
Veprimi   : vendos mbretëreshën në rreshtin e radhës në një kolonë të lirë/sigurt.
Kostoja   : 1 për çdo mbretëreshë të vendosur  ->  g = numri i mbretëreshave.
Qëllimi   : N mbretëresha të vendosura.
"""
import heapq
import itertools
import random
import time

INF = float("inf")


# --------------------------- problemi ---------------------------
class BlockedQueens:
    def __init__(self, n, blocked):
        self.n = n
        self.blocked = set(blocked)  # {(rreshti, kolona)}

    def is_safe(self, state, col):
        row = len(state)
        if (row, col) in self.blocked:
            return False
        for r, c in enumerate(state):
            if c == col or abs(c - col) == row - r:
                return False
        return True

    def safe_cols(self, state, row):
        """Kolonat ku mund të vendoset mbretëresha në rreshtin `row` (jo vetëm i radhës)."""
        return [c for c in range(self.n)
                if (row, c) not in self.blocked
                and all(c != qc and abs(c - qc) != row - qr for qr, qc in enumerate(state))]

    def successors(self, state):
        return [state + (c,) for c in range(self.n) if self.is_safe(state, c)]

    def is_goal(self, state):
        return len(state) == self.n


# --------------------------- heuristikat ---------------------------
def h1_remaining(p, state):
    """h1 = numri i mbretëreshave që mbeten (N - k). ADMISSIBLE: çdo mbretëreshë
    kërkon të paktën një hap."""
    return p.n - len(state)


def h2_forward_check(p, state):
    """h2 = h1, por nëse ndonjë rresht i mbetur nuk ka asnjë katror të sigurt
    gjendja është pa zgjidhje -> h = INF. ADMISSIBLE (INF vetëm kur h* = INF) dhe
    më informuese se h1 (h2 >= h1)."""
    for row in range(len(state), p.n):
        if not p.safe_cols(state, row):
            return INF
    return p.n - len(state)


def h3_weighted(p, state):
    """h3 = 2 * (N - k) (+ INF për rreshta pa katror të sigurt). NUK është
    admissible (mbivlerëson koston reale N-k), por e drejton kërkimin më
    'lakmueshëm'."""
    h = h2_forward_check(p, state)
    return h if h == INF else 2 * h


HEURISTICS = {"h1_remaining": h1_remaining,
              "h2_forward_check": h2_forward_check,
              "h3_weighted": h3_weighted}


# --------------------------- A* ---------------------------
def astar(p, h):
    """A*: f = g + h. Në rast barazimi në f, preferohet g më i madh (më thellë)."""
    counter = itertools.count()
    start = ()
    h0 = h(p, start)
    frontier = [(h0, -0, next(counter), 0, start)]
    best_g = {start: 0}
    expanded = generated = 0
    while frontier:
        f, _, _, g, state = heapq.heappop(frontier)
        if g > best_g.get(state, INF):
            continue
        if p.is_goal(state):
            return state, g, expanded, generated
        expanded += 1
        for s in p.successors(state):
            g2 = g + 1
            if g2 < best_g.get(s, INF):
                h2 = h(p, s)
                if h2 == INF:
                    continue
                best_g[s] = g2
                generated += 1
                heapq.heappush(frontier, (g2 + h2, -g2, next(counter), g2, s))
    return None, INF, expanded, generated


# --------------------------- instancat ---------------------------
def random_instance(n, n_blocked, seed):
    rnd = random.Random(seed)
    cells = [(r, c) for r in range(n) for c in range(n)]
    return BlockedQueens(n, rnd.sample(cells, n_blocked))


def show(p, state):
    for r in range(p.n):
        print(" ".join("Q" if state[r] == c else ("X" if (r, c) in p.blocked else ".")
                       for c in range(p.n)))


if __name__ == "__main__":
    # Shembulli nga përshkrimi i problemit (N=4 do ishte pa zgjidhje -> përdorim N=8)
    instances = [("N=8, 3 të bllokuara", BlockedQueens(8, [(0, 0), (1, 1), (3, 2)])),
                 ("N=8, 10 të bllokuara", random_instance(8, 10, seed=1)),
                 ("N=12, 20 të bllokuara", random_instance(12, 20, seed=2)),
                 ("N=16, 30 të bllokuara", random_instance(16, 30, seed=3))]
    for name, prob in instances:
        print(f"\n=== {name} ===")
        for hname, h in HEURISTICS.items():
            t = time.time()
            sol, cost, exp, gen = astar(prob, h)
            dt = time.time() - t
            print(f"{hname:18s} kosto={cost} expanded={exp:7d} generated={gen:7d} koha={dt:.3f}s")
            last = sol
        if last:
            show(prob, last)
        else:
            print("Nuk ka zgjidhje")
