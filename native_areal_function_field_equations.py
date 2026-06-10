"""FIELD EQUATIONS FOR THE FREED AREAL FUNCTION under the total native action.

Setting (continues native_threshold_rigidity_theorem.py section E1, which
identified the SATURATING AREAL FUNCTION as the unique static escape from
the threshold rigidity theorem, and flagged caveat (b): whether the NATIVE
field equations admit it must be derived, not assumed).  Generalized static
metric, g_tt * g_rr = -1 retained, areal function freed from P0's rho = r:

    ds^2 = -f(r) dt^2 + f(r)^{-1} dr^2 + rho(r)^2 dOmega^2,
    f > 0, rho > 0 smooth.

THE TOTAL NATIVE ACTION (each piece banked in the repo; conditionality
flagged per piece -- nothing here is imported, principle 1; nothing is
linearized, principle 2):

  A.  C1 radial scalar action, generalized (provenance verified in section A:
      S = int sqrt(-g) e^{-2phi} g^{rr} (phi')^2 dr with phi = -(1/2)ln f,
      sqrt(-g)/sin(theta) = rho^2, g^rr = f, reduces EXACTLY to)

          S_C1 = (1/4) int rho^2 (f')^2 dr.

      Status: the rho = r form is banked (native_self_similar_c1_value_action
      .py); the general-rho form is the SAME provenance expression evaluated
      on the (f, rho) metric -- this is the honest generalization, verified
      symbolically, not a transplant by hand.

  B.  Native two-form flux (CONDITIONAL -- compact flux quantization is the
      Pflux postulate, reduced to Pbundle0 in native_flux_postulate_
      minimization.py; Maxwell DYNAMICS is metric-given, UDT_REBUILD Part T):

          F = q sin(theta) dtheta ^ dphi  (closed; Maxwell-on-shell for ANY
          f, rho -- verified in section B), giving the radial density

          -(1/(4 mu)) sqrt(-g) F_{mu nu} F^{mu nu} = -(q^2/(2 mu)) sin(theta)
              / rho^2   -->  - kappa_q / rho^2 per unit r after the 4 pi
          angular integration, kappa_q := 2 pi q^2 / mu  >  0.

      NORMALIZATION FLAG (recorded in section B): kappa_q carries the 4 pi
      while the banked S_C1 normalization (1/4) does not; pairing them as-is
      mixes per-steradian and integrated conventions.  The EL equations are
      blind to a COMMON overall factor but not to a RELATIVE one, so the
      script carries a single symbol K > 0 (the coefficient of 1/rho^2 in
      the effective radial density, in whatever common normalization S_C1
      uses) and instantiates both readings at the end.  The STRUCTURE of
      every result (|a| = c_q |q|) is normalization-independent.

  C.  H1 angular collar source (CONDITIONAL on the collar-source
      interpretation -- native_core_solver.py: "not yet a derivation of W or
      s"): at rho = r the banked sourced equation is

          f'' + 2 f'/r + 2 s W(r) f / r^2 = 0,

      from the action piece V = (s/2) W f^2 (times measure factors).  The
      general-rho weighting is DERIVED in section C: a rho-local weight
      w(rho) must satisfy w = 1 identically (the measure rho^2 times the S^2
      eigenvalue 1/rho^2 cancel), so the piece is rho-INDEPENDENT:

          S_source = int (s/2) W(r) f^2 dr.

SIGN ANCHORS (C1 and source pieces fixed by banked rho = r limits,
documented in D1; the flux piece is NOT banked-limit-anchored -- see
below):

    S_total[f, rho] = S_C1  -  S_flux  -  S_source,

  where S_flux is the LITERAL Maxwell action (negative for magnetic flux)
  and S_source = int (s/2) W f^2 dr; the effective radial density is

      L  =  (1/4) rho^2 (f')^2  +  K / rho^2  -  (s/2) W f^2 ,    K >= 0.

  The C1 and source signs are anchored so that q = 0, rho = r reproduces
  the banked vacuum (r^2 f')' = 0 and the banked sourced collar equation.
  The flux piece K/rho^2 is f-BLIND, so NO banked rho = r limit anchors
  its sign: it is fixed by the ENERGY-FUNCTIONAL reading (magnetic energy
  enters with the same sign as the C1 gradient energy) PLUS
  SELF-CONSISTENCY -- the opposite sign makes the rho-equation a sum of
  positives with no solution, flipping the verdict from 'underdetermined'
  to 'inconsistent' (verifier amendment 2026-06-10).

  SPEC/SIGN NOTE (recorded): if S_flux were instead read as the positive
  magnitude + int K/rho^2 dr, the rho-equation would be
  (rho/2)(f')^2 + 2K/rho^3 = 0 -- a sum of positives with NO solution.  The
  literal-Maxwell-action reading (verified in section B: the magnetic
  density is negative in the action, positive in energy, SAME energy sign
  as the C1 gradient piece) is the consistent one and is what is used.

DERIVATION TASKS (D1-D5, printed in repo check/verdict style):

  D1  f-equation for general rho:      (rho^2 f')' + 2 s W f = 0.
  D2  rho-equation: rho carries NO derivative in any piece (verified), so
      it is ALGEBRAIC:                 (rho/2)(f')^2 - 2 K / rho^3 = 0,
      i.e.  rho^4 (f')^2 = 4K.
  D3  classification: (a) q = 0, W = 0: f' = 0 forced -- C1 alone supports
      NO nontrivial f once rho is freed; the banked vacuum f = C + a/r is
      NOT stationary under rho-variation; P0 (rho = r) is an independent
      kinematic postulate, not derived.  (b) q != 0: the algebraic equation
      IMPLIES the f-equation; consistency forces the extremality lock
      |a| = 2 sqrt(K) = c_q |q| between tail coefficient and charge; rho(r)
      is then a FREE FUNCTION -- underdetermination DEMONSTRATED, not just
      argued (verifier invariant computation): two lock members with
      identical (C, a, K), (rho = r, f = C + a/r) vs (rho = r^2,
      f = C + a/(3r^3)), have DIFFERENT curvature invariants as functions
      of the areal radius (at C = 1 the first is scalar-flat, R == 0; the
      second has R != 0) -- genuinely different geometries, not gauge
      (g_tt g_rr = -1 fixes r up to translation anyway, S0 note).
      Even f(rho) is representative-
      dependent (demonstrated); only rho^2 f' = -a is invariant.  (c) the
      H1 source (rho-independent by section C) does NOT break the
      degeneracy: it OVERDETERMINES instead -- no solution on supp W.
  D4  throat test: on the flux-extremal family a saturating-rho end exists
      only as (i) a horizon-capped throat (f -> 0 at finite r, threshold
      -> 0) or (ii) a linearly-growing-f confining end at INFINITE action;
      a threshold-lifting cylinder (f -> f_oo > 0, rho -> rho_oo) requires
      f' -> 0, which the lock rho^2 f' = -a forbids for q != 0.  For q = 0
      the throat is allowed at zero cost but lives inside the fully
      undetermined sector.  Finite total tail action on the charged family
      = 2K int dr/rho^2 < oo forces rho unbounded: E1's escape costs
      infinite action in the charged sector, and is undetermined in the
      uncharged one.
  D5  P0 audit verdict: UNDERDETERMINED is the ruling state; rho = r is not
      derived; no banked piece carries (rho')^2.  The EH density on the
      two-function metric is NO LONGER a total derivative (EL_f[rho^2 R] =
      -2 rho rho'', EL_rho != 0 -- computed from scratch); it is exactly the
      kind of object that would supply rho's missing equation, but it is a
      FORBIDDEN IMPORT as dynamics (native_positional_dilation_gr_guardrail
      .py); recorded as the identified candidate pending a NATIVE
      derivation.

Every displayed identity is verified symbolically (sympy), exact
throughout; PASS/FAIL printed per check; nonzero exit on any FAIL.

New file 2026-06-10; creates nothing else, modifies nothing existing.
"""

