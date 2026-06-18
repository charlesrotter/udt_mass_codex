"""
B2-1 GAUGE TEST (the load-bearing physical check).

Question: is the d_t^2 h content in the l=2 even-parity diagonal warp
  delta g_thth = +r^2 h P2,  delta g_psps = -r^2 sin^2th h P2
a PHYSICAL radiative DOF, or removable by a gauge (diffeomorphism) vector xi?

Method (rigorous, no GR-folklore trust): generate the MOST GENERAL pure-gauge
even-parity l=2 metric perturbation from a gauge vector xi_mu and check whether
ANY xi reproduces the author's warp pattern. If the author's perturbation
CANNOT be written as a Lie derivative of the background metric, it has a
gauge-invariant part -> physical.

Pure-gauge perturbation: h_munu^gauge = nabla_mu xi_nu + nabla_nu xi_mu
                                      = L_xi g_munu.

Even-parity l=2 gauge vector on flat round bg (c=1), standard RW basis:
  xi_t   = T(t,r) P2
  xi_r   = R(t,r) P2
  xi_th  = Th(t,r) dP2/dth
  xi_ps  = 0   (even parity)
Compute L_xi g and compare its (thth, psps) trace-free part to the author's.
Key diagnostic: can a gauge xi produce delta g_thth with a d_t^2-supporting
structure WITHOUT also forcing delta g_tt, delta g_tr, delta g_rr to be
nonzero? The author's warp has delta g_tt = delta g_tr = delta g_rr = 0.
"""
import sympy as sp

t, r, th = sp.symbols('t r theta', real=True)
x = [t, r, th, sp.Symbol('psi')]
ps = x[3]

# flat round background, c=1
g = sp.diag(-1, 1, r**2, r**2*sp.sin(th)**2)
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

P2 = (3*sp.cos(th)**2 - 1)/2
dP2 = sp.diff(P2, th)

T = sp.Function('T')(t, r)
R = sp.Function('R')(t, r)
Th = sp.Function('Th')(t, r)

# covariant gauge vector (lower index)
xi = [T*P2, R*P2, Th*dP2, sp.Integer(0)]

# L_xi g = nabla_mu xi_nu + nabla_nu xi_mu ; nabla_mu xi_nu = d_mu xi_nu - Gam^l_{mu nu} xi_l
def cov_d(xi_lower, mu, nu):
    val = sp.diff(xi_lower[nu], x[mu])
    for l in range(4):
        val -= Gam[l][mu][nu]*xi_lower[l]
    return val

hgauge = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        hgauge[a, b] = sp.simplify(cov_d(xi, a, b) + cov_d(xi, b, a))

print("Pure-gauge l=2 even perturbation components:")
labels = ['t', 'r', 'th', 'ps']
for a in range(4):
    for b in range(a, 4):
        if hgauge[a, b] != 0:
            print(f"  h_{labels[a]}{labels[b]} =", sp.simplify(hgauge[a, b]))

print("\nAuthor's warp requires: h_tt=0, h_tr=0, h_rr=0, and h_thth=+r^2 h P2, h_psps=-r^2 sin^2 h P2.")
print("Check: can gauge give h_tt=0 AND h_tr=0 AND h_rr=0 with h_thth nonzero & time-dependent?")
print("  h_tt   =", sp.simplify(hgauge[0, 0]))   # = 2 d_t T * P2
print("  h_tr   =", sp.simplify(hgauge[0, 1]))
print("  h_rr   =", sp.simplify(hgauge[1, 1]))
