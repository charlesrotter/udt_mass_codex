# H4 · N4a — Source/background audit: FAIL → the far-field monopole is AMBIENT-SCREENED (a frame question, not a budget limit)

> **★ REFINED (2026-07-05, `H4_screening_taxonomy_MAP.md`, blind-verified):** the screening TERM + frozen indicial
> roots below STAND, but the extrapolation to a *persistent log-periodic* far field was frozen-W-conditional and
> does NOT survive the running ambient. The true φ_amb(r) runs (φ_amb≈½ln((8/Z_φ)ln r)) ⇒ W=e^{−2φ_amb}→0 ⇒ the
> clean 1/r monopole is RECOVERED over all physical radii (exactly in Branch-G/shallow); the oscillation is a
> bounded near-core skirt that never completes a cycle. So **"log-periodicity = discreteness" is DEAD**, and N4a's
> screening is REFINED to *at most a MARGINAL LOGARITHMIC* (non-oscillatory, non-conserved-flux, physically-moot
> for a finite cell) tail at strict r→∞ — NOT overturned. Net: the far field is *nearly* (not strictly)
> branch-blind; the real branch fork is INTERIOR (active-P vs dead-G). See the taxonomy MAP for the full verdict.
>
> **LABEL FIX (2026-07-05, revised-N4 `H4_N4rev_...`):** below/elsewhere this doc says "DEEP ⇒ screened/oscillatory"
> — that is BACKWARDS. Complex (oscillatory) roots need W₀=e^{−2φ_amb}>Z_φ/32 ⇔ **φ_amb < ½ln(32/Z_φ) = SHALLOW.**
> So **SHALLOW = strong-screening/oscillatory; DEEP = clean.** The running ambient DEEPENS outward ⇒ clean recovered
> at large r. Physics unchanged; only the shallow/deep labels are corrected.

**Status: BANKED, blind-verified (2026-07-05). Outcome = FAIL (revise N4 before any response solve) + reclassify
the banked N4 from D-budget to D-SOURCE-FRAME.** Audit agent a37ebac2cb6d74620; blind adversarial verifier
aac5cfdbb07e82dc9 (verified the catch two independent ways; adjudicated the N2 rescue; confirmed the
reclassification). Armchair/CAS + bounded-numeric on the SAVED source only (no mass solve, no L⁻¹ solve, no
hopfion re-solve). DATA-BLIND; Z_φ symbolic; no ξ-anchor; no open decision taken. Scripts:
`h4_scripts/verify_screening.py`, `n4a_ell_audit.py`.

