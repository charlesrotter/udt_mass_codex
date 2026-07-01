"""W1 ROUTE C — SECOND-SECTOR AUDIT: w-derivative content of every banked
non-C1 native sector, on w-on / shear-on backgrounds.

Declaration binding: w_stiffness_push_declaration.md (Route C — "the banked
non-C1 native sectors (two-form flux, H1 collar source, responsive-source
structure) evaluated on w-on / shear-on backgrounds: do any carry
w-derivatives natively?  Known: no native sector carries rho' — the
analogous question for w has never been posed").  Metric-led in method;
no EH import (native_positional_dilation_gr_guardrail.py binds); no
linearization anywhere (every check exact sympy; the single O(kappa)
computation in S4 reproduces a banked O(kappa) statement, it is not a
result-grade truncation of this audit).

THE CLASS (P1, exact; R-areal canon rho = r holds — the angular block is
freed, NOT rho).  Nondegeneracy parameterization used throughout:

    v(r, theta) := 1 + w(r, theta) > 0      (dL/dw = dL/dv identically),

    ds^2 = -f dT^2 + f^{-1} dr^2 + 2 q dr dtheta
           + r^2 v^2 dtheta^2 + r^2 sin^2(theta) v^{-2} dvphi^2,

f, q, v functions of (r, theta); det(angular block) = r^4 sin^2(theta)
exactly for all v (areal canon).  Shear/breathing enlargement in S6:
angular block r^2 A(r,theta) dtheta^2 + r^2 sin^2(theta) B(r,theta)
dvphi^2 with A, B INDEPENDENT (covers w = unimodular shape, s = shear,
k = breathing simultaneously; k is audited structurally only — the
R-areal canon forbids freeing it as dynamics).

THE SECTOR INVENTORY AUDITED (definitions quoted with provenance):

  S1  C1 anchor (NOT a Route-C target — settled by the 2026-06-11
      theorems, pde_p1_results.md / nonstationary_opener_results.md;
      re-verified here only as the baseline the other sectors are
      compared against):
          S_C1 = -(c/2) Int e^{-2phi} g^{mu nu} d_mu phi d_nu phi
                 sqrt(-g) d^4x,   f = e^{-2phi}.
  S2  Native two-form flux (CONDITIONAL on Pflux -> Pbundle0;
      native_areal_function_field_equations.py section B):
          F = Q_f sin(theta) dtheta ^ dvphi  (closed),
          S_flux = -(1/(4 mu)) Int sqrt(-g) F_{mu nu} F^{mu nu} d^4x.
  S3  H1 collar source (CONDITIONAL on the collar-source interpretation;
      native_core_solver.py via native_areal_function_field_equations.py
      section C, where the rho-local weight w(rho) = 1 is FORCED by the
      banked rho = r limit):
          S_source = Int (s/2) W(r) f^2 dr        (rho-independent),
      banked sourced equation  f'' + 2 f'/r + 2 s W f / r^2 = 0.
  S4  Responsive-source structure (sourced_second_jet_results.md finding
      6 + n_derivation_results.md): source = the metric's own ell = 1
      angular amplitude, f = F(y)(1 + kappa(y) cos theta); reduced
      potential P = (3 a^2 / 8 F) G1(kappa) [corrected prefactor,
      n_derivation_results.md "Corrections" section], Hessian blocks
          H_ij = (1/4) Int dOmega [ 2 grad(Yi).grad(Yj)/B
                 - 2 F kap (1-c^2)(Yi_c Yj + Yj_c Yi)/B^2
                 + 2 (1-c^2) F^2 kap^2 Yi Yj / B^3 ],  B = F(1+kap c),
      with V_a1g1 = -sqrt(5) kappa/(2F), V_a0g0 = -sqrt(15) kappa/(3F);
      plus the licensed source-completion family S_src = Int c_n(y) f^n dy
      (sourced_second_jet_results.md finding 1; coordinate-vs-proper
      measure fork per n_derivation_results.md).
  S5  S_phi0 boundary functional = the DtN quadratic form (banked positive
      1 of sphi0_derivation_panel_results.md: "the second variation of the
      C1 action on the self-similar collar, restricted to boundary data")
      — a DERIVED functional of C1; audited via the conjugate-momentum and
      second-variation structure.

EXCLUDED from audit (inventoried, with reasons — see results report):
  EH density / EH remainder (NOT banked; guardrail-forbidden import);
  weld mass term 2sE0 (refuted-as-native, measure_fork_results.md; f-sector
  object regardless); GHY/Brown-York/Robin phi0 candidates (candidate
  scorecard only, never banked — the banked object IS the DtN form, S5);
  spectrum-stage operator algebra End(H1) = 1+3+5 / two-form selector /
  W(P) = Tr(P)/12 (operator bookkeeping on H1, not action sectors);
  probe kinetic densities (diagnostics, not action pieces — their metric
  dependence is algebraic too, spot-noted in S3); breathing mode k
  (R-areal canon forbids freeing it; covered structurally by S6 anyway).

VERDICT PROVED BELOW (every check exact):
  NO banked non-C1 native sector carries derivatives of w (or of shear/
  breathing, or of q) — radial or angular, any order.  Each sector's
  density is ZEROTH-JET in the entire angular block.  The single new
  w-structure found is ALGEBRAIC: the flux sector's w-tadpole
      dL_flux/dw = +(Q_f^2/(2 mu)) sin(theta) f q^2 / (r D^{3/2})  (exact),
  nonzero only at q != 0, opposing the banked q*-branch C1 w-force in
  sign, vanishing on spherical — an algebraic counter-force, NOT a
  stiffness (it cannot give w gradient energy or dynamics at any order).

New file 2026-06-11 (W1 Route C); creates nothing else, modifies nothing
existing; not banked, not committed — report-back only per the push
declaration.
"""

