"""NATIVE WELD STATUS DERIVATION: is the rung-2 (t,theta) momentum-
constraint weld NATIVE to the C1 dynamics, or an Einstein import?

THE QUESTION.  The macro CMB work (AUDIT.md, S116 dispatch, 'Step 1')
derived and data-tested the rung-2 weld by perturbing the canonical UDT
metric ds^2 = -e^{-2phi0}dt^2 + e^{2phi0}dr^2 + r^2 dOmega^2 with the
even-parity RW-gauge set (H0, H1, H2, K)·Y(theta) and reading off the
LINEARIZED EINSTEIN component dG^t_theta:

    d_r(e^{-2phi0} H1) = 2 d_t(dphi) + d_t K - 16 pi G e^{-2phi0} dT^t_th.

But this repo also PROVED (native_rho_dynamics_gr_balance_test.py) that
UDT does NOT impose the theta-theta Einstein equation (Einstein tension
Delta = pi c a^2/r^4 > 0 on the banked vacuum) and that the C1 stress is
NOT conserved on the banked vacuum (leftover (c/8)f'^3/f).  So the weld's
status was unresolved: native consequence of the C1 dynamics, or an
Einstein import that happens to work empirically at macro scope?  This
file settles it, exactly, on a GENERAL static background f(r) =
e^{-2phi0(r)} (arbitrary profile - covers both the macro cell and the
matter cell).

SCOPE NOTE (CLAUDE.md, principle 2).  Principle 2 forbids approximations
and linearizations as stated results or inputs.  This file uses linear
PERTURBATION MODES around EXACT backgrounds - i.e. normal-mode analysis
of an exact configuration via its exact second-order action - which is
in scope: nothing about the BACKGROUND is linearized anywhere (the full
nonlinear phi0(r) profile is carried symbolically throughout), and the
second-order action is the exact epsilon^2 coefficient of the exact C1
action, not an approximation to it.  Mode analysis around exact
backgrounds is how the repo's own no-go theorems and the macro weld were
derived; what principle 2 forbids is linearizing exp(-2 phi0) itself.

RESULTS (every displayed identity sympy-verified — plus one numerical
eigensolve for the W3(e') counterexample; PASS/FAIL printed; nonzero
exit on any FAIL):

  W1  KINEMATIC TIES + THE K-VERDICT.  The UDT structure g_tt =
      -e^{-2phi}, g_rr = e^{+2phi} with phi = phi0 + dphi·Y gives, in the
      standard RW parametrization (dg_tt = -f H0 Y, dg_rr = (1/f) H2 Y):

          H0 = -2 dphi,   H2 = +2 dphi   (so H0 = -H2),

      and g_tt·g_rr = -1 holds EXACTLY at all perturbative orders (the
      B = 1/A identity is automatic, not imposed).  K-verdict: the
      perturbed areal radius is r(1 + K Y/2); removing K from g_thth by
      the theta-dependent areal re-chart NECESSARILY generates
      g_{r theta} = e^{2phi0}(rK/2) d_th Y =/= 0 for ell >= 2 (the
      G-harmonic obstruction Theta·(Y'' - cot th Y') forces Theta = 0;
      verified on the ell = 2 witness; at ell = 1 the obstruction
      vanishes and K IS removable).  So for ell >= 2, K is NOT pure
      gauge; demanding the perturbed metric remain of P0 form in an
      areal chart (the strict perturbed-level extension of canon C-1)
      FORCES K = 0 as a configuration-space restriction, not a gauge
      choice.  Honest status: that extension of C-1 to perturbations is
      itself a reading (C-1 as canonized is a statement about the
      static sector); K is therefore carried SYMBOLICALLY through
      W2-W3, where the native variational analysis independently
      disqualifies it (W3, parametrization obstruction).  H1 is
      untouched by C-1 (it enters neither g_tt·g_rr nor g_thth).

  W2  EINSTEIN SIDE, IDENTITY LEVEL (guardrail-legal: curvature
      identities follow from the metric alone).  On general phi0(r),
      with the W1 ties imposed and (H1, K) kept:

          dG^t_theta = e^{2phi0} [ -(1/2) d_r(e^{-2phi0} H1)
                        + d_t(dphi) + (1/2) d_t K ] · d_theta Y

      EXACTLY - the AUDIT.md S116 'Step 1' radial operator, now verified
      on an ARBITRARY profile (AUDIT computed it on the canonical
      cosmological one).  Coefficient of Y is exactly 0; no Y'' and no
      ell(ell+1) anywhere (the constraint is ell-flat, confirming the
      S116 finding at general f).  Bonus exact fact: dT^t_theta[C1] = 0
      at first order, so at matter scope (C1 the only content) the
      Einstein weld would be SOURCE-FREE: d_r(f H1) = 2 d_t dphi + d_t K.

  W3  THE NATIVE SIDE (the heart).  The exact second-order C1 action on
      the UDT perturbed configuration (variation rule documented below)
      contains NO derivatives of H1 or K - both enter algebraically
      (structural: the C1 action carries no metric derivatives, so
      metric perturbations can never acquire native kinetic terms from
      it).  The native H1 Euler-Lagrange equation is the ALGEBRAIC weld

          f phi0' H1 = 2 d_t(dphi)    <=>    f' H1 = -4 d_t(dphi)
          [i.e.  -(1/2)(d_r e^{-2phi0}) H1 = 2 d_t(dphi)],

      STRUCTURAL IDENTIFICATION (verifier, a709e4306bdf91b3a): EL_H1 is
      exactly -r^2·(delta T_tr) - the native weld is first-order
      VANISHING RADIAL ENERGY FLUX (T_tr = 0), the matter-only remnant
      of GR's (t,r) slot.  In GR, H1-variation yields the (t,r)
      Einstein equation, never the (t,theta) weld, which only arrives
      via Bianchi plus the rest of the Einstein system (which W4 closes
      off natively).  This explains why grade (d) was forced.  It is

      NOT the Einstein differential constraint d_r(e^{-2phi0}H1) =
      2 d_t dphi + d_t K.  GRADE: (d) - H1 does NOT drop out (not (c)),
      and the equation is not the Einstein weld with different
      coefficients (not (b)): it welds the SAME pair (H1 <-> d_t dphi)
      but with algebraic (0th-order) instead of first-order radial
      structure, and no K.  Verified inequivalent by witness.  Limits:
      where phi0' = 0 the H1 sector vanishes identically from the
      second-order action (grade (c) on locally-flat backgrounds).
      K-verdict (native side): the K Euler-Lagrange equation is
      PARAMETRIZATION-AMBIGUOUS - g_thth = r^2(1 + KY) vs r^2 e^{KY}
      give K-equations differing by exactly T^th_th[bg]·r^2·K (the
      banked angular-stress / Einstein-tension object of the gr-balance
      file).  A second-order action is parametrization-independent only
      in directions where the background is stationary; UDT's PROVEN
      refusal of the theta-theta Einstein equation is precisely the
      failure of stationarity in the g_thth direction.  K is therefore
      NOT a well-defined native variational field on the banked
      background: the native system is (dphi, H1), with K = 0 the
      canon-consistent slice (agreeing with W1).
      CONSEQUENCE (new, exact): eliminating the auxiliary H1 through its
      own algebraic weld FLIPS the sign of the dphi time-kinetic term
      ((c/2) -> (c/2) - c = -(c/2): the cross-coupling contributes
      exactly -c), so the on-shell native (dphi, H1) system is ELLIPTIC
      in (t, r):

          + r^2 d_t^2(dphi) + d_r(r^2 f^2 d_r dphi)
          - 4 r^2 f^2 E0 dphi - lam f dphi = 0,
          E0 := phi0'' + 2 phi0'/r - 2 phi0'^2  (= 0 in vacuum; = the
          source density in a sourced cell),

      and for E0 >= 0 a positive-definite quadratic form (pointwise
      lam f + 4 r^2 f^2 E0 >= 0 suffices) shows real-frequency normal
      modes have NO nontrivial solutions under Dirichlet-type boundary
      conditions - omega^2 < 0 (relaxation/instability) is the native
      spectrum THERE.  The no-real-omega conclusion is PROVEN ONLY FOR
      E0 >= 0 (verifier correction): on collars with E0 < 0 the balance
      can flip.  Verifier counterexample, reproduced numerically in
      W3(e'): phi0 = -3(r - 3/2)^2 on [1, 2], ell = 2, Dirichlet -
      real mode omega^2 = +7.53; vacuum control on the same cell:
      omega^2 = -12.6.  THE FINDING: on SOURCED collars (E0 = the
      angular source term, nonzero on matter cells) the native elliptic
      system CAN support real-frequency oscillation modes - the source
      that softens the core can open its own oscillation window.
      With H1 EXCLUDED instead (strict
      diagonal P0 reading), the dphi equation is the clean HYPERBOLIC
      wave equation - r^2 d_t^2 dphi + d_r(r^2 f^2 d_r dphi) - ... = 0
      with characteristic speed dr/dt = f (same light cones as the
      macro carrier).  The physical character of the matter-side
      breathing sector depends decisively on H1's field status.

  W4  BIANCHI/CONSERVATION ROUTE: does NOT imply the weld.  The
      contracted Bianchi identity div G = 0 is verified at orders 0 and
      1 (identity, any metric).  But the C1 stress obeys, at first
      order,

          (div T)_theta = c f^2 (E0 - phi0'^2) · dphi · d_theta Y,

      INDEPENDENT of H1 and K - the same scalar density (E0 - phi0'^2)
      whose radial projection is the banked background leftover
      (div T)_r = c f^2 phi0'(E0 - phi0'^2) = (c/4)f'(f'' + 2f'/r) +
      (c/8)f'^3/f (the gr-balance result, re-derived here from scratch).
      On the vacuum shell (E0 = 0) the first-order leftover is
      -c f^2 phi0'^2 dphi =/= 0 for any nontrivial breathing.  Since
      div G = 0 identically, imposing the FULL theta-row of Einstein
      equations would force (div T)_theta = 0, i.e. dphi = 0: the
      Einstein theta-row is INCONSISTENT with any breathing mode on the
      UDT background.  Hence Bianchi + conservation cannot derive the
      (t,theta) weld; at matter scope the weld is an independent INPUT
      (and natively, W3 supplies a DIFFERENT H1 equation).

  W5  VERDICT: the rung-2 weld in its Einstein differential form is NOT
      native to the C1 dynamics at matter scope - and it is EQUALLY an
      import structurally at MACRO scope (the non-C1 macro content
      changes the SOURCE TERM, not the constraint's pedigree; macro
      total-conservation self-consistency is unverified).  Macro
      empirical support is CHANNEL-SPECIFIC: phase/interleaving/TE
      PASSED; the EE amplitude is the standing ~2x overshoot.  And the
      validated phase signature (H1 in quadrature with dphi) follows
      from H1 ~ d_t(dphi) in TIME structure, which BOTH welds supply -
      the macro phase channel may not discriminate them.  Phase-2
      discriminator: rerun the macro projection with the native
      algebraic weld H1 = -4 d_t(dphi)/f' and compare radial structure
      against the CMB record.  The native C1 system has its OWN weld -
      algebraic, H1 = -4 d_t(dphi)/f' - so the phi-angular dynamical
      coupling of canon C-3 SURVIVES natively in modified form.  The
      final matter-side system (canon slice K = 0, finite cell
      [0, R_cell], phi0(R_cell) = 0 interface per C-2) is printed in
      W5, with both H1 readings recorded.  Spectra are phase 2.

VARIATION RULE USED (W3, documented per the dispatch spec): the honest
native variation treats phi as BOTH metric and field - dphi is varied
EVERYWHERE phi appears (the e^{-2phi} action weight, the gradient slots,
AND the metric factors g_tt = -e^{-2phi}, g_rr = e^{+2phi} inside g^{mu
nu} and sqrt(-g)); H1 and K are varied as independent metric fields
where present.  The self-coupling difference against the frozen-metric
(GR-import) rule is computed exactly and printed.

HONEST CAVEATS (binding):
  - Mode bookkeeping: single axisymmetric even-parity mode Y(theta),
    ell >= 1 (so that the first-order action integrates to zero by
    int Y dOmega = 0); normalization int Y^2 dOmega = 1, lam :=
    int (d_th Y)^2 dOmega (= ell(ell+1) for spherical harmonics).  The
    ell = 0 monopole and odd-parity sectors are out of scope.  K's
    gauge rigidity holds for ell >= 2; at ell = 1 K is removable
    (verified) and the K-discussion is moot there.
  - RW gauge: the configuration space used IS the RW-gauge even-parity
    set; the G-harmonic (the second sphere-block angular structure) is
    set to zero exactly as in the macro derivation.  Statements about
    K's status are statements within this (standard, macro-matched)
    parametrization.
  - The W3 grade is about the C1 action as banked.  If Charles canonizes
    additional native sectors that carry metric derivatives (an EH-like
    remainder, the A3 rho-dynamics candidates, boundary blocks), H1 and
    K could acquire genuine native kinetic terms and the grade must be
    re-derived; this file then provides the C1 baseline they must be
    added to.
  - The elliptic/no-real-omega statement is PROVEN ONLY FOR E0 >= 0
    (pointwise lam f + 4 r^2 f^2 E0 >= 0 suffices); it is a property of
    the second-order C1 action with H1 variational and eliminated
    on-shell, under boundary conditions making the boundary term
    vanish.  On sourced collars with E0 < 0 it FAILS - the W3(e')
    counterexample has a genuine real mode - so the E0 < 0 oscillation
    window is a FINDING, not a loophole.  Exotic
    (non-Dirichlet/Neumann-mixed, pumped-boundary) conditions are
    phase-2 territory and could evade it even at E0 >= 0.  It is NOT a
    claim about the macro weld sector, which is governed by the
    (imported, data-tested) Einstein constraint plus non-C1 content.
  - phi0'(r) zeros: at isolated radii where phi0' = 0 the native
    algebraic weld degenerates (0 = 2 d_t dphi there) - the native H1
    equation is solvable for H1 only where phi0' =/= 0.  Recorded, not
    resolved.

SPEC CROSS-CHECKS (sympy wins; here sympy CONFIRMS):
  - H2 = 2 dphi and H0 = -2 dphi exactly as the dispatch spec expected.
  - Background C1 EL in vacuum: phi0'' + 2 phi0'/r - 2 phi0'^2 = 0,
    exactly as the spec stated (re-derived, and (r^2 f')' = 0 is its
    f-language form).
  - AUDIT.md S116 radial operator confirmed at GENERAL f, including the
    K-term: the dG^t_theta K-coefficient is +(1/2) e^{2phi0} d_t K, so
    the refined weld carries '+ d_t K' with coefficient exactly 1 -
    matching the S116 refinement.
  No spec-math corrections were required; the new exact findings (the
  algebraic native weld, the kinetic flip, the K parametrization
  obstruction, the first-order conservation leftover) are reported above.

New file 2026-06-10; amended same-day per blind verifier (agent
a709e4306bdf91b3a): (i) the no-real-omega claim scoped to E0 >= 0 with
the E0 < 0 real-mode counterexample reproduced numerically (W3(e'),
three new checks); (ii) the EL_H1 = -r^2 dT_tr radial-energy-flux
identification added (W3(a), new check); (iii) macro-scope wording
tightened (equally an import structurally; channel-specific empirical
support; the phase channel may not discriminate the two welds).  All
existing checks unweakened.  Creates nothing else, modifies nothing
existing.  Runtime: ~5 seconds (4D linearized Einstein tensor on
symbolic functions, O(eps)-truncated throughout; one small dense
eigensolve in W3(e')).
"""

