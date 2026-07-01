"""W1 ROUTE C — BLIND ADVERSARIAL VERIFIER (new file, 2026-06-11).

Independent re-derivation + targeted attacks on the claims of
w_stiffness_routeC_sector_audit.py (41/41 PASS claimed).  This file was
written WITHOUT reusing the route script's code paths: the metric, flux,
and Hessian objects are rebuilt from their banked definitions, and the
identity checks use DIFFERENT methods (numeric finite differences and
Gauss quadrature where the route used symbolic series).

ATTACK MAP
  V0  independent rebuild of the P1 class; flux closed form + tadpole
      formulas re-derived from scratch; q* branch of C1 re-derived
      (the sign claim of the tadpole's "opposition" depends on it).
  V1  ENLARGEMENT BEYOND THE ROUTE: off-diagonal angular block
      g_thetaphi = r^2 p(r,theta) — does any sector density acquire
      angular-block derivatives there?  (S6 only audited diagonal A, B.)
  V2  general Maxwell potential, all four components A_mu(r,theta), on
      the off-diagonal-extended block: density differentiates only A.
  V3  THE MAXWELL RE-SOLVING ATTACK (sharpest): at q != 0 the banked
      monopole representative is OFF Maxwell-shell (route's own check);
      Maxwell dynamics is banked as metric-given (UDT_REBUILD Part T via
      native_areal_function_field_equations.py section B), so the
      on-shell flux sector at q != 0 is E[F*(g), g] with F* a PDE
      solution that depends functionally on the metric.  The zeroth-jet
      density argument does NOT by itself control the w-content of the
      ON-SHELL sector.  Checks: (a) residual is O(q^1) and nonzero;
      (b) the cross-Hessian d^2E/dw dA vanishes IDENTICALLY at q = 0
      (diagonal class airtight: no field response to w at all) but is
      NONZERO at q != 0 (a w-response of the solved field EXISTS there);
      (c) order counting: the response correction to the on-shell
      w-force is O(q^3), so the route's tadpole formula IS the exact
      on-shell w-force at its leading O(q^2) — but the claim "the
      action's derivative content is unaffected [by re-solving]" is an
      overstatement for the on-shell SECTOR functional: at q != 0,
      integrating out the solved field produces a NONLOCAL w-w kernel
      (order-zero symbol: M^T G M with M first-order, G ~ k^-2 — no k^2
      growth, hence still no gradient stiffness and no propagation, but
      not pointwise-algebraic either).
  V4  claim-4 identity (responsive Hessian = C1 angular second
      variation) checked by NUMERIC second mixed finite differences at
      random points with explicit non-harmonic test functions (mpmath,
      30 digits) — method-independent of the route's symbolic check.
  V5  banked couplings V_a1g1 = -sqrt(5) kappa/(2F), V_a0g0 =
      -sqrt(15) kappa/(3F) re-derived by Gauss-Legendre quadrature of
      the FULL (unexpanded) Hessian integrand + central difference in
      kappa — no series expansion, independent of the route's method.
  V6  NON-VACUITY GUARD on the route's S5 momenta checks (diff w.r.t. a
      Derivative atom can be vacuously zero): redo as a first-variation
      computation with an explicit fluctuation function; require the
      variation itself be NONZERO while containing no fluctuation
      derivatives.
  V7  STATICS-PREMISE PROBE (attack E): rebuild flux/source/completion
      densities with f, q, v functions of (t, r, theta): verify the
      "structural extension to the full time row" note (no metric time
      derivatives appear).  The same-minus time-row metric enlargement
      is excluded by the banked theorem-grade elimination; the weld
      objects (f phi0' H1 = 2 d_t(dphi), rung-2) are TIME-sector
      constraint identities, not action pieces — adjudicated in the
      report, not here.

Verifier agent: blind adversarial pass, 2026-06-11.  Run:
    python3 w_stiffness_routeC_verifier.py
"""