from __future__ import annotations

import sys

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


def derivative_targets(expr: sp.Expr) -> set:
    """The set of FUNCTIONS that appear differentiated anywhere in expr."""
    expr = sp.sympify(expr).doit()
    return {d.expr.func for d in expr.atoms(sp.Derivative)}


def contains_func(expr: sp.Expr, fn) -> bool:
    return fn.func in {a.func for a in sp.sympify(expr).atoms(sp.Function)}


# ---------------------------------------------------------------------------
# S0 — the P1 class with LIVE FIELDS (sympy Functions, so that derivative
#      content is a checkable property, not a notational convention)
# ---------------------------------------------------------------------------
hr("S0 — P1 METRIC CLASS, live fields f(r,th), q(r,th), v(r,th) = 1+w  "
   "(R-areal canon: rho = r NOT freed)")

t = sp.Symbol("T", real=True)
r = sp.Symbol("r", positive=True)
th = sp.Symbol("theta", real=True)
ph = sp.Symbol("varphi", real=True)
coords = [t, r, th, ph]
cc = sp.symbols("c", positive=True)          # C1 normalization constant
mu = sp.symbols("mu", positive=True)         # Maxwell normalization
Qf = sp.symbols("Q_f", real=True)            # flux charge (NOT g_rtheta!)
s_s = sp.symbols("s", real=True)             # collar source strength
Wr = sp.Function("W")(r)                     # collar window (banked profile)
sth = sp.sin(th)                             # carried symbolically

f = sp.Function("f", positive=True)(r, th)
q = sp.Function("q", real=True)(r, th)
v = sp.Function("v", positive=True)(r, th)   # v = 1 + w > 0 (nondegeneracy)

Wfac = v**2
g = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, q, 0],
    [0, q, r**2 * Wfac, 0],
    [0, 0, 0, r**2 * sth**2 / Wfac]])
D2 = r**2 * Wfac - f * q**2

detg = sp.factor(g.det())
check("det g = -(r^2 sin^2/v^2)(r^2 v^2 - f q^2) exactly",
      sp.simplify(detg + (r**2 * sth**2 / Wfac) * D2) == 0)
check("angular-block det = r^4 sin^2(theta) for ALL v — areal canon exact",
      sp.simplify(g[2, 2] * g[3, 3] - r**4 * sth**2) == 0)
sqrtmg = r * sth * sp.sqrt(D2) / v
check("sqrt(-g) = r sin(th) sqrt(D)/v, D = r^2 v^2 - f q^2 exactly",
      sp.simplify(sqrtmg**2 + detg) == 0)
ginv = g.inv()
check("exact inverse: g g^{-1} = 1 (4x4)",
      sp.simplify(g * ginv - sp.eye(4)) == sp.zeros(4, 4))
sqrtmg_q0 = sp.simplify(sqrtmg.subs(q, 0))
check("LOAD-BEARING MEASURE FACT: at q = 0, sqrt(-g) = r^2 sin(theta) "
      "EXACTLY — the unimodular (areal-canon) measure is w-FREE",
      sp.simplify(sqrtmg_q0 - r**2 * sth) == 0)

# ---------------------------------------------------------------------------
# S1 — C1 baseline anchor (settled by theorem; re-verified as comparator)
# ---------------------------------------------------------------------------
hr("S1 — C1 BASELINE (theorem anchor, pde_p1_results.md — NOT a Route-C "
   "target)")