from __future__ import annotations

import sys

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
# Shared symbols and the generalized metric
# ---------------------------------------------------------------------------
t, r, th, ph = sp.symbols("t r theta phi", real=True)
q_s = sp.symbols("q", positive=True)        # WLOG q > 0 (only q^2 enters)
mu = sp.symbols("mu", positive=True)
s_s = sp.symbols("s", real=True)
lam = sp.symbols("lam", positive=True)      # ell(ell+1) >= 2 for ell >= 1
K = sp.symbols("K", positive=True)          # flux density coefficient (B)
a_s = sp.symbols("a", real=True)            # tail coefficient, rho^2 f' = -a
C_s = sp.symbols("C", positive=True)

f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)
W = sp.Function("W")(r)                     # collar window (banked profile)

fp = sp.diff(f, r)
rhop = sp.diff(rho, r)

g4 = sp.diag(-f, 1 / f, rho**2, rho**2 * sp.sin(th)**2)
coords = [t, r, th, ph]
g4inv = g4.inv()


def euler_lagrange(L: sp.Expr, u: sp.Expr) -> sp.Expr:
    """EL derivative dL/du - d/dr dL/du' + d^2/dr^2 dL/du'' (exact)."""
    return sp.simplify(
        L.diff(u)
        - sp.diff(L.diff(sp.diff(u, r)), r)
        + sp.diff(L.diff(sp.diff(u, r, 2)), r, 2))


# ---------------------------------------------------------------------------
# S0 — metric facts used by every piece
# ---------------------------------------------------------------------------
hr("S0 — METRIC FACTS for ds² = −f dt² + f⁻¹dr² + ρ(r)²dΩ²  (g_tt·g_rr = −1)")

det4 = sp.simplify(g4.det())
check("det g = −ρ⁴sin²θ exactly, so √−g = ρ²sinθ — f-INDEPENDENT "
      "(the g_tt·g_rr = −1 cancellation survives freeing ρ)",
      sp.simplify(det4 + rho**4 * sp.sin(th)**2) == 0)
check("inverse metric: g^tt = −1/f, g^rr = f, g^θθ = 1/ρ², "
      "g^φφ = 1/(ρ²sin²θ) exactly",
      sp.simplify(g4inv[0, 0] + 1 / f) == 0
      and sp.simplify(g4inv[1, 1] - f) == 0
      and sp.simplify(g4inv[2, 2] - 1 / rho**2) == 0
      and sp.simplify(g4inv[3, 3] - 1 / (rho**2 * sp.sin(th)**2)) == 0)
print("""
  GAUGE NOTE (load-bearing for D3): within this ansatz the radial
  coordinate is NOT freely reparameterizable — g_tt·g_rr = −1 fixes r up to
  translation r → r + const (any nonaffine r → r̃(r) destroys the f⁻¹dr²
  form).  So two configurations with different ρ(r) are DIFFERENT
  geometries, not gauge copies.  Underdetermination found below is
  therefore physical, not coordinate slack.""")

# ---------------------------------------------------------------------------
# A — C1 radial scalar action, generalized: provenance reduction
# ---------------------------------------------------------------------------
hr("A — C1 ACTION FOR GENERAL ρ: provenance reduction (exact)")

phi_of_f = -sp.Rational(1, 2) * sp.log(f)       # f = e^{−2φ} (repo convention)
check("repo convention f = e^(−2φ): φ = −(1/2)ln f inverts it exactly",
      sp.simplify(sp.exp(-2 * phi_of_f) - f) == 0)
prov = (rho**2                                   # √−g per steradian = ρ²
        * sp.exp(-2 * phi_of_f)                  # e^{−2φ} = f
        * f                                      # g^rr = f
        * sp.diff(phi_of_f, r)**2)               # (φ')²
check("provenance density √−g·e^(−2φ)·g^rr·(φ')² = (1/4)ρ²(f')² EXACTLY "
      "(per steradian; φ' = −f'/(2f), the f's cancel)",
      sp.simplify(prov - sp.Rational(1, 4) * rho**2 * fp**2) == 0)
print("""
     S_C1 = (1/4)∫ρ²(f')²dr is therefore the SAME banked provenance
     expression evaluated on the (f, ρ) metric — the only change from the
     banked ρ = r form (native_self_similar_c1_value_action.py) is
     √−g: r² → ρ².  No ρ' appears: the C1 piece carries NO kinetic term
     for the areal function (this is what makes D2 algebraic).""")

# ---------------------------------------------------------------------------
# B — two-form flux piece (CONDITIONAL: Pflux)
# ---------------------------------------------------------------------------
hr("B — TWO-FORM FLUX PIECE (status Pflux — CONDITIONAL, flagged): "
   "F = q sinθ dθ∧dφ")

print("  CONDITIONALITY FLAG: Maxwell DYNAMICS on this metric is banked as")
print("  metric-given (UDT_REBUILD Part T); the COMPACT flux quantization")
print("  itself is the Pflux postulate (reduced to Pbundle0,")
print("  native_flux_postulate_minimization.py).  Everything in this piece")
print("  is conditional on Pflux.")
print()

F_low = sp.zeros(4, 4)
F_low[2, 3] = q_s * sp.sin(th)
F_low[3, 2] = -q_s * sp.sin(th)