from __future__ import annotations

import sys

import mpmath as mp
import numpy as np
import sympy as sp

FAILURES: list[str] = []
NCHECK = 0


def check(label: str, ok: bool) -> None:
    global NCHECK
    NCHECK += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def diff_funcs(expr) -> set:
    """Functions appearing differentiated anywhere in expr (own impl)."""
    expr = sp.sympify(expr).doit()
    out = set()
    for d in expr.atoms(sp.Derivative):
        out.add(d.expr.func)
    return out


# ===========================================================================
hr("V0 — INDEPENDENT REBUILD: P1 metric, flux density, tadpole, q* branch")
# ===========================================================================
t, r, th, ph = sp.symbols("T r theta varphi", real=True)
r = sp.Symbol("r", positive=True)
cc = sp.Symbol("c", positive=True)
mu = sp.Symbol("mu", positive=True)
Qf = sp.Symbol("Q_f", real=True)
s_s = sp.Symbol("s", real=True)
Wr = sp.Function("W")(r)
sth = sp.sin(th)
coords = [t, r, th, ph]

f = sp.Function("f", positive=True)(r, th)
q = sp.Function("q", real=True)(r, th)
v = sp.Function("v", positive=True)(r, th)

# build the metric as a sum of symmetric products (different construction
# from the route's explicit Matrix fill)
g = sp.zeros(4, 4)
for (a, b, val) in [(0, 0, -f), (1, 1, 1 / f), (1, 2, q),
                    (2, 2, r**2 * v**2), (3, 3, r**2 * sth**2 / v**2)]:
    g[a, b] = val
    g[b, a] = val
D2 = r**2 * v**2 - f * q**2
detg = sp.factor(g.det())
check("independent det: -det g = r^2 sin^2(th) D / v^2, D = r^2 v^2 - f q^2",
      sp.simplify(-detg - r**2 * sth**2 * D2 / v**2) == 0)
sqrtmg = r * sth * sp.sqrt(D2) / v
ginv = g.inv()

# flux density rebuilt
F0 = sp.zeros(4, 4)
F0[2, 3] = Qf * sth
F0[3, 2] = -Qf * sth
F0up = ginv * F0 * ginv
L_flux = sp.simplify(-(1 / (4 * mu)) * sqrtmg
                     * sum(F0[i, j] * F0up[i, j] for i in range(4)
                           for j in range(4)))
check("claimed closed form: L_flux = -(Q_f^2/(2 mu)) sin(th)(1+w)/(r sqrt(D))"
      "  [v = 1+w]",
      sp.simplify(L_flux + (Qf**2 / (2 * mu)) * sth * v / (r * sp.sqrt(D2)))
      == 0)
check("claimed tadpole: dL_flux/dw = +(Q_f^2/(2 mu)) sin(th) f q^2 /"
      " (r D^{3/2}) exactly",
      sp.simplify(sp.diff(L_flux, v)
                  - (Qf**2 / (2 * mu)) * sth * f * q**2
                  / (r * D2**sp.Rational(3, 2))) == 0)
check("q = 0: L_flux is exactly w-blind (independent rebuild)",
      not any(a.func == v.func
              for a in sp.simplify(L_flux.subs(q, 0)).atoms(sp.Function)))
check("flux density zeroth-jet (independent jet scan): no Derivative atoms",
      diff_funcs(L_flux) == set())

# C1 density rebuilt with the FULL g^{mu nu} contraction (all 16 terms,
# not just the 3 the route hand-picked — guards a dropped-term error)
phi = -sp.log(f) / 2
dphi = [sp.diff(phi, x) for x in coords]
Kkin_full = sum(ginv[i, j] * dphi[i] * dphi[j]
                for i in range(4) for j in range(4))
L_C1 = sp.simplify(-(cc / 2) * f * Kkin_full * sqrtmg)
check("C1 rebuilt with all 16 inverse-metric terms: only f differentiated",
      diff_funcs(L_C1) == {f.func})