from __future__ import annotations

import sys

import numpy as np
import sympy as sp

FAILURES: list[str] = []


def check(label: str, ok: bool) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# Shared symbols
# ---------------------------------------------------------------------------
t, r, th, az, eps = sp.symbols("t r theta varphi epsilon", real=True)
c_s = sp.symbols("c", positive=True)          # C1 normalization (repo c = 2)
lam = sp.symbols("lam", positive=True)        # int (d_th Y)^2 dOmega
GN = sp.symbols("G_N", positive=True)         # Newton constant (symbolic)

phi0 = sp.Function("phi0", real=True)(r)      # background dilation, ARBITRARY
p = sp.Function("deltaphi", real=True)(t, r)  # dphi mode amplitude
h = sp.Function("H1", real=True)(t, r)        # H1 mode amplitude
k = sp.Function("K", real=True)(t, r)         # K mode amplitude
Y = sp.Function("Y", real=True)(th)           # angular profile, ARBITRARY

F = sp.exp(-2 * phi0)                         # f = e^{-2 phi0}
phi0p = sp.diff(phi0, r)
E0 = sp.diff(phi0, r, 2) + 2 * phi0p / r - 2 * phi0p**2   # background C1 EL
Yp = sp.Derivative(Y, th)
coords = [t, r, th, az]
N4 = 4


def trunc(e: sp.Expr) -> sp.Expr:
    """Keep orders eps^0 and eps^1 of an eps-polynomial expression."""
    e = sp.expand(e)
    return e.coeff(eps, 0) + eps * e.coeff(eps, 1)


def dsimp(e: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.expand(e))


# ===========================================================================
# W1 — kinematic reduction from the canon: the H0/H2 ties and the K-verdict
# ===========================================================================
hr("W1 — KINEMATIC TIES FROM THE CANON (B = 1/A at perturbed level) "
   "AND THE K-VERDICT")

phi_full = phi0 + eps * p * Y
gtt_udt = -sp.exp(-2 * phi_full)
grr_udt = sp.exp(2 * phi_full)