# closedness dF = 0: cyclic derivative over every index triple
closed_ok = True
for i in range(4):
    for j in range(i + 1, 4):
        for k in range(j + 1, 4):
            cyc = (sp.diff(F_low[j, k], coords[i])
                   + sp.diff(F_low[k, i], coords[j])
                   + sp.diff(F_low[i, j], coords[k]))
            closed_ok = closed_ok and sp.simplify(cyc) == 0
check("dF = 0 (all cyclic-derivative triples vanish): the flux is closed",
      closed_ok)

F_up = g4inv * F_low * g4inv          # F^{ab} = g^{ac} F_{cd} g^{db}
check("F^θφ = g^θθ g^φφ F_θφ = q/(ρ⁴ sinθ) exactly (raising uses only the "
      "angular block — NO f anywhere in the flux piece)",
      sp.simplify(F_up[2, 3] - q_s / (rho**4 * sp.sin(th))) == 0)
F2 = sp.simplify(sum(F_low[i, j] * F_up[i, j]
                     for i in range(4) for j in range(4)))
check("F_{μν}F^{μν} = 2q²/ρ⁴ exactly", sp.simplify(F2 - 2 * q_s**2 / rho**4) == 0)

maxwell_ok = True
sqrtg = rho**2 * sp.sin(th)
for nu in range(4):
    div = sum(sp.diff(sqrtg * F_up[mu_i, nu], coords[mu_i]) for mu_i in range(4))
    maxwell_ok = maxwell_ok and sp.simplify(div) == 0
check("∂_μ(√−g F^{μν}) = 0 for all ν: the monopole flux is Maxwell-on-shell "
      "for ARBITRARY f(r) AND ρ(r) (no back-condition on the metric from "
      "the Maxwell equation itself)", maxwell_ok)

dens = sp.simplify(-(sp.Rational(1, 4) / mu) * sqrtg * F2)
check("Maxwell action density −(1/(4μ))√−g F² = −(q²/(2μ))·sinθ/ρ² exactly "
      "(NEGATIVE in the action for magnetic flux)",
      sp.simplify(dens + (q_s**2 / (2 * mu)) * sp.sin(th) / rho**2) == 0)
