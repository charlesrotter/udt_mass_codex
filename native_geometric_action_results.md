# The Native UDT Geometric Action — the angular-curvature-mismatch action (closes the G/P gate)

**Date:** 2026-07-01. **Provenance:** derivation by Charles (in-session); driver CAS disposal
(`verify_native_geo_action.py`); blind-adversarial verifier recorded below. **Status:** DERIVED/verified
GIVEN the action FORM; the action-form's UNIQUENESS is the new residual (flagged). NOT canon.
**Builds on + closes the OPEN gate in:** `gp_switch_criterion_results.md` (the "is 𝒦 bulk or boundary-split?"
question that made the switch criterion conditional).

---

## Result — the native geometric action

    S_geo = ∫ dt dr d²x  c√h [ (Z_φ/2)φ'² + R^{(2)}[h] + W_χ(φ)·𝒦 ]
    𝒦 = K_AB K^AB − K² ,   K_AB = ½ e^{-φ} ∂_r h_AB ,   √-g = c√h (φ-free)
    W_χ(φ) = e^{2φ}  (χ free / depth-shift gauge / Branch G)
           = 1       (χ pinned / finite angular cell / Branch P)

This is the action-level form of the G/P switch: the branch is the weight `W_χ` on the transverse
extrinsic term, and `W_χ` is fixed by whether the aspect ratio χ is a pinned observable (per
`gp_switch_criterion_results.md`). **Not bare EH** — see the gating result below.

---

## Derivation skeleton (Charles) + CAS disposal (all round-case checks exact)

1. **Only 𝒦 carries the depth-shift weight** among the local 2nd-order transverse scalars
   (`R^{(2)}`, `K_AB K^AB`, `K²`, `φ'²`): `K_AB→e^{-λ}K_AB` ⇒ `𝒦→e^{-2λ}𝒦`. (verified)
2. **`R^{(2)}+𝒦` is the Gauss angular-curvature MISMATCH** (intrinsic-plus-extrinsic). For a flat round
   foliation (`h=r²Ω`, φ=0): `R^{(2)}=2/r²`, `𝒦=−2/r²`, so `R^{(2)}+𝒦=0` — the correct flat cancellation. (verified)
3. **Branch G (shift is gauge):** every bulk term must be shift-invariant; since `𝒦→e^{-2λ}𝒦`, the compensated
   invariant is `e^{2φ}𝒦`. Round: `R^{(2)}+e^{2φ}𝒦 = 2/r² − 2/r² = 0` for ANY φ → the angular sector cancels in
   the G exterior, leaving only the kinetic → `Z_φ(r²φ')'=0`. (verified)
4. **Branch P (χ pinned, shift physical):** 𝒦 uncompensated; `∂𝒦/∂φ = −2𝒦 ≠ 0`. Varying (measure √h):
   `∂_r(√h Z_φ φ') = −2√h 𝒦` → round: `Z_φ(r²φ')' = 4e^{-2φ}`. (verified, up to overall EL-sign convention)

---

## THE GATING RESULT — 𝒦 is genuinely BULK in the native action (EH is the empty red herring)

The `gp_switch_criterion_results.md` bulk-P claim was conditional on "is 𝒦 a standalone bulk term, or part of
a total-derivative curvature combination?" Resolved (CAS):
- **Native action (measure √h):** `√h·𝒦 = −2e^{-2φ}sinθ` is NOT a total r-derivative (profile-dependent) →
  **𝒦 is genuinely BULK.** (The `R^{(2)}` piece `√h·R^{(2)}=2sinθ = d/dr(2r sinθ)` IS boundary — so all the
  bulk φ-content sits in 𝒦.)
- **4D EH (measure √-g):** `√-g R = c sinθ·d/dr[…]` is a pure boundary term (empty) — established in
  `native_field_equations_constrained_two_player_results.md`.
- **The native action is neither 3D-EH nor 4D-EH:** `R^{(3)} = R^{(2)}+𝒦 + 4e^{-2φ}φ'/r` (so the native
  integrand `R^{(2)}+𝒦` is NOT the 3-Ricci scalar), and the native measure is `√h`, not `√g₃=e^φ√h`.

**Conclusion:** 𝒦's bulk-ness is real; EH "hides" it only because EH (the `√-g R` combination) is a total
derivative on this family — i.e. EH is the WRONG native action (the Principle-7 scar). **⇒ Branch P is a genuine
bulk cell-interior equation; the switch criterion is now UNCONDITIONAL on the bulk-vs-boundary point.**

---

## OFF-ROUND UNIQUENESS + the Z_φ FORK (2026-07-01, added; CAS `verify_offround_uniqueness.py`; blind-verified)

Charles's off-round derivation (the round degeneracy forced this). Two results:

**(A) 𝒦 = K_AB K^AB − K² is UNIQUELY forced off-round; an independent K² is EXCLUDED.** For any 2-surface in a
LOCALLY FLAT 3-geometry, Gauss gives `R^{(2)} = K² − K_AB K^AB` (verified off-round on a paraboloid: both =
2/(ρ²+1)²). Demand the angular action assign ZERO mismatch to flat geometry: `a R^{(2)} + b K_AB K^AB + d K² = 0`
⇒ (using Gauss) `(b−a)K_AB K^AB + (d+a)K² = 0` for ALL shapes ⇒ **b=a, d=−a**. Normalizing a=1 gives exactly
`R^{(2)} + K_AB K^AB − K²`. An added `α K²` is nonzero for a flat off-round embedding → assigns false bulk cost to
flat space → excluded. **This closes the K²-ambiguity residual** (which round-h could not resolve — the invariants
were degenerate). SCOPE (premises, honest): unique WITHIN the class {built from R^{(2)},K_AB K^AB,K²; no false
curvature on flat; same W_χ weight on the extrinsic block; NO derivative-mixing}.

**(B) Z_φ (the longitudinal kinetic normalization) is a genuine FORK — NOT fixed by current principles.**
- Angular flatness does not touch φ'² (φ' absent from Gauss) → Z_φ free from (A).
- R1 shift symmetry fixes the FORM φ'² (φ' invariant) but not its coefficient → Z_φ free from shift.
- ONE principle fixes it: derive the kinetic from the R1-weighted longitudinal (t,r)-block curvature. `R_L =
  2e^{-2φ}(φ''−2φ'²)` (CAS); `e^{2φ}R_L = 2φ''−4φ'²`; `−e^{2φ}R_L` integrated with √h (IBP, `(√h)'=√h e^φ K`) →
  `4φ'² + 2e^φ K φ'`. So **Z_φ=8, D=2** — BUT this FORCES a mixed longitudinal-transverse term `2e^φ K φ'`.
