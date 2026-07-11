## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-11 |
| **Mode** | DERIVE→VERIFY→OBSERVE — `UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md`. Phases A + B + C done; D/E pending. |
| **Object** | banked H3 Q_H=1 carrier ONLY (`prod_an256.npz`). NEVER f2d π₂ hedgehog. |
| **Device** | V100, float64, one process. |
| **Observing or targeting?** | OBSERVE whether a clean cutoff-independent local mass exists under the frozen action. Aimed HARDEST at the load-bearing positivity ρ+S=2ρ_4≥0 and at the EH-action premise (the comfortable answer is a clean mass — do not over-claim it). |
| **Verifier status** | Section-2 identities machine-verified (real + random field). Phase C: independent surface flux (≠ volume) agrees ~1.2%, Poisson residual 0.95%. Phase B (rigorous generalized eigenproblem, fixed-boundary): **UNRESOLVED — converged localized negative mode at a non-critical field; blocked on proper re-relaxation.** |
| **Build-on grade** | **CONDITIONAL / Phase-B-UNRESOLVED** — Phases A+C clean, but the clean mass is NOT established: conditional on (i) the EH-action premise and (ii) an UNRESOLVED stability gate (Phase B) that surfaced a concern. **NOT unconditionally UDT-derived; NOT stability-verified.** |

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