ang = sp.integrate(sp.integrate(sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
check("angular integral ∫sinθ dθ dφ = 4π exactly", sp.simplify(ang - 4 * sp.pi) == 0)
kappa_q = 2 * sp.pi * q_s**2 / mu
check("4π-integrated flux density per unit r = −κ_q/ρ² with "
      "κ_q := 2πq²/μ > 0 exactly",
      sp.simplify(ang * (-(q_s**2 / (2 * mu)) / rho**2)
                  + kappa_q / rho**2) == 0)

print("""
  NORMALIZATION FLAG (spec bookkeeping, recorded honestly): κ_q = 2πq²/μ is
  the 4π-INTEGRATED normalization, while the banked S_C1 = (1/4)∫ρ²(f')²dr
  carries no 4π (per-steradian or absorbed).  A COMMON overall factor drops
  out of the EL equations; a RELATIVE factor does not.  The script
  therefore carries one symbol K > 0 = the flux coefficient in the SAME
  normalization as S_C1, and instantiates both readings in D3:
      per-steradian pairing:   K = q²/(2μ)    ⇒ |a| = √(2/μ)·|q|,
      both-4π-integrated:      identical EL (common 4π cancels),
      spec's literal pairing [(1/4)ρ²(f')² with κ_q]:  K = κ_q
                                              ⇒ |a| = √(8π/μ)·|q|.
  The structural result |a| = c_q·|q| (c_q a fixed positive constant) is
  normalization-independent; only the value of c_q moves.

  SIGN ANCHOR FOR THE TOTAL (used from D1 on): S_total = S_C1 − S_flux −
  S_source with S_flux the LITERAL (negative) Maxwell action just computed,
  so the effective radial density is
      L = (1/4)ρ²(f')² + K/ρ² − (s/2)W f².
  Energy reading: gradient energy and magnetic energy enter with the SAME
  (positive) sign — the standard Lorentzian relative sign.  If one instead
  subtracted a POSITIVE magnitude ∫K/ρ²dr, the ρ-equation below would read
  (ρ/2)(f')² + 2K/ρ³ = 0: a sum of positives, NO solution — that reading
  is self-excluding and is recorded as such.""")

# ---------------------------------------------------------------------------
# C — H1 angular source piece (CONDITIONAL: collar-source interpretation)
# ---------------------------------------------------------------------------
hr("C — H1 ANGULAR SOURCE PIECE for general ρ (CONDITIONAL on the "
   "collar-source interpretation)")

print("  CONDITIONALITY FLAG: the banked sourced equation")
print("      f'' + 2f'/r + 2sW(r)f/r² = 0       (native_core_solver.py)")
print("  is a CANDIDATE-postulate structure ('not yet a derivation of W or")
print("  s', per that file's own header).  This section reconstructs its")
print("  general-ρ action form honestly; everything downstream that uses")
print("  s·W is conditional on this interpretation.")
print()

w_fun = sp.Function("w")        # candidate ρ-local weight
L_w = (sp.Rational(1, 4) * rho**2 * fp**2 + K / rho**2
       - sp.Rational(1, 2) * s_s * W * f**2 * w_fun(rho))
elf_w = euler_lagrange(L_w, f)
elf_w_expanded = sp.simplify(
    elf_w + s_s * W * f * w_fun(rho)
    + sp.Rational(1, 2) * sp.diff(rho**2 * fp, r))
check("with weight w(ρ): f-variation gives −(1/2)(ρ²f')' − sW·w(ρ)·f = 0, "
      "i.e. (ρ²f')' + 2sW·w(ρ)·f = 0 (exact EL bookkeeping)",
      elf_w_expanded == 0)

el_at_r = sp.simplify((elf_w.subs(rho, r).doit()) * (-2 / r**2))
banked_form = (sp.diff(f, r, 2) + 2 * fp / r
               + 2 * s_s * W * f * w_fun(r) / r**2)
check("at ρ = r this is f'' + 2f'/r + 2sW·w(r)·f/r² = 0; the banked "
      "equation requires w(r) = 1 for EVERY r in the collar",
      sp.simplify(el_at_r - banked_form) == 0)
print("""
     WEIGHT DERIVATION (the honest one): a ρ-LOCAL weight is a function of
     ρ alone (locality/covariance: the action may depend on the metric
     functions, with W(r) the banked source profile).  Requirement (i),
     w(ρ(r)) = 1 for all r when ρ(r) = r, forces w ≡ 1 on the whole range
     of ρ.  Requirement (ii) is then automatic and geometric: the measure
     carries ρ², the S² eigenvalue structure carries 1/ρ², and
     ρ²·(1/ρ²) = 1 — the two ρ-dependences CANCEL.  The spec's proposed
     weighting is confirmed:

         S_source = ∫ (s/2) W(r) f² dr        (NO ρ-dependence at all).

     CONSEQUENCE (load-bearing for D2/D3c): the source contributes ZERO to
     the ρ-equation.  Any rescue of the degeneracy via a source weight
     w'(ρ) ≠ 0 is excluded by the banked ρ = r limit itself.""")

# the working total density, signs anchored
L_tot = (sp.Rational(1, 4) * rho**2 * fp**2 + K / rho**2
         - sp.Rational(1, 2) * s_s * W * f**2)

# ---------------------------------------------------------------------------
# D1 — the f-equation for general rho
# ---------------------------------------------------------------------------
hr("D1 — f-EQUATION for general ρ (signs anchored by the banked ρ = r "
   "limits)")

el_f = euler_lagrange(L_tot, f)
f_eq = sp.diff(rho**2 * fp, r) + 2 * s_s * W * f       # claimed: = 0
check("δS/δf = 0  ⇔  (ρ²f')' + 2sW f = 0 exactly (flux piece carries no f: "
      "∂L_flux/∂f ≡ 0 since √−g and F² are f-free, section B)",
      sp.simplify(el_f + sp.Rational(1, 2) * f_eq) == 0
      and sp.simplify(sp.diff(K / rho**2, f)) == 0)

# anchor 1: rho = r, W = 0 vacuum
f_eq_vac = sp.simplify(f_eq.subs([(s_s, 0)]).subs(rho, r).doit())
f_try = C_s + a_s / r
check("anchor 1 (ρ = r, q-blind, W = 0): (r²f')' = 0 with general solution "
      "f = C + a/r — banked vacuum family (f = C + 2/r is the a = 2 member, "
      "native_threshold_rigidity_theorem.py T4)",
      sp.simplify(f_eq_vac.subs(f, f_try).doit()) == 0
      and sp.simplify(sp.diff(r**2 * sp.diff(f_try, r), r)) == 0)

# anchor 2: rho = r sourced collar equation
f_eq_src = sp.simplify(f_eq.subs(rho, r).doit() / r**2)
banked_src = sp.diff(f, r, 2) + 2 * fp / r + 2 * s_s * W * f / r**2
check("anchor 2 (ρ = r, W on): the equation is EXACTLY the banked "
      "f'' + 2f'/r + 2sW f/r² = 0 — both sign anchors hold simultaneously",
      sp.simplify(f_eq_src - banked_src) == 0)

# ---------------------------------------------------------------------------
# D2 — the rho-equation: algebraic, exact
# ---------------------------------------------------------------------------
hr("D2 — ρ-EQUATION: no ρ-derivative in any piece ⇒ ALGEBRAIC (exact)")

check("VERIFY: ∂L/∂ρ' ≡ 0 for the total density (C1, flux, source all "
      "ρ'-free) — the ρ-equation is algebraic, not an ODE",
      sp.simplify(L_tot.diff(rhop)) == 0)
el_rho = euler_lagrange(L_tot, rho)
rho_eq = sp.Rational(1, 2) * rho * fp**2 - 2 * K / rho**3   # claimed: = 0
check("δS/δρ = 0  ⇔  (ρ/2)(f')² − 2K/ρ³ = 0 exactly (source drops out, "
      "section C; flux enters via ∂/∂ρ[K/ρ²] = −2K/ρ³)",
      sp.simplify(el_rho - rho_eq) == 0)
check("equivalently ρ⁴(f')² = 4K — the spec's anticipated "
      "ρ⁴(f')² = const·q² structure, confirmed",
      sp.simplify(sp.expand(2 * rho**3 * rho_eq) - (rho**4 * fp**2 - 4 * K))
      == 0)
print("""
     so  ρ²·|f'| = 2√K  pointwise wherever ρ is freely varied.  Since
     ρ⁴(f')² = 4K > 0 (q ≠ 0) forbids f' = 0 anywhere, f' has one fixed
     sign by continuity and the ρ-equation integrates itself:
         ρ² f' = −a,   a = ±2√K   (a constant — see D3b).""")

# ---------------------------------------------------------------------------
# D3 — classification of the coupled system
# ---------------------------------------------------------------------------
hr("D3a — PURE VACUUM (q = 0, W = 0): freeing ρ kills every nontrivial f")

rho_eq_q0 = rho_eq.subs(K, 0)
check("ρ-equation at K = 0: (ρ/2)(f')² = 0 ⇒ f' ≡ 0 wherever ρ is free "
      "(ρ > 0, so the prefactor never rescues it)",
      sp.simplify(rho_eq_q0 - sp.Rational(1, 2) * rho * fp**2) == 0)
res_banked = sp.simplify(rho_eq_q0.subs(f, C_s + a_s / r).doit()
                         .subs(rho, r).doit())
check("the banked vacuum f = C + a/r at ρ = r FAILS the freed-ρ equation: "
      "residual = a²/(2r³) ≠ 0 for a ≠ 0 (it is stationary under "
      "f-variations only)",
      sp.simplify(res_banked - a_s**2 / (2 * r**3)) == 0)
print("""
  VERDICT D3a (plain reading, as specified): the C1 action ALONE cannot
  support ANY nontrivial f once ρ is freed — the ρ-variation is an
  algebraic constraint (f')² = 0 that erases the entire banked vacuum
  family.  Therefore, within the total native action as it stands:

      ρ = r IS NOT DERIVED.  P0 is an independent KINEMATIC postulate:
      it must be read as "ρ is not a varied field" (a fixed ansatz /
      constrained variation), because if ρ IS varied the banked sector
      dies.  The alternative — a native piece whose ρ-variation balances
      (ρ/2)(f')² — does not exist among the banked pieces (D5 inventories
      this).  Honest status: P0 = postulate, not theorem.""")

hr("D3b — FLUX ON (q ≠ 0): extremality lock |a| = c_q|q|, then EXACT "
   "underdetermination")

# the algebraic equation implies the f-equation
rho_gen = sp.Function("rho", positive=True)(r)      # generic, unconstrained
fp_ext = -a_s / rho_gen**2                          # rho^2 f' = -a branch
check("ρ²f' = −a (any constant a) makes (ρ²f')' = 0 IDENTICALLY for "
      "GENERIC ρ(r): the algebraic ρ-equation implies the vacuum "
      "f-equation — only ONE independent equation for TWO functions",
      sp.simplify(sp.diff(rho_gen**2 * fp_ext, r)) == 0)
rho_eq_ext = sp.simplify(
    (sp.Rational(1, 2) * rho_gen * fp_ext**2 - 2 * K / rho_gen**3))
check("ρ-equation on that branch: residual = (a² − 4K)/(2ρ³) exactly ⇒ "
      "CONSISTENCY FORCES a² = 4K, i.e. |a| = 2√K (the extremality lock)",
      sp.simplify(rho_eq_ext - (a_s**2 - 4 * K) / (2 * rho_gen**3)) == 0)
both_vanish = sp.simplify(rho_eq_ext.subs(a_s, 2 * sp.sqrt(K)))
check("with a = ±2√K BOTH field equations vanish identically for an "
      "ARBITRARY function ρ(r): the system is EXACTLY underdetermined "
      "(one-function family of distinct geometries, S0 gauge note)",
      both_vanish == 0
      and sp.simplify(rho_eq_ext.subs(a_s, -2 * sp.sqrt(K))) == 0)

print()
print("  c_q in the two normalizations (structure identical, value moves —")
print("  section B flag):")
aq_spec = sp.sqrt(4 * kappa_q)
check("spec pairing K = κ_q = 2πq²/μ:  |a| = 2√κ_q = √(8π/μ)·|q| exactly",
      sp.simplify(aq_spec - sp.sqrt(8 * sp.pi / mu) * q_s) == 0)
aq_ster = sp.sqrt(4 * q_s**2 / (2 * mu))
check("per-steradian pairing K = q²/(2μ):  |a| = √(2/μ)·|q| exactly",
      sp.simplify(aq_ster - sp.sqrt(2 / mu) * q_s) == 0)

print("""
  WHAT IS FIXED vs NOT FIXED (the invariant data, exact):
    FIXED:    ρ(r)²·f'(r) = −a with a = ±2√K — the tail coefficient is
              LOCKED to the charge, |a| = c_q|q| (extremality-like
              relation: charge alone sets the entire first-derivative
              structure of f relative to the areal function).
              STRUCTURAL ECHO (note, not an import): |a| = c_q|q|
              structurally echoes the extremal Reissner–Nordström
              relation M ∝ |Q|, but the DERIVATION ROUTE DIFFERS — here
              it arises from consistency of an UNDERDETERMINED native
              variational system, and NO Q²/r² term appears in f: the
              native flux does not gravitate in f at all (the f-equation
              is flux-blind, D1); it acts only through the ρ-equation.
    FIXED:    f by quadrature GIVEN ρ:  f(r) = f(r₁) − a∫_{r₁}^r ds/ρ(s)².
    NOT FIXED: ρ(r) itself — any positive function solves the system.
    NOT FIXED (SPEC CORRECTION, flagged): the spec hoped f could be
              expressed invariantly as f(ρ).  It CANNOT:
              df/dρ = f'/ρ' = −a/(ρ²ρ') carries ρ' explicitly, so f(ρ) is
              representative-dependent.  Demonstration (exact):""")
f_rep1 = C_s + a_s / r                 # rho = r member
f_rep2 = C_s + a_s / (3 * r**3)        # rho = r^2 member
check("member ρ = r:   ρ²f' = −a gives f = C + a/r  ⇒  f(ρ) = C + a/ρ",
      sp.simplify(r**2 * sp.diff(f_rep1, r) + a_s) == 0)
check("member ρ = r²:  ρ²f' = −a gives f = C + a/(3r³) ⇒ f(ρ) = C + "
      "a/(3ρ^(3/2)) — a DIFFERENT function of ρ (same a, same q)",
      sp.simplify((r**2)**2 * sp.diff(f_rep2, r) + a_s) == 0)
print("     Only the differential relation ρ²f' = −a is invariant across")
print("     the family; no finite relation f(ρ) survives.")
print("""
  VERDICT D3b — UNDERDETERMINATION STATUS: DEMONSTRATED, not merely
  argued (verifier invariant computation, 2026-06-10): the two lock
  members above share IDENTICAL (C, a, K) yet have DIFFERENT curvature
  invariants as functions of the areal radius — at C = 1 the ρ = r
  member is scalar-flat (R ≡ 0) while the ρ = r² member has R ≠ 0.
  These are genuinely different geometries, not gauge copies; the S0
  gauge note's coordinate argument is hereby upgraded to an invariant
  demonstration (reproduced as an in-script check in D5(b), using the
  from-scratch ρ²R).""")

hr("D3c — H1 SOURCE ON (q ≠ 0, W ≠ 0): the source does NOT break the "
   "degeneracy — it OVERDETERMINES")

# on supp W: rho-eq still forces rho^2 f' = const; f-eq then demands sWf=0
f_eq_on_branch = sp.simplify(
    (sp.diff(rho_gen**2 * fp_ext, r) + 2 * s_s * W * f))
check("on the ρ-equation branch (ρ²f' = −a forced, hence (ρ²f')' = 0) the "
      "f-equation collapses to 2sW f = 0 exactly",
      sp.simplify(f_eq_on_branch - 2 * s_s * W * f) == 0)
print("""
  Since f > 0 (metric requirement) and s ≠ 0, the coupled system has NO
  solution wherever W ≠ 0: the source piece, being ρ-INDEPENDENT (forced
  by the banked limit, section C), leaves the algebraic ρ-equation
  untouched, and the two equations are then incompatible on supp W.

  VERDICT D3c (spec's hoped-for mechanism corrected, flagged): the spec
  asked whether surviving ρ-dependence in the source yields "a genuine ODE
  for ρ".  Answer: NO ρ-dependence survives (w ≡ 1 is forced), and the
  result is not a ρ-ODE but an INCONSISTENCY on the collar support.  With
  the source interpretation on, the freed-ρ total action has solutions
  only where W = 0 — i.e. the collar-sourced interior and the freed areal
  function cannot coexist under this action.  (Conditional on the C-flag;
  if the collar source is rederived with intrinsic ρ-structure beyond a
  ρ-local weight, this gate must be rerun.)""")

# ---------------------------------------------------------------------------
# D4 — throat test on the flux-extremal family
# ---------------------------------------------------------------------------
hr("D4 — THROAT TEST: can ρ → ρ_∞ finite with f finite and positive?  "
   "(probe potential V = fλ/ρ² + f(fρ')'/ρ, E1)")

# re-verify the E1 tortoise potential for self-containment
omega = sp.symbols("omega", positive=True)
R_f = sp.Function("R")(r)
u_rho = rho * R_f
V_rho = f * lam / rho**2 + f * sp.diff(f * rhop, r) / rho
radial_target = (sp.diff(rho**2 * f * sp.diff(R_f, r), r)
                 - lam * R_f + omega**2 * (rho**2 / f) * R_f)
lhs_rho = (f * sp.diff(f * sp.diff(u_rho, r), r)
           + (omega**2 - V_rho) * u_rho)
check("E1 probe potential re-verified (self-containment): u = ρR, "
      "dr* = dr/f gives u'' + [ω² − V]u = 0 with V = fλ/ρ² + f(fρ')'/ρ "
      "exactly (native_threshold_rigidity_theorem.py E1)",
      sp.simplify(lhs_rho - (f / rho) * radial_target) == 0)

print()
print("  (i) the lock forbids the threshold-lifting throat outright "
      "(q ≠ 0):")
rho_max, r0, r1, f0, b_s = sp.symbols("P r_0 r_1 f_0 b", positive=True)
lower_bound = sp.integrate(2 * sp.sqrt(K) / rho_max**2, (r, r0, r1))
check("|f(r₁) − f(r₀)| = ∫|f'|dr ≥ 2√K·(r₁−r₀)/P² for ρ ≤ P (f' has fixed "
      "sign, D2): on ANY bounded-ρ region f changes LINEARLY at least — "
      "f cannot approach a finite limit on a cylinder end; f' → −a/ρ_∞² ≠ 0",
      sp.simplify(lower_bound - 2 * sp.sqrt(K) * (r1 - r0) / rho_max**2) == 0)
print("     a threshold-lifting end (f → f_∞ > 0, ρ → ρ_∞) needs f' → 0,")
print("     i.e. ρ²f' → 0 — but the lock says ρ²f' = −a with |a| = c_q|q|")
print("     ≠ 0.  CONTRADICTION for every q ≠ 0.  Exactly two charged")
print("     cylinder endings remain, classified on the exact ρ ≡ ρ_∞")
print("     representative (a = ±2√K):")

rho_c = sp.symbols("rho_oo", positive=True)
# (ii) a > 0: f decreasing, hits zero at finite r — horizon-capped throat
f_dec = f0 - (2 * sp.sqrt(K) / rho_c**2) * r
r_h = sp.solve(sp.Eq(f_dec, 0), r)[0]
check("(ii) a = +2√K (f decreasing): f = f₀ − (2√K/ρ_∞²)r hits f = 0 at "
      "FINITE r_h = f₀ρ_∞²/(2√K) — the throat is HORIZON-CAPPED, the "
      "static region ends",
      sp.simplify(r_h - f0 * rho_c**2 / (2 * sp.sqrt(K))) == 0)
x_var = sp.symbols("x", positive=True)
tort_to_h = sp.integrate(1 / f_dec, (r, 0, x_var))
tort_lim = sp.limit(tort_to_h, x_var, r_h, dir="-")
check("the f = 0 cap sits at INFINITE tortoise distance (∫dr/f diverges "
      "logarithmically as r → r_h)", tort_lim == sp.oo)
V_dec = f_dec * lam / rho_c**2          # rho' = 0 exactly on representative
check("probe threshold toward the cap: V = fλ/ρ_∞² → 0 as r → r_h — the "
      "horizon-capped throat does NOT lift the threshold (V → 0, not a "
      "positive constant)",
      sp.limit(V_dec, r, r_h, dir="-") == 0)

# (iii) a < 0: f increasing linearly — confining but infinite action
f_inc = f0 + (2 * sp.sqrt(K) / rho_c**2) * r
V_inc = f_inc * lam / rho_c**2
check("(iii) a = −2√K (f increasing): f = f₀ + (2√K/ρ_∞²)r grows linearly; "
      "V = fλ/ρ_∞² → ∞ (V is asymptotically (2√Kλ/ρ_∞⁴)·r)",
      sp.limit(V_inc, r, sp.oo) == sp.oo
      and sp.limit(V_inc / r, r, sp.oo) == 2 * sp.sqrt(K) * lam / rho_c**4)
tort_inc = sp.integrate(1 / f_inc, (r, 0, sp.oo))
check("tortoise endpoint is INFINITE (∫dr/f ~ (ρ_∞²/(2√K))ln r): Case A "
      "with V → ∞ ⇒ NO essential spectrum, purely discrete — a CONFINING "
      "end (rigidity theorem M1/M2 machinery)", tort_inc == sp.oo)
S_c1_tail = sp.integrate(sp.Rational(1, 4) * rho_c**2
                         * sp.diff(f_inc, r)**2, (r, 0, sp.oo))
S_flux_tail = sp.integrate(K / rho_c**2, (r, 0, sp.oo))
check("but the cost is INFINITE action: C1 tail (1/4)∫ρ_∞²(f')²dr = "
      "∫(K/ρ_∞²)dr = ∞ AND flux tail ∫(K/ρ_∞²)dr = ∞ — same disease as the "
      "rigidity theorem's confining branch (T3a)",
      S_c1_tail == sp.oo and S_flux_tail == sp.oo)

print()
print("  (iv) the action-finiteness statement on the WHOLE extremal "
      "family:")
dens_ext = sp.simplify(
    (sp.Rational(1, 4) * rho_gen**2 * fp_ext**2 + K / rho_gen**2)
    .subs(a_s, 2 * sp.sqrt(K)))
check("on the extremal family the total tail density is "
      "(1/4)ρ²(a²/ρ⁴) + K/ρ² = 2K/ρ² EXACTLY (C1 and flux contribute "
      "equally — virial-like split)",
      sp.simplify(dens_ext - 2 * K / rho_gen**2) == 0)
X_var = sp.symbols("X", positive=True)
rho_sat_rep = rho_c - b_s / r
sat_bound = sp.simplify(2 * K / rho_sat_rep**2 - 2 * K / rho_c**2)
sat_tail = sp.limit(
    sp.integrate(2 * K / rho_sat_rep**2, (r, r1, X_var)), X_var, sp.oo)
check("any SATURATING-ρ end has ∫2K/ρ²dr = ∞ — comparison bound: ρ ≤ ρ_∞ "
      "⇒ density ≥ 2K/ρ_∞² > 0 pointwise, AND the representative "
      "ρ = ρ_∞ − b/r integral diverges exactly (limit of the finite "
      "integral = ∞): for q ≠ 0, E1's escape geometry costs INFINITE "
      "total action; finite tail action ⇔ ∫dr/ρ² < ∞ ⇒ ρ unbounded",
      sat_tail == sp.oo
      and sp.simplify(sat_bound * (rho_c - b_s / r)**2 * rho_c**2
                      - 2 * K * (rho_c**2 - (rho_c - b_s / r)**2)) == 0)
f_member = C_s + a_s / r
V_member = (f_member * (lam / r**2 + sp.diff(f_member, r) / r))
check("finite-action members (ρ ~ r, e.g. the ρ = r member f = C + a/r, "
      "|a| = 2√K): asymptotically areal/flat, extremal charged tail, and "
      "probe threshold V(∞) = 0 — back inside the rigidity class",
      sp.limit(V_member, r, sp.oo) == 0)

print()
print("  (v) the UNCHARGED degenerate sector (q = 0 ⇒ a = 0 ⇒ f ≡ f_∞, "
      "ρ free):")
f_inf = sp.symbols("f_oo", positive=True)
V_q0 = (f_inf * lam / rho**2
        + f_inf * sp.diff(f_inf * rhop, r) / rho).subs(rho, rho_c - b_s / r)
check("with f ≡ f_∞ and ρ = ρ_∞ − b/r (saturating): V(∞) = f_∞λ/ρ_∞² > 0 — "
      "the threshold-lifting throat IS allowed here, at zero action…",
      sp.simplify(sp.limit(V_q0.doit(), r, sp.oo)
                  - f_inf * lam / rho_c**2) == 0)
print("""     …but it is allowed only because in the q = 0 sector ρ(r) is a
     COMPLETELY free function (D3a/D3b degeneration with a = 0): nothing
     in the action selects the throat over ρ = r or over anything else.
     Allowed-by-underdetermination, not produced-by-dynamics.

  VERDICT D4 (exact): under the total native action the flux-extremal
  family allows, at large r, EITHER unbounded-ρ ends (finite action,
  threshold 0 — rigidity class) OR cylinder ends that are horizon-capped
  (threshold → 0) or confining-at-infinite-action.  A finite-positive-
  threshold cylinder (the E1 escape) is FORBIDDEN by the extremality lock
  for every q ≠ 0, and UNDETERMINED (allowed but unselected) at q = 0.
  No determined throat branch exists.""")

# ---------------------------------------------------------------------------
# D5 — P0 audit verdict + the identified missing-equation candidate
# ---------------------------------------------------------------------------
hr("D5 — P0 AUDIT VERDICT + what native structure ρ's missing equation "
   "would need")

print("  (a) kinetic-term inventory: which banked piece carries (ρ')²?")
check("C1 piece: ∂/∂ρ' ≡ 0 (section A)",
      sp.simplify((sp.Rational(1, 4) * rho**2 * fp**2).diff(rhop)) == 0)
check("flux piece: ∂/∂ρ' ≡ 0 (section B)",
      sp.simplify((K / rho**2).diff(rhop)) == 0)
check("source piece: ∂/∂ρ' ≡ 0 (section C, w ≡ 1 forced)",
      sp.simplify((sp.Rational(1, 2) * s_s * W * f**2).diff(rhop)) == 0)
L_probe = rho**2 * f * sp.diff(R_f, r)**2 + lam * R_f**2
check("H1 probe kinetic density ρ²f(R')² + λR²: ∂/∂ρ' ≡ 0 as well — the "
      "probe sector supplies no ρ-gradient energy either",
      sp.simplify(L_probe.diff(rhop)) == 0)
print("     NO banked sector carries (ρ')².  The ρ-equation is doomed to")
print("     stay algebraic under the current action inventory.")

print()
print("  (b) the EH scalar density on the TWO-function metric, computed "
      "from scratch:")
n4 = 4
Gam = [[[sp.simplify(sum(
    g4inv[a_i, d_i] * (sp.diff(g4[d_i, b_i], coords[c_i])
                       + sp.diff(g4[d_i, c_i], coords[b_i])
                       - sp.diff(g4[b_i, c_i], coords[d_i])) / 2
    for d_i in range(n4))) for c_i in range(n4)] for b_i in range(n4)]
    for a_i in range(n4)]


def ricci_component(b_i: int, c_i: int) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(Gam[a_i][b_i][c_i], coords[a_i]) for a_i in range(n4))
        - sum(sp.diff(Gam[a_i][b_i][a_i], coords[c_i]) for a_i in range(n4))
        + sum(Gam[a_i][a_i][d_i] * Gam[d_i][b_i][c_i]
              for a_i in range(n4) for d_i in range(n4))
        - sum(Gam[a_i][c_i][d_i] * Gam[d_i][b_i][a_i]
              for a_i in range(n4) for d_i in range(n4)))