check("UDT structure: g_tt·g_rr = -1 EXACTLY at all orders in eps "
      "(delta(g_tt g_rr) = 0 is automatic, not imposed)",
      sp.simplify(gtt_udt * grr_udt + 1) == 0)

dgtt = sp.expand(sp.series(gtt_udt, eps, 0, 2).removeO()).coeff(eps, 1)
dgrr = sp.expand(sp.series(grr_udt, eps, 0, 2).removeO()).coeff(eps, 1)
# RW parametrization: dg_tt = -f H0 Y, dg_rr = (1/f) H2 Y
H0_val = sp.simplify(dgtt / (-F * Y))
H2_val = sp.simplify(dgrr / ((1 / F) * Y))
check("RW match: dg_tt = -f·H0·Y with H0 = -2 dphi exactly (spec "
      "expectation confirmed)", sp.simplify(H0_val + 2 * p) == 0)
check("RW match: dg_rr = (1/f)·H2·Y with H2 = +2 dphi exactly (spec "
      "expectation confirmed)", sp.simplify(H2_val - 2 * p) == 0)

H0g, H2g = sp.symbols("H0g H2g", real=True)
prod_gen = (-F * (1 + eps * H0g * Y)) * ((1 / F) * (1 + eps * H2g * Y))
check("generic RW fields: delta(g_tt g_rr) = -(H0 + H2)·Y, so the "
      "perturbed B = 1/A identity <=> H0 = -H2; with metric-is-phi "
      "(H2 = 2 dphi) this forces H0 = -2 dphi — the ties are the unique "
      "B=1/A-compatible reduction",
      sp.simplify(sp.expand(prod_gen).coeff(eps, 1) + (H0g + H2g) * Y) == 0)

rpos = sp.Symbol("rpos", positive=True)
areal = sp.sqrt(rpos**2 * (1 + eps * k.subs(r, rpos) * Y))
areal_ser = sp.series(areal, eps, 0, 2).removeO()
check("perturbed areal radius: sqrt(g_thth) = r·(1 + K·Y/2) + O(eps²) — "
      "the (th,phi)-sphere areal radius shifts by r·K·Y/2",
      sp.simplify(areal_ser - (rpos + eps * rpos * k.subs(r, rpos)
                               * Y / 2)) == 0)

print()
print("  K-removal analysis (is K pure gauge / removable into an areal "
      "re-chart?):")
g0m = sp.diag(-F, 1 / F, r**2, r**2 * sp.sin(th)**2)
Tf = sp.Function("T", real=True)(t, r)
Rf = sp.Function("R", real=True)(t, r)
Thf = sp.Function("Theta", real=True)(t, r)
xi = [Tf * Y, Rf * Y, Thf * sp.diff(Y, th), 0]   # general even-parity vector


def lie_g(mu: int, nu: int) -> sp.Expr:
    return sp.expand(
        sum(xi[a] * sp.diff(g0m[mu, nu], coords[a]) for a in range(N4))
        + sum(g0m[a, nu] * sp.diff(xi[a], coords[mu]) for a in range(N4))
        + sum(g0m[mu, a] * sp.diff(xi[a], coords[nu]) for a in range(N4)))


check("(L_xi g)_thth = 2rR·Y + 2r²Theta·Y'' exactly",
      dsimp(lie_g(2, 2) - (2 * r * Rf * Y
                           + 2 * r**2 * Thf * sp.diff(Y, th, 2))) == 0)
check("(L_xi g)_phph = sin²th·(2rR·Y) + 2r²Theta·sin th·cos th·Y' exactly",
      dsimp(lie_g(3, 3) - (2 * r * Rf * Y * sp.sin(th)**2
                           + 2 * r**2 * Thf * sp.sin(th) * sp.cos(th)
                           * sp.diff(Y, th))) == 0)
# removing K from BOTH sphere slots needs the G-harmonic combination to vanish
obstruction = dsimp(lie_g(2, 2) * sp.sin(th)**2 - lie_g(3, 3)
                    - 2 * r**2 * Thf * sp.sin(th)**2
                    * (sp.diff(Y, th, 2) - sp.cos(th) / sp.sin(th)
                       * sp.diff(Y, th)))
check("trace/G-harmonic split: (L_xi g)_thth·sin²th - (L_xi g)_phph = "
      "2r²Theta·sin²th·(Y'' - cot th·Y') — removing K from BOTH sphere "
      "slots while keeping the RW form (G-harmonic = 0) requires "
      "Theta·(Y'' - cot th·Y') = 0", obstruction == 0)
Y2 = 3 * sp.cos(th)**2 - 1            # ell = 2 witness
Y1 = sp.cos(th)                       # ell = 1 witness
gharm = lambda Yw: sp.simplify(sp.diff(Yw, th, 2)
                               - sp.cos(th) / sp.sin(th) * sp.diff(Yw, th))
check("ell = 2 witness (Y = 3cos²th - 1): Y'' - cot th·Y' = 6 sin²th =/= 0 "
      "=> Theta = 0 is FORCED for ell >= 2",
      sp.simplify(gharm(Y2) - 6 * sp.sin(th)**2) == 0)
check("ell = 1 honesty (Y = cos th): Y'' - cot th·Y' = 0 — at ell = 1 the "
      "obstruction vanishes and K IS removable (dipole caveat recorded)",
      gharm(Y1) == 0)
# with Theta = 0 forced, R = rK/2 cancels K; the price is the (r,th) slot
sub_fix = {Thf: 0, Rf: r * k / 2}
check("with Theta = 0, R = rK/2: (L_xi g)_thth = r²K·Y and (L_xi g)_phph "
      "= r²K·Y·sin²th — K removed from the sphere block",
      dsimp(lie_g(2, 2).subs(sub_fix) - r**2 * k * Y) == 0
      and dsimp(lie_g(3, 3).subs(sub_fix)
                - r**2 * k * Y * sp.sin(th)**2) == 0)
rth_residual = dsimp(lie_g(1, 2).subs(sub_fix).doit())
check("THE PRICE: the same transformation generates "
      "delta g_{r th} = -e^{2phi0}·(rK/2)·d_th Y =/= 0 — the perturbed "
      "metric leaves the P0/RW class (no diagonal-block areal chart "
      "exists for K =/= 0, ell >= 2)",
      dsimp(rth_residual - sp.exp(2 * phi0) * (r * k / 2)
            * sp.diff(Y, th)) == 0)

print("""
  W1 K-VERDICT (honest): for ell >= 2, K is NOT pure gauge within the
  P0/RW class (the G-harmonic obstruction forces Theta = 0; the unique
  K-removing re-chart generates g_{r th} =/= 0, i.e. exits the class).
  Demanding that the perturbed metric still be of P0 form in a perturbed
  AREAL chart — the strict perturbed-level extension of canon C-1 —
  therefore FORCES K = 0 as a restriction of the UDT configuration
  space, not as a gauge choice.  Because that extension of C-1 (a
  static-sector canon) to perturbations is itself a reading, K is
  carried SYMBOLICALLY through W2-W3; W3's variational analysis then
  disqualifies K independently.  H1 is untouched by C-1 (absent from
  g_tt·g_rr and from g_thth): the canon leaves H1 FREE.  Candidate
  matter-side systems after W1: (dphi, H1) [strict canon] or
  (dphi, H1, K) [loose reading] — decided in W3.""")

# ===========================================================================
# W2 — the Einstein side at identity level: dG^t_theta on general f
# ===========================================================================
hr("W2 — EINSTEIN SIDE (IDENTITY LEVEL): dG^t_theta ON GENERAL f = "
   "e^{-2phi0(r)}, W1 TIES IMPOSED, (H1, K) KEPT")

# metric to O(eps): UDT ties (H0 = -2p, H2 = +2p), H1, K
gm = sp.zeros(4, 4)
gm[0, 0] = -F + eps * 2 * F * p * Y
gm[1, 1] = 1 / F + eps * (2 / F) * p * Y
gm[0, 1] = gm[1, 0] = eps * h * Y
gm[2, 2] = r**2 * (1 + eps * k * Y)
gm[3, 3] = r**2 * sp.sin(th)**2 * (1 + eps * k * Y)

g0i = sp.diag(*[1 / sp.expand(gm[i, i]).coeff(eps, 0) for i in range(N4)])
g1m = gm.applyfunc(lambda e: sp.expand(e).coeff(eps, 1))
ginv = (g0i - eps * g0i * g1m * g0i).applyfunc(trunc)
check("inverse metric to O(eps): g·g^{-1} = id + O(eps²) "
      "(first-order inverse exact)",
      sp.simplify((gm * ginv).applyfunc(trunc) - sp.eye(4))
      == sp.zeros(4, 4))

Gam = [[[None] * N4 for _ in range(N4)] for _ in range(N4)]
for a in range(N4):
    for b in range(N4):
        for cc in range(b, N4):
            expr = sum(ginv[a, d] * (sp.diff(gm[d, b], coords[cc])
                                     + sp.diff(gm[d, cc], coords[b])
                                     - sp.diff(gm[b, cc], coords[d])) / 2
                       for d in range(N4))
            expr = trunc(expr)
            Gam[a][b][cc] = expr
            Gam[a][cc][b] = expr