# q* branch re-derivation (basis of the 'opposition' sign claim) —
# pointwise symbols (the elimination is pointwise-algebraic), with the
# route's declared Delta > 0 branch condition imposed by an explicit
# positive parameter: F_th^2 = F F_r^2 R^2 V^2 - Delta, Delta > 0.
Fs, Frs, Vs, Rs, qs2, tau = sp.symbols("F F_r V R q tau", positive=True)
# Delta = X/(1+tau) with X = F F_r^2 R^2 V^2 encodes 0 < Delta < X, so
# the simplifier can resolve every nested-sqrt sign on the branch
Dl = Fs * Frs**2 * Rs**2 * Vs**2 / (1 + tau)
Fths = sp.sqrt(Fs * Frs**2 * Rs**2 * Vs**2 - Dl)   # Delta > 0 branch
sths = sp.Symbol("sin_th", positive=True)
Dpt = Rs**2 * Vs**2 - Fs * qs2**2
Lpt = (-(cc / 8) * Rs * sths
       * (Fs * Rs**2 * Vs**2 * Frs**2 - 2 * Fs * qs2 * Frs * Fths
          + Fths**2) / (Vs * Fs * sp.sqrt(Dpt)))
qroots = sp.solve(sp.diff(Lpt, qs2), qs2)
target_pt = -(cc / 8) * sths * (Fs * Rs**2 * Frs**2 - Fths**2 / Vs**2) / Fs
hit = any(sp.simplify(sp.simplify(Lpt.subs(qs2, sol)) - target_pt) == 0
          for sol in qroots)
check("q* elimination re-derived from scratch (Delta > 0 branch): the "
      "root of dL_C1/dq = 0 gives L_eff = -(c/8) sin(th)[f r^2 f_r^2 - "
      "f_th^2/(1+w)^2]/f exactly (the banked sign-flipped branch); NOTE "
      "the match requires the Delta > 0 condition — on Delta < 0 the "
      "eliminated density flips overall sign and the w-force there is "
      "POSITIVE (same sign as the flux tadpole, not opposed)", hit)
fr, fth = sp.diff(f, r), sp.diff(f, th)
target = -(cc / 8) * sth * (f * r**2 * fr**2 - fth**2 / v**2) / f
wforce = sp.simplify(sp.diff(target, v))
check("branch w-force re-derived: dL_eff/dw = -(c/4) sin(th) f_th^2/"
      "(f(1+w)^3) — NEGATIVE; the flux tadpole (positive) indeed opposes it",
      sp.simplify(wforce + (cc / 4) * sth * fth**2 / (f * v**3)) == 0)

# ===========================================================================
hr("V1 — ENLARGEMENT THE ROUTE DID NOT AUDIT: off-diagonal angular block "
   "g_theta-phi = r^2 p(r,theta)")
# ===========================================================================
Af = sp.Function("A", positive=True)(r, th)
Bf = sp.Function("B", positive=True)(r, th)
pf = sp.Function("p", real=True)(r, th)
gX = sp.zeros(4, 4)
for (a, b, val) in [(0, 0, -f), (1, 1, 1 / f), (1, 2, q),
                    (2, 2, r**2 * Af), (3, 3, r**2 * sth**2 * Bf),
                    (2, 3, r**2 * pf)]:
    gX[a, b] = val
    gX[b, a] = val
gXinv = gX.inv()
sqrtmgX = sp.sqrt(sp.factor(-gX.det()))
KkinX = sum(gXinv[i, j] * dphi[i] * dphi[j]
            for i in range(4) for j in range(4))
L_C1_X = -(cc / 2) * f * KkinX * sqrtmgX
F0upX = gXinv * F0 * gXinv
L_flux_X = -(1 / (4 * mu)) * sqrtmgX * sum(
    F0[i, j] * F0upX[i, j] for i in range(4) for j in range(4))