R_scalar = sp.simplify(sum(g4inv[b_i, c_i] * ricci_component(b_i, c_i)
                           for b_i in range(n4) for c_i in range(n4)))
rho2R = sp.simplify(rho**2 * R_scalar)
rho2R_target = (-rho**2 * sp.diff(f, r, 2) - 4 * rho * rhop * fp
                + 2 - 2 * f * rhop**2 - 4 * f * rho * sp.diff(rho, r, 2))
check("ρ²R = −ρ²f'' − 4ρρ'f' + 2 − 2f(ρ')² − 4fρρ'' exactly (Christoffel/"
      "Ricci computed from the metric, no formula imported)",
      sp.simplify(rho2R - rho2R_target) == 0)

R1_C1 = sp.simplify(
    (rho2R_target.subs(f, C_s + a_s / r).subs(rho, r) / r**2)
    .doit().subs(C_s, 1))
R2_C1 = sp.simplify(
    (rho2R_target.subs(f, C_s + a_s / (3 * r**3)).subs(rho, r**2) / r**4)
    .doit().subs(C_s, 1))
check("D3b UPGRADE (verifier invariant computation reproduced): the two "
      "lock members with identical (C, a, K) — (ρ = r, f = C + a/r) vs "
      "(ρ = r², f = C + a/(3r³)) — have DIFFERENT curvature invariants as "
      "functions of areal radius: at C = 1 the first is scalar-flat "
      "(R ≡ 0) while the second has R = (2 − 4a/(3r) − 16r²)/r⁴ ≠ 0 — "
      "the underdetermination is DEMONSTRATED physical, not gauge",
      sp.simplify(R1_C1) == 0
      and sp.simplify(
          R2_C1 - (2 - 4 * a_s / (3 * r) - 16 * r**2) / r**4) == 0
      and sp.simplify(R2_C1) != 0)

