## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-11 |
| **Mode** | DERIVE→VERIFY→OBSERVE — `UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md`. Phases A + B + C done; D/E pending. |
| **Object** | banked H3 Q_H=1 carrier ONLY (`prod_an256.npz`). NEVER f2d π₂ hedgehog. |
| **Device** | V100, float64, one process. |
| **Observing or targeting?** | OBSERVE whether a clean cutoff-independent local mass exists under the frozen action. Aimed HARDEST at the load-bearing positivity ρ+S=2ρ_4≥0 and at the EH-action premise (the comfortable answer is a clean mass — do not over-claim it). |
| **Verifier status** | Section-2 identities machine-verified on the real H3 field AND a random field; Phase-C cutoff-independence to spread 1.1e-11. **Independent verifier (`hopfion_static_mass_verify.py`) + Phase B Hessian not yet run** ⇒ CONDITIONAL. |
| **Build-on grade** | **CONDITIONAL** — Phases A+C pass, but the mass is CONDITIONAL on (i) the EH-action premise (see §2) and (ii) Phase B (no localized negative mode) + D/E, none of which are run. **NOT unconditionally UDT-derived.** |

### Premise ledger

| Item | Tag |
|------|-----|
| UDT dilation metric form | DERIVED upstream |
| Unit 3-vector carrier n:Σ→S² | **POSIT** (`matter_carrier_provenance_audit`) |
| L2 (unique 2-deriv), L4=\|Ω\|² (native stabilizer) | DERIVED given carrier |
| **Geometric action ∫√−g R/(2κ_g)** | **CONDITIONAL-DERIVED** (metric-only/local/2-derivative minimality = Lovelock; Λ=0 by local-room asymptotic flatness; κ_g = overall normalization). NOT re-derived from positional dilation here. |
| Physical-metric coupling S_m[g,n] (no ḡ, no reciprocal-interior, no G/P) | WORKING/REOPENED (Charles-authorized overturn of P16-C / reciprocal / G-P for this solve) |
| ρ+S = 2ρ_4 ≥ 0 | **DERIVED + machine-verified** (§1) |
| M_N = 2∫Nρ_4 → 2E_4 (weak field) | **DERIVED identity; Phase-C verified** |
| ξ=κ_4=1 (banked gauge); κ_g dimensionless continuation | FREE, not fitted |
| Axisymmetry | **MEASURED ~8–10% residual — NOT machine-small** (§Phase A) |

---

# Phases A + C — a clean cutoff-independent local mass exists (CONDITIONAL on the EH frame)

## Provenance
git SHA `88aed6ccc05556162fba3ea19f71a869081c6da4` (grok, +58 ahead of main). Field
`hopfion_arc_scripts_2026-07-05/prod_an256.npz`, sha256 `5878f1dbaf870bd143be754490d805470afa028c462b986fa7f83dbd6b757b81`.
V100 / float64. All numbers from `hopfion_static_mass_out.json`.

## Phase A — baseline reproduced
E2=143.219, E4=143.297, **E2/E4=0.9995**, Q_H=0.9917 — the banked H3 within discretization error. Not forced.

