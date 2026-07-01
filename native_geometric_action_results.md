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

## RESIDUAL (the new open item) — action-form uniqueness

The derivation MOTIVATES the action form (`R^{(2)}+𝒦` = Gauss angular-mismatch; `√h` = the 4D `√-g`) but does
NOT prove it UNIQUE. The native action is a foliation-adapted construction, distinct from 3D-EH (`√g₃ R^{(3)}`,
which CAS shows is also NOT a total derivative here — a third, different action) and 4D-EH (empty). So:
- **𝒦 is bulk GIVEN this action form** — solid.
- **Whether this is the unique admissible native geometric action** — OPEN. Other admissible local 2nd-order
  combinations (e.g. adding `(K)²` with an independent coefficient, or an `X`-type kinetic ratio) are not yet
  excluded. This is the residual that a "minimality/uniqueness" derivation must settle.
- **Blind-verifier sharpening (load-bearing for the uniqueness test):** on ROUND h, `K²`, `K_AB K^AB`, and `𝒦`
  are ALL ∝ `e^{-2φ}/r²` — mutually DEGENERATE — so a free `K²` coefficient merely rescales the same structure
  and cannot be excluded in the round case. **Uniqueness can only be tested on GENERAL (non-round) h**, where the
  three quadratic invariants become independent. ⇒ the action-uniqueness derivation must go off-round.

## Premise ledger
| item | status |
|---|---|
| only 𝒦 carries the shift weight; G/P round cancellations; S_G, S_P EL | DERIVED (CAS) |
| 𝒦 genuinely BULK in the √h-measure action; 4D-EH empty | DERIVED (CAS) — closes the switch-criterion gate |
| the native action FORM (√h × [kinetic + R^{(2)} + W_χ𝒦]) | **MOTIVATED, not proven unique** (residual) |
| W_χ = e^{2φ}(G)/1(P) fixed by χ-pinning | DERIVED (from `gp_switch_criterion_results.md`) |
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

## OPEN (next candidates)
1. **Action-form uniqueness/minimality** (the residual above) — is `√h[kinetic + R^{(2)} + W_χ𝒦]` the unique
   admissible native geometric action, or are there other admissible terms (independent K², X-ratio, ...)?
2. Then the **G↔P matching problem** at the seal (where χ gets pinned), and only after that a constrained-two-
   player SOLVER.