def ricci(b: int, cc: int) -> sp.Expr:
    return trunc(
        sum(sp.diff(Gam[a][b][cc], coords[a]) for a in range(N4))
        - sum(sp.diff(Gam[a][b][a], coords[cc]) for a in range(N4))
        + sum(Gam[a][a][d] * Gam[d][b][cc]
              for a in range(N4) for d in range(N4))
        - sum(Gam[a][cc][d] * Gam[d][b][a]
              for a in range(N4) for d in range(N4)))


Ric = sp.zeros(4, 4)
for i in range(N4):
    for j in range(i, N4):
        Ric[i, j] = ricci(i, j)
        Ric[j, i] = Ric[i, j]
Rs = trunc(sum(ginv[i, j] * Ric[i, j] for i in range(N4)
               for j in range(N4)))
Gmix = sp.Matrix(N4, N4, lambda i, j: trunc(sum(
    ginv[i, kk] * (Ric[kk, j] - sp.Rational(1, 2) * Rs * gm[kk, j])
    for kk in range(N4))))
print("  (linearized Einstein tensor computed from scratch, O(eps) exact)")

# background anchors (tie to the gr-balance file, in f-language)
fgen = sp.Function("f", positive=True)(r)
to_f = {phi0: -sp.log(fgen) / 2}
Gthth_bg = dsimp(Gmix[2, 2].coeff(eps, 0))
check("background anchor: G^th_th = -f·E0 with E0 = phi0'' + 2phi0'/r - "
      "2phi0'^2 — the theta-theta Einstein-VACUUM equation IS the banked "
      "vacuum equation (A2 of the gr-balance file, re-derived)",
      dsimp(Gthth_bg + F * E0) == 0)
check("f-language: G^th_th = f''/2 + f'/r exactly (matches the banked "
      "identity (r²f')'/(2r²))",
      sp.simplify(Gthth_bg.subs(phi0, -sp.log(fgen) / 2).doit()
                  - (sp.diff(fgen, r, 2) / 2 + sp.diff(fgen, r) / r)) == 0)
Gtt_bg = dsimp(Gmix[0, 0].coeff(eps, 0))
check("background anchor: G^t_t = (r f' + f - 1)/r² in f-language "
      "(matches gr-balance A2)",
      sp.simplify(Gtt_bg.subs(phi0, -sp.log(fgen) / 2).doit()
                  - (r * sp.diff(fgen, r) + fgen - 1) / r**2) == 0)

dG_tth = dsimp(Gmix[0, 2].coeff(eps, 1))
pred_op = sp.exp(2 * phi0) * (
    -sp.Rational(1, 2) * sp.diff(F * h, r)
    + sp.Derivative(p, t) + sp.Rational(1, 2) * sp.Derivative(k, t))
check("THE W2 RESULT (exact, general phi0(r)): dG^t_theta = e^{2phi0}·"
      "[-(1/2) d_r(e^{-2phi0} H1) + d_t(dphi) + (1/2) d_t K]·d_th Y — "
      "AUDIT.md S116 'Step 1' operator confirmed on an arbitrary profile, "
      "K-coefficient exactly +1/2",
      dsimp(dG_tth - pred_op * sp.diff(Y, th)) == 0)
ratio = dsimp(dG_tth / sp.diff(Y, th))
check("coefficient of Y(theta) is exactly 0 and no Y'' appears: "
      "dG^t_theta / d_th Y is theta-free (clean transverse vector; "
      "ell-flat — no ell(ell+1) anywhere, at GENERAL f)",
      not ratio.has(Y) and not ratio.has(th))

# C1 stress at first order: the weld source at matter scope
phi_w2 = phi0 + eps * p * Y
E2w = trunc(sp.series(sp.exp(-2 * phi_w2), eps, 0, 2).removeO())
dphi_w2 = [sp.diff(phi_w2, x) for x in coords]
grad2_w2 = trunc(sum(ginv[i, j] * dphi_w2[i] * dphi_w2[j]
                     for i in range(N4) for j in range(N4)))
Tlow = sp.Matrix(N4, N4, lambda i, j: trunc(
    c_s * E2w * (dphi_w2[i] * dphi_w2[j]
                 - sp.Rational(1, 2) * gm[i, j] * grad2_w2)))
Tmix = sp.Matrix(N4, N4, lambda i, j: trunc(sum(
    ginv[i, kk] * Tlow[kk, j] for kk in range(N4))))
check("background C1 stress anchor: T^th_th = -(c/2) e^{-4phi0} phi0'^2 "
      "= -(c/8) f'^2 — the gr-balance angular TENSION, re-derived",
      dsimp(Tmix[2, 2].coeff(eps, 0)
            + sp.Rational(1, 2) * c_s * F**2 * phi0p**2) == 0)
check("dT^t_theta[C1] = 0 at first order EXACTLY — at matter scope (C1 "
      "the only content) the Einstein weld would be SOURCE-FREE",
      dsimp(Tmix[0, 2].coeff(eps, 1)) == 0)

print("""
  W2 RESULT (exact, general f):  dG^t_theta =
      e^{2phi0} [ -(1/2) d_r(e^{-2phi0} H1) + d_t(dphi) + (1/2) d_t K ]
      · d_th Y
  so IF the (t,theta) Einstein equation dG^t_theta = 8 pi G dT^t_theta is
  imposed (an import, per the guardrail), the weld reads
      d_r(e^{-2phi0} H1) = 2 d_t(dphi) + d_t K - 16 pi G e^{-2phi0} tau,
  dT^t_theta =: tau·d_th Y — exactly the AUDIT.md refined weld; and at
  matter scope tau[C1] = 0.  This is identity-level geometry (guardrail-
  legal); whether anything NATIVE enforces it is W3/W4.""")

# ===========================================================================
# W3 — the native side: exact second-order C1 action and ALL its EL equations
# ===========================================================================
hr("W3 — THE NATIVE SIDE: SECOND-ORDER C1 ACTION "
   "S = -(c/2) int e^{-2phi} g^{mu nu} d_mu phi d_nu phi sqrt(-g)")


def build_L(gthth_pert: sp.Expr, phi_metric: sp.Expr,
            phi_scalar: sp.Expr) -> sp.Expr:
    """Exact C1 density.  phi_metric enters the metric factors; phi_scalar
    the explicit scalar slots (e^{-2phi} weight and gradients).  The
    NATIVE rule sets phi_metric = phi_scalar (self-coupled variation);
    the frozen-metric contrast keeps phi_metric at background."""
    g = sp.zeros(4, 4)
    g[0, 0] = -sp.exp(-2 * phi_metric)
    g[1, 1] = sp.exp(2 * phi_metric)
    g[0, 1] = g[1, 0] = eps * h * Y
    g[2, 2] = gthth_pert
    g[3, 3] = gthth_pert * sp.sin(th)**2
    ginvL = g.inv()
    sqrtg = sp.sqrt(-g.det())
    dphiL = [sp.diff(phi_scalar, x) for x in [t, r, th]]
    grad2 = sum(ginvL[i, j] * dphiL[i] * dphiL[j]
                for i in range(3) for j in range(3))
    L = -sp.Rational(1, 2) * c_s * sp.exp(-2 * phi_scalar) * grad2 * sqrtg
    return L.subs(sp.Abs(sp.sin(th)), sp.sin(th))


def angular_reduce(L2_over_sin: sp.Expr, label: str) -> sp.Expr:
    """Reduce the eps^2 density to the mode Lagrangian via
    int Y^2 dOmega = 1, int Y'^2 dOmega = lam."""
    e = sp.expand(L2_over_sin)
    A = e.coeff(Y, 2).subs(Yp, 0)
    B = e.coeff(Yp, 2).subs(Y, 0)
    check(f"angular structure of L2 [{label}]: only Y² and (d_th Y)² "
          "appear (residual after extraction = 0)",
          dsimp(e - A * Y**2 - B * Yp**2) == 0)
    return sp.expand(A + lam * B)


phiM = phi0 + eps * p * Y
L_I = build_L(r**2 * (1 + eps * k * Y), phiM, phiM)        # param I
L_II = build_L(r**2 * sp.exp(eps * k * Y), phiM, phiM)     # param II