## The catch (load-bearing; reaches into banked N2)
The Branch-P φ-equation ∂_r(√h Z_φ φ') = −2√h𝒦 has a **φ-DEPENDENT source** (round: RHS = 4e^{−2φ}). Linearizing
φ = φ_amb(r) + ε·δφ about the true N=0 ambient, the EXTERIOR (matter stress T=0) perturbation equation is NOT the
source-free Euler equation (r²δφ')'=0 → δφ=−δq/r that N2/N4 used, but a **screened operator**:
```
Z_φ (r² δφ')' + 8 e^{−2φ_amb} δφ = 0        (verified 2 ways: direct ∂/∂φ of 4e^{−2φ}; and via N1's ∂𝒦/∂φ=−2𝒦)
```
Indicial roots (r^s, e^{−2φ_amb}=W₀ locally frozen — a legitimate Frobenius/WKB criterion):
```
s = −1/2 ± √(Z_φ − 32 W₀) / (2√Z_φ)
```
- **W₀ = 0** (or ≪ Z_φ/32, shallow ambient): roots {0, −1} → const + **1/r Coulomb** = N2's clean monopole. Recovered.
- **W₀ < Z_φ/32:** two real roots; δφ decays with a SHIFTED exponent ≠ 1 (not a clean 1/r).
- **W₀ > Z_φ/32** (deep ambient; critical depth φ_amb = ln(4√2) ≈ **1.73** at Z_φ=1, ≈0.69 at Z_φ=8): COMPLEX roots
  ⇒ δφ ~ **r^{−1/2} cos(ω ln r)**, ω = √(32W₀−Z_φ)/(2√Z_φ) — **log-periodic oscillation, NO clean monopole mass.**
The operator is scale-invariant (Euler) ⇒ there is no fixed "screening length"; it is log-periodic. Physical
conclusion (no scale separation from ℓ_hopf≈1.1, no clean far-field monopole above critical depth) stands.

**Why N2 missed it (order counting — the decisive point):** the screening term 8e^{−2φ_amb}δφ is O(ε¹) in the
perturbation AND O(amp²) in the hopfion amplitude — EXACTLY the same order as the kinetic term Z_φ(r²δφ')' and as
δq itself. It cannot be dropped on order grounds; only a SHALLOW background (W₀ ≪ Z_φ/32) shrinks it. N2 conflated
"matter-source-free" (T=0) with "source-free": T=0 kills the matter stress but NOT the φ-dependent GEOMETRIC 𝒦
source, which is present in the round Branch-P ambient. N2 had itself half-seen this (its Task 4: "round+φ≡0 is
NOT a vacuum of E^{AB}") but applied it only to the SHEAR sector, never to its own MONOPOLE — the internal
inconsistency the audit exposes.

## The resolution — it reduces to the OPEN G/P switch criterion (verifier's symmetric completion)
The shallow-ambient escape is EQUIVALENTLY the **Branch-G / continuum-exterior** regime, which
`native_field_equations_constrained_two_player_results.md` §6/§10 names as the NATURAL exterior:
- **Branch-G exterior** (source-free, (√h Z_φ φ')'=0): δφ = −δq/r EXACTLY — **N2's clean monopole mass holds.**
- **Branch-P deep ambient:** screened / log-periodic — **no clean monopole mass.**
⇒ **Whether the hopfion has a clean far-field mass is set by the (OPEN) G/P switch criterion for its far field**,
equivalently by how deep it sits in the cell's φ-profile (a DATA-BLIND, unpinned location). This is a genuine
FRAME/SOURCE question — no bounded L⁻¹ response-solve budget resolves it, because the far-field operator FLIPS
CHARACTER (real power-law ↔ complex-oscillatory) at the critical depth.

## Target grades (audit + verification)
- **T1 (H3 stress valid as source): PASS.** ρ=r theorem + φ-blind ⇒ bare metric exactly Euclidean ⇒ field n and
  stress T^{AB} correct (regenerated: E=286.52, E2/E4=0.9995, virial to 14 digits). The dropped feature is NOT in
  the source — it is in the response OPERATOR (T4). The linear background×perturbation cross-term is a total
  r-derivative (→0), consistent with N2.
- **T2 (regime P/G exterior): FAIL.** Branch P has NO source-free exterior (ambient 𝒦_amb=−2e^{−2φ_amb}/r² sources
  φ everywhere). The "G-like source-free tail" was the error; the correct far field is either Branch-G (clean) or
  screened Branch-P.
- **T3 (L⁻¹ BCs / radius-independence): FAIL.** ∂_rΠ_φ = −2√h𝒦 ≠ 0 in the P-ambient ⇒ the φ-flux physically LEAKS
  with radius. N2's "radius-dependence = numerical box-control" diagnostic is a **Branch-G property only**; in P it
  misreads a physical distributed source as an artifact.
- **T4 (rebuild operator on true φ_amb): FAIL — the core finding.** The bare-Euler operator (roots 1,2 for δh;
  {0,−1} for δφ) is the locally-flat/source-free approximation; the true operator carries +8e^{−2φ_amb}δφ and must
  be rebuilt on φ_amb(r) before any BVP. N4 flagged "the true-φ_amb correction" as owed but SCOPED it to the shear
  exponent while presenting the mass-bearing MONOPOLE as SOLID — under-scoped onto the load-bearing channel.
- **T5 (ℓ=0/ℓ=2 adequate): PASS.** ℓ4/ℓ2 = 0.6% (τ), 1.9% (shear); ℓ6/ℓ2 ≤ 1.3% — all ≪ the H3 floor. ℓ=0/ℓ=2
  truncation adequate (carry ℓ=4 as a cheap ~1–2% cross-check).
- **T6 (no smuggled private seal): PASS.** The screening is a property of the distributed AMBIENT-MEDIUM 𝒦 source
  (Branch-P's finite-domain character is DERIVED, not imposed), NOT a wall. Frame C(a) intact; the retired
  sealed-cell/depth-stiffness frame is NOT revived.

## Consequences (applied to the banked docs)
1. **N2 — CONDITIONS-CHANGED (conditional, not dead):** its clean monopole δφ=−δq/r and its radius-independence /
   box-control diagnostic are valid ONLY on a source-free (Branch-G / continuum) or shallow-ambient
   (e^{−2φ_amb} < Z_φ/32) far field. On a deep Branch-P ambient the far field is screened/log-periodic with no
   clean monopole. Flagged in `H4_N2_farfield_reduction_results.md`.
2. **N4 — reclassified D-BUDGET → D-SOURCE-FRAME:** the CF1/CF2 gap is not merely unfinished compute; it includes a
   genuine frame uncertainty (does a clean monopole mass exist at the unpinned depth) resolved only by the G/P
   switch. The bare-Euler BVP would return a SPURIOUS clean monopole (a false-clean answer) and MUST NOT be run
   as-was. Flagged in `H4_N4_backreaction_solve_results.md`.
3. **The revised N4 (when re-authorized) must:** (a) rebuild the linearized monopole + shear operator on the TRUE
   φ_amb(r) with the +8e^{−2φ_amb}δφ screening term; (b) determine the far-field character as a function of the
   ambient depth / the G/P assignment; (c) report the mass CONDITIONALLY (clean δm=−δq in Branch-G/shallow;
   screened/no-clean-monopole in deep-P). This is genuinely gated on the OPEN G/P switch criterion.

## What survives intact
The H3 stress source (T1); the ℓ=0/ℓ=2 truncation (T5); frame C(a) / no private seal (T6); and the Phase-A
ALGEBRA of N4 (g₁ total-derivative → only δh^(1) needed; flux = ½⟨T,L⁻¹T⟩) — correct UNDER its source-free-exterior
premise, which the P-ambient violates (so the algebra is a Branch-G / shallow-ambient statement). Method note: this
frame error was caught by a source/background AUDIT (Charles-requested) BEFORE compute, and it reached into a
DOUBLY blind-verified banked result — a make-visible-early win.