L_src_X = sp.Rational(1, 2) * s_s * Wr * f**2 * sqrtmgX / r**2
check("C1 on the off-diagonal-extended block: differentiates f ONLY "
      "(no dA, dB, dp, dq) — claim-2 structure survives the enlargement "
      "the route did not test",
      diff_funcs(L_C1_X) == {f.func})
check("flux on the off-diagonal-extended block: NO derivatives at all",
      diff_funcs(L_flux_X) == set())
check("source (proper reading) on the off-diagonal-extended block: NO "
      "derivatives",
      diff_funcs(L_src_X) == set())

# ===========================================================================
hr("V2 — GENERAL MAXWELL POTENTIAL, ALL FOUR COMPONENTS, on the extended "
   "block: no Christoffels can enter (independent of the route's 2-comp.)")
# ===========================================================================
Amu = [sp.Function(f"A_{n}", real=True)(r, th) for n in range(4)]
Fg = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Fg[a, b] = sp.diff(Amu[b], coords[a]) - sp.diff(Amu[a], coords[b])
FgupX = gXinv * Fg * gXinv
L_max_X = -(1 / (4 * mu)) * sqrtmgX * sum(
    Fg[i, j] * FgupX[i, j] for i in range(4) for j in range(4))
check("general 4-potential Maxwell density on the extended block "
      "differentiates ONLY the A_mu — never f, q, A, B, p",
      diff_funcs(L_max_X) <= {a.func for a in Amu})

# ===========================================================================
hr("V3 — MAXWELL RE-SOLVING ATTACK at q != 0 (the on-shell sector is "
   "E[F*(g), g], F* a metric-dependent PDE solution)")
# ===========================================================================
# (a) residual of the monopole rep: nonzero, leading order O(q^1)
eps = sp.Symbol("epsilon", real=True)
sub_q = {q: eps * q}
res_phi = sum(sp.diff(sqrtmg * F0up[m, 3], coords[m]) for m in range(4))
res_phi_eps = sp.expand(sp.series(res_phi.subs(sub_q).doit(), eps, 0, 2)
                        .removeO())
res_O0 = sp.simplify(res_phi_eps.coeff(eps, 0))
res_O1 = sp.simplify(res_phi_eps.coeff(eps, 1))
check("monopole Maxwell residual (nu = varphi): O(q^0) term vanishes "
      "(on-shell at q = 0 for ANY f, w)", res_O0 == 0)
check("monopole Maxwell residual: O(q^1) term NONZERO — the correction "
      "field A1 is O(q) and solves a PDE with metric-dependent "
      "coefficients (F* is a functional of the metric)", res_O1 != 0)
check("the O(q) residual involves DERIVATIVES of metric functions "
      "(f and/or v differentiated) — the re-solved flux inherits metric "
      "derivative content through its SOURCE",
      len(diff_funcs(res_O1) & {f.func, v.func, q.func}) > 0)

# (b) cross-Hessian d^2 E / dw dA: the operator that propagates a field
# response dA*/dw into the on-shell w-Hessian
a_t = sp.Function("a_t", real=True)(r, th)
a_p = sp.Function("a_p", real=True)(r, th)
dF = sp.zeros(4, 4)
for (a, b, val) in [(1, 0, sp.diff(a_t, r)), (2, 0, sp.diff(a_t, th)),
                    (1, 3, sp.diff(a_p, r)), (2, 3, sp.diff(a_p, th))]:
    dF[a, b] = val
    dF[b, a] = -val
cross = -(1 / (2 * mu)) * sqrtmg * sum(
    F0up[i, j] * dF[i, j] for i in range(4) for j in range(4))
cross_w = sp.simplify(sp.diff(cross, v))
check("cross-Hessian d^2E/dw dA vanishes IDENTICALLY at q = 0 (every "
      "fluctuation direction a_t, a_p): on the diagonal class the solved "
      "field has NO w-response — the route's q = 0 conclusions are "
      "airtight on-shell, not just off-shell",
      sp.simplify(cross_w.subs(q, 0).doit()) == 0)