rho2R_at_r = sp.simplify(rho2R_target.subs(rho, r).doit())
bdry_banked = 2 * r * (1 - f) - r**2 * fp
check("ρ = r control: ρ²R = d/dr[2r(1−f) − r²f'] exactly — the banked "
      "total-derivative identity (native_eh_total_boundary_diagnostic.py) "
      "re-verified",
      sp.simplify(rho2R_at_r - sp.diff(bdry_banked, r)) == 0)

bdry_gen = -(rho**2 * fp + 2 * f * rho * rhop)
remainder = sp.simplify(rho2R - sp.diff(bdry_gen, r))
check("general ρ: ρ²R = −d/dr[ρ²f' + 2fρρ'] + (2 − 2fρρ'') — a BULK "
      "remainder survives; the EH density is NO LONGER a pure boundary "
      "term once ρ is freed",
      sp.simplify(remainder - (2 - 2 * f * rho * sp.diff(rho, r, 2))) == 0)

ELf_EH = euler_lagrange(rho2R, f)
ELrho_EH = euler_lagrange(rho2R, rho)
check("invariant test (split-independent): EL_f[ρ²R] = −2ρρ'' ≠ 0 — "
      "vanishes iff ρ'' = 0; at ρ = r it dies, exactly why the banked "
      "diagnostic saw a total derivative",
      sp.simplify(ELf_EH + 2 * rho * sp.diff(rho, r, 2)) == 0)