## Phase C — frozen-source linear lapse mass — PASS (REVISED 2026-07-11: isolated BC + discrete face fluxes)
**(Correction chain: the original "M_N=2∫ρ_4 to 1e-11" was the tautological volume self-check; a first redo used
an interpolated-sphere flux on a PERIODIC (zero-pad FFT) solve — which drifted with R from periodic images. Now
replaced by a TRUE isolated-boundary solve + discrete face fluxes.)**
- **Isolated (Hockney free-space Green's function) Poisson solve** `D²u=ρ_4`, u→0 — **no periodic images**.
- **DISCRETE cubic FACE fluxes** `∮∇u·n̂ dS` over nested boxes (exact discrete Gauss law; ∇u by FD, summed over
  the 6 discrete faces — a computation *independent* of the volume ∫ρ_4): the flux **plateaus FLAT at E_4=143.30**
  across every enclosing box (R=3.3→5.6: 143.31→143.30), **plateau spread = 5.9e-4 (0.06%)** — the image drift
  is gone. `M_N = 2·flux = 286.45` vs 2E_4 = 286.59 ⇒ **M_N/2E_4 = 0.9995 (0.05%).**
- Interior Poisson FD residual 1.8e-2 (the Hockney solve targets the continuum, not the FD, Laplacian; the face
  flux is exact regardless via Gauss). Grid convergence: N=256 → 0.9995, N=128 → 1.007 (converging with N).
- Lapse depressed (correct mass sign).

**Status: PASS (rigorous).** The clean, positive local mass **M_N = 2E_4** is confirmed by an INDEPENDENT
discrete face flux to **0.05%**, plateau-flat under true isolated BC. **The contrast with Branch-P holds:**
ρ_4=(κ_4/4)Y is COMPACT (flux converges/plateaus), unlike the never-vanishing Branch-P vacuum source that DRIFTS
— but the cleanness is a property of the (CONDITIONAL-DERIVED) EH frame.

## Adversarial note on the EH-action premise (per Charles's steer)
The geometric term ∫√−g R/(2κ_g) is Lovelock-unique among **metric-only, local, ≤2-derivative** actions in 4D
(up to the overall κ_g and a Λ term); **Λ=0 is the local-room asymptotic-flatness scope** (dispatch §6), a
scoped choice, not a fitted coefficient. So closing Phase C needs **no** preferred-coframe invariant and **no**
unchosen coefficient beyond κ_g ⇒ **no `BLOCKED_ACTION_FORK` at this phase.** BUT: EH is CONDITIONAL-DERIVED
(it is *assumed* metric-only/local/2-derivative, not re-derived from positional dilation), and it is exactly
the standard self-gravitating-soliton (ADM) structure — so the clean mass M_N=2E_4 is **conditional on that
frame**, not an unconditional UDT derivation. Whether the metric-only EH action survives against the native
positional-dilation geometric action is the open frame question (D/E + Charles).

## Phase B — Hessian (RIGOROUS, REVISED 2026-07-11 per Charles) — **UNRESOLVED (with concern)**
Generalized eigenproblem `H v = λ M v` (M = quadrature mass = h³I ⇒ physical normalization
λ_phys=λ_euclid/h³, comparable across grids); **fixed-asymptotic perturbations** (η=0 on a boundary layer);
analytic-symmetry deflation ONLY (3 trans + 3 rot + 1 target-SO(2)); matrix-free FD-of-gradient HVP;
LOBPCG-lite. **This supersedes the earlier "PASS-on-FAIL-criterion" reading, which used inconsistent Euclidean
normalization, no fixed boundary, and un-re-relaxed fields — that reading is retracted.**

- **At the 256³ production minimizer** (virial 0.9995, but **gradnorm 0.13 ⇒ NOT a true critical point**): the
  Rayleigh minimization **CONVERGES to a localized negative mode** — λ_phys=**−312**, res_phys=52
  (res/|λ|=0.17 ⇒ converged), **in_core=0.995** (highly localized).
- **Residual-gradient alignment check (decisive diagnostic):** the residual-gradient direction has **POSITIVE**
  curvature (λ_phys(ĝ)=+574); the converged negative mode is **orthogonal** to it ⇒ **the negative is NOT the
  "field-still-settling" residual-gradient artifact.**
- **Multi-resolution re-relaxation is BLOCKED:** naive arrested-Newton **collapses** the coarse hopfion (Derrick
  shrink) without the production Derrick-rescale machinery (coarse "re-relaxed" fields gave virial 1.0–1.38,
  gradnorm *grew* — invalid). The correct fix is to re-relax with `fs_hopfion`/`drive_production` rescale at each grid.

**Verdict: UNRESOLVED (with concern).** A converged, localized, negative Hessian mode exists at the 256³ field
and is not the trivial residual-gradient artifact — but the field is **not a true critical point**, and a
Hessian certifies (in)stability only *at* a critical point. So this **does not** rigorously establish
instability, and it **no longer supports** stability either. **NOT `PASS` (do not treat the Phase-A/C clean
mass as established), NOT `FAIL_H3_INSTABILITY` (field not critical).** Resolving it **requires** the Hessian at
a properly re-relaxed minimizer (gradnorm→0), which needs the production rescale machinery. Physics prior: the
Q_H=1 FS hopfion is a known stable soliton, so the *true* minimizer is likely stable — but this numerics neither
confirms nor refutes it, and the rigorous test surfaced a genuine open question that must be closed first.

## Pre-registered gate status
- **Phase A:** PASS (baseline reproduced; axisymmetry Fourier 0.02% ⇒ axisymmetric).
- **Phase B (Hessian, rigorous):** **UNRESOLVED (with concern)** — a converged localized negative mode
  (λ_phys=−312, in_core 0.995), not the residual-gradient artifact, at a field that is not a true critical
  point (gradnorm 0.13). Neither PASS nor FAIL; blocked on proper re-relaxation (production rescale machinery).
- **Phase C (linear lapse):** **PASS (rigorous)** — isolated-BC (Hockney) solve + discrete face fluxes confirm M_N=2E_4 to 0.05%, plateau-flat (spread 0.06%).
- **Phase D (full linear metric), Phase E (continuation):** HALTED (per Charles).

## Verdict (this checkpoint, REVISED 2026-07-11)
**`PHASE_A_C_PASS ; PHASE_B_UNRESOLVED`.** Phases A and C are clean: the identities ρ+S=2ρ_4≥0 are
machine-exact, and the local mass **M_N ≈ 2E_4** is confirmed by an INDEPENDENT surface flux to ~1–2%.
**BUT the stability gate (Phase B) is UNRESOLVED with a concern** — the rigorous generalized eigenproblem
finds a converged localized negative mode (not the residual-gradient artifact) at a field that is not a true
critical point. **Therefore the clean mass is NOT established:** it is CONDITIONAL on (i) the EH-action premise
(CONDITIONAL-DERIVED, not native-dilation-derived), AND (ii) an UNRESOLVED Phase B that must be closed by the
Hessian at a properly re-relaxed minimizer (production Derrick-rescale machinery) before stability — and thus
`PASS_LOCAL_MASS_BRANCH` — can be claimed. Phases D/E halted per Charles.

## NOT claimed
- NOT: an unconditional UDT-derived mass — it is conditional on the EH/metric-only action premise.
- NOT: `PASS_LOCAL_MASS_BRANCH` — Phase B (no localized negative mode), D, E are unrun.
- NOT: a particle label, measured-mass comparison, or fitted coupling (κ_g free; ξ=κ_4=1 gauge).
- NOT: axisymmetry imposed (measured ~10% residual; Phase E must go full-3D or re-examine).
- NOT: G=8πT smuggled — the geometric term is Lovelock-unique metric-only, Λ=0 local-room scope, κ_g the only normalization.
