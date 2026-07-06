
---

> **CONDITIONS-CHANGED (2026-07-06 pre-native-era census) — NOT current native-micro canon; premise-scoped.**
> Companion verifier to the everything-on P2/P3/P4 arc (frame B, a(φ)=−1 / G=kap8·T), which is CONDITIONS-CHANGED
> (2026-07-06). Verifies DATA-BLIND machinery, banked no native-micro physics. Superseded frame; the 2026-07-01 native
> constrained-two-player operator (EH-empty, φ-blind matter, geometric 𝒦) is the current frame. See
> pre_native_era_census.md + NEGATIVES_REGISTRY.

# P3 VERIFIER PASS -- blind adversarial

**Verifier:** Claude (Opus 4.8, 1M), independent blind adversarial verifier.
**Date:** 2026-06-20.  **Branch:** p3-aphi-coupling.  **DATA-BLIND** (no mass/ratio/wall).
**Target:** p3_aphi_coupling_results.md + p3_aphi_matter.py, p3_validate_baseline.py,
p3_explore_aphi.py.  Method: arc cross-read, sympy identities, cheap torch evals
(baseline collapse, FD-variational gate, non-absorbability, sign), greps.

## CLAIM-BY-CLAIM

**1. PLACEMENT (smuggle crux) -- STANDS (with one flagged freedom).**
- (a) action-density placement consistent with arc's G=(8piG/c4)e^{(a+1)phi}T:
  YES. Arc (udt_field_equations sec.2b/sec.3, udt_a_exponent) banks weight on the
  matter SOURCE, curvature side = GR, a under-determined, a=-1=GR admissible. The
  code puts W on S_m=int sqrt(-g) W L; varying gives Tw = -2/sqrt(-g) d(sqrt(-g)WL)/dg
  = W*T (phi external multiplier). VERIFIED empirically: stress(k=1) == W*T_unweighted
  EXACTLY (max diff 0.0).
- (b) W uniform on whole L (not a sector split): YES. W multiplies the full Tab and
  the full action density; no a_eff kinetic/angular split. The smuggle (weight one
  invariant) is explicitly avoided.
- (c) SAME W in stress and EL: YES. FD-variational gate (autograd EL vs FD dS_w/dF,
  full off-diag metric) re-run independently: k=0 rel-err 1.32e-5, k=1 rel-err 9.33e-6.
  EL is the true variation of the SAME weighted action.
- FLAGGED FREEDOM (not a smuggle, but the arc does NOT pin it): the arc derives the
  weight for CONSTANT a. Promoting a->a(phi), the exponent convention W=e^{(a+1)phi}
  (PRODUCT) is a CHOICE; the alternative W=e^{int(a+1)dphi} (the ruler-integral the
  explore script itself uses for its fingerprint, line 59-60) differs when a runs.
  P3 declares W=e^{(a+1)phi}; defensible as a declared form, but it is a generalization
  freedom, not arc-forced. Has NO effect on the baseline (k=0 both forms ->1).

**2. BASELINE a=-1 (k=0) reproduces P2 BITWISE -- STANDS.**
Independently re-run on the non-diagonal position-dependent-phi config (phi in [-0.4,0],
e_rt,e_rp,e_tp live): max|W-1|=0.0, max|a+1|=0.0, max|dT|=0.0, max|dEL|=0.0. sympy:
a(k=0)=-1, (a+1)|_{k=0}=0, W|_{k=0}=1 identically. The whole P3 layer collapses to P2
exactly at k=0. (M_MS round-anchor not re-run -- slow; the bitwise stress/EL identity
at k=0 forces it.)

**3. MODIFIED CONSERVATION -- PARTIAL / DEFECT at k!=0.**
The vanishing at a=-1 is CORRECT and emergent: at k=0 the exchange coeff is identically
0 -> div T=0 (verified). BUT the coefficient is WRONG for k!=0 given the code's OWN
weight. For W=e^{(a+1)phi} with a=a(phi), Bianchi forces
  div T = -(d ln W/dphi) phi' T,  and  d ln W/dphi = (a+1) + phi*da/dphi,  NOT (a+1).
sympy: (1/W)dW/dphi = k e0^p e^{-p phi}(1 - p phi) = (a+1) + phi*da/dphi (exact).
The code (p3_aphi_matter.py line 172/181) uses aP1=(a+1) as the coefficient, so the
reported "genuine Bianchi source" (report sec.3.2, 4.7e-2 at k=1) is MIS-COEFFICIENTED:
true coef vs code coef differ by phi*da/dphi -> 17% at phi=-0.2, 29% at phi=-0.4 (k=1).
The report's headline identity "div T = -(a+1)phi'T emerges from Bianchi" is the
CONSTANT-a arc identity; it is NOT the correct identity for the implemented running-a
weight. SCOPE OF DAMAGE: the exch term is NOT used in the baseline, the FD gate, or the
solver -- only in a single reported diagnostic number at k!=0. The baseline (a+1=0) and
solver are untouched. So this is a wrong reported characterization at k!=0, not a
contamination of P4's inherited capability. Must be recorded; downgrades the
conservation claim from STANDS to PARTIAL.

