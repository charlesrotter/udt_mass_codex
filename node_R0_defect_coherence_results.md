# R0 — The bare π₂ S² defect does NOT cohere on N=0 (global monopole); redirect to the native π₃ HOPFION

**Status: BANKED (blind-verified). A load-bearing NEGATIVE + a corpus correction + a native LEAD (π₃).**
Deriver a6f0c2f868005223f; blind adversarial verifier aa69f2e6532adffd8 (FAIL-WITH-REVISIONS: core
confirmed + strengthened, 2 revisions). Armchair/CAS, no numeric solve, data-blind. Fork-3b reframe, NODE-R0
of `microphysics_after_concentric_failure_MAP.md`.

## R0 verdict: FAIL — the native degree-1 π₂ defect cannot be a finite-energy LOCALIZED particle (seal-free)

The bare native π₂ winding (unit hedgehog n=x̂, Θ≡θ, no radial profile) is a **GLOBAL MONOPOLE**:
- L2 density = ξ/r² (solid-angle-deficit / "global-monopole" stress, T^t_t=T^r_r=−ξ/r²); per-shell energy
  dE/dr = 4πξ = CONSTANT ⇒ **E = 4πξ·R grows linearly with box** — the energy is smeared over the whole
  universe cell, NOT a localized lump.
- **The scissors (airtight, topological):** deg(n|_{S_r})∈ℤ is continuous in r ⇒ constant unless n unwinds.
  Protected (deg=1 on every enclosing sphere) ⇒ per-shell floor ⇒ delocalized. To localize (n→const,
  deg→0) the field must UNWIND at an outer edge = a SEAL, which THROWS AWAY the protection.
  **Protected ⇔ delocalized. Cannot have both on L2+L4.**
- **The ambient is INVISIBLE to the static φ-blind defect** (verified A1): √h=r²sinθ is φ-free (B=1/A);
  the angular channel is shift-weight-1 / φ-blind (δS_m/δφ=0, canon C-2026-07-05-1); ρ=r is a theorem
  (C-2026-06-10-1); L4's area-form norm is metric-free. So "the medium bounds the defect" (MAP §4) is FALSE.
- **Loophole CLOSED (verifier strengthening):** the one open channel — transverse back-reaction
  n→h_AB→𝒦→φ — cannot help: the per-shell winding energy obeys the **Bogomolny bound
  ∫_{S_r}(ξ/2)|∇n|²_h dA ≥ 4πξ·|deg|, a 2D CONFORMAL INVARIANT** independent of the transverse metric h_AB
  (any size/shape). No throat/areal saturation lowers the 4πξ floor while deg=1. Delocalization survives
  FULL transverse back-reaction.
- Native IR-regulators all eliminated: V(n) forbidden under full target SO(3) (F2, blind-verified —
  caveat: if SO(3)→SO(2) later, V re-enters); L4/L6 are IR-convergent (fix the core, not the r⁻² tail);
  ρ=r kills areal saturation.

**Clean-failures that genuinely fire:** #1 (finite-localized needs the unwinding seal) + #3 (localization
needs the cell edge = a box). NOT #2 (deg-1 doesn't unwind) — that is the whole point of the scissors.

## Revisions (verifier)
1. **Disqualifier = DELOCALIZATION, not non-finiteness.** On the finite N=0 cell E₂=4πξ·r_cell is FINITE —
   but universe-smeared (a global charge, not a particle). R0's failure is "not LOCALIZED."
2. **R0's import-flag was MIS-AIMED — corrected.** Θ(core)=π is NATIVE core regularity (n→const at the
   origin), NOT a smuggled S³-Skyrme BC. The genuine problem is Θ(seal)=0 at finite radius = the unwinding
   SEAL. **CORPUS CORRECTION (sharper):** the committed native_stabilizer "sized √(κ/ξ) soliton"
   (`native_profile_bvp.py:10`) uses a **NON-UNIT-NORM ansatz** |n|²=1−cos²θ·sin²Θ ≠ 1 — an S³-Skyrme
   *profile* form mis-fitted onto the S² 3-vector target. **It was never a clean protected unit-S² π₂
   object; its "charge 1" via Θ:π→0 is not the π₂ degree of a unit field.** (Matches the corpus's own
   flagged "S² defect vs imported S³ Skyrme" tension.) native_stabilizer's √(κ/ξ) soliton is thereby
   flagged CONDITIONS-CHANGED / import-held.

## THE REDIRECT — native L2+L4 IS the Faddeev–Skyrme model; its native soliton is the π₃ HOPFION

**NATIVE-CANDIDATE (verified A5), does NOT clash with N=3.** The native action L2 (Dirichlet O(3) sigma) +
L4 (=|ω_H1|² Faddeev/Skyrme term) on the unit 3-vector n:R³→S² is EXACTLY the **Faddeev–Niemi model**, whose
native solitons are **HOPFIONS** — knotted, finite-energy, LOCALIZED, SEAL-FREE, classified by the Hopf
charge Q_H∈π₃(S²)=ℤ (a linking/knotting number, Q_H=∫A∧dA, F=dA the pullback area form):
- **evades the scissors:** n→const at ∞ (not a point defect) ⇒ no per-shell degree, no r⁻² floor ⇒
  genuinely finite + localized (Vakulenko–Kapitansky bound E ≳ |Q_H|^{3/4}); size fixed by √(κ/ξ) via L4.
- **native, no import:** same unit 3-vector, same S² target, same DERIVED L2+L4 action — no S³ target.
- **no clash with N=3:** the Hopf map is S³→**S²** (target still S^{N−1}, N=3); π₃(S²)=ℤ exists PRECISELY
  because π₂(S²)=ℤ (the Hopf fibration) — π₃ rides on the same S² that D1's N=3 selects. Only the READING of
  "the charge" changes: from a boundary 2-form degree (π₂, D1 Forcing-A) to a **bulk 3-form linking number**
  (π₃). N=3 (Forcing-B, target rank) is untouched.
- **discreteness:** Q_H∈ℤ is a NATIVE INTEGER = the INTERIOR/TOPOLOGICAL discreteness the constraint
  generator (MAP §9-5) demanded — not a seal, not an ω_n tower. R1's "interior holonomy" hope is realized
  concretely as the Hopf linking number.

**Status: a LEAD, not banked.** It owes a genuine derivation that native L2+L4 admits a Q_H=1 hopfion on the
N=0 background (a gated R3-class solve), plus re-expressing "charge" as the Hopf linking number. Orchestra
caveat also stands (R0 tested the SOLO static defect; multi-defect ensembles not addressed).

## Premise tags
- per-shell 4πξ|deg| floor, conformal-invariant (loophole-closing) = DERIVED (verifier CAS + Bogomolny).
- √h φ-free, angular weight-1, δS_m/δφ=0, ρ=r = THEORY (native field eq; C-2026-06-10-1; C-2026-07-05-1).
- corpus √(κ/ξ) soliton = non-unit-norm S³-mis-fit = DERIVED (verifier, native_profile_bvp.py:10).
- π₃ hopfion native, finite+localized+seal-free, N=3-compatible = NATIVE-CANDIDATE LEAD (owes the solve).
- static scope = CHOSE (ω≠0 canon-closed C-2026-07-05-1); full-SO(3) (V forbidden) = load-bearing THEORY.