**Axisymmetry (azimuthal Fourier test — REVISED 2026-07-11, replaces the coarse bin test):** the m≥1 power
fraction of ρ is **0.0002 (0.02%)** (m=1,2,3 ≈ 0; m=4 ≈ 1e-4). The field is axisymmetric about ẑ to ~0.02%
power ⇒ **the axisymmetric metric ansatz IS justified.** (My earlier bin-test "~8–10%" was a binning artifact,
now retracted — Charles's instinct to replace it was correct and it flips the conclusion.)

## §1 — Section-2 identities (the load-bearing check) — MACHINE-VERIFIED
On the real H3 field and a random smooth unit field:
- **ρ+S = (κ_4/2)Y = 2ρ_4**: max rel err **7.5e-16** (H3), **4.1e-16** (random) — a genuine algebraic identity.
- **(κ_4/2)Y = 2ρ_4**: exact. **S = −(ξ/2)X + (κ_4/4)Y**: rel err 1.7e-15.
- **Positivity: min Y = 0, min ρ_4 = 0 ⇒ ρ+S ≥ 0 machine-exactly.**
- **Key structural fact:** the ξ·X (L2 kinetic) terms **CANCEL** in ρ+S; only the compact L4 term ρ_4=(κ_4/4)Y
  sources the lapse trace. So `D²N = κ_g N ρ_4` has a **positive, COMPACT** source.

## Phase C — frozen-source linear lapse mass — PASS (REVISED 2026-07-11, rigorous independent check)
Solve `D²u = ρ_4` (FD-consistent, centered zero-pad FFT), then evaluate the flux TWO INDEPENDENT ways.
**(Correction: my earlier "M_N=2∫ρ_4 cutoff-independent to 1e-11" used the source-volume integral as its own
Gauss-law check — tautological. Replaced by an actual Poisson residual + an INDEPENDENT nested-surface flux.)**
- **Actual Poisson residual (interior):** ‖lap_FD(u)−ρ_4‖/‖ρ_4‖ = **9.5e-3** (controlled).
- **INDEPENDENT nested-surface flux** `∮_{S_R}∇u·dS` (∇u from the solved u, spherical quadrature — a
  computation *separate* from the volume ∫ρ_4): at R=3.0 (just outside r_tex≈2.5) flux = **141.6** vs volume
  E_4 = **143.3** ⇒ **agree to ~1.2%.** `M_N = 2·flux = 283.1` vs 2E_4 = 286.6 ⇒ **~1.2%**.
- The ~1.2% gap is discretization (sharp ρ_4) + surface interpolation; the further-R drift (flux→136 at R=5.5)
  is finite-box periodic-image contamination, not physics.
- Lapse depressed (u<0 — correct mass sign).

**Honest status:** the clean, positive local mass **M_N ≈ 2E_4** is confirmed by an INDEPENDENT surface flux to
**~1–2%** (not machine-clean, not the tautological volume self-check). **The contrast with Branch-P still
holds:** ρ_4=(κ_4/4)Y is COMPACT (source flux converges), unlike the never-vanishing Branch-P vacuum source
that DRIFTS — but the cleanness is a property of the (CONDITIONAL-DERIVED) EH frame.

## Adversarial note on the EH-action premise (per Charles's steer)
The geometric term ∫√−g R/(2κ_g) is Lovelock-unique among **metric-only, local, ≤2-derivative** actions in 4D
(up to the overall κ_g and a Λ term); **Λ=0 is the local-room asymptotic-flatness scope** (dispatch §6), a
scoped choice, not a fitted coefficient. So closing Phase C needs **no** preferred-coframe invariant and **no**
unchosen coefficient beyond κ_g ⇒ **no `BLOCKED_ACTION_FORK` at this phase.** BUT: EH is CONDITIONAL-DERIVED
(it is *assumed* metric-only/local/2-derivative, not re-derived from positional dilation), and it is exactly
the standard self-gravitating-soliton (ADM) structure — so the clean mass M_N=2E_4 is **conditional on that
frame**, not an unconditional UDT derivation. Whether the metric-only EH action survives against the native
positional-dilation geometric action is the open frame question (D/E + Charles).

## Phase B — Hessian classification (the adversarial gate) — no CONVERGED localized negative mode
Constrained tangent-space Hessian (η=(I−nn^T)δn), matrix-free FD-of-gradient HVP, **analytic-symmetry
deflation ONLY** (3 translations + 3 rotations + 1 target-SO(2); no unexplained modes deflated), LOBPCG-lite
Rayleigh minimization. `hopfion_static_mass_hessian_out.json`.

- **Coarse subsampled grids show localized negatives that SCALE AWAY (~h²), not converge:** λ(h=0.28)=−4.07,
  λ(h=0.19)=−1.65, fit λ∝h^2.1 → **0 in the continuum**. They ride **off-equilibrium** subsampled fields
  (virial 1.08–1.30, not ≈1) — the hopfion tube (~0.7 wide) is under-resolved at h≈0.2–0.28. These are
  **discretization artifacts**, and the FAIL criterion ("localized negative that CONVERGES with refinement")
  is the OPPOSITE of what is observed.
- **At the true 256³ minimizer (virial 0.9995):** the lowest deflated mode is POSITIVE for 20 of 22 Rayleigh
  iterations (0.065 → 0.0047, extended near-zero continuum, in_core≈0.03 ≈ uniform). The unconverged tail
  dipped to λ=−0.002, but **|λ|=0.002 ≪ residual 0.031 ⇒ NOT a converged eigenpair** — it is at the
  residual-gradient floor (the banked field has gradnorm 0.13, an incomplete production minimization) blended
  with the expected gapless near-zero continuum.
- **Scale/Derrick mode E''(1)=2E_4 > 0** confirmed.

**Verdict (per the pre-registered criterion):** **no CONVERGED localized negative Hessian mode** ⇒ does NOT trip
`FAIL_H3_INSTABILITY`, and satisfies the PASS condition "no converged localized negative mode." **Caveat (honest,
not forced to a pristine PASS):** the near-zero spectrum is not machine-clean positive-definite — the gapless
continuum + the field's residual gradnorm leave the very-lowest modes marginal/unconverged (the tail touched
−0.002). The cleanest closure is a fully-relaxed field (arrested-Newton to small gradnorm) + a converged
eigensolver, or the coupled metric-carrier Hessian (a **separate later gate**, per Charles).

## Pre-registered gate status
- **Phase A:** PASS (baseline reproduced; axisymmetry flagged ~10%).
- **Phase B (Hessian):** **PASS on the FAIL-criterion** (no converged localized negative mode; coarse negatives
  scale ~h²→0; 256³ marginal tail is residual-gradient-floor, unconverged) — **caveat-flagged** (not machine-clean
  positive-definite; wants a relaxed-field converged eigensolve to fully close).
- **Phase C (linear lapse):** **PASS** — source/flux identity converges, cutoff-independent, correct sign.
- **Phase D (full linear metric), Phase E (continuation):** NOT RUN.

## Verdict (this checkpoint)
**`PHASE_A_B_C_PASS_CONDITIONAL`** — under the frozen EH+physical-coupling action, the H3 carrier has a clean,
positive, cutoff-independent local mass M_N = 2E_4 = E_2+E_4 (weak field), resting on the machine-verified
positivity ρ+S=2ρ_4≥0, with **no converged localized negative Hessian mode** (Phase B; caveat-flagged). **This is
NOT yet `PASS_LOCAL_MASS_BRANCH`** (needs Phase D full linear metric + Phase E nonlinear continuation, and the
Phase-B near-zero spectrum tightened on a relaxed field) and remains **CONDITIONAL on the EH-action premise**
(CONDITIONAL-DERIVED, not native-dilation-derived).

## NOT claimed
- NOT: an unconditional UDT-derived mass — it is conditional on the EH/metric-only action premise.
- NOT: `PASS_LOCAL_MASS_BRANCH` — Phase B (no localized negative mode), D, E are unrun.
- NOT: a particle label, measured-mass comparison, or fitted coupling (κ_g free; ξ=κ_4=1 gauge).
- NOT: axisymmetry imposed (measured ~10% residual; Phase E must go full-3D or re-examine).
- NOT: G=8πT smuggled — the geometric term is Lovelock-unique metric-only, Λ=0 local-room scope, κ_g the only normalization.
