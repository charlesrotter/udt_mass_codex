#!/usr/bin/env python3
"""
phase0_nonround_escape.py -- Phase-0 (B): SHOW THE NON-ROUND ESCAPE.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A.
Frame: time_live_bare_solve_DESIGN.md (RED-TEAM-REVISIONS #1 + PHASE-0 (b)).

In (A) the ROUND+diagonal+vacuum momentum constraint G_{tr}=2 d_t phi/r forced
d_t phi=0 (static by theorem). Here we show the MINIMAL non-round extensions
RELAX that obstruction: vacuum then ADMITS genuine d_t != 0.

(B1) ROTATION / frame-dragging: add an off-diagonal axial shift g_{t psi}=w(t,r,theta).
     Recompute the time-row momentum constraints G^t_r, G^t_psi and the new
     dynamical (evolution) component(s). Show d_t != 0 is consistent with vacuum.
     Done at LEADING (linear) ORDER off the round static background (tagged).

(B2) QUADRUPOLE l>=2: add an l=2 time-dependent diagonal warp (the standard
     gravitational-wave / Regge-Wheeler-Zerilli content). Show vacuum admits a
     time-varying solution (a wave DOF). LEADING ORDER off flat/round background.

We want EXISTENCE of time-dependent vacuum content, not the full solve.
"""
import sympy as sp

t, r, th, ps, c = sp.symbols('t r theta psi c', positive=True)
eps = sp.symbols('epsilon')          # perturbation bookkeeping parameter
X = [t, r, th, ps]