L2red = {}
for name, L in [("param I: g_thth = r²(1+KY)", L_I),
                ("param II: g_thth = r² e^{KY}", L_II)]:
    ser = sp.series(L, eps, 0, 3).removeO()
    L0 = dsimp(ser.coeff(eps, 0) / sp.sin(th))
    L1 = dsimp(ser.coeff(eps, 1) / sp.sin(th))
    if name.startswith("param I:"):
        check("background density: L0 = -(c/2) e^{-4phi0} r² phi0'^2 "
              "(the banked C1 density)",
              dsimp(L0 + sp.Rational(1, 2) * c_s * F**2 * r**2
                    * phi0p**2) == 0)
        L1Y = dsimp(L1 / Y)
        check("first-order action: L1 is proportional to Y (h- and "
              "Y'-free), so int L1 dOmega = 0 for ell >= 1 — the "
              "background is stationary WITHIN the mode sector and the "
              "second-order action is well-posed there",
              not L1Y.has(Y) and not L1Y.has(h))
        # background EL re-derivation (spec cross-check)
        L0f = -sp.Rational(1, 2) * c_s * F**2 * r**2 * phi0p**2
        ELbg = sp.diff(L0f, phi0) - sp.diff(sp.diff(L0f, phi0p), r)
        check("background C1 EL: EL_phi0 = c e^{-4phi0} r² (phi0'' + "
              "2phi0'/r - 2phi0'^2) — vacuum equation exactly as the "
              "dispatch spec stated; (r²f')' = 0 is its f-language form",
              dsimp(ELbg - c_s * F**2 * r**2 * E0) == 0)
    L2red[name.split(":")[0].strip()] = angular_reduce(
        ser.coeff(eps, 2) / sp.sin(th), name)

L2 = L2red["param I"]
pt, pr_ = sp.Derivative(p, t), sp.Derivative(p, r)

check("STRUCTURAL FACT: the second-order C1 action contains NO "
      "derivatives of H1 or K (both parametrizations) — a matter-type "
      "action carries no metric derivatives, so H1 and K are AUXILIARY "
      "(algebraic) fields natively; no native kinetic terms exist for "
      "them in C1",
      not any(L2v.has(d) for L2v in L2red.values()
              for d in [sp.Derivative(h, t), sp.Derivative(h, r),
                        sp.Derivative(k, t), sp.Derivative(k, r)]))

# organized closed form of L2 (param I)
L2_target = c_s * (
    sp.Rational(1, 2) * r**2 * pt**2
    - sp.Rational(1, 2) * F**2 * r**2 * pr_**2
    + 4 * F**2 * r**2 * phi0p * p * pr_
    - 4 * F**2 * r**2 * phi0p**2 * p**2
    - sp.Rational(1, 2) * lam * F * p**2
    - F * r**2 * phi0p * h * pt
    + sp.Rational(1, 4) * F**2 * r**2 * phi0p**2 * h**2
    + F**2 * r**2 * phi0p * (2 * phi0p * p - pr_) * k)
check("closed form (param I): L2/c = (1/2)r²(d_t dphi)² - (1/2)f²r²"
      "(d_r dphi)² + 4f²r²phi0'·dphi·d_r dphi - 4f²r²phi0'^2 dphi² - "
      "(lam/2) f dphi² - f r² phi0'·H1·d_t dphi + (1/4) f²r²phi0'^2 H1² "
      "+ f²r²phi0'(2phi0' dphi - d_r dphi)·K  exactly",
      dsimp(L2 - L2_target) == 0)

print()
print("  (a) the native H1 equation — THE DECISIVE QUESTION:")
EL_h_I = dsimp(sp.diff(L2, h))
EL_h_II = dsimp(sp.diff(L2red["param II"], h))
check("H1 sector is parametrization-SAFE: EL_H1 identical in both "
      "g_thth parametrizations (the background is stationary in the "
      "g_tr direction — no linear H1 term exists in L1)",
      dsimp(EL_h_I - EL_h_II) == 0)
check("EL_H1 = (c/2) r² e^{-4phi0} phi0'·[phi0'·H1 - 2 e^{2phi0}·"
      "d_t dphi] exactly",
      dsimp(EL_h_I - sp.Rational(1, 2) * c_s * r**2 * F**2 * phi0p
            * (phi0p * h - 2 * sp.exp(2 * phi0) * pt)) == 0)
native_weld = sp.Eq(F * phi0p * h, 2 * pt)
check("THE NATIVE WELD (exact, phi0' =/= 0): EL_H1 = 0  <=>  "
      "f phi0'·H1 = 2 d_t dphi  <=>  f'·H1 = -4 d_t dphi  <=>  "
      "-(1/2)(d_r e^{-2phi0})·H1 = 2 d_t dphi — ALGEBRAIC, not "
      "differential",
      sp.solve(sp.Eq(EL_h_I, 0), h)
      == [2 * sp.exp(2 * phi0) * pt / phi0p]
      and dsimp(F * phi0p - (-sp.Rational(1, 2) * sp.diff(F, r))) == 0)
check("phi0' -> 0 limit: EL_H1 vanishes IDENTICALLY (H1 drops out of "
      "the second-order C1 action on locally-flat backgrounds — grade "
      "(c) holds there, and only there)",
      dsimp(EL_h_I.subs(phi0, 0).doit()) == 0)
dT_tr1 = sp.expand(Tlow[0, 1]).coeff(eps, 1)
check("STRUCTURAL IDENTIFICATION (verifier): EL_H1·Y = -r²·(dT_tr) "
      "EXACTLY — the native weld is first-order VANISHING RADIAL "
      "ENERGY FLUX (delta T_tr = 0), the matter-only remnant of GR's "
      "(t,r) slot; in GR, H1-variation yields the (t,r) Einstein "
      "equation, never the (t,theta) weld (that needs Bianchi + the "
      "REST of the Einstein system, which W4 closes off natively) — "
      "this is why grade (d) was forced",
      dsimp(EL_h_I * Y + r**2 * dT_tr1) == 0)

# inequivalence with the Einstein weld: witness
print()
print("  (b) native weld vs Einstein weld — inequivalence witness:")
einstein_weld_lhs = sp.diff(F * h, r) - 2 * pt - sp.Derivative(k, t)
fw = 1 + 2 / r                                  # native banked member
phi0w = -sp.log(fw) / 2
pw = t * r                                      # any smooth breathing
hw = -4 * sp.diff(pw, t) / sp.diff(fw, r)       # solves the NATIVE weld
resid_native = (fw * (-sp.diff(fw, r) / (2 * fw)) * hw
                - 2 * sp.diff(pw, t))
resid_einstein = sp.diff(fw * hw, r) - 2 * sp.diff(pw, t)
check("witness (vacuum f = 1 + 2/r, dphi = t·r, K = 0): H1 = "
      "-4 d_t dphi / f' satisfies the native weld exactly but leaves "
      "Einstein-weld residual d_r(f H1) - 2 d_t dphi = 6r² + 6r =/= 0 — "
      "the two welds are INEQUIVALENT equations",
      sp.simplify(resid_native) == 0
      and sp.simplify(resid_einstein - (6 * r**2 + 6 * r)) == 0)

print()
print("  (c) the native K equation — the parametrization obstruction:")
EL_k_I = dsimp(sp.diff(L2, k))
EL_k_II = dsimp(sp.diff(L2red["param II"], k))
check("EL_K [param I] = -c r² f phi0' · d_r(f·dphi) — a pure radial "
      "constraint d_r(f·dphi) = 0 on dphi (no K in it!)",
      dsimp(EL_k_I + c_s * r**2 * F * phi0p * sp.diff(F * p, r)) == 0)
diff_k = dsimp(EL_k_II - EL_k_I)
check("EL_K [param II] - EL_K [param I] = -(c/2) r² e^{-4phi0} phi0'^2 K"
      " = T^th_th[bg]·r²·K exactly — the K-equation DEPENDS ON THE "
      "PARAMETRIZATION, and the ambiguity coefficient IS the banked "
      "angular stress (the unbalanced theta-theta object of the "
      "gr-balance file)",
      dsimp(diff_k + sp.Rational(1, 2) * c_s * r**2 * F**2 * phi0p**2 * k)
      == 0
      and dsimp(diff_k - (-sp.Rational(1, 2) * c_s * F**2 * phi0p**2)
                * r**2 * k) == 0)
print("""      => K is NOT a well-defined native variational field: a
      second-order action is field-redefinition invariant only in
      directions where the background action is stationary, and UDT's
      PROVEN non-imposition of the theta-theta Einstein equation is
      exactly the failure of stationarity in the g_thth direction.  (In
      GR the total action is background-stationary in ALL metric
      directions, so this ambiguity cancels — the contrast is UDT's own
      banked departure, now biting at perturbed level.)  Native system:
      (dphi, H1); K = 0 is the canon-consistent slice (agrees with W1).""")

print()
print("  (d) the native dphi equation (general f, K kept for the record):")
EL_p = dsimp(sp.diff(L2, p) - sp.diff(sp.diff(L2, pt), t)
             - sp.diff(sp.diff(L2, pr_), r))
EL_p_target = c_s * (
    -r**2 * sp.diff(p, t, 2)
    + r**2 * F * phi0p * sp.diff(h, t)
    + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
    - 4 * r**2 * F**2 * E0 * p
    - lam * F * p
    + F**2 * r**2 * (E0 * k + phi0p * sp.diff(k, r)))