phi = -sp.Rational(1, 2) * sp.log(f)
Kkin = (ginv[1, 1] * sp.diff(phi, r)**2
        + 2 * ginv[1, 2] * sp.diff(phi, r) * sp.diff(phi, th)
        + ginv[2, 2] * sp.diff(phi, th)**2)
L_C1 = sp.simplify(-(cc / 2) * f * Kkin * sqrtmg)
fr, fth = sp.diff(f, r), sp.diff(f, th)
A_ = f * r**2 * Wfac * fr**2 + fth**2
L_C1_closed = (-(cc / 8) * r * sth
               * (A_ - 2 * f * q * fr * fth) / (v * f * sp.sqrt(D2)))
check("L_C1 = -(c/8) r sin(th)[f r^2 v^2 f_r^2 - 2 f q f_r f_th + f_th^2]"
      "/(v f sqrt(D)) exactly (the P1 closed form, v = 1+w)",
      sp.simplify(L_C1 - L_C1_closed) == 0)
check("C1 STRUCTURAL FACT (theorem #21/#22 baseline): the ONLY "
      "differentiated function in L_C1 is f — q and w enter with NO "
      "derivatives at any nonlinear order",
      derivative_targets(L_C1) == {f.func})
# the banked w-force on the q* branch (pde_p1 anchor), Delta > 0 branch:
ww, ffv, frv, fthv = sp.symbols("w_v f_v f_rv f_thv", real=True)
Leff_branch = (-(cc / 8) * sth
               * (ffv * r**2 * frv**2 - fthv**2 / (1 + ww)**2) / ffv)
wforce_C1 = sp.simplify(sp.diff(Leff_branch, ww))
check("banked C1 w-force: dL_eff/dw = -(c/4) sin(th) f_th^2/(f (1+w)^3) "
      "exactly (pde_p1_results.md, q*-eliminated branch) — ALGEBRAIC "
      "and NEGATIVE",
      sp.simplify(wforce_C1
                  + (cc / 4) * sth * fthv**2
                  / (ffv * (1 + ww)**3)) == 0)
spot = wforce_C1.subs([(ffv, 2), (fthv, 3), (ww, 1), (cc, 1)])
check("rational spot-check: f = 2, f_th = 3, w = 1, c = 1 gives "
      "dL/dw = -(9/64) sin(th)",
      sp.simplify(spot + sp.Rational(9, 64) * sth) == 0)

# ---------------------------------------------------------------------------
# S2 — NATIVE TWO-FORM FLUX on the w-on class
# ---------------------------------------------------------------------------
hr("S2 — NATIVE TWO-FORM FLUX SECTOR on w-on / q-on backgrounds "
   "(CONDITIONAL: Pflux -> Pbundle0)")

F_low = sp.zeros(4, 4)
F_low[2, 3] = Qf * sth
F_low[3, 2] = -Qf * sth

closed_ok = True
for i in range(4):
    for j in range(i + 1, 4):
        for k in range(j + 1, 4):
            cyc = (sp.diff(F_low[j, k], coords[i])
                   + sp.diff(F_low[k, i], coords[j])
                   + sp.diff(F_low[i, j], coords[k]))
            closed_ok = closed_ok and sp.simplify(cyc) == 0
check("dF = 0 — closedness is metric-independent, survives w, q on",
      closed_ok)

F_up = ginv * F_low * ginv
F2 = sp.simplify(sum(F_low[i, j] * F_up[i, j]
                     for i in range(4) for j in range(4)))
check("F_{mu nu}F^{mu nu} = 2 Q_f^2 v^2 / (r^2 D) exactly on the w-on "
      "class (reduces to 2 Q_f^2/r^4 at v = 1, q = 0, the banked "
      "spherical value)",
      sp.simplify(F2 - 2 * Qf**2 * Wfac / (r**2 * D2)) == 0
      and sp.simplify(F2.subs([(v, 1), (q, 0)]) - 2 * Qf**2 / r**4) == 0)

L_flux = sp.simplify(-(sp.Rational(1, 4) / mu) * sqrtmg * F2)
L_flux_closed = -(Qf**2 / (2 * mu)) * sth * v / (r * sp.sqrt(D2))
check("L_flux = -(Q_f^2/(2 mu)) sin(th) v/(r sqrt(D)) exactly",
      sp.simplify(L_flux - L_flux_closed) == 0)

check("VERDICT INPUT: L_flux contains NO derivative of ANY field — not "
      "of w, not of q, not of f (zeroth-jet in the whole metric); the "
      "flux sector cannot carry w-stiffness at any order",
      derivative_targets(L_flux) == set())

