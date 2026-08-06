# Adversarial Review 2 — interpretation & frame status (vary-phi probe)

Reviewer: independent adversarial pass (Opus), 2026-08-06. UNBANKED. Not committed.
Direction: attacks the IMPORT/faithfulness/NOVELTY/SCOPE and the frame-status reading.
Companion to the TRIVIAL/projection-algebra review.

## Independent algebra checks (all PASS — reproduced from scratch in sympy)

- `G^t_t == G^r_r` on the reciprocal-lock ansatz: `G^t_t - G^r_r = 0` exactly. CONFIRMED.
- `G^th_th` matches the notes. CONFIRMED.
- Reduced radial Lagrangian `L = R r^2` matches the notes. CONFIRMED.
- Full 2nd-order Euler-Lagrange in phi: `E[phi] = 0` identically. CONFIRMED.
- **DECISIVE (novelty):** `L = R r^2` is EXACTLY `d/dr[ 2r(1-e^{-2phi}) + 2 r^2 e^{-2phi} phi' ]`.
  Computed `L - dB = 0` where `dB` is the derivative of the boundary term the **2026-07-01**
  native-field-equations work already published (`r^2 R = d/dr[2r(1-e^{-2phi})+2r^2 e^{-2phi} phi']`).
  The new "null Lagrangian / E[phi]=0" is the SAME mathematical object as the banked
  "sqrt(-g) R is a pure boundary term => bare EH gives no bulk phi equation."

The derivation is arithmetically clean and honestly self-reported. The disputes are interpretive.

## 1. FRAME STATUS — SUPPORT or UNDERMINE "vary phi not the metric"?

Split, and the honest reading is the weaker one.
- SUPPORTED: the *structural* escape-claim. Constrained phi-variation is NOT the free-metric
  equation `G=0` (it is the projection onto one direction), so Lovelock's forced-Einstein does not
  govern it. That much is real and correctly shown.
- UNDERMINED: the *operational* promise. The frame is sold as "varying phi YIELDS a native
  non-Einstein LAW." With the only action tried (EH-reference) it yields NOTHING — `E[phi]=0`,
  zero equations for one field. Worse than incidental: the mechanism shows the reciprocal lock
  ALIGNS the phi-direction with the flat direction of the EH action (proj ∝ `G^r_r - G^t_t`, which
  the lock annihilates). The vacuity is *structural to lock+EH*, not bad luck.
- Verdict on the two offered readings: "frame is alive but EH is the wrong action" is HONEST ONLY
  as a hypothesis, NOT as a demonstrated status — nothing here shows any action gives a nonvacuous
  phi-law on this slice. "Effectively dead" overstates the other way: one action on one slice is
  not the frame. The evidence supports: **frame's escape-claim confirmed; frame produced NO law
  from the one action tried; aliveness is UNDETERMINED pending an untested different action.**
  The driver's own doc verdict (UNDERDETERMINED, "EH-reference does not [give a phi-law]") is
  honest; the LIVE-level gloss "the native action is NOT EH" is a fair *inference* but must not be
  read as "we have shown the native action exists elsewhere."

## 2. IMPORT / DOUBLE-STANDARD

- EH-as-reference: CLEAN. Tagged CHOSE/reference-only, Category-A GR-as-reference, not claimed as
  the native action. F-IMPORT does not fire. `g[phi]` treated as native (positional dilation) is
  consistent with canon. No import fault.
- The real catch is a PROGRAM-LEVEL assumption. LIVE.md's law-order architecture audit
  (2026-08-05) states NEITHER response-first NOR action-first is derived, and response-first is the
  current working priority. This probe is a pure ACTION-first exercise, and its forward conclusion
  ("we need a different native action") quietly re-commits to action-first that the audit left OPEN.
  Proposing "just find the right native action" is a legitimate lead ONLY if bounded (which action,
  what would falsify it). As an open-ended "the content lives in some other action," it is an
  UNFALSIFIABLE DEFER — you can always claim the right action is not yet found. **DEFER-RISK flagged.**

## 3. THE BOUNDARY LEAD

- Genuine as a POINTER: the reduced action is provably a pure boundary term (L - dB = 0, section
  above). When a bulk action collapses to a total derivative, its dynamical content, if any, is
  boundary-carried — a real mathematical consequence, and consonant with the finite-cell canon and
  Principle 4 (boundary terms are a mine).
- NOT credited as CONTENT: the probe did not vary the boundary term, evaluate it on the finite
  cell / x_max, or show it carries any phi-law. "The physics is in the boundary" is therefore an
  UNDEMONSTRATED hope. The DERIVATION_NOTES phrasing ("the open door this leaves") is honest; any
  headline that upgrades it to "content lives in the boundary" is mild F-STEER.
- Ruling: **credit the observation (it IS a boundary term); do NOT credit the lead as content.**
  Lightly F-steered if stated as more than a pointer.

## 4. NOVELTY

RE-DERIVATION. The core result "EH is phi-blind on the reciprocal lock / supplies no phi-law" is
mathematically IDENTICAL to the banked, CAS-verified, blind-verified 2026-07-01 finding
(`native_field_equations_..._results.md`: `sqrt(-g) R` = pure boundary term => no bulk phi eqn).
Proven here: the new Lagrangian is byte-for-byte the derivative of that same boundary term. This is
VERIFICATION of a banked result, not a new one. The genuinely new elements are (a) the
Lovelock-escape / vary-phi-not-g FRAMING and (b) the explicit projection mechanism (phi-variation
∝ `G^r_r - G^t_t`, annihilated by the lock). Both are useful lenses; neither adds physical content.

## 5. SCOPE

Honest. Stamped static / radial / EH-reference / no native action / no physics / no mass; `c=1`
premise noted; reciprocal-lock dependence made load-bearing and visible. Add one caveat: the
vacuity is *reciprocal-lock-specific*, and that premise should travel with any citation of this
result (a different lock/off-round could change the projection direction — untested).

## VERDICT

**RE-DERIVATION-ONLY**, with a **DEFER-RISK** on the forward "need a different native action"
conclusion. The escape-from-Lovelock structural claim is real; the operational payoff under EH is
zero and re-proves a July finding. The boundary lead is a GENUINE POINTER, not credited as content;
mildly F-steered if stated as a conclusion. Nothing here is bankable as new.

STRONGEST POINT: `L = R r^2` is exactly the total derivative of the 2026-07-01 boundary term
(`L - dB = 0` verified independently), so "EH phi-blind on the lock" is verification of an
already-banked result, not a new discovery.