**4. NON-ABSORBABILITY -- STANDS.**
da/dphi = -p k e0^p e^{-p phi}: =0 at k=0 (constant a, absorbable=GR relabel),
!=0 at k!=0. Re-run: max|da/dphi| over phi[-3,1] = 2.009e1 (k=1,p=1), 8.069e2 (k=1,p=2),
0 (k=0) -- matches report. da/dphi is an intrinsic property of the function, gauge-
invariant -> cannot be flattened by any units choice. The exploration tests a genuine
FUNCTION, not an absorbable constant.

**5. EXPLORATION STRUCTURE + SELF-CORRECTION -- STANDS (one stale inline comment).**
Suppression sign CORRECT: over phi in [-0.4,0], k>0, p=1, eps0=1, (a+1)=k e^{-p phi}>0
and phi<0 => (a+1)phi<0 => W<1. Re-run: W in [0.74..1.0] (k=0.5), [0.55..1.0] (k=1) --
all <=1, suppression. The report sec.3.3 self-correction (suppression, not amplification)
is honest and is the load-bearing reading. Residual: p3_explore_aphi.py lines 102-103
still print "AMPLIFIES toward the deep core" (hedged with "sign-watch in report"); the
script is immutable + the report carries the correction, so not load-bearing, but the
stale comment exists.

**6. DISCIPLINE / PRINCIPLE 7 -- STANDS.**
a!=-1 stated UNFORCED / "not the answer" throughout; a=-1=GR admissible (matches arc
"a under-determined"). No GR-form smuggle (curvature side = GR is the arc's separately-
verified result, not a P3 default; the modification lives only in the matter weight).
phi-as-external-potential scoping (omitted curvature-side dW/dg) correctly FLAGGED
(sec.4, BUILD_MAP VII-b), not hidden. Greps clean: no m*PI Skyrme BC; the only B=1/A is
the labelled FREE choice in the non-solve test config (solver carries a,b INDEPENDENT in
the state vector u, solved by two Einstein residuals -- NOT tied); no linearization;
no wall numbers (data-blind confirmed). Time row zeroed = the only declared freeze (P4).

**7. IS "DONE" HONEST -- PARTIAL.**
The a(phi) CAPABILITY is genuinely wired, baseline-validated bitwise, and FD-consistency-
gated -> "DONE" for the capability is largely fair, and the deep-phi physics is correctly
downstream (P5/P6). HOWEVER the modified-conservation diagnostic at k!=0 is reported with
the wrong coefficient (Claim 3), and the weight-exponent convention for running a is an
undeclared generalization freedom (Claim 1 flag). Neither touches the baseline or solver,
but both are part of the "capability" being called DONE. Recommend: status should read
DONE-for-baseline-wiring + PARTIAL-on-the-running-a conservation characterization
(fix the exch coefficient to (a+1)+phi*da/dphi, or re-declare W).

## HEADLINE RULINGS
(a) Placement = the DERIVED one, no smuggle: YES (uniform on whole L, same W stress+EL,
    matches arc). One flagged freedom: the running-a exponent convention is not arc-pinned.
(b) a=-1 collapses to P2 bitwise: YES (0.0 across W, a+1, dT, dEL; sympy-exact).
(c) Modified conservation correct + emergent: emergent + correct at a=-1; INCORRECT
    COEFFICIENT at a(phi)!=-1 (uses (a+1), true is (a+1)+phi da/dphi). PARTIAL.
(d) a!=-1 genuinely non-absorbable: YES (da/dphi!=0, gauge-invariant).
(e) "DONE" honest or PARTIAL: PARTIAL -- DONE for the baseline-validated wiring; the
    running-a conservation diagnostic is mis-coefficiented and should be fixed/re-scoped.
Principle-7 violation: NONE (vacuum=GR is arc-derived, not defaulted; a!=-1 never forced).
Hidden freeze: NONE beyond the declared time-row zero.

## NET
P3 STANDS on its LOAD-BEARING spine: the DERIVED placement, the BITWISE baseline, the
FD consistency gate, and genuine non-absorbability. ONE real defect: the modified-
conservation exchange coefficient is the constant-a identity (a+1), not the correct
running-a identity (a+1)+phi*da/dphi, so the reported k!=0 "Bianchi source" number is
wrong by ~17-29% on the tested range -- confined to a diagnostic, not the baseline/solver.
P4 SAFELY INHERITS: a weight-capable native S^2 matter sector (stress & EL both carry
e^{(a+1)phi} on the full off-diag metric), a=-1 the validated GR baseline. P4 must NOT
inherit the (a+1) conservation coefficient for running a -- fix to (a+1)+phi da/dphi (or
re-declare the weight as e^{int(a+1)dphi}) before any running-a conservation result is
banked.