L_flux_q0 = sp.simplify(L_flux.subs(q, 0))
check("DIAGONAL CLASS (q = 0): L_flux = -(Q_f^2/(2 mu)) sin(th)/r^2 — "
      "EXACTLY w-BLIND (v drops out entirely; the unimodular measure "
      "fact of S0 + areal flux surfaces)",
      sp.simplify(L_flux_q0 + Qf**2 * sth / (2 * mu * r**2)) == 0
      and not contains_func(L_flux_q0, v))

# the ONLY new w-structure in the whole audit: the algebraic flux w-tadpole
wtad = sp.simplify(sp.diff(L_flux, v))   # dL/dw = dL/dv (v = 1+w)
wtad_closed = (Qf**2 / (2 * mu)) * sth * f * q**2 \
    / (r * D2**sp.Rational(3, 2))
check("FLUX w-TADPOLE (exact): dL_flux/dw = +(Q_f^2/(2 mu)) sin(th) "
      "f q^2 / (r D^{3/2}) — ALGEBRAIC, POSITIVE (opposes the banked "
      "q*-branch C1 w-force in sign), prop. q^2 (vanishes identically "
      "on the diagonal class)",
      sp.simplify(wtad - wtad_closed) == 0)
check("spherical limit: the tadpole vanishes at q = 0 (and q* itself "
      "vanishes when f_th = 0) — Route-D filter (i) satisfied by the "
      "algebraic structure",
      sp.simplify(wtad.subs(q, 0)) == 0)
spot2 = wtad.subs([(Qf, 1), (mu, 1), (v, 1), (f, 3),
                   (q, sp.Rational(1, 2)), (r, 1)])
check("rational spot-check: Q_f = mu = r = 1, v = 1, f = 3, q = 1/2 "
      "(D = 1/4, D^{3/2} = 1/8): dL_flux/dw = 3 sin(th) exactly",
      sp.simplify(spot2 - 3 * sth) == 0)
spot3 = L_flux.subs([(Qf, 1), (mu, 1), (v, 1), (f, 3),
                     (q, sp.Rational(1, 2)), (r, 1)])
check("rational spot-check: same point, L_flux = -sin(th) exactly",
      sp.simplify(spot3 + sth) == 0)

# Maxwell-on-shell status of the monopole representative on w-on classes
div_ok_q0 = True
sqg_F_q0 = (sqrtmg * F_up).subs(q, 0)
for nu_i in range(4):
    div = sum(sp.diff(sp.simplify(sqg_F_q0[mu_i, nu_i]), coords[mu_i])
              for mu_i in range(4))
    div_ok_q0 = div_ok_q0 and sp.simplify(div) == 0
check("monopole stays Maxwell-on-shell on the FULL diagonal w-on class "
      "(q = 0, arbitrary f(r,th), w(r,th)): d_mu(sqrt(-g) F^{mu nu}) = 0 "
      "all nu",
      div_ok_q0)
div_phi = sp.simplify(sum(sp.diff(sp.simplify(sqrtmg * F_up[mu_i, 3]),
                                  coords[mu_i]) for mu_i in range(4)))
check("at q != 0 the monopole representative is generally OFF "
      "Maxwell-shell (the nu = varphi divergence is not identically "
      "zero) — scoped observation: the flux rep needs re-solving on "
      "q-on backgrounds; the action's derivative content is unaffected",
      sp.simplify(div_phi) != 0
      and sp.simplify(div_phi.subs(q, 0).doit()) == 0)

# stronger statement: ANY Maxwell field, not just the monopole rep
At = sp.Function("A_t", real=True)(r, th)
Aph = sp.Function("A_phi", real=True)(r, th)
F_gen = sp.zeros(4, 4)
for (a_i, b_i, val) in [(1, 0, sp.diff(At, r)), (2, 0, sp.diff(At, th)),
                        (1, 3, sp.diff(Aph, r)), (2, 3, sp.diff(Aph, th))]:
    F_gen[a_i, b_i] = val
    F_gen[b_i, a_i] = -val
F_gen_up = ginv * F_gen * ginv
L_max_gen = sp.simplify(-(sp.Rational(1, 4) / mu) * sqrtmg
                        * sum(F_gen[i, j] * F_gen_up[i, j]
                              for i in range(4) for j in range(4)))
check("GENERAL MAXWELL SECTOR (any even-sector A_mu(r,th)): the density "
      "differentiates ONLY the potentials A_t, A_phi — never w, q, or f; "
      "the Maxwell sector is zeroth-jet in the metric BY STRUCTURE "
      "(no Christoffels enter F_{mu nu}F^{mu nu} sqrt(-g))",
      derivative_targets(L_max_gen) <= {At.func, Aph.func})

