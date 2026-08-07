"""Q1b: does ANY Killing vector survive time-live? Solve full Killing system in 1+1
generic phi(t,x). V = P(t,x) d_t + Q(t,x) d_x. Killing eq: nabla_(a V_b) = 0 (3 eqs in 2D).
Show generic phi admits no solution (=> no stationary timelike KV; copresence un-pinned).
"""
import sympy as sp

t, x, c = sp.symbols('t x c', positive=True)
phi = sp.Function('phi')(t, x)
coords = [t, x]
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi))
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = len(coords); G = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sum(ginv[a, d]*(sp.diff(g[d, b], coords[cc]) + sp.diff(g[d, cc], coords[b])
                        - sp.diff(g[b, cc], coords[d])) for d in range(n))
                G[a][b][cc] = sp.simplify(s/2)
    return G
G = christoffel(g, ginv, coords)

P = sp.Function('P')(t, x); Q = sp.Function('Q')(t, x)
V = [P, Q]                       # contravariant
Vlow = [sp.simplify(sum(g[a, b]*V[b] for b in range(2))) for a in range(2)]  # covariant

def covder(Vlow, a, b):  # nabla_a V_b
    s = sp.diff(Vlow[b], coords[a]) - sum(G[cc][a][b]*Vlow[cc] for cc in range(2))
    return sp.simplify(s)

KE = {}
for a in range(2):
    for b in range(a, 2):
        KE[(a, b)] = sp.simplify(covder(Vlow, a, b) + covder(Vlow, b, a))
for k in KE:
    print("KE", k, "= 0  :")
    sp.pprint(sp.simplify(KE[k]))
    print()