check("cross-Hessian NONZERO at q != 0: a w-response of the solved flux "
      "field EXISTS on the q-on class — the zeroth-jet density argument "
      "alone does NOT control the on-shell sector's w-content there",
      sp.simplify(cross_w) != 0)

# (c) order counting at a generic POINT (algebraic coefficients):
fs, qs, vs, rs = sp.symbols("f_s q_s v_s r_s", positive=True)
pt = {f: fs, q: eps * qs, v: vs, r: rs}
c_thph = (sqrtmg * F0up[2, 3]).subs(pt).doit()
c_rph = (sqrtmg * F0up[1, 3]).subs(pt).doit()
dv_c_thph = sp.series(sp.diff(c_thph, vs), eps, 0, 3).removeO()
dv_c_rph = sp.series(sp.diff(c_rph, vs), eps, 0, 3).removeO()
ok_orders = (sp.simplify(dv_c_thph.coeff(eps, 0)) == 0
             and sp.simplify(dv_c_thph.coeff(eps, 1)) == 0
             and sp.simplify(dv_c_rph.coeff(eps, 0)) == 0
             and sp.simplify(dv_c_rph.coeff(eps, 1)) == 0)
check("order counting: d/dw of the cross coefficients sqrt(-g)F0^{th ph}, "
      "sqrt(-g)F0^{r ph} are both O(q^2); with the response A1 = O(q) the "
      "on-shell correction to the w-force is O(q^3) — the route's tadpole "
      "formula IS the exact on-shell w-force at its leading order O(q^2)",
      ok_orders)
tad_pt = sp.series(sp.diff(
    (-(Qf**2 / (2 * mu)) * sth * vs
     / (rs * sp.sqrt(rs**2 * vs**2 - fs * (eps * qs)**2))), vs),
    eps, 0, 3).removeO()
check("consistency: the tadpole itself is O(q^2) with the claimed "
      "coefficient +(Q_f^2/(2 mu)) sin(th) f q^2/(r (r v)^3) at leading "
      "order",
      sp.simplify(tad_pt.coeff(eps, 2)
                  - (Qf**2 / (2 * mu)) * sth * fs * qs**2
                  / (rs**4 * vs**3)) == 0)

# ===========================================================================
hr("V4 — CLAIM 4 IDENTITY by numeric finite differences (independent "
   "method): d^2/dx1 dx2 [|grad f|^2 / f] vs the quoted Hessian integrand")
# ===========================================================================
mp.mp.dps = 30
kapN, FN = mp.mpf("0.37"), mp.mpf("1.55")


def gdN(g1, g2, c, p, h=mp.mpf("1e-8")):
    d1c = (g1(c + h, p) - g1(c - h, p)) / (2 * h)
    d2c = (g2(c + h, p) - g2(c - h, p)) / (2 * h)
    d1p = (g1(c, p + h) - g1(c, p - h)) / (2 * h)
    d2p = (g2(c, p + h) - g2(c, p - h)) / (2 * h)
    return (1 - c**2) * d1c * d2c + d1p * d2p / (1 - c**2)


def Y1N(c, p):
    return (1 - c**2) * mp.cos(p) + mp.mpf("0.3") * c


def Y2N(c, p):
    return c**3 - mp.mpf("0.2") * mp.sin(p) * mp.sqrt(1 - c**2)


def BN(c, p):
    return FN * (1 + kapN * c)


pts = [(mp.mpf("0.41"), mp.mpf("0.9")), (mp.mpf("-0.63"), mp.mpf("2.2")),
       (mp.mpf("0.05"), mp.mpf("4.7"))]