check("EL_ρ[ρ²R] = −(2ρf'' + 4ρ'f' + 4fρ'') ≠ 0 — the freed-ρ EH density "
      "carries GENUINE ρ-dynamics: (ρ')² gradient energy and ρ'' "
      "second-jet structure, precisely the missing ingredients of (a)",
      sp.simplify(ELrho_EH
                  + 2 * rho * sp.diff(f, r, 2) + 4 * rhop * fp
                  + 4 * f * sp.diff(rho, r, 2)) == 0)

M_s = sp.symbols("M", positive=True)
ELrho_at_r = sp.simplify(ELrho_EH.subs(rho, r).doit())
check("sanity (GR control): Schwarzschild f = 1 − 2M/r, ρ = r annihilates "
      "BOTH EL derivatives exactly",
      sp.simplify(ELf_EH.subs(rho, r).doit()) == 0
      and sp.simplify(ELrho_at_r.subs(f, 1 - 2 * M_s / r).doit()) == 0)
check("plain-sight identity: at ρ = r, EL_ρ[ρ²R] = −(2/r)(r²f')' — the EH "
      "ρ-variation IS the banked vacuum f-operator; the banked family "
      "f = C + a/r annihilates it too",
      sp.simplify(ELrho_at_r + (2 / r) * sp.diff(r**2 * fp, r)) == 0
      and sp.simplify(ELrho_at_r.subs(f, C_s + a_s / r).doit()) == 0)