# ---------------------------------------------------------------------------
# S3 — H1 COLLAR SOURCE on the w-on class
# ---------------------------------------------------------------------------
hr("S3 — H1 COLLAR SOURCE on w-on backgrounds (CONDITIONAL: collar-source "
   "interpretation; weight w(rho) = 1 forced by the banked rho = r limit)")

L_src_banked = sp.Rational(1, 2) * s_s * Wr * f**2
check("reading (i), the literal banked piece S_source = Int (s/2) W(r) "
      "f^2 dr: contains NO angular-block field at all — w and q ABSENT "
      "(w-BLIND, stronger than algebraic), and no derivatives of anything",
      not contains_func(L_src_banked, v)
      and not contains_func(L_src_banked, q)
      and derivative_targets(L_src_banked) == set())

L_src_coord = L_src_banked * sth
L_src_proper = sp.simplify(L_src_banked * sqrtmg / r**2)
check("reading (ii), coordinate-measure angular lift (s/2) W f^2 sin(th): "
      "still w-BLIND, no derivatives",
      not contains_func(L_src_coord, v)
      and derivative_targets(L_src_coord) == set())
check("reading (iii), proper-measure lift (s/2) W f^2 sqrt(-g)/r^2: at "
      "q = 0 it EQUALS reading (ii) exactly (unimodular measure, S0) — "
      "w-blind on the diagonal class; at q != 0 w enters ALGEBRAICALLY "
      "through sqrt(D)/v; no derivatives in any reading",
      sp.simplify(L_src_proper.subs(q, 0) - L_src_coord) == 0
      and derivative_targets(L_src_proper) == set())

# the H1 carrier's angular gradient energy on the DEFORMED sphere
chi = sp.Function("chi", real=True)(th, ph)
E_carrier = sp.simplify(
    (sp.simplify(ginv[2, 2].subs(q, 0)) * sp.diff(chi, th)**2
     + ginv[3, 3] * sp.diff(chi, ph)**2) * sqrtmg_q0)
E_target = (sp.diff(chi, th)**2 / v**2
            + v**2 * sp.diff(chi, ph)**2 / sth**2) * sth
check("H1 carrier angular Dirichlet energy on the deformed sphere "
      "(q = 0): integrand = [chi_th^2/v^2 + v^2 chi_ph^2/sin^2] sin(th) "
      "— differentiates ONLY chi; w enters ALGEBRAICALLY, so ANY "
      "deformed-sphere eigenvalue functional lambda[w] has an algebraic "
      "(Hellmann-Feynman) w-variation and supplies NO w-gradient energy",
      derivative_targets(E_carrier) == {chi.func}
      and sp.simplify(E_carrier - E_target) == 0)

# ---------------------------------------------------------------------------
# S4 — RESPONSIVE-SOURCE STRUCTURE and the source-completion family
# ---------------------------------------------------------------------------
hr("S4 — RESPONSIVE SOURCE + COMPLETION FAMILY: derived functionals of "
   "C1; their w-content reduces to C1's (settled by theorem)")

y = sp.symbols("y", positive=True)
n_s = sp.symbols("n", real=True)
cn = sp.Function("c_n")(y)
L_compl_coord = cn * f**n_s
check("licensed completion family S_src = Int c_n(y) f^n dy (coordinate "
      "measure, the operationally banked choice): contains NO metric "
      "beyond f, hence no w, no q, no derivatives — w-BLIND",
      derivative_targets(L_compl_coord) == set()
      and not contains_func(L_compl_coord, v))
L_compl_proper = (cn * f**n_s) * sqrtmg
check("proper-measure variant c_n f^n sqrt(-g): at q = 0 it is EXACTLY "
      "c_n f^n r^2 sin(th) — w-free (unimodular measure); at q != 0 "
      "algebraic in w; NO derivatives of anything in either branch of "
      "the measure fork",
      sp.simplify(L_compl_proper.subs(q, 0)
                  - cn * f**n_s * r**2 * sth) == 0
      and derivative_targets(L_compl_proper) == set())

# --- the responsive Hessian IS the C1 angular second variation -------------
cv, phv = sp.symbols("c_u phi_a", real=True)   # c_u = cos(theta) on S^2
kap = sp.Symbol("kappa", positive=True)
Fb = sp.Symbol("F", positive=True)
x1, x2 = sp.symbols("x1 x2", real=True)
Y1 = sp.Function("Y1", real=True)(cv, phv)
Y2 = sp.Function("Y2", real=True)(cv, phv)
Bb = Fb * (1 + kap * cv)