ok4 = True
for (c0, p0) in pts:
    hx = mp.mpf("1e-6")

    def dens(x1, x2, c=c0, p=p0):
        def fp(cc_, pp_):
            return BN(cc_, pp_) + x1 * Y1N(cc_, pp_) + x2 * Y2N(cc_, pp_)
        return gdN(fp, fp, c, p) / fp(c, p)

    fd = (dens(hx, hx) - dens(hx, -hx) - dens(-hx, hx)
          + dens(-hx, -hx)) / (4 * hx**2)
    Bv = BN(c0, p0)
    dY1c = (Y1N(c0 + mp.mpf("1e-8"), p0)
            - Y1N(c0 - mp.mpf("1e-8"), p0)) / mp.mpf("2e-8")
    dY2c = (Y2N(c0 + mp.mpf("1e-8"), p0)
            - Y2N(c0 - mp.mpf("1e-8"), p0)) / mp.mpf("2e-8")
    quoted = (2 * gdN(Y1N, Y2N, c0, p0) / Bv
              - 2 * FN * kapN * (1 - c0**2)
              * (dY1c * Y2N(c0, p0) + dY2c * Y1N(c0, p0)) / Bv**2
              + 2 * (1 - c0**2) * FN**2 * kapN**2
              * Y1N(c0, p0) * Y2N(c0, p0) / Bv**3)
    ok4 = ok4 and abs(fd - quoted) < mp.mpf("1e-4") * (1 + abs(quoted))
check("claim-4 identity holds NUMERICALLY at 3 random points with "
      "non-harmonic test functions (mixed central differences, mpmath)",
      ok4)

# ===========================================================================
hr("V5 — BANKED COUPLINGS by Gauss-Legendre quadrature + central "
   "difference in kappa (no series, no symbolic integrate)")
# ===========================================================================
cN, pN = sp.symbols("cN pN", real=True)
kapS, FS = sp.symbols("kapS FS", positive=True)
BS = FS * (1 + kapS * cN)
Ya1 = sp.sqrt(sp.S(3) / (4 * sp.pi)) * sp.sqrt(1 - cN**2) * sp.cos(pN)
Yg1 = sp.sqrt(sp.S(15) / (4 * sp.pi)) * cN * sp.sqrt(1 - cN**2) * sp.cos(pN)
Ya0 = sp.sqrt(sp.S(3) / (4 * sp.pi)) * cN
Yg0 = sp.sqrt(sp.S(5) / (16 * sp.pi)) * (3 * cN**2 - 1)


def gdS(g1, g2):
    return ((1 - cN**2) * sp.diff(g1, cN) * sp.diff(g2, cN)
            + sp.diff(g1, pN) * sp.diff(g2, pN) / (1 - cN**2))


def H_full_num(Yi, Yj, kap_val, F_val=2.0, ngl=80):
    integ = (2 * gdS(Yi, Yj) / BS
             - 2 * FS * kapS * (1 - cN**2)
             * (sp.diff(Yi, cN) * Yj + sp.diff(Yj, cN) * Yi) / BS**2
             + 2 * (1 - cN**2) * FS**2 * kapS**2 * Yi * Yj / BS**3)
    fn = sp.lambdify((cN, pN, kapS, FS), integ, "numpy")
    xc, wc = np.polynomial.legendre.leggauss(ngl)
    xp = (np.arange(ngl) + 0.5) * 2 * np.pi / ngl   # trapezoid in phi
    wp = np.full(ngl, 2 * np.pi / ngl)
    CC, PP = np.meshgrid(xc, xp, indexing="ij")
    vals = fn(CC, PP, kap_val, F_val)
    return 0.25 * float(np.einsum("i,j,ij->", wc, wp, vals))


for (Yi, Yj, coef, name) in [(Ya1, Yg1, -np.sqrt(5) / 2, "V_a1g1"),
                             (Ya0, Yg0, -np.sqrt(15) / 3, "V_a0g0")]:
    dk = 1e-3
    slope = (H_full_num(Yi, Yj, dk) - H_full_num(Yi, Yj, -dk)) / (2 * dk)
    expect = coef / 2.0      # F = 2: coupling = coef*kappa/F
    check(f"quadrature re-derivation: {name}/kappa = {expect:+.6f} "
          f"(got {slope:+.6f}) at F = 2 — banked value reproduced "
          "independently",
          abs(slope - expect) < 5e-5)