- **The fork:**
  - **Route A (sector-orthogonal, no derivative mixing, D=0): Z_φ FREE** (the currently-banked action).
  - **Route B (longitudinal-curvature completion): Z_φ=8, and the action gains `2e^φ K φ'` (D=2).**
- The `e^φ K φ'` derivative-mixing term is the crux: excluded-by-premise in A, forced in B. **Recorded as a real
  fork; consilience (a fitted-constant-free particle spectrum) could later select between them — the math alone
  does not.**

## RESIDUAL (updated) — Z_φ / derivative-mixing fork (was: action-form uniqueness)

The angular EXTRINSIC structure is now UNIQUE (section above: off-round angular-flatness excludes independent K²,
fixing 𝒦=K_AB K^AB−K²). What remains OPEN is the **longitudinal kinetic normalization Z_φ and the derivative-mixing
term**, a genuine FORK:
- **Route A (sector-orthogonal, the banked action): Z_φ FREE**, no `e^φ K φ'` term.
- **Route B (longitudinal-curvature completion): Z_φ=8**, action gains the mixed `2e^φ K φ'` (D=2).
Neither is forced by angular flatness or R1 shift symmetry alone; Route B needs the extra "kinetic-from-weighted-
longitudinal-curvature" premise (which also brings the mixing term). Consilience (a fitted-constant-free spectrum)
could later select; the math alone does not. (Historical note: round-h could not even pose the K² test — the
invariants were degenerate; the off-round derivation resolved it.)

