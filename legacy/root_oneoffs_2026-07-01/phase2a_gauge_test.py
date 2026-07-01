#!/usr/bin/env python3
"""
phase2a_gauge_test.py -- PHASE-2a step 1 (THE GATE): is the Phase-0 B1 frame-drag
profile g_tpsi = eps*w(r,theta) a GENUINE bounded physical rotating mode, or a
coordinate/gauge rotation (a relabeling)?

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE.
c=1. Reuses the Phase-0 sympy Einstein machinery (independent re-derivation here).

Phase-0/verifier found the joint vacuum profile Wf = r^2 sin^2(theta) (linearized-
Kerr frame-drag) solves all O(eps) constraints. OPEN QUESTION (verifier-flagged):
is that r^2-growing profile a BOUNDED physical rotating mode, or a rotation GAUGE
mode (pure coordinate)?

GAUGE-INVARIANT TESTS run here (any ONE positive => physical; all gauge => stop):
  (T1) RIGID-ROTATION GAUGE SUBTRACTION. A pure coordinate rotation
       psi -> psi + Omega(t) generates an off-diagonal g_tpsi = Omega'(t)*r^2 sin^2(th)
       (to linear order, on flat bg). If the FOUND w(r,theta) is EXACTLY of this
       form (w = const * r^2 sin^2 th, with the time-dep that a coordinate rotation
       would give), it is PURE GAUGE -- removable by un-rotating. Test: does
       w = c0 * r^2 sin^2(theta) get killed by psi -> psi - integral Omega dt?
  (T2) KOMAR ANGULAR MOMENTUM J. Compute the Komar J = -(1/16 pi) oint
       nabla^a xi^b dS_ab with xi = d/dpsi (axial Killing vector) on a large
       sphere. A pure gauge rotation carries J=0 (no real angular momentum); a
       physical rotating geometry carries J != 0 that cannot be transformed away.
  (T3) CURVATURE. Does the frame-drag change a curvature SCALAR (Kretschmann
       R_abcd R^abcd) at O(eps) or O(eps^2)? Pure gauge cannot change an invariant.
       (At O(eps) linear, invariants built from a vacuum bg are typically gauge;
       the honest test is whether J -- the conserved charge -- is nonzero, T2.)

The decisive object is T2 (Komar J): J is the gauge-invariant conserved charge.
If J=0 for the bounded/regular profile, rotation adds no physical content at this
(linear, single-shift) order; if J!=0, rotation is physical and we proceed to the
nonlinear solve (step 2).
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
eps = sp.symbols('epsilon')
X = [t, r, th, ps]
sin, cos, cot = sp.sin, sp.cos, sp.cot


def christoffel(g, X):
    n = len(X)
    ginv = g.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, cc], X[b])
                                       + sp.diff(g[d, b], X[cc])
                                       - sp.diff(g[b, cc], X[d]))
                Gamma[a][b][cc] = sp.Rational(1, 2) * s
    return Gamma, ginv


def riemann_lower(g, X):
    """R_{abcd} fully lowered."""
    n = len(X)
    Gamma, ginv = christoffel(g, X)
    # R^a_{bcd}
    Rup = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    s = sp.diff(Gamma[a][b][d], X[cc]) - sp.diff(Gamma[a][b][cc], X[d])
                    for e in range(n):
                        s += Gamma[a][cc][e] * Gamma[e][b][d] - Gamma[a][d][e] * Gamma[e][b][cc]
                    Rup[a][b][cc][d] = s
    Rlow = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    s = sp.S(0)
                    for e in range(n):
                        s += g[a, e] * Rup[e][b][cc][d]
                    Rlow[a][b][cc][d] = s
    return Rlow, ginv


def kretschmann(g, X):
    Rlow, ginv = riemann_lower(g, X)
    n = len(X)
    # raise all indices
    Rup4 = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    s = sp.S(0)
                    for p in range(n):
                        for q in range(n):
                            for u in range(n):
                                for v in range(n):
                                    s += (ginv[a, p] * ginv[b, q] * ginv[cc, u] * ginv[d, v]
                                          * Rlow[p][q][u][v])
                    Rup4[a][b][cc][d] = s
    K = sp.S(0)
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    K += Rlow[a][b][cc][d] * Rup4[a][b][cc][d]
    return sp.simplify(K)


print("=" * 78)
print("PHASE-2a STEP 1 (THE GATE): gauge-vs-physical of the B1 frame-drag")
print("=" * 78)

# ---------------------------------------------------------------------------
# (T1) RIGID-ROTATION GAUGE SUBTRACTION
# A coordinate rotation psi' = psi - alpha(t). Under it the FLAT metric
#   ds^2 = -dt^2 + dr^2 + r^2 dth^2 + r^2 sin^2 th dpsi^2
# picks up (writing in the new chart, then dropping the O(alpha'^2) term):
#   g_{t psi} = + alpha'(t) * r^2 sin^2(theta)   (the gauge frame-drag).
# So a PURE GAUGE frame-drag has spatial profile EXACTLY Wf_gauge = r^2 sin^2 th.
# ---------------------------------------------------------------------------
print("\n--- (T1) Rigid-rotation gauge shift profile ---")
alpha = sp.Function('alpha')(t)
# flat metric in rotating chart psi -> psi - alpha(t): substitute dpsi -> dpsi - alpha' dt
# g_tpsi term coefficient:
Wf_gauge = r**2 * sin(th)**2
print("  A pure coordinate rotation psi->psi-alpha(t) yields")
print("    g_tpsi = alpha'(t) * r^2 sin^2(theta);  spatial profile Wf_gauge =", Wf_gauge)
print("  The Phase-0/verifier joint vacuum profile was Wf = r^2 sin^2(theta).")
print("  => Wf MATCHES the rigid-rotation gauge profile EXACTLY (spatial part).")
print("  This is the SMOKING GUN to check with the gauge-invariant charge (T2).")

# ---------------------------------------------------------------------------
# (T2) KOMAR ANGULAR MOMENTUM of the found profile.
# Build the linearized metric g = flat + eps * h with h_{t psi} = w(r,theta),
# w = Wf (time-independent stationary frame-drag, as the constraint allows).
# Komar J = +(1/16 pi) oint_{S} eps^{ab}{}_{cd} nabla^c xi^d dS_ab,  xi = d/dpsi.
# Equivalent practical form: J = (1/16 pi) oint  (nabla^a xi^b - nabla^b xi^a) dS_ab
# Use the standard result J = -(1/8 pi) oint nabla^a xi^b dS_{ab} over a 2-sphere
# at radius r, with dS_{ab} the area element with normals (t-direction, r-direction).
# For a stationary axisymmetric metric, the Komar J integrand reduces to a
# surface integral of derivatives of g_{t psi}. We compute it symbolically.
# ---------------------------------------------------------------------------
print("\n--- (T2) Komar angular momentum J (gauge-invariant conserved charge) ---")

W = sp.Function('W')(r, th)   # general stationary profile; substitute later
g = sp.Matrix([
    [-1,        0,    0,            eps * W],
    [0,         1,    0,            0],
    [0,         0,    r**2,         0],
    [eps * W,   0,    0,            r**2 * sin(th)**2],
])

Gamma, ginv = christoffel(g, X)

# axial Killing vector xi^mu = (0,0,0,1) ; lower: xi_mu = g_{mu psi}
xi_up = sp.Matrix([0, 0, 0, 1])
xi_low = g * xi_up

# covariant derivative nabla^a xi^b (the Komar 2-form F^{ab} = nabla^a xi^b - nabla^b xi^a)
# nabla_a xi_b = d_a xi_b - Gamma^c_{ab} xi_c
def nabla_lower(a, b):
    expr = sp.diff(xi_low[b], X[a])
    for cidx in range(4):
        expr -= Gamma[cidx][a][b] * xi_low[cidx]
    return expr

# Komar 2-form antisymmetric F_{ab} = nabla_a xi_b - nabla_b xi_a
# The Komar integral over a 2-sphere at fixed t,r: J = -(1/16 pi) oint F^{rt}*sqrt(-g_2)...
# Practical reduction (Wald): J = -(1/8 pi) oint nabla^mu xi^nu dS_{mu nu},
# with dS_{mu nu} = -2 n_[mu s_nu] sqrt(sigma) dth dpsi (n=timelike, s=radial unit normals).
# We compute the integrand F^{tr} = g^{ta} g^{rb} F_{ab} and the area measure.

# To O(eps): F_{tr} relevant component
F_tr = nabla_lower(0, 1) - nabla_lower(1, 0)        # not the J integrand directly
# The J flux uses the {t,r} normal pair. Standard formula:
#   J = (1/16 pi) oint_{S_inf}  nabla^a xi^b dS_ab,  dS_ab = (n_a s_b - n_b s_a) dArea
# n_a = (-N,0,0,0) (unit timelike), s_a = (0, sqrt(g_rr),0,0) (unit radial).
# nabla^a xi^b dS_ab = 2 nabla^a xi^b n_[a s_b] = (nabla^t xi^r - nabla^r xi^t)*(n_t s_r)*...
# Cleanest: J = -(1/8 pi) oint  F^{tr} (n_t s_r) sqrt(sigma) dth dpsi, sigma=induced 2-metric det.
# Compute F^{tr} = nabla^t xi^r - nabla^r xi^t.
def nabla_upper(a, b):
    # nabla^a xi^b = g^{a m} g^{b n} nabla_m xi_n ... but simpler: nabla^a xi^b = g^{am} nabla_m xi^b
    # xi^b is the vector; nabla_m xi^b = d_m xi^b + Gamma^b_{m c} xi^c
    out = sp.S(0)
    for m in range(4):
        nab_m_xi_b = sp.diff(xi_up[b], X[m])
        for cidx in range(4):
            nab_m_xi_b += Gamma[b][m][cidx] * xi_up[cidx]
        out += ginv[a, m] * nab_m_xi_b
    return out

Ftr_up = sp.expand(nabla_upper(0, 1) - nabla_upper(1, 0))
Ftr_up = sp.series(Ftr_up, eps, 0, 2).removeO()
Ftr_up = sp.simplify(Ftr_up.coeff(eps, 1)) * eps  # keep O(eps) (linear)
print("  F^{tr} = nabla^t xi^r - nabla^r xi^t  (to O(eps)):")
print("   ", sp.simplify(Ftr_up))

# area measure of the 2-sphere {t,r fixed}: induced metric diag(r^2, r^2 sin^2 th)
# sqrt(sigma) = r^2 sin th (to O(eps); the off-diag does not change det at O(eps))
sqrt_sigma = r**2 * sin(th)
# unit normals: n_t = -1 (flat lapse to O(eps)), s_r = +1 (flat). The Komar measure
# n_[a s_b] picks (t,r). The J integrand (1/16pi) * F^{ab} dS_ab with dS_ab = 2 n_[a s_b] dArea:
# integrand = (1/16 pi) * F^{tr} * 2 * (n_t s_r) * sqrt_sigma ... = (1/8pi) F^{tr}(n_t s_r) sqrt_sigma
# With n_t=-1, s_r=1 (lowered components for the measure): use the Komar normalization
# J = (1/16 pi) oint F^{ab} dS_ab. We report the th,psi integrand and its sphere integral.
n_t = -1
s_r = 1
J_integrand = sp.Rational(1, 16) / sp.pi * (Ftr_up / eps) * 2 * (n_t * s_r) * sqrt_sigma
# integrate over psi (0..2pi) and theta (0..pi)
J = sp.integrate(sp.integrate(J_integrand, (ps, 0, 2 * sp.pi)), (th, 0, sp.pi))
J = sp.simplify(J)
print("\n  Komar J (per unit eps), GENERAL stationary profile W(r,theta):")
print("    J/eps =", J, "   (a function of W and its r-derivative at the sphere)")

# Now substitute the FOUND profile W = r^2 sin^2(theta) (linearized-Kerr / gauge form)
print("\n  Substitute the FOUND profile W = r^2 sin^2(theta):")
J_found = sp.simplify(J.subs(sp.Function('W')(r, th), r**2 * sin(th)**2).doit())
# recompute the integrand fresh with explicit W to be safe
Wexpr = r**2 * sin(th)**2
g2 = g.subs(W, Wexpr)
Gamma2, ginv2 = christoffel(g2, X)
xi_low2 = g2 * xi_up
def nabla_upper2(a, b):
    out = sp.S(0)
    for m in range(4):
        nab = sp.diff(xi_up[b], X[m])
        for cidx in range(4):
            nab += Gamma2[b][m][cidx] * xi_up[cidx]
        out += ginv2[a, m] * nab
    return out
Ftr2 = sp.expand(nabla_upper2(0, 1) - nabla_upper2(1, 0))
Ftr2 = sp.series(Ftr2, eps, 0, 2).removeO()
Ftr2_lin = sp.simplify(Ftr2.coeff(eps, 1))
print("    F^{tr} (O(eps) coeff) for W=r^2 sin^2 th:", Ftr2_lin)
sqrt_sigma2 = r**2 * sin(th)
J_integrand2 = sp.Rational(1, 16) / sp.pi * Ftr2_lin * 2 * (n_t * s_r) * sqrt_sigma2
J2 = sp.simplify(sp.integrate(sp.integrate(J_integrand2, (ps, 0, 2 * sp.pi)), (th, 0, sp.pi)))
print("    Komar J/eps for the found profile =", J2)

# ---------------------------------------------------------------------------
# (T3) KRETSCHMANN at O(eps), O(eps^2) for the found profile (curvature reality)
# ---------------------------------------------------------------------------
print("\n--- (T3) Kretschmann invariant change from the frame-drag (found profile) ---")
Kfull = kretschmann(g2, X)
Kser = sp.series(Kfull, eps, 0, 3).removeO()
K0 = sp.simplify(Kser.coeff(eps, 0))
K1 = sp.simplify(Kser.coeff(eps, 1))
K2 = sp.simplify(Kser.coeff(eps, 2))
print("    K at O(eps^0) (flat bg):", K0)
print("    K at O(eps^1):", K1)
print("    K at O(eps^2):", K2)

print("\n" + "=" * 78)
print("VERDICT LOGIC:")
print("  If J/eps == 0 AND K-change == 0 for the found bounded/constraint profile")
print("    => the B1 frame-drag is PURE GAUGE (a relabeling) -> rotation adds")
print("       NOTHING at linear single-shift order -> OUTCOME C-rot, STOP.")
print("  If J/eps != 0 (real conserved angular momentum) => PHYSICAL -> proceed")
print("       to the nonlinear rotating solve (step 2).")
print("=" * 78)
