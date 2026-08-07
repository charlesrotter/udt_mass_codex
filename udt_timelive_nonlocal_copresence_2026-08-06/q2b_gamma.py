"""Q2b: gamma = -g(U,u) for matter 4-velocity U at rapidity w vs copresence u.
Static: gamma collapses to E/|xi| (conserved Killing energy). Time-live: no KV -> test if
gamma still reduces to a conserved metric quantity, or is a genuine non-Killing scalar.
Also: frame-invariant boost sectional curvature R_{01 01} (unambiguous N3 density).
"""
import sympy as sp

t, x, w = sp.symbols('t x w', real=True)
c = sp.symbols('c', positive=True)
phi = sp.Function('phi')(t, x)
coords = [t, x]
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi))
ginv = g.inv()

# copresence u and spatial unit e_x
uup = [sp.exp(phi)/c, 0]
exup = [0, sp.exp(-phi)]
# U = u cosh w + e_x sinh w  (rapidity w relative to copresence)
Uup = [sp.simplify(uup[i]*sp.cosh(w) + exup[i]*sp.sinh(w)) for i in range(2)]
# gamma = -g(U,u)
ulow = [sp.simplify(sum(g[a, b]*uup[b] for b in range(2))) for a in range(2)]
gamma = sp.simplify(-sum(ulow[a]*Uup[a] for a in range(2)))
print("gamma = -g(U,u) =", gamma)   # expect cosh w (chosen-probe: F-GAUGE unless U physical)

# Killing energy w.r.t. xi=d_t (NOT conserved time-live since d_t not Killing)
xi = [1, 0]
xilow = [sp.simplify(sum(g[a, b]*xi[b] for b in range(2))) for a in range(2)]
E = sp.simplify(-sum(xilow[a]*Uup[a] for a in range(2)))
print("E = -g(U, d_t) =", E)
normxi = sp.simplify(sp.sqrt(-sum(xilow[a]*xi[a] for a in range(2))))
print("|xi| = sqrt(-g(xi,xi)) =", normxi)
print("E/|xi| =", sp.simplify(E/normxi), "   (== gamma? static-style collapse)")

# Is E conserved? dE/dtau along U for a GENERIC phi(t,x): only conserved if d_t Killing.
# Demonstrate: for a free (geodesic) U, dE/dtau = (1/2) U^a U^b (partial_? ...) -> nonzero iff phi_t!=0.
# Structural statement: conservation of E requires L_xi g=0 which fails time-live (Q1). We note it.
print("\nStatic collapse gamma=E/|xi| holds ALGEBRAICALLY, but E is conserved ONLY if d_t Killing;")
print("time-live d_t is NOT Killing (Q1) so E is NOT a conserved charge -> gamma not tied to one.")

# frame-invariant boost sectional curvature R_{hat0 hat1 hat0 hat1}
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
def Riem_low(a, b, cd, dd):  # R_{a b c d}
    n = 2
    Rup = (sp.diff(G[a][dd][b], coords[cd]) - sp.diff(G[a][cd][b], coords[dd])
           + sum(G[a][cd][e]*G[e][dd][b] - G[a][dd][e]*G[e][cd][b] for e in range(n)))
    return Rup
Rup_txtx = sp.simplify(Riem_low(0, 1, 0, 1))          # R^t_{x t x}
Rlow_txtx = sp.simplify(sum(g[0, m]*Riem_low(m, 1, 0, 1) for m in range(2)))  # R_{t x t x}
# orthonormal: e0^t=e^{phi}/c, e1^x=e^{-phi}
Rframe = sp.simplify(Rlow_txtx*(sp.exp(phi)/c)**2*(sp.exp(-phi))**2)
print("\nR_{hat0 hat1 hat0 hat1} (frame-invariant, LOCK) =", sp.simplify(Rframe))
