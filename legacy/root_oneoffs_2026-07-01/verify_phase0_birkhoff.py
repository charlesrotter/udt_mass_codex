"""
BLIND VERIFIER for Phase-0 Claim (A) BIRKHOFF.
Independent sympy re-derivation. Does NOT read the author's scripts.

Metric:  ds^2 = -e^{-2 phi(t,r)} c^2 dt^2 + e^{+2 phi(t,r)} dr^2 + r^2 dOmega^2
Vacuum:  test whether G_{t r} forces d_t phi = 0.
"""
import sympy as sp

t, r, th, ps, c = sp.symbols('t r theta psi c', positive=True, real=True)
phi = sp.Function('phi')(t, r)

# coords
x = [t, r, th, ps]

# metric (lower)
g = sp.zeros(4, 4)
g[0, 0] = -sp.exp(-2*phi) * c**2
g[1, 1] = sp.exp(2*phi)
g[2, 2] = r**2
g[3, 3] = r**2 * sp.sin(th)**2

ginv = g.inv()

def christoffel(g, ginv, x):
    n = len(x)
    Gam = [[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], x[cc]) + sp.diff(g[d, cc], x[b]) - sp.diff(g[b, cc], x[d]))
                Gam[a][b][cc] = sp.simplify(s/2)
    return Gam

Gam = christoffel(g, ginv, x)

def ricci(Gam, x):
    n = len(x)
    Ric = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            s = 0
            for cc in range(n):
                s += sp.diff(Gam[cc][a][b], x[cc]) - sp.diff(Gam[cc][a][cc], x[b])
                for d in range(n):
                    s += Gam[cc][cc][d]*Gam[d][a][b] - Gam[cc][a][d]*Gam[d][b][cc]
            Ric[a, b] = sp.simplify(s)
    return Ric

Ric = ricci(Gam, x)
Rscal = sp.simplify(sum(ginv[a, b]*Ric[a, b] for a in range(4) for b in range(4)))

# Einstein tensor lowered
G = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        G[a, b] = sp.simplify(Ric[a, b] - sp.Rational(1, 2)*g[a, b]*Rscal)

Gtr = sp.simplify(G[0, 1])
print("G_{t r} (lowered) =", Gtr)
print("G_{t r} / d_t phi =", sp.simplify(Gtr / sp.diff(phi, t)))

# mixed G^t_r
Gtr_mixed = sp.simplify(sum(ginv[0, d]*G[d, 1] for d in range(4)))
print("G^t_r (mixed) =", Gtr_mixed)

# Tie
tie = sp.simplify(g[0, 0]*g[1, 1])
print("g_tt * g_rr =", tie)

# Check vacuum diagonal eqs too: do they admit a non-static solution?
print("\nDiagonal vacuum components (lowered):")
for i, nm in enumerate(['tt', 'rr', 'thth', 'psps']):
    print(f"  G_{nm} =", sp.simplify(G[i, i]))