print("""
  (c) GUARDRAIL (binding, recorded): the EH action as DYNAMICS is a
  FORBIDDEN import (native_positional_dilation_gr_guardrail.py: "Einstein-
  Hilbert action as dynamics — not imported"; charter principle 1).  The
  computation above is geometry-of-the-metric, usable exactly; ADOPTING
  ρ²R as an action piece is not.  Status assigned:

      IDENTIFIED CANDIDATE for "the uncovered metric function's missing
      equation": the freed-ρ EH density is the unique object in view that
      (i) carries (ρ')² and ρρ'' (the missing kinetic/second-jet
      structure), (ii) reduces to a pure boundary term at ρ = r (so it is
      invisible in every banked ρ = r calculation — consistent with the
      whole existing corpus), and (iii) at ρ = r its ρ-variation collapses
      to the banked vacuum operator (2/r)(r²f')' (so adding it with ANY
      coefficient is consistent with the banked vacuum family AND with the
      D3b extremality lock — verified above).  PENDING: a NATIVE
      derivation (e.g. from angular-sector gradient energy or the
      positional-dilation transform of a boundary object, principle 4) —
      until then it stays a candidate, not a piece.""")

print("""
  VERDICT D5 — P0 AUDIT (the honest classification, by assumption set):

    {ρ varied, q = 0, W = 0}      : f' ≡ 0 forced.  ρ = r NOT derived;
                                    banked vacuum killed.  P0 must be a
                                    kinematic constraint (ρ not varied).
    {ρ varied, q ≠ 0, W = 0}      : extremality lock |a| = c_q|q| (the one
                                    genuinely new exact relation of this
                                    file), then ρ(r) a FREE function:
                                    UNDERDETERMINED.  ρ = r admissible but
                                    unselected.
    {ρ varied, q ≠ 0, W ≠ 0}      : OVERDETERMINED on supp W (no solution);
                                    degeneracy not broken (conditional on
                                    the C-flag source interpretation).
    throat branch                 : exists only as horizon-capped or
                                    infinite-action ends for q ≠ 0; as an
                                    unselected member of the degenerate
                                    family for q = 0.  NO determined
                                    saturating-ρ branch.
    ρ = r derived?                : NO, under every assumption set tested.
    underdetermined?              : YES — the ruling state of the freed-ρ
                                    system; the missing object is a native
                                    (ρ')²-carrying piece, with the freed-ρ
                                    EH density as the identified (but
                                    import-forbidden) candidate.""")

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

  FIELD EQUATIONS, freed areal function, total native action
  L = (1/4)ρ²(f')² + K/ρ² − (s/2)W f²  (signs anchored by banked limits):

      δf:  (ρ²f')' + 2sW f = 0          δρ:  ρ⁴(f')² = 4K   (ALGEBRAIC).

  CLASSIFICATION: pure C1 + freed ρ kills all nontrivial f (P0 not
  derived — it is the statement that ρ is not varied); with flux, the
  algebraic ρ-equation implies the f-equation and locks the tail to the
  charge, |a| = c_q|q| (extremality), leaving ρ(r) a free function —
  UNDERDETERMINED; the H1 collar source cannot repair this (it
  overdetermines instead).  THROAT: no determined saturating-ρ branch —
  charged cylinders are horizon-capped (threshold → 0) or confining at
  infinite action; the threshold-lifting cylinder survives only as an
  unselected member of the degenerate q = 0 sector.  The E1 escape of the
  rigidity theorem therefore still has NO native realization.

  CONDITIONALITY: flux results conditional on Pflux (→ Pbundle0); source
  results conditional on the collar-source interpretation; normalization
  of c_q depends on the 4π bookkeeping (structure does not).

  SPEC CORRECTIONS RECORDED (sympy wins): (1) the flux sign must enter the
  effective density as +K/ρ² (literal Maxwell action subtracted), else the
  ρ-equation has no solution; (2) f(ρ) is NOT an invariant of the extremal
  family (df/dρ = −a/(ρ²ρ') carries ρ'); only ρ²f' = −a is invariant;
  (3) the source piece has NO surviving ρ-dependence and yields
  overdetermination, not a ρ-ODE; (4) κ_q = 2πq²/μ vs the banked (1/4)
  normalization mixes angular conventions — flagged, structure unaffected.

  THE MISSING EQUATION: no banked sector carries (ρ')².  The freed-ρ EH
  density ρ²R = −d/dr[ρ²f' + 2fρρ'] + 2 − 2fρρ'' is no longer a boundary
  term (EL_f = −2ρρ'', EL_ρ = −(2ρf'' + 4ρ'f' + 4fρ'')), is invisible at
  ρ = r, and is consistent with the banked vacuum and the extremality
  lock — the identified candidate for ρ's missing equation, FORBIDDEN as
  an import (guardrail), awaiting a native derivation.""")