def gd(gg, hh):
    return ((1 - cv**2) * sp.diff(gg, cv) * sp.diff(hh, cv)
            + sp.diff(gg, phv) * sp.diff(hh, phv) / (1 - cv**2))


f_pert = Bb + x1 * Y1 + x2 * Y2
gen_integrand = gd(f_pert, f_pert) / f_pert          # the C1 angular density
hess_12 = sp.simplify(sp.diff(gen_integrand, x1, x2).subs([(x1, 0),
                                                           (x2, 0)]))
quoted_12 = (2 * gd(Y1, Y2) / Bb
             - 2 * Fb * kap * (1 - cv**2)
             * (sp.diff(Y1, cv) * Y2 + sp.diff(Y2, cv) * Y1) / Bb**2
             + 2 * (1 - cv**2) * Fb**2 * kap**2 * Y1 * Y2 / Bb**3)
check("IDENTITY (exact, generic Y1, Y2): d^2/dx1 dx2 [|grad f|^2/f] at "
      "x = 0 with f = B + x.Y, B = F(1+kappa c) EQUALS the quoted "
      "responsive-Hessian integrand — the responsive-source Hessian IS "
      "the C1 angular second variation; it is NOT an independent sector",
      sp.simplify(hess_12 - quoted_12) == 0)

# spot-reproduce the two banked O(kappa) couplings (the banked statement is
# itself O(kappa) — sourced_second_jet_results.md finding 6; reproducing a
# banked leading-order statement is not a linearized result of this audit)
Ya1 = sp.sqrt(sp.S(3) / (4 * sp.pi)) * sp.sqrt(1 - cv**2) * sp.cos(phv)
Yg1 = sp.sqrt(sp.S(15) / (4 * sp.pi)) * cv * sp.sqrt(1 - cv**2) * sp.cos(phv)
Ya0 = sp.sqrt(sp.S(3) / (4 * sp.pi)) * cv
Yg0 = sp.sqrt(sp.S(5) / (16 * sp.pi)) * (3 * cv**2 - 1)


def H_okap(Yi, Yj):
    integ = (2 * gd(Yi, Yj) / Bb
             - 2 * Fb * kap * (1 - cv**2)
             * (sp.diff(Yi, cv) * Yj + sp.diff(Yj, cv) * Yi) / Bb**2
             + 2 * (1 - cv**2) * Fb**2 * kap**2 * Yi * Yj / Bb**3)
    integ = sp.series(sp.expand(integ), kap, 0, 2).removeO()
    integ = sp.expand_trig(sp.expand(integ))
    val = sp.integrate(sp.integrate(integ, (phv, 0, 2 * sp.pi)),
                       (cv, -1, 1))
    return sp.Rational(1, 4) * sp.simplify(val)


check("banked coupling reproduced: V_a1g1 = -sqrt(5) kappa/(2F) at "
      "O(kappa) exactly",
      sp.simplify(H_okap(Ya1, Yg1) + sp.sqrt(5) * kap / (2 * Fb)) == 0)
check("banked coupling reproduced: V_a0g0 = -sqrt(15) kappa/(3F) at "
      "O(kappa) exactly",
      sp.simplify(H_okap(Ya0, Yg0) + sp.sqrt(15) * kap / (3 * Fb)) == 0)
print("""
     CONSEQUENCE: the responsive 'shape' directions (gamma0, gamma1,
     gamma2) are ell = 2 harmonics OF THE FIELD f, not deformations of
     the metric angular block — the responsive sector never touches w as
     an independent field, and as a functional OF C1 it inherits the
     theorem (#21/#22): no w-derivatives at any order.""")

# ---------------------------------------------------------------------------
# S5 — S_phi0 / DtN boundary functional: conjugate momenta and second jet
# ---------------------------------------------------------------------------
hr("S5 — S_phi0 BOUNDARY FUNCTIONAL (= the DtN quadratic form, derived "
   "from C1): w carries NO boundary momentum and NO fluctuation gradient")

L_total = (L_C1 + L_flux + L_src_proper)
pi_w = sp.simplify(sp.diff(L_total, sp.Derivative(v, r)))
pi_q = sp.simplify(sp.diff(L_total, sp.Derivative(q, r)))
pi_w_th = sp.simplify(sp.diff(L_total, sp.Derivative(v, th)))
check("TOTAL banked stack (C1 + flux + source): the conjugate momenta "
      "pi_w = dL/d(w_r), pi_q = dL/d(q_r), and dL/d(w_th) ALL vanish "
      "IDENTICALLY — the exact w-analog of 'no native sector carries "
      "rho'' (branch_iii_hunt_results.md); no boundary functional built "
      "from this stack can carry w boundary data",
      pi_w == 0 and pi_q == 0 and pi_w_th == 0)