check("EL_dphi = c·[ -r² d_t² dphi + r² f phi0' d_t H1 + d_r(r² f² "
      "d_r dphi) - 4 r² f² E0·dphi - lam f·dphi + f² r²(E0·K + "
      "phi0'·d_r K) ] exactly — the dphi potential term is -4f²r²E0·dphi"
      ", which VANISHES on the vacuum background (E0 = 0): background-EL "
      "simplification as directed",
      dsimp(EL_p - EL_p_target) == 0)

print()
print("  (e) eliminating the auxiliary H1 on its own weld — the kinetic "
      "flip:")
h_star = 2 * sp.exp(2 * phi0) * pt / phi0p
L2_eff = dsimp(L2.subs(h, h_star))
pt2_coeff = sp.expand(L2_eff).coeff(pt, 2)
check("effective Lagrangian after H1 elimination: the (d_t dphi)² "
      "coefficient is -(c/2)r² — FLIPPED from +(c/2)r² (the H1 coupling "
      "contributes exactly -c·r²; auxiliary-field elimination "
      "-B²/(4A) with A = (c/4)f²phi0'^2r², B = c f phi0' r²)",
      dsimp(pt2_coeff + sp.Rational(1, 2) * c_s * r**2) == 0)
EL_p_eff = dsimp(sp.diff(L2_eff, p) - sp.diff(sp.diff(L2_eff, pt), t)
                 - sp.diff(sp.diff(L2_eff, pr_), r))
check("equivalence of elimination routes: EL of the effective "
      "Lagrangian == EL_dphi with H1 = H1*(dphi) substituted (legal "
      "because dL/dH1 = 0 at H1*)",
      dsimp(EL_p_eff - EL_p.subs(h, h_star).doit()) == 0)
EL_p_onshell = dsimp(EL_p.subs(h, h_star).doit().subs(k, 0))
onshell_target = c_s * (r**2 * sp.diff(p, t, 2)
                        + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
                        - 4 * r**2 * F**2 * E0 * p - lam * F * p)
check("ON-SHELL NATIVE SYSTEM (K = 0): + r² d_t² dphi + d_r(r² f² "
      "d_r dphi) - 4 r² f² E0 dphi - lam f dphi = 0 — ELLIPTIC in "
      "(t, r): the native weld flips the time-kinetic sign",
      dsimp(EL_p_onshell - onshell_target) == 0)
# no-real-frequency quadratic form: the SL identity behind it.
# SCOPE (verifier correction): the positivity argument needs pointwise
# lam f + 4r²f²E0 >= 0 (in particular E0 >= 0); the E0 term must be
# KEPT in the mode equation on sourced backgrounds.
u = sp.Function("u", real=True)(r)
omega = sp.symbols("omega", positive=True)
mode_eq_gen = dsimp(onshell_target.subs(p, u * sp.cos(omega * t)).doit()
                    / (c_s * sp.cos(omega * t)))
check("normal modes dphi = u(r)cos(omega t), GENERAL E0 (verifier "
      "amendment — the E0 term stays): (r²f²u')' = (lam f + 4r²f²E0 + "
      "omega² r²)·u",
      dsimp(mode_eq_gen - (-omega**2 * r**2 * u
                           + sp.diff(r**2 * F**2 * sp.diff(u, r), r)
                           - 4 * r**2 * F**2 * E0 * u
                           - lam * F * u)) == 0)
mode_eq = dsimp(onshell_target.subs(E0, 0)
                .subs(p, u * sp.cos(omega * t)).doit()
                / (c_s * sp.cos(omega * t)))
check("normal modes on VACUUM (E0 = 0): (r²f²u')' = (lam f + omega² "
      "r²)·u — and u·(r²f²u')' = d_r(r²f²u'u) - r²f²u'^2, so int over "
      "the cell with vanishing boundary term gives int[r²f²u'^2 + "
      "lam f u² + omega² r² u²] = 0: NO nontrivial real-omega modes "
      "PROVEN FOR E0 >= 0 (pointwise lam f + 4r²f²E0 >= 0 suffices; "
      "covers every vacuum background) — omega² < 0 (relaxation/"
      "instability) is the native spectrum THERE; for E0 < 0 the "
      "argument fails and the window is REAL (next checks); "
      "boundary-condition caveat in the docstring",
      dsimp(mode_eq - (-omega**2 * r**2 * u
                       + sp.diff(r**2 * F**2 * sp.diff(u, r), r)
                       - lam * F * u)) == 0
      and dsimp(u * sp.diff(r**2 * F**2 * sp.diff(u, r), r)
                - sp.diff(r**2 * F**2 * sp.diff(u, r) * u, r)
                + r**2 * F**2 * sp.diff(u, r)**2) == 0)

print()
print("  (e') the E0 < 0 oscillation window — verifier counterexample, "
      "reproduced numerically:")


def top_mode(phi0_fn, dphi0_fn, ddphi0_fn, lam_v=6.0, n=800,
             ra=1.0, rb=2.0):
    """Largest generalized eigenvalue omega² of the Reading-A mode
    problem (r²f²u')' - (lam f + 4r²f²E0)u = omega² r² u with
    Dirichlet ends (second-order finite differences, symmetric
    weight-reduced dense eigensolve); also returns the pointwise
    minimum of the positivity density q(r) = lam f + 4r²f²E0."""
    rg = np.linspace(ra, rb, n + 2)
    hg = rg[1] - rg[0]
    fg = np.exp(-2.0 * phi0_fn(rg))
    E0g = (ddphi0_fn(rg) + 2.0 * dphi0_fn(rg) / rg
           - 2.0 * dphi0_fn(rg)**2)
    qg = lam_v * fg + 4.0 * rg**2 * fg**2 * E0g
    coefg = rg**2 * fg**2
    chalf = 0.5 * (coefg[:-1] + coefg[1:])
    A = np.zeros((n, n))
    for i in range(n):
        j = i + 1
        A[i, i] = -(chalf[j - 1] + chalf[j]) / hg**2 - qg[j]
        if i > 0:
            A[i, i - 1] = chalf[j - 1] / hg**2
        if i < n - 1:
            A[i, i + 1] = chalf[j] / hg**2
    S = np.diag(1.0 / rg[1:-1])          # M = diag(r²); M^{-1/2} A M^{-1/2}
    return (float(np.linalg.eigvalsh(S @ A @ S)[-1]), float(np.min(qg)),
            float(np.max(E0g)))


w2_src, qmin_src, E0max_src = top_mode(lambda x: -3.0 * (x - 1.5)**2,
                                       lambda x: -6.0 * (x - 1.5),
                                       lambda x: -6.0 + 0.0 * x)
w2_vac, qmin_vac, E0max_vac = top_mode(lambda x: 0.0 * x,
                                       lambda x: 0.0 * x,
                                       lambda x: 0.0 * x)
check("counterexample collar phi0 = -3(r - 3/2)² on [1, 2], ell = 2 "
      f"(lam = 6): E0 < 0 throughout (max E0 = {E0max_src:.2f}) and "
      "the pointwise positivity density fails badly (min q = "
      f"{qmin_src:.1f} < 0), while the vacuum control satisfies it "
      f"(min q = {qmin_vac:.2f} > 0)",
      E0max_src < 0 and qmin_src < 0 and qmin_vac > 0)
check("REAL-FREQUENCY MODE on the sourced collar (Dirichlet, n = 800): "
      f"top eigenvalue omega² = {w2_src:+.3f} = +7.53 > 0 — a real "
      "oscillation mode EXISTS where E0 < 0 (verifier value +7.53 "
      "reproduced)",
      w2_src > 0 and abs(w2_src - 7.53) < 0.02)
check("vacuum control on the same cell (phi0 = 0, ell = 2): top "
      f"eigenvalue omega² = {w2_vac:+.3f} = -12.6 < 0 — no real modes, "
      "exactly as the E0 >= 0 theorem demands (verifier value -12.6 "
      "reproduced)",
      w2_vac < 0 and abs(w2_vac + 12.64) < 0.02)
print("""      THE FINDING (verifier-corrected scope): on SOURCED collars
      (E0 = the angular source term, nonzero exactly on matter cells)
      the native elliptic system CAN support real-frequency oscillation
      modes — the source that softens the core can open its own
      oscillation window.  Whether the PHYSICAL sourced cell (banked
      eta = 1/18, ell = 1 source) sits inside the window is the phase-2
      computation.""")
EL_p_h0 = dsimp(EL_p.subs(h, 0).subs(k, 0))
check("contrast — H1 EXCLUDED by hand (strict diagonal P0 reading): "
      "-r² d_t² dphi + d_r(r² f² d_r dphi) - 4r²f²E0 dphi - lam f dphi "
      "= 0 — HYPERBOLIC (wave) with characteristic speed dr/dt = f, the "
      "same light cones as the macro carrier (principal symbol "
      "-omega² + f²k_r²)",
      dsimp(EL_p_h0 - c_s * (-r**2 * sp.diff(p, t, 2)
                             + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
                             - 4 * r**2 * F**2 * E0 * p
                             - lam * F * p)) == 0)

