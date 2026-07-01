# The G↔P Switch Criterion — when the depth-shift breaks (finite-cell → Branch P)

**Date:** 2026-07-01. **Provenance:** derivation target set by Charles (sharpened in-session); driver
derivation with CAS anchors (`switch_criterion_derivation.py`); blind-adversarial verifier recorded below.
**Status:** DERIVED necessary+sufficient criterion (scoped); one honest open sub-question flagged. NOT canon.
**Builds on:** `native_field_equations_constrained_two_player_results.md` (the constrained-two-player frame +
the G/P regimes). Answers its OPEN item "derive the G↔P switch criterion."

---

## The question (Charles, sharpened)

The field-eq derivation left G and P as two REGIMES (G = strict depth-gauge continuum exterior; P = angular-
scale-physical finite-cell), with the open target: **what geometric condition switches G→P?** The driver's
first MAP ("P iff fixed angular scale") was too broad; Charles sharpened it to: **P iff the finite domain pins
a DIMENSIONLESS radial-to-angular invariant that makes the constant-φ mode measurable** — and demanded the
boundary-vs-bulk distinction be settled (is P a bulk equation, or just G with P-like boundary data?).

---

## Result 1 — the single shift-breaking term (CAS)

Under the constant depth-shift φ→φ+λ, in the constrained action
`S = ∫ c√h [ (Z/2)φ'² + R^{(2)}[h] + 𝒦_branch + L_m^UDT ]`:
- kinetic `e^{2φ}g^{rr}φ'² = φ'²` — φ'-only → **invariant**;
- `R^{(2)}[h]` — h-only → **invariant**;
- `L_m^UDT` (channel-corrected, undilated) — φ-blind → **invariant**;
- `𝒦 = K_AB K^AB − K²`, `K_AB = ½e^{-φ}∂_r h_AB` → `𝒦 → e^{-2λ}𝒦` — **BREAKS the shift.**

**All shift-breaking is carried by the transverse extrinsic term 𝒦 (the radial evolution of the transverse
2-geometry) — nothing else.**

## Result 2 — the invariant the shift moves: the cell ASPECT RATIO

    χ = L_radial / √(A/4π),   L_radial = ∫_{r_c}^{r_i} e^φ dr (proper radial extent),   A = transverse area.
Under φ→φ+λ: `L_radial → e^λ L_radial`, `A` fixed (h is φ-independent) → **χ → e^λ χ**. χ is a ratio of PROPER
lengths ⇒ no coordinate change can undo it. (Gauss-Bonnet: `∫√h R^{(2)} = 8π`, topological/size-blind — the
scale is NOT in R^{(2)}; it is in 𝒦, i.e. the radial evolution — consistent with χ.)

## Result 3 — the SWITCH CRITERION (necessary + sufficient)

The shift is broken → **Branch P** iff ALL THREE hold:
- **(N1)** transverse scale √A pinned (angular size fixed);
- **(N2)** radial interval [r_c, r_i] pinned (so L_radial is a finite fixed observable);
- **(N3)** 𝒦 ≠ 0 (transverse geometry actually evolves with r).

Then χ is a fixed physical observable the shift MOVES ⇒ the shift is not a symmetry ⇒ 𝒦 cannot be R1-
compensated ⇒ **Branch P**. Otherwise the shift is a redundancy ⇒ **Branch G**.
Sufficiency: χ moves under the shift and is coordinate-invariant, so no other redundancy undoes it. Necessity:
each of N1/N2/N3 has an explicit counterexample below.

**Blind-verifier logical refinement (2026-07-01) — the three legs are NOT independent; minimal driver ≈ N1∧N3:**
- **χ's gauge-rigidity is carried by N1.** A coordinate change cannot undo χ→e^λχ, BUT a field rescaling
  `h_AB→e^{2λ}h_AB` would (it sends √A→e^λ√A, cancelling). That rescaling changes A — a physical observable —
  so it is exactly what N1 (pin √A) forbids. So N1 does more than "pin the angular scale": it makes χ rigid.
- **N2 is meaningful only via N3.** "Radial interval pinned" is a diffeo-invariant statement ONLY when 𝒦≠0
  (r-dependent transverse geometry supplies physical anchors for the endpoints). If 𝒦=0, r is featureless and an
  r-rescale absorbs the shift regardless. So N3 promotes N2 to a genuine pin; the minimal logical content is N1∧N3.

## Result 4 — adversarial tasks (Charles) resolved

- **Task 1 — fixed angular scale ALONE is INSUFFICIENT** ✅ (confirms the sharpening). Pin √A but leave the
  radial extent free (continuum exterior r→∞) ⇒ χ not a fixed finite observable ⇒ shift absorbable ⇒ **G**.
  So "P iff angular size pinned" is FALSE; the correct object is the radial-to-angular RATIO (needs N2).