eps = sp.symbols("epsilon", real=True)
om = sp.Function("omega", real=True)(r, th)
L_pert = L_total.subs(v, v + eps * om)
d2L = sp.diff(L_pert, eps, 2).subs(eps, 0)
check("second variation in the w-direction: d^2L/deps^2 contains NO "
      "derivative of the fluctuation omega(r,th) — the C1 second jet "
      "(whose boundary restriction IS S_phi0, sphi0 panel positive 1) "
      "gives w-fluctuations ZERO gradient stiffness and ZERO DtN content",
      om.func not in derivative_targets(d2L))

# ---------------------------------------------------------------------------
# S6 — GENERAL ANGULAR BLOCK: shear-on, the structural theorem
# ---------------------------------------------------------------------------
hr("S6 — GENERAL ANGULAR BLOCK g_thth = r^2 A, g_phph = r^2 sin^2 B "
   "(A, B independent: covers w, shear s, breathing k simultaneously)")

Af = sp.Function("A", positive=True)(r, th)
Bf = sp.Function("B", positive=True)(r, th)
gG = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, q, 0],
    [0, q, r**2 * Af, 0],
    [0, 0, 0, r**2 * sth**2 * Bf]])
gGinv = gG.inv()
DG = r**2 * Af - f * q**2
sqrtmgG = r * sth * sp.sqrt(DG * Bf)
check("general block: sqrt(-g) = r sin(th) sqrt((r^2 A - f q^2) B) "
      "exactly",
      sp.simplify(sqrtmgG**2 + gG.det()) == 0)

KkinG = (gGinv[1, 1] * sp.diff(phi, r)**2
         + 2 * gGinv[1, 2] * sp.diff(phi, r) * sp.diff(phi, th)
         + gGinv[2, 2] * sp.diff(phi, th)**2)
L_C1_G = sp.simplify(-(cc / 2) * f * KkinG * sqrtmgG)
F_upG = gGinv * F_low * gGinv
L_flux_G = sp.simplify(-(sp.Rational(1, 4) / mu) * sqrtmgG
                       * sum(F_low[i, j] * F_upG[i, j]
                             for i in range(4) for j in range(4)))
L_src_G = sp.Rational(1, 2) * s_s * Wr * f**2 * sqrtmgG / r**2

check("C1 on the general block: differentiates f ONLY (no dA, dB, dq at "
      "any order) — the P1 structural lemma is a property of C1, not of "
      "the unimodular reduction",
      derivative_targets(L_C1_G) == {f.func})
check("flux on the general block: NO derivatives at all — sees the "
      "angular block only algebraically",
      derivative_targets(L_flux_G) == set())
check("flux anatomy on the diagonal general block (q = 0): "
      "L_flux = -(Q_f^2/(2 mu)) sin(th)/(r^2 sqrt(A B)) exactly — the "
      "flux sees the angular block ONLY through the AREAL combination "
      "A B (Stokes: the trapped flux is fixed; the energy scales with "
      "the flux-surface area), algebraically",
      sp.simplify(L_flux_G.subs(q, 0)
                  + (Qf**2 / (2 * mu)) * sth
                  / (r**2 * sp.sqrt(Af * Bf))) == 0)
check("on the unimodular slice B = 1/A (the w/shear class, A B = 1): "
      "L_flux(q=0) = -(Q_f^2/(2 mu)) sin(th)/r^2 — EXACTLY shape-BLIND, "
      "reproducing S2's diagonal-class w-blindness (g^thth carries 1/A "
      "while g^phph carries A; the F^2 contraction uses both and only "
      "their areal product survives)",
      sp.simplify(L_flux_G.subs(q, 0).subs(Bf, 1 / Af)
                  + (Qf**2 / (2 * mu)) * sth / r**2) == 0
      and derivative_targets(L_flux_G.subs(Bf, 1 / Af)) == set())
check("source on the general block (proper reading): NO derivatives; "
      "coordinate reading contains no A, B at all",
      derivative_targets(L_src_G) == set()
      and not contains_func(L_src_coord, Af))

allD = (derivative_targets(L_C1_G) | derivative_targets(L_flux_G)
        | derivative_targets(L_src_G))