print()
print("  (f) variation-rule documentation — native (self-coupled) vs "
      "frozen-metric (GR-import) rule:")
pfro = sp.Function("deltaphi_s", real=True)(t, r)
L_frozen = build_L(r**2 * (1 + eps * k * Y), phi0,
                   phi0 + eps * pfro * Y)
ser_f = sp.series(L_frozen, eps, 0, 3).removeO()
L2_frozen = angular_reduce(ser_f.coeff(eps, 2) / sp.sin(th),
                           "frozen-metric contrast")
pfro_t = sp.Derivative(pfro, t)
pfro_r = sp.Derivative(pfro, r)
EL_p_frozen = dsimp(sp.diff(L2_frozen, pfro)
                    - sp.diff(sp.diff(L2_frozen, pfro_t), t)
                    - sp.diff(sp.diff(L2_frozen, pfro_r), r)
                    ).subs(pfro, p)
self_coupling = dsimp(EL_p.subs(h, 0).subs(k, 0)
                      - EL_p_frozen.subs(h, 0).subs(k, 0).doit())
check("the self-coupling terms (native minus frozen-metric dphi "
      "equation, H1 = K = 0 slice) are EXACTLY -2c r² f² (E0 + "
      "phi0'^2)·dphi — a pure mass-like shift (no gradient and no lam "
      "content), nonzero on every nontrivial background: the UDT "
      "metric-is-phi self-coupling is REAL in the mode equations, not "
      "a relabeling, and on the vacuum shell it reduces to "
      "-2c r² f² phi0'^2·dphi",
      dsimp(self_coupling + 2 * c_s * r**2 * F**2
            * (E0 + phi0p**2) * p) == 0 and self_coupling != 0)
print(f"      self-coupling difference = {sp.factor(self_coupling)}")

print("""
  W3 GRADE (the decisive question, honest): outcome (d) — SOMETHING
  ELSE, precisely characterized.  The native H1 equation EXISTS (so not
  (c), except on locally-flat slices phi0' = 0) and welds the same pair
  (H1 <-> d_t dphi) as the Einstein constraint, but it is ALGEBRAIC —
      f phi0'·H1 = 2 d_t(dphi),   i.e.   H1 = -4 d_t(dphi)/f',
  with NO d_r(H1) and NO K — not the Einstein differential weld with
  altered coefficients (so not (b), and certainly not (a)).  Verified
  inequivalent by witness.  The Einstein weld d_r(e^{-2phi0}H1) =
  2 d_t dphi + d_t K is therefore NOT implied by the C1 dynamics: at
  matter scope it is an IMPORT.  The native system's own structure:
  H1 auxiliary, K variationally ill-defined (the theta-theta refusal
  biting at perturbed level), and the on-shell breathing sector
  ELLIPTIC in time — a genuinely different dynamical regime from the
  imported-weld macro sector.""")

# ===========================================================================
# W4 — the Bianchi/conservation route
# ===========================================================================
hr("W4 — BIANCHI/CONSERVATION ROUTE: DOES div G = 0 + C1 CONSERVATION "
   "IMPLY THE WELD?")


def div_mixed(A: sp.Matrix, nu: int) -> sp.Expr:
    return trunc(
        sum(sp.diff(A[mu, nu], coords[mu]) for mu in range(N4))
        + sum(Gam[mu][mu][la] * A[la, nu]
              for mu in range(N4) for la in range(N4))
        - sum(Gam[la][mu][nu] * A[mu, la]
              for mu in range(N4) for la in range(N4)))


divG_th = div_mixed(Gmix, 2)
check("contracted Bianchi identity, theta-component: div G_theta = 0 at "
      "order eps^0 AND order eps^1 on the full perturbed UDT "
      "configuration (identity verified, machinery validated)",
      dsimp(divG_th.coeff(eps, 0)) == 0
      and dsimp(divG_th.coeff(eps, 1)) == 0)

divT_r = div_mixed(Tmix, 1)
divT_r0 = dsimp(divT_r.coeff(eps, 0))
check("background r-component: (div T)_r = c f² phi0'(E0 - phi0'^2) "
      "exactly — equals the gr-balance identity (c/4)f'(f'' + 2f'/r) + "
      "(c/8)f'^3/f in f-language; on the vacuum shell (E0 = 0) the "
      "leftover -c f² phi0'^3 = (c/8) f'^3/f =/= 0 stands: the C1 "
      "stress is NOT conserved on its own vacuum (banked result, "
      "re-derived from scratch)",
      dsimp(divT_r0 - c_s * F**2 * phi0p * (E0 - phi0p**2)) == 0
      and sp.simplify(
          divT_r0.subs(phi0, -sp.log(fgen) / 2).doit()
          - (c_s / 4 * sp.diff(fgen, r)
             * (sp.diff(fgen, r, 2) + 2 * sp.diff(fgen, r) / r)
             + c_s / 8 * sp.diff(fgen, r)**3 / fgen)) == 0)

divT_th = div_mixed(Tmix, 2)
divT_th1 = dsimp(divT_th.coeff(eps, 1))
check("first-order theta-component: (div T)_theta = c f² (E0 - "
      "phi0'^2)·dphi·d_th Y exactly — INDEPENDENT of H1 and K: no "
      "choice of H1 (native weld, Einstein weld, anything) changes it",
      dsimp(divT_th1 - c_s * F**2 * (E0 - phi0p**2) * p
            * sp.diff(Y, th)) == 0
      and not divT_th1.has(h) and not divT_th1.has(k))
check("(div T)_theta = (div T)_r[background density] promoted by "
      "dphi·d_th Y / phi0': the background non-conservation density "
      "(E0 - phi0'^2) is EXACTLY what leaks into the perturbative "
      "(t,theta) budget",
      dsimp(divT_th1 * phi0p - divT_r0 * p * sp.diff(Y, th)) == 0)
check("on the vacuum background (E0 = 0): (div T)_theta = "
      "-c f² phi0'^2 · dphi · d_th Y =/= 0 for ANY nontrivial breathing "
      "(it vanishes only at dphi = 0 or phi0' = 0)",
      dsimp(divT_th1.subs(sp.diff(phi0, r, 2),
                          2 * phi0p**2 - 2 * phi0p / r)
            + c_s * F**2 * phi0p**2 * p * sp.diff(Y, th)) == 0)
# the E-budget: with E := G - 8 pi G_N T, div E_theta = -8 pi G_N div T_theta
Emix = (Gmix - 8 * sp.pi * GN * Tmix).applyfunc(trunc)
divE_th = div_mixed(Emix, 2)
check("Einstein-budget bookkeeping: div(G - 8 pi G_N T)_theta = "
      "-8 pi G_N (div T)_theta at first order (Bianchi kills the G "
      "side) — so imposing the FULL theta-row of Einstein equations "
      "(E^mu_theta = 0 for all mu, all theta-row components) would "
      "force (div T)_theta = 0, i.e. dphi = 0 on the vacuum cell: the "
      "Einstein theta-row is INCONSISTENT with any breathing mode on "
      "the UDT background",
      dsimp(divE_th.coeff(eps, 1)
            + 8 * sp.pi * GN * divT_th1) == 0)

print("""
  W4 VERDICT (exact): the Bianchi/conservation route does NOT imply the
  weld — in either direction:
  (i)  div G = 0 is an identity (verified at both orders): by itself it
       relates dG^t_theta to dG^r_theta and the angular components; it
       implies the (t,theta) constraint only if the OTHER Einstein
       equations are imposed — and the repo has PROVEN UDT does not
       impose the theta-theta one (Einstein tension Delta > 0).
  (ii) the C1 stress is not conserved: the banked background leftover
       (c/8)f'^3/f (re-derived) is promoted at first order to the
       (t,theta) budget as (div T)_theta = c f²(E0 - phi0'^2)·dphi·
       d_th Y =/= 0 — independent of H1 — so the full Einstein
       theta-row would force dphi = 0.  The non-conservation does not
       merely fail to derive the weld; it makes the surrounding
       Einstein system inconsistent with breathing, leaving the single
       (t,theta) component as a freestanding IMPORT wherever it is used.
""")

# ===========================================================================
# W5 — verdict and the final matter-side weld system
# ===========================================================================
hr("W5 — VERDICT + THE FINAL MATTER-SIDE WELD SYSTEM")

