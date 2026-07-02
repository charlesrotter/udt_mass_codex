# Embedded-cell seal closure — H_cell = H_ambient (the scale pin) — DERIVED

**Date:** 2026-07-01. **Mode:** gated DERIVE (Charles's go, in-session). **Driver:** Claude Code.
**Script:** `verify_embedded_closure.py` (SymPy; E1/E1b/E2-C1/E2-C2/E3 all TRUE). **Status:**
BLIND-VERIFIED 2026-07-01 (agent `adb6620f`) — central claim SURVIVES. **No wall numbers. No solving.**
**Foundation:** `f2d_virial_step0_results.md` (Step-0 free-boundary transversality, BLIND-VERIFIED),
`seal_matching_junction_results.md` (JC1/JC2), the native-frame docs. **Frozen contract:**
`discreteness_preregistration.md` AMENDMENT 2026-07-01b (Class A EMBEDDED sub-class).

## Why (lay)
The strictly-closed drum (Class A FREE, H=0) has **nothing to set its size** — the first
`cell_solver_f2d` scans confirmed it: from every seed the cell either collapses to a point or
inflates without bound (the Derrick check flags the inflations as spurious). No isolated finite
cell. That is the expected symptom of a cell floating in a void. The **embedded** drum instead sits
inside the universe and shares a movable wall with the surrounding material; the wall settles where
the two "pressures" balance. This note derives that balance condition and shows it is exactly
**H_cell(seal) = H_ambient** — the ambient universe's value pins the cell's size.

## The derivation (native; Weierstrass–Erdmann corner condition for a shared interface)
Two-domain reduced radial action, seal at the shared position r_s:
`S = ∫_{r_c}^{r_s} L̄_cell dr + ∫_{r_s}^{R} L̄_amb dr + S_seal`, both media governed by the SAME
reduced Branch-P Lagrangian L̄ (Step-0 V2), with in general different field values / matter content.

Vary the fields (total endpoint variation Δq, single-valued at the seal) AND the seal position δr_s.
The single variable-endpoint transversality formula (E1, CAS-verified on a concrete L):
`δ ∫_{a}^{s} L dr = ∫ EL·δq dr + π·Δq|_s + (L̄ − q'π)|_s · δs`, with π = ∂L̄/∂q'.
Adding the two domains (the ambient integral carries the seal as its LOWER limit → opposite sign),
the bulk EL terms vanish on-shell and the interface contribution is (E2, CAS-verified):
`δS|_seal = (π_cell − π_amb)·Δq + (H_amb − H_cell)·δr_s + (seal)`, where `H ≡ q'π − L̄`.

Δq and δr_s are INDEPENDENT arbitrary variations ⇒ their coefficients vanish separately:
- **(C1) momentum continuity** `π_cell = π_amb` — the junction conditions JC1 `[√h Z_φ φ']=0`
  (dilation flux) and JC2 (transverse momentum), now for cell-meets-AMBIENT (not cell-meets-vacuum-G).
- **(C2) Hamiltonian continuity** `H_cell(r_s) = H_amb(r_s)` — **the embedded closure.**

`H` here is exactly the conserved radial Hamiltonian already in the solver (`cell_solver_f2d.H_of_r`)
and Step-0 (V4/V5): E3 (CAS) confirms the θ-integrated corner quantity `Σ_q q'π_q − L̄` EQUALS the
solver's `H_of_r` expression. So the quantity the solver already monitors IS the corner quantity.

## Reduction to the closed cell (consistency)
If the ambient is vacuum (`L̄_amb = 0`, no fields ⇒ `H_amb = 0`), C2 becomes `H_cell = 0` — precisely
Step-0's closed-cell condition (V5, already blind-verified). The embedded result is the one-line
generalization from `H_amb = 0` to `H_amb ≠ 0`. C1 with vacuum gives `π_cell = 0` = the mirror-fold
Neumann BC. So closed (Class A FREE) and embedded (Class A EMBEDDED) are the two ends of one derived
structure — as the Step-0 headline anticipated.

## The scale pin (why this fixes the runaway)
For the closed cell the rigid winding forces `H_cell(seal) ≈ −0.97 ≠ 0` at every size (the fixed-L
scan) — the closure is unreachable, so no finite cell. With `H_cell = H_amb` the target is no longer
0 but the ambient value, set by the universe cell's own solution at the cell's location. Because
`H` is the native analog of the Misner–Sharp mass/density (Q = 2 p_F; Misner–Sharp = the cell's
public charge — CANON), **H_amb is the ambient Misner–Sharp density**: the surrounding universe's
density selects which cell sizes can close. This reproduces natively the project's recurring
indication that particle formation requires a specific ambient density / narrow band — here as the
MECHANISM of scale selection, not a side effect.

## Premise ledger (chose / derived)
| # | Premise | tag |
|---|---------|-----|
| 1 | Exterior = ambient UNIVERSE INTERIOR (a Branch-P/matter solution), not vacuum G | THEORY (finite-cell canon; universe is a solution of the same equations) |
| 2 | Seal position r_s is a free variable of the TOTAL action (both media adjust) | CHOSE (embedded analog of Step-0's "r_s dynamical"; alternative = seal externally pinned) |
| 3 | Seal is smooth / source-free (Class A EMBEDDED); φ, ρ, momentum continuous | CHOSE (source-free first; a seal source term S_seal adds to C1/C2 → Class B) |
| 4 | H_amb set by the universe cell's own solution at the seal (its M–S density) | THEORY (same equations govern the universe cell) — but its VALUE is DERIVATION-OWED (below) |
| 5 | Both media use the same reduced L̄ (Branch P, W=1) | THEORY (both are interior cells) — the universe cell's regime (P vs a large-χ limit) is to confirm |

## Scope / what is and is NOT established
- **Established (CAS):** the corner conditions C1 (momentum continuity) and C2 (`H_cell = H_amb`)
  from the shared-interface variation; the identity that the solver's H is the corner quantity;
  the closed-cell (H=0) reduction.
- **Owed:** (a) BLIND adversarial verification of this derivation (the free-endpoint/corner argument
  and the sign of C2 are the load-bearing pieces). (b) The VALUE `H_amb` from an actual universe-cell
  solution (not just "some ambient constant") — i.e. solve/constrain the universe cell and read its
  H at the matter cell's location; until then `H_amb` is a derived-but-unquantified constant. (c)
  Whether `H_cell = H_amb` actually ADMITS an isolated finite cell (the next solve — DO NOT assume it
  does; the closed cell taught us the closure can be unreachable). (d) Class-B (seal source) variant.
- **Pre-reg tie-in:** this is the Class A EMBEDDED sub-class registered in AMENDMENT 2026-07-01b; the
  9 acceptance criteria are unchanged; `H_amb` is held FIXED per scan (one ambient state at a time),
  it is NOT a per-solution knob.

## VERIFIER
**Blind adversarial pass — 2026-07-01, agent `adb6620f`. Central claim `H_cell=H_amb` SURVIVES.**
A fresh zero-context verifier re-derived the two-domain interface variation FROM SCRATCH with a
DIFFERENT concrete Lagrangian and independently checked every load-bearing piece:
- **C1 (π_cell=π_amb) PASS**; **C2 (H_cell=H_amb) PASS — sign confirmed TWO independent ways**
  (assembly route + an explicit (interface-value v, position s) route); explicitly ruled out the
  wrong signs `(H_cell−H_amb)` and `(H_amb−2H_cell)`.
- **#1 (is r_s legitimately free?) PASS-with-caveat** — a standard Weierstrass–Erdmann free-corner
  variation between two media; the "single-valued Δq at the seal" treatment is correct (the (v,s)
  formulation gives the identical result); physical assumptions (free interface, both media adjust,
  source-free) honestly tagged CHOSE, not smuggled.
- **#3 (C1,C2 independent?) PASS** — v and s are independent DOFs; H is not implied by π-continuity;
  L̄ autonomous in r ⇒ H conserved per domain ⇒ C2 pins the two conserved constants (non-vacuous
  precisely because the fields kink at the seal / distinct matter content).
- **E1 PASS (not hollow)**; **E3 PASS and closed for GENERAL f** (the verifier verified the Legendre/
  Hamiltonian identity at the density level for generic f, exercising the f_r-kinetic moments I_r,
  I_4r that vanish at rigid f=θ).

**Three artifact-honesty gaps the verifier flagged, now FIXED in `verify_embedded_closure.py`:**
(1) dead `*0`/`if False` cruft removed; (2) **E1b added** — the ambient LOWER-limit sign flip that E2
relied on is now independently derived in-script (was hardcoded); (3) **E3 upgraded to GENERAL f** at
the density level (was rigid-f only, which never exercised I_r/I_4r). Re-run: E1/E1b/C1/C2/E3 all TRUE.
The verifier's from-scratch re-derivations are its record; the script now matches the claim.