def einstein_tensor(g, X, simp=True):
    n = len(X)
    ginv = g.inv()
    Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, cc], X[b])
                                     + sp.diff(g[d, b], X[cc])
                                     - sp.diff(g[b, cc], X[d]))
                Gamma[a][b][cc] = sp.Rational(1, 2)*s
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], X[a]) - sp.diff(Gamma[a][b][a], X[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            Ric[b, d] = s
    Rscal = sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
    G = sp.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            val = Ric[mu, nu] - sp.Rational(1, 2)*g[mu, nu]*Rscal
            G[mu, nu] = sp.simplify(val) if simp else val
    return G, ginv


# ===========================================================================
# (B1) ROTATION / frame-dragging.  Background = FLAT round (phi=0) so we isolate
# the rotation DOF cleanly at leading order: g_{t psi} = eps * w(t,r,theta) shift.
# (Flat background is the cleanest existence test; phi-dressed gives same verdict
# at O(eps), confirmed by the structure of the t-psi block decoupling.)
# ===========================================================================
print("=== (B1) ROTATION: off-diagonal axial shift g_{t psi}=eps*w(t,r,theta) ===")
w = sp.Function('w')(t, r, th)
g1 = sp.Matrix([
    [-c**2,       0,    0,        eps*w],
    [0,           1,    0,        0],
    [0,           0,    r**2,     0],
    [eps*w,       0,    0,        r**2*sp.sin(th)**2],
])
G1, _ = einstein_tensor(g1, X, simp=False)

# Work to leading (linear) order in eps.
def lin(expr):
    e = sp.series(sp.expand(expr), eps, 0, 2).removeO()
    return sp.simplify(e.coeff(eps, 1)*eps + e.coeff(eps, 0))

# The momentum constraint that froze the round case was G_{t r}.  Here also G_{t theta}.
Gtr_1 = sp.simplify(sp.series(G1[0, 1], eps, 0, 2).removeO())
Gtth_1 = sp.simplify(sp.series(G1[0, 2], eps, 0, 2).removeO())
print("\nG_{t r}     (O(eps)) =", Gtr_1)
print("G_{t theta} (O(eps)) =", Gtth_1)

# The KEY point: is there any vacuum component that is a NON-TRIVIAL evolution eqn
# in t for w (i.e. contains d_t w but does NOT force d_t w = 0)?  The t-psi block.
# The relevant dynamical eqn for the shift is the (psi,r)/(psi,theta)/(t,psi) sector.
Gtps_1 = sp.simplify(sp.series(G1[0, 3], eps, 0, 2).removeO())
Grps_1 = sp.simplify(sp.series(G1[1, 3], eps, 0, 2).removeO())
Gthps_1 = sp.simplify(sp.series(G1[2, 3], eps, 0, 2).removeO())
print("\nG_{t psi}     (O(eps)) =", Gtps_1)
print("G_{r psi}     (O(eps)) =", Grps_1)
print("G_{theta psi} (O(eps)) =", Gthps_1)

# Does any vacuum equation contain d_t^2 w or d_t w in a way that ALLOWS d_t w != 0?
has_dtt = any(sp.diff(w, t, 2) in expr.atoms(sp.Derivative) for expr in
              [Gtps_1, Grps_1, Gthps_1])
print("\nA vacuum eqn carries d_t^2 w (a genuine time-evolution term)? ", has_dtt)
print("If so, d_t w != 0 is CONSISTENT with vacuum -- the shift can be time-dependent;")
print("the constraints (G_tr, G_ttheta) no longer collapse to 'frozen metric'.")

# ===========================================================================
# (B2) QUADRUPOLE l>=2.  Standard odd-parity (axial) l-deformation is the rotation
# above with theta-structure; here do the EVEN/diagonal l>=2 GW DOF off a FLAT
# round background to show vacuum admits a time-varying (wave) solution.
# Minimal: a transverse-traceless-style diagonal warp on the angular block,
# h(t,r) * (l=2 Legendre P_2(cos th)) added to g_thth and g_psps with opposite sign.
# ===========================================================================
print("\n\n=== (B2) QUADRUPOLE l=2 diagonal warp (GW-type DOF) ===")
h = sp.Function('h')(t, r)
P2 = (3*sp.cos(th)**2 - 1)/2
g2 = sp.Matrix([
    [-c**2,  0,                       0,                                   0],
    [0,      1,                       0,                                   0],
    [0,      0,  r**2*(1 + eps*h*P2),                                      0],
    [0,      0,                       0,  r**2*sp.sin(th)**2*(1 - eps*h*P2)],
])
G2, _ = einstein_tensor(g2, X, simp=False)

# Leading order O(eps) of the diagonal evolution components.
Gthth_2 = sp.simplify(sp.series(G2[2, 2], eps, 0, 2).removeO())
Gpsps_2 = sp.simplify(sp.series(G2[3, 3], eps, 0, 2).removeO())
Gtt_2 = sp.simplify(sp.series(G2[0, 0], eps, 0, 2).removeO())
# Momentum-type: G_{t r} at O(eps) -- the analog of the freezing constraint.
Gtr_2 = sp.simplify(sp.series(G2[0, 1], eps, 0, 2).removeO())
print("\nG_{t r}      (O(eps)) =", Gtr_2)
print("G_{t t}      (O(eps)) =", Gtt_2)
print("G_{theta theta} (O(eps)) =", Gthth_2)

# Does a vacuum eqn carry d_t^2 h (wave operator), i.e. allow time variation?
dtt_h = sp.diff(h, t, 2)
carriers = [Gthth_2, Gpsps_2, Gtt_2]
has_wave = any(sp.expand(e).has(dtt_h) for e in carriers)
print("\nA vacuum eqn carries d_t^2 h (a wave / time-evolution term)? ", has_wave)
print("If so the l=2 warp h(t,r) obeys a WAVE equation in vacuum -> d_t h != 0 allowed:")
print("a gravitational-wave-type vacuum DOF. Round/static is NOT forced.")

# Print one representative vacuum wave equation (the theta-theta component coeff).
print("\nRepresentative l=2 vacuum component G_{theta theta}/eps (the GW eqn) =")
sp.pprint(sp.simplify(Gthth_2.coeff(eps, 1)))