print("""  NATIVE STATUS OF THE RUNG-2 WELD — the honest verdict:

  1. The Einstein differential weld d_r(e^{-2phi0}H1) = 2 d_t dphi +
     d_t K - 16 pi G e^{-2phi0} dT^t_th is CONFIRMED at identity level
     on general f (W2: it is exactly what dG^t_theta = 8 pi G dT^t_th
     says; AUDIT.md S116 validated on arbitrary profiles, K-coefficient
     +1).  But it is NOT native:
       - not from the C1 dynamics (W3, grade (d): the C1 system's own
         H1 equation is the ALGEBRAIC weld f phi0'H1 = 2 d_t dphi);
       - not from Bianchi/conservation (W4: identity needs the
         theta-row, which UDT provably rejects and which is
         inconsistent with breathing).
     At MATTER scope the Einstein weld is an IMPORT (guardrail item:
     'Einstein equations as source equations — not imported') — and it
     is EQUALLY an import STRUCTURALLY at MACRO scope: the non-C1
     macro content (recycling radiation sector, dT^t_th =/= 0) changes
     the SOURCE TERM of the constraint, not its pedigree, and macro
     total-conservation self-consistency is unverified.  The macro
     empirical support is CHANNEL-SPECIFIC: phase/interleaving/TE
     PASSED; the EE amplitude is the standing ~2x overshoot.  And the
     validated phase signature (H1 in quadrature with dphi) follows
     from H1 ~ d_t(dphi) in TIME structure, which BOTH welds supply —
     the macro phase channel may not discriminate them.  PHASE-2
     DISCRIMINATOR (named): rerun the macro projection with the native
     algebraic weld H1 = -4 d_t(dphi)/f' and compare the RADIAL
     structure against the CMB record.  The macro/micro relation is
     now sharp and recorded: macro uses the Einstein weld with sources,
     empirically supported channel-by-channel; the native cell supplies
     a DIFFERENT, algebraic weld with the same time structure.

  2. The phi-angular dynamical coupling itself (canon C-3's surviving
     hunch-home) DOES exist natively: H1 is welded to d_t dphi by the
     C1 action's own constraint — just not by the Einstein operator.
     STRUCTURALLY (verifier identification): the native weld is
     EL_H1 = -r²·dT_tr = 0 — first-order vanishing radial energy flux,
     the matter-only remnant of GR's (t,r) slot.  In GR, H1-variation
     yields the (t,r) equation, never the (t,theta) weld, which only
     arrives via Bianchi plus the rest of the Einstein system — and W4
     closes that route off natively.  Grade (d) was forced.

  FINAL MATTER-SIDE WELD SYSTEM (native variation rule; canon slice
  K = 0 [W1 strict reading + W3 obstruction]; general static cell
  background f = e^{-2phi0(r)}, E0 := phi0'' + 2phi0'/r - 2phi0'^2 the
  background C1 EL density [= 0 in vacuum, = source in a sourced cell];
  domain r in [0, R_cell], phi0(R_cell) = 0 at the mirror interface per
  canon C-2, core endpoint phi0 -> -infinity]:

    READING A — H1 variational (the dispatch-directed native rule):
      (A1)  f phi0'·H1 = 2 d_t(dphi)            [native ALGEBRAIC weld]
            <=>  f'·H1 = -4 d_t(dphi)
      (A2)  + r² d_t²(dphi) + d_r(r² f² d_r dphi)
            - 4 r² f² E0·dphi - lam f·dphi = 0   [on-shell, ELLIPTIC]
      Normal modes dphi = u(r)e^{-i omega t}:
            (r²f²u')' = (lam f + 4r²f²E0 + omega² r²)·u
      — positive-definite form => no real-omega modes under boundary
      conditions with vanishing boundary term WHENEVER pointwise
      lam f + 4r²f²E0 >= 0 (in particular E0 >= 0: every vacuum
      background); omega² < 0 (relaxation/instability spectrum) there.
      On SOURCED collars with E0 < 0 the oscillation window OPENS
      (W3(e'): real mode omega² = +7.53 on the witness collar).
      Phase-2 questions: whether the PHYSICAL sourced cell (banked
      eta = 1/18, ell = 1 source) sits inside the window; boundary
      conditions at the phi = 0 interface (mirror) and the core
      endpoint; and whether the macro boundary pumps this sector.

    READING B — H1 excluded (strict diagonal P0 reading):
      (B1)  - r² d_t²(dphi) + d_r(r² f² d_r dphi)
            - 4 r² f² E0·dphi - lam f·dphi = 0   [HYPERBOLIC breathing]
      with characteristic speed dr/dt = f (the macro carrier's light
      cones) and SL weight r²f² (the C1 e^{-2phi} weight makes it
      differ from the minimally-coupled operator).

    READING C — H1 external + Einstein weld imposed (the macro import,
      recorded for completeness at matter scope):
      (C1)  d_r(e^{-2phi0} H1) = 2 d_t(dphi)     [+ d_t K if K kept;
            source-free since dT^t_theta[C1] = 0]
      with (B1) as the dphi equation.  This is the S116 structure
      transplanted; it is NOT selected by anything native (W3/W4).

  The choice among A/B/C is the H1-field-status question — the sharp,
  named residue of this dispatch.  A is what the banked C1 action plus
  the honest variation rule says; its elliptic character forbids native
  real-frequency breathing on VACUUM (E0 >= 0) cells — either a deep
  feature (vacuum-cell modes are NOT free oscillations — consistent
  with the repo's no-native-discreteness record to date) or evidence
  that the C1 action is incomplete at perturbed level (the rho-dynamics
  direction) — while on SOURCED collars the E0 < 0 window (W3(e')) is
  the candidate home of native oscillation modes: source-enabled,
  weld-coupled, finite-cell.  Phase 2 (spectra) must run on Reading A
  first, on the banked sourced backgrounds.

  GRADES (repo convention):
    W1 K-verdict:        K = 0 FORCED on the strict perturbed-level
                         canon (ell >= 2); not pure gauge; W3
                         independently disqualifies K as a native
                         variational field.  System: (dphi, H1).
    W2:                  AUDIT S116 weld operator CONFIRMED at general
                         f (identity level), K-coefficient +1, ell-flat,
                         matter-scope source = 0.
    W3 (decisive):       grade (d) — native ALGEBRAIC weld
                         f phi0'H1 = 2 d_t dphi = vanishing radial
                         energy flux (EL_H1 = -r²·dT_tr); Einstein weld
                         NOT implied; (c) only on phi0' = 0 slices;
                         no-real-omega proven for E0 >= 0 only, real
                         mode exhibited at E0 < 0 (omega² = +7.53).
    W4:                  Bianchi route: NO implication; Einstein
                         theta-row inconsistent with breathing
                         (non-conservation leak computed exactly).
    Weld native status:  EINSTEIN IMPORT structurally at BOTH scopes;
                         macro empirical support CHANNEL-SPECIFIC
                         (phase/interleaving/TE pass; EE ~2x overshoot
                         standing; phase channel may not discriminate
                         the welds); native counterpart exists and
                         differs.""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
hr("SUMMARY")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print("""  All symbolic/exact checks PASSED.

  W1  Ties: H0 = -2 dphi, H2 = +2 dphi; g_tt g_rr = -1 automatic at all
      orders.  K: not pure gauge (ell >= 2); strict perturbed-level
      canon C-1 forces K = 0; areal re-chart price = g_{r th} =/= 0.
  W2  dG^t_theta = e^{2phi0}[-(1/2)d_r(e^{-2phi0}H1) + d_t dphi +
      (1/2)d_t K]·d_th Y at GENERAL f — AUDIT S116 confirmed; ell-flat;
      dT^t_theta[C1] = 0 (matter-scope weld would be source-free).
  W3  Grade (d): the native H1 equation is the ALGEBRAIC weld
      f phi0'·H1 = 2 d_t dphi (<=> f'H1 = -4 d_t dphi), identically
      EL_H1 = -r²·dT_tr — first-order VANISHING RADIAL ENERGY FLUX
      (verifier identification); no native d_r H1, no native K equation
      (parametrization-obstructed by the banked theta-theta refusal);
      H1 elimination flips the dphi time-kinetic sign: the on-shell
      native sector is ELLIPTIC.  No real-omega modes PROVEN FOR
      E0 >= 0 (all vacuum backgrounds); on sourced collars with E0 < 0
      the oscillation window OPENS — counterexample reproduced
      (omega² = +7.53 real mode; vacuum control -12.6).  Einstein weld
      != native weld (witness-verified).
  W4  Bianchi implies nothing here: div G = 0 verified (identity);
      (div T)_theta^(1) = c f²(E0 - phi0'^2)·dphi·d_th Y =/= 0
      (H1-independent; the banked non-conservation leak, promoted) —
      the Einstein theta-row would force dphi = 0.
  W5  Verdict: the rung-2 weld is an EINSTEIN IMPORT structurally at
      BOTH scopes (macro support empirical and channel-specific; the
      phase channel may not discriminate the welds — phase-2
      discriminator: native-weld macro projection vs the CMB record);
      the native matter-side system is (dphi, H1) with the algebraic
      weld + an elliptic on-shell breathing equation (Reading A),
      recorded alongside Readings B/C.  Spectra on the banked sourced
      backgrounds = phase 2, highest leverage.""")