# ===========================================================================
hr("V6 — NON-VACUITY GUARD on the route's S5 momenta checks")
# ===========================================================================
L_src_proper = sp.Rational(1, 2) * s_s * Wr * f**2 * sqrtmg / r**2
L_total = L_C1 + L_flux + L_src_proper
dv_ = sp.Function("deltav", real=True)(r, th)
dq_ = sp.Function("deltaq", real=True)(r, th)
e1 = sp.Symbol("e1")
var_w = sp.diff(L_total.subs(v, v + e1 * dv_), e1).subs(e1, 0).doit()
var_q = sp.diff(L_total.subs(q, q + e1 * dq_), e1).subs(e1, 0).doit()
check("first variation in w is NONZERO (the check is not vacuous) yet "
      "contains NO derivative of the fluctuation — pi_w = 0 confirmed by "
      "an independent construction",
      sp.simplify(var_w) != 0 and dv_.func not in diff_funcs(var_w))
check("first variation in q is NONZERO yet contains NO derivative of the "
      "fluctuation — pi_q = 0 confirmed independently",
      sp.simplify(var_q) != 0 and dq_.func not in diff_funcs(var_q))

# ===========================================================================
hr("V7 — STATICS-PREMISE PROBE: time-dependent fields f, q, v (t, r, th)")
# ===========================================================================
fT = sp.Function("f", positive=True)(t, r, th)
qT = sp.Function("q", real=True)(t, r, th)
vT = sp.Function("v", positive=True)(t, r, th)
gT = sp.zeros(4, 4)
for (a, b, val) in [(0, 0, -fT), (1, 1, 1 / fT), (1, 2, qT),
                    (2, 2, r**2 * vT**2), (3, 3, r**2 * sth**2 / vT**2)]:
    gT[a, b] = val
    gT[b, a] = val
gTinv = gT.inv()
sqrtmgT = sp.sqrt(sp.factor(-gT.det()))
F0upT = gTinv * F0 * gTinv
L_flux_T = -(1 / (4 * mu)) * sqrtmgT * sum(
    F0[i, j] * F0upT[i, j] for i in range(4) for j in range(4))
L_src_T = sp.Rational(1, 2) * s_s * Wr * fT**2 * sqrtmgT / r**2
phiT = -sp.log(fT) / 2
KkinT = sum(gTinv[i, j] * sp.diff(phiT, coords[i]) * sp.diff(phiT, coords[j])
            for i in range(4) for j in range(4))
L_C1_T = -(cc / 2) * fT * KkinT * sqrtmgT
check("NONSTATIONARY fields: flux density still zeroth-jet (no d_t of any "
      "metric function) — the 'structural extension to the time row' note "
      "verified for the flux", diff_funcs(L_flux_T) == set())
check("NONSTATIONARY fields: source density still zeroth-jet",
      diff_funcs(L_src_T) == set())
check("NONSTATIONARY fields: C1 differentiates f only (now including f_t) "
      "— still no dw, dq",
      diff_funcs(L_C1_T) == {fT.func})

# ===========================================================================
hr("SUMMARY")
# ===========================================================================
print(f"  verifier checks run: {NCHECK}")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print("""  All verifier checks PASSED.  See the verifier report for the
  adjudicated verdicts (notably: claim 1/3 AMENDED — at q != 0 the
  on-shell flux sector has a metric-dependent field response (V3b),
  absent identically at q = 0; the zeroth-jet density statement is
  confirmed but does not by itself settle the ON-SHELL sector's
  w-content on the q-on class; order counting (V3c) shows the response
  correction enters at O(q^3), one order past the tadpole).""")
