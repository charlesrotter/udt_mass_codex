# Derivation notes — copresence -> P-opt

Date: 2026-08-05. **STATUS: LEAD / UNBANKED. NOT A RESULT.** Owner-favorable (Charles's own
claim) -> extra skepticism. Two adversarial reviews owed; Charles must confirm the copresence
definition; external review owed for any bank. Four-check N/A to a lead. No data/fit touched.

## The argument (exact where computational; self-checked only)

1. **C2 + C3 => P-opt, by construction.** If copresence-distance is the light/optical path
   ell_opt = integral(dr/A) (C2), and depth is uniform per copresence-distance (C3
   homogeneity), then dphi/dell_opt = const => dell_opt = kappa dphi = **P-opt** => A = 1-r/X
   (L). So the entire result rests on the two premises C2, C3.

2. **x_max SUPPORTS C2 by killing the natural alternatives (VERIFIED).** Among the three
   "uniform depth per X" parametrizations:
   - X = null-affine  -> A = e^{-r/X} (exponential): proper distance to x_max = INFINITE -> x_max-EXCLUDED.
   - X = optical/light -> A = 1-r/X (L): proper distance = 2X FINITE -> x_max-OK. (= P-opt)
   - X = proper-dist  -> A = (1-r/L0)^2 (quadratic): proper distance = INFINITE -> x_max-EXCLUDED.
   So with x_max read as **finite maximum PROPER separation** (the kernel), the proper-distance
   and affine alternatives to C2 give x_max-VIOLATING profiles. Among these three, only the
   light-distance choice (L) survives. **x_max forces the light-distance reading among the
   natural candidates.** Note the horizon signature: L has finite proper size but INFINITE
   optical/causal reach (ell_opt ∝ phi -> infinity) -- exactly an x_max horizon.

3. **H is excluded by C3 (VERIFIED).** Review-B's finite-proper counterexample H=(X-r)/(X+r)
   has dphi/dell_opt = 1/(1+r/X)^2 -- NOT constant -- so H violates homogeneity (C3). Under C2+C3,
   H is excluded and L is selected. (L: dphi/dell_opt = 1/2, constant.)

## Honest status of each premise (the reviews must hammer these)
- **C2 (copresence-distance = light distance): the load-bearing assumption.** Argued: in a
  static/all-now/no-expansion universe you locate a remote co-present object operationally by
  LIGHT (radar); proper distance requires traversing. x_max SUPPORTS it (the proper alternative
  is x_max-excluded, step 2). But it is a physical-operational choice narrowed by x_max, NOT a
  standalone theorem, AND the candidate set {affine, optical, proper} may be INCOMPLETE (other
  distance measures unchecked). This is the crack the reviews must widen.
- **C3 (homogeneity = uniform depth per copresence-distance): possibly loaded.** Is "no
  preferred depth" faithfully = "uniform depth per light-distance," or does that phrasing
  assume the answer? Attack.
- **x_max = finite PROPER distance:** the reading used. If x_max means a different distance,
  step 2 changes.
- **Copresence DEFINITION is the driver's interpretation of Charles's term** -- Charles must
  confirm C1-C3 before any bank.

## Conditional verdict (LEAD): OP2-DERIVED-CONDITIONAL
IF (C2 light-distance, x_max-supported) AND (C3 homogeneity) AND (candidate set complete) AND
(Charles confirms the copresence definition), THEN reciprocal + copresence + x_max DERIVE P-opt
=> A=1-r/X => the native SNe fit (z(z+2), chi^2/dof=0.91) upgrades from conditional-on-P-opt to
DERIVED-from-copresence. This substantially supports Charles's claim -- but it rests on C2,
which is x_max-supported-but-not-proven and hinges on the candidate set being complete. NOT a
result until the reviews survive and Charles confirms the definition. Nothing banks.

## CONSOLIDATED CORRECTION (2026-08-05): REFUTED by both reviews

Files: ADVERSARIAL_REVIEW_B_circularity.md (REFUTE), ADVERSARIAL_REVIEW_A_completeness.md (NARROW).
Verdict: **OP2-DERIVED-CONDITIONAL is RETRACTED. Copresence does NOT derive P-opt.**

**Review B (REFUTE) — circular + unfaithful:**
- C2 + C3 (dist=ell_opt ; dphi/dell_opt=const) with g_xx=1/A is IDENTICALLY "A linear in r" = P-opt.
  Step 1 has ZERO derivational content ("by construction", as the driver conceded). The selective
  weight is entirely on x_max (step 2).
- x_max does NOT close it: H=(X-r)/(X+r) has finite proper distance X(2+pi)/2 ~= 2.571X (verified),
  survives x_max, is non-linear. Excluding H needs C3-optical = P-opt restated. Assumes conclusion.
- FAITHFULNESS: copresence = SIMULTANEITY; light connects DIFFERENT-time events, not co-present
  ones. So copresence argues for PROPER (now-slice) distance, not light distance -> quadratic ->
  x_max-excluded (proper reading). C2 (light) was the CONVENIENT reading that dodges the exclusion
  to reach L. Reciprocity IS genuinely used (substrate) but is agnostic among profiles; the
  tautological C3 is the selector -- so "reciprocity leads directly to P-opt" is FALSE.

**Review A (NARROW) — the x_max reading is unlicensed and does all the forcing:**
- G14 explicitly leaves the separation type `s` OPEN and forbids wall/edge/center readings. The notes
  SILENTLY substituted s = PROPER distance -- the ONLY reading under which L is unique. Survivor sets:
  finite-PROPER -> {L}; finite-COORDINATE/areal (arguably more natural) -> {L, quadratic}; finite-
  OPTICAL (the copresence measure itself) -> {} (even L excluded). So "x_max SUPPORTS C2 (VERIFIED)"
  OVERCLAIMS -- retracted.
- STRUCTURAL: A = exp(-2k*X_copres) => the dilation wall sits at INFINITE copresence-distance ALWAYS.
  So finite x_max can NEVER be in the copresence measure; it needs a SECOND, different measure, and
  that second-measure pick (optical-for-copresence vs proper-for-x_max) is what selects L -- an
  unforced post-hoc mismatch, not a derivation.
- A finite-proper FAMILY exists: A=(1-r/X)^{1/n}, finite proper distance for all n>1/2; L is only n=1.

**CORRECTED VERDICT: REFUTED.** Copresence (as formalized) does not derive P-opt: the C2+C3 core is
circular, and the x_max "support" relied on an unlicensed proper-distance reading of a deliberately-
OPEN separation type. P-opt remains a genuine INDEPENDENT assumption; the SNe fit (z(z+2), 0.91)
stays conditional on it. Deep honest residue: the profile is fixed by the RELATIONSHIP between two
distance measures (e.g. optical vs proper); nothing (reciprocity, x_max, copresence) fixes that
relationship -- it is the same unselected law/profile gate open all session. Nothing banks.