check("STRUCTURAL THEOREM (Route C verdict, shear-on class): the union "
      "of differentiated functions across the ENTIRE banked native stack "
      "on the general angular block is {f} — no banked sector carries "
      "dA, dB, dq, i.e. no w-, s-, or k-derivative ANYWHERE, any order",
      allD == {f.func})

# ---------------------------------------------------------------------------
# S7 — on-shell survival: can anything supply stiffness at C1-stationary
#      configurations?
# ---------------------------------------------------------------------------
hr("S7 — ON-SHELL STATEMENT + the one algebraic novelty")

print("""
  Since NO banked non-C1 sector carries w- or s-derivatives (S2-S6), no
  sector can supply gradient stiffness ON any configuration — stationary
  or not; 'on-shell rescue' is structurally impossible: a term with no
  dw anywhere has no dw after restriction either.  The ONLY new
  w-structure in the banked stack is the ALGEBRAIC flux w-tadpole of S2:

      dL_flux/dw = +(Q_f^2/(2 mu)) sin(th) f q^2 / (r D^{3/2})   (exact)

  - sign: POSITIVE (pushes w UP), opposing — on the q*-eliminated
    branch — C1's negative w-force -(c/4) sin(th) f_th^2/(f (1+w)^3)
    (the corner-driving force of the P1 theorem);
  - support: vanishes identically at q = 0 and on spherical backgrounds
    (q* prop. f_r f_th); lives ONLY on the flux-on, q-on class;
  - status: NOT a stiffness (no derivatives — w stays non-dynamical,
    pointwise-algebraic); it deforms the w-FATE ALGEBRA, not the w
    CHARACTER.  Scoped observation for the registry: the P1 corner
    theorem ('C1 drives the shape sector to metric degeneracy') carries
    premise C1-ONLY; on the flux-on q-on class the joint algebraic
    system gains this opposing term and the corner conclusion needs
    re-derivation there (conditional on Pflux).""")

expr = sp.simplify(sp.diff(L_C1 + L_flux, v))
check("the joint w-equation of (C1 + flux) is pointwise ALGEBRAIC in w "
      "(no derivative of v = 1+w appears in dL/dv)",
      v.func not in derivative_targets(expr))
expr_q0 = sp.simplify(expr.subs(q, 0))
check("at q = 0 the joint w-force reduces EXACTLY to C1's alone (flux "
      "adds nothing on the diagonal class): dL/dw|_{q=0} = "
      "+(c/4) sin(th) f_th^2/(f v^3)  [diagonal-POINT force; the banked "
      "NEGATIVE corner-driving force -(c/4)... of pde_p1 lives on the "
      "q*-ELIMINATED branch — sign flip = the angular flip, same object]",
      sp.simplify(expr_q0
                  - (cc / 4) * sth * sp.diff(f, th)**2
                  / (f * v**3)) == 0)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
hr("SUMMARY")
print(f"  checks run: {NCHECK}")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print("""  All checks PASSED.

  ROUTE C VERDICT (premise-scoped negative + one algebraic positive):

  NEGATIVE (theorem-grade on the audited class): no banked non-C1 native
  sector — two-form flux, H1 collar source (all three measure readings),
  responsive-source structure, source-completion family, S_phi0/DtN —
  carries derivatives of w or of the shear/breathing fields, radial or
  angular, any order.  Every sector is zeroth-jet in the angular block;
  pi_w = pi_q = 0 identically for the total stack (the exact w-analog of
  'no native sector carries rho'').  PREMISE SET: P1 static axisymmetric
  even-sector class (+ the S6 general angular block); R-areal canon
  rho = r; sector definitions as banked (flux = monopole rep,
  conditional Pflux; collar source with forced weight w(rho) = 1,
  conditional collar-source interpretation; responsive source = C1's
  own ell = 1 angular activity; completion family on either branch of
  the coordinate/proper measure fork); statics (the extension to the
  full time row is structural for flux/source — their densities carry
  no metric derivatives regardless of time dependence — but is recorded
  as a note, not a separately audited claim).

  POSITIVE (algebraic only, conditional on Pflux): the flux sector
  supplies the exact w-tadpole +(Q_f^2/(2 mu)) sin(th) f q^2/(r D^{3/2}),
  opposing the C1 w-runaway in sign, supported only at q != 0.  It is
  NOT the forced object (it carries no w-derivatives and cannot make w
  dynamical); it is registry-relevant as a CONDITIONS note on the P1
  corner theorem's C1-only premise.

  CONSEQUENCE FOR W1: the native w-stiffness sector, if it exists, is
  NOT hiding in the banked non-C1 inventory.  Routes A (class-enlargement
  of C1's own computation) and B (forced completion) carry the remaining
  weight.""")
