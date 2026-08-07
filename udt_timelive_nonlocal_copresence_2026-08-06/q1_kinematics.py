"""Q1: un-pinning + copresence congruence kinematics, TIME-LIVE reciprocal lock.
Exact sympy, float-free. Metric ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}(dx^2+dy^2+dz^2),
phi=phi(t,x,y,z) (carry full dependence; specialize as noted). Copresence u = d_t/sqrt(-g_tt).
Reports: (i) Killing check for xi=d_t time-live; (ii) theta, sigma^2, omega^2, acceleration.
"""
import sympy as sp

t, x, y, z, c = sp.symbols('t x y z c', real=True, positive=False)
c = sp.symbols('c', positive=True)
phi = sp.Function('phi')(t, x, y, z)
coords = [t, x, y, z]

# metric (reciprocal lock)
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), sp.exp(2*phi), sp.exp(2*phi))
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], coords[cc])
                                     + sp.diff(g[d, cc], coords[b])
                                     - sp.diff(g[b, cc], coords[d]))
                Gamma[a][b][cc] = sp.simplify(s/2)
    return Gamma

Gamma = christoffel(g, ginv, coords)

# --- (i) Killing check: L_xi g = 0 for xi = d_t (components (1,0,0,0)) ---
xi = sp.Matrix([1, 0, 0, 0])
# (L_xi g)_{ab} = xi^c d_c g_ab + g_cb d_a xi^c + g_ac d_b xi^c ; xi const comps -> only first term
Lie = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Lie[a, b] = sp.simplify(sum(xi[cc]*sp.diff(g[a, b], coords[cc]) for cc in range(4)))
print("L_xi g  (xi=d_t):")
sp.pprint(Lie)
print("Killing iff all zero. Nonzero entries carry factor phi_t.")