## Premise ledger
| item | status |
|---|---|
| only 𝒦 carries the shift weight; G/P round cancellations; S_G, S_P EL | DERIVED (CAS) |
| 𝒦 genuinely BULK in the √h-measure action; 4D-EH empty | DERIVED (CAS) — closes the switch-criterion gate |
| angular extrinsic term 𝒦=K_AB K^AB−K² (independent K² EXCLUDED) | DERIVED off-round (angular-flatness; CAS) — closes the K² residual |
| W_χ = e^{2φ}(G)/1(P) fixed by χ-pinning | DERIVED (from `gp_switch_criterion_results.md`) |
| **Z_φ normalization + `e^φ K φ'` mixing term** | **OPEN FORK: Z_φ free (route A) / Z_φ=8 + D=2 (route B)** |
| the angular-flatness / no-derivative-mixing / same-W_χ premises of the uniqueness class | CHOSE (named) |
| rides upstream CHOSE: constrained-metric form; R1+P5 shift levers | inherited |

## VERIFIER
- **CAS (driver, `verify_native_geo_action.py`):** G/P round cancellations; e^{2φ}𝒦 φ-free; S_G/S_P EL;
  √h𝒦 bulk (not total deriv); R^{(3)}=R^{(2)}+𝒦+4e^{-2φ}φ'/r; native action ≠ 3D/4D-EH. ALL confirmed.
- **Blind-adversarial (agent `ad0a086f9944c5426`, 2026-07-01, independent from-scratch sympy + total-derivative/
  uniqueness attacks):** ALL claims **CONFIRMED, none refuted.** 𝒦-is-bulk verified by the no-local-antiderivative
  argument; R^{(3)}=(R^{(2)}+𝒦)+4e^{-2φ}φ'/r exact; native action ≠ 3D-EH (√g₃R^{(3)} leaves irreducible bulk
  2(e^{φ}+e^{-φ})) ≠ 4D-EH (empty). Uniqueness: CONFIRMED motivated-not-unique + the ROUND-h DEGENERACY finding
  (K²/K_ABK^AB/𝒦 all ∝ e^{-2φ}/r² on round-h → uniqueness must be tested off-round). Scope: all headline numbers
  are round-h + static φ(r); on general h the three quadratic invariants are independent.

## OFF-ROUND / Z_φ VERIFIER
- **CAS (driver, `verify_offround_uniqueness.py`):** off-round flat Gauss identity R^{(2)}=K²−K_ABK^AB (paraboloid,
  both 2/(ρ²+1)²); uniqueness algebra b=a,d=−a; R_L=2e^{-2φ}(φ''−2φ'²); e^{2φ}R_L=2φ''−4φ'²; IBP→4φ'²+2e^φKφ'
  (Z_φ=8,D=2 route B). ALL confirmed.
- **Blind-adversarial (agent `a85ac2c0954a1bdd9`, 2026-07-01, independent embeddings from scratch — paraboloid +
  ellipsoid for the Gauss identity, general h_AB for B-5):** ALL 7 claims **CONFIRMED, none refuted.** Sharpenings:
  (i) the K²-exclusion is valid quantified over the FULL off-round family — a single minimal surface (K≡0, pins only
  b=a) or umbilic patch (collapses both invariants) is insufficient; non-minimal/non-umbilic members restore both
  constraints. (ii) B-5 is the Jacobi formula (convention-robust). (iii) Route B's Z_φ=8 and D=2 are an INSEPARABLE
  package (both IBP products of the one integrand 2φ''−4φ'²) — no principle gives Z_φ=8 without the mixing term; and
  that forced mixing term `2√h e^φ K φ'` IS a φ-angular coupling (dilaton gradient × transverse expansion), forced
  by the algebra, not imposed — dropping it while keeping Z_φ=8 would be inconsistent with its own derivation.

## OPEN (next candidates)
1. **Z_φ / derivative-mixing FORK** (the residual above) — route A (Z_φ free, sector-orthogonal) vs route B (Z_φ=8
   with forced `e^φKφ'`). Not settleable by the current geometric principles; a candidate for CONSILIENCE selection
   (does a fitted-constant-free spectrum pick one?). The angular extrinsic term is now UNIQUE (K² excluded off-round).
2. Then the **G↔P matching problem** at the seal (where χ gets pinned), and only after that a constrained-two-
   player SOLVER.