- **Task 2 — topology ALONE is INSUFFICIENT** ✅. degree(n:S²→S²) is a dimensionless integer — pins winding/
  charge, not a length ⇒ does NOT pin χ. Topology can SOURCE h_AB (help build the cell) but is not the switch.
- **Task 3 — BULK vs BOUNDARY: P is a genuine BULK equation** (given N3), not boundary-only. `∂𝒦/∂φ = -2𝒦 ≠ 0`
  feeds the bulk φ-EL, and `∫√h 𝒦 = -2√(...)∫e^{-2φ}dr` is profile-dependent (NOT a total derivative) ⇒ the
  zero-mode breaking is not boundary-determined ⇒ bulk P (source `-2𝒦`), e.g. round: `Z(r²φ')' = 4e^{-2φ}`.
  **SCOPE (honest):** holds for the action AS CONSTRUCTED (𝒦 a standalone piece). If 𝒦 turns out to be part of
  a total-derivative curvature combination (the open "what is the native geometric action" item), the bulk-vs-
  boundary split could move. → the one thing still gating full bulk-P certainty.
- **Task 4 — minimal invariant** = the aspect ratio **χ** (proper radial extent / transverse scale). Its
  fixation is what forces P.

## Result 5 — regime map (Charles's sharper view, now derived)

- **G governs the bulk** wherever χ is NOT a fixed observable (continuum exterior; unbounded/free radial
  extent) — the shift is a true redundancy → scale-free.
- **P governs the INTERIOR** of a cell that pins χ (finite radial interval + fixed transverse scale + evolving
  transverse geometry) → φ-angular bulk coupling. P is a **cell-interior bulk equation**, NOT the whole finite
  domain automatically — only where χ is pinned and 𝒦≠0.
- **The cell wall / seal** is where χ becomes pinned — the matching layer between G (exterior) and P (interior).

This matches the finite-cell canon (finite mirrored cells; no spatial infinity) and Charles's φ-angular
discreteness hunch — but the derivation ADDED constraints (N2 pinned radial interval; N3 evolving transverse
geometry) and FALSIFIED the naive "fixed angular scale" / "topology alone" versions. It sharpened the prior,
did not rubber-stamp it.

## Premise ledger / scope

| item | status |
|---|---|
| only 𝒦 breaks the shift | DERIVED (CAS) |
| invariant = aspect ratio χ = L_radial/√A; χ→e^λχ | DERIVED |
| N+S criterion (N1∧N2∧N3 ⇔ P) | DERIVED (suff.: χ coord-invariant moves; nec.: counterexamples) |
| fixed-angular-scale-alone / topology-alone insufficient | DERIVED (counterexamples) |
| P is bulk (not boundary-only) | DERIVED **scoped to 𝒦-as-standalone action piece** |
| what IS the native geometric action (𝒦 standalone vs boundary combination) | **OPEN — gates full bulk-P certainty** |
| rides upstream CHOSE levers: R1+P5 (shift rule), constrained-metric form (φ purely longitudinal) | inherited (flagged in the field-eq doc) |

## Hypothesis-discipline note
This confirms the finite-cell→P→φ-angular hunch. It is NOT a rubber-stamp: it added N2/N3 and falsified the two
naive versions. The blind verifier (below) was aimed at REFUTING the sufficiency (find a χ-pinned config where
the shift is still a redundancy) and the bulk claim (find 𝒦 as a total derivative).

## VERIFIER
- **CAS anchors (driver, `switch_criterion_derivation.py`):** only-𝒦-breaks; χ→e^λχ; ∂𝒦/∂φ=-2𝒦; ∫√h R^{(2)}=8π.
- **Blind-adversarial (agent `a72e132c99a545cdb`, 2026-07-01, independent from-scratch sympy + counterexample/
  field-redefinition attacks):** ALL claims **CONFIRMED, none refuted.** Three premise-dependency flags folded in:
  (i) Claim 1 assumes L_m φ-independent (holds — our channel-corrected matter IS φ-blind); (ii) χ-rigidity carried
  by N1 (a h-rescale would undo it; N1 forbids that); (iii) N1/N2/N3 not independent — N2 is diffeo-meaningful only
  via N3, minimal driver ≈ N1∧N3. Round-case (h=r²Ω) specificity noted for the bulk-EL anchors (claims 5–6);
  claims 1–4 hold for general h; the self-similar-h case is where the r-rescale attack comes closest (blocked by N2).

## OPEN (next)
~~Derive what the native geometric action IS (is 𝒦 standalone-bulk or a total-derivative combination?)~~ **RESOLVED
2026-07-01 → `native_geometric_action_results.md`:** 𝒦 is genuinely BULK in the native √h-measure action (4D-EH is
the empty total-derivative red herring) ⇒ **the bulk-P point of this criterion is now UNCONDITIONAL.** New residual:
the native action FORM is motivated-not-unique, and on ROUND h the quadratic invariants are DEGENERATE, so
action-uniqueness must be tested OFF-ROUND. Then (later) the G↔P MATCHING problem at the seal; then a solver.
