## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-11 |
| **Mode** | DERIVE→VERIFY→OBSERVE — `UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md`. Phases A + C done; B/D/E pending. |
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

**Axisymmetry (measured before imposing):** residual ‖f−⟨f⟩_φ‖/‖f‖ = **0.077 (ρ), 0.086 (ρ_4), 0.105 (S)** —
**~8–10%, NOT machine-small.** Consequence (per dispatch §Phase C/E): the axisymmetric metric ansatz is **NOT
cleanly justified**; Phase C (below) is a FULL-3D Poisson solve (no averaging, unaffected), but **Phase E must
use a full-3D static metric or re-examine axisymmetry** — do not average the stress.

## §1 — Section-2 identities (the load-bearing check) — MACHINE-VERIFIED
On the real H3 field and a random smooth unit field:
- **ρ+S = (κ_4/2)Y = 2ρ_4**: max rel err **7.5e-16** (H3), **4.1e-16** (random) — a genuine algebraic identity.
- **(κ_4/2)Y = 2ρ_4**: exact. **S = −(ξ/2)X + (κ_4/4)Y**: rel err 1.7e-15.
- **Positivity: min Y = 0, min ρ_4 = 0 ⇒ ρ+S ≥ 0 machine-exactly.**
- **Key structural fact:** the ξ·X (L2 kinetic) terms **CANCEL** in ρ+S; only the compact L4 term ρ_4=(κ_4/4)Y
  sources the lapse trace. So `D²N = κ_g N ρ_4` has a **positive, COMPACT** source.

## Phase C — frozen-source linear lapse mass — PASS (cutoff-independent)
`D²u = ρ_4`, u→0. Mass by Gauss law `M_N(R) = 2∮_{S_R}∇u·dS = 2∫_{r<R}ρ_4`:
- **M_N → 286.594 = 2E_4** exactly; **far-R spread 1.1e-11** — CUTOFF-INDEPENDENT (plateaus by R≈4.6 because
  ρ_4 is compact). Table: M_N(2.13)=274.2, M_N(2.95)=285.2, M_N(3.77)=286.56, M_N(4.59)=M_N(5.40)=286.594.
- **M_N/(E2+E4) = 1.0003** = the weak-field prediction 2E_4/(E2+E4) exactly.
- Lapse u(center) = −12.96 (well; N=1+κ_g u depressed — correct mass sign).

**The contrast that matters:** unlike the native Branch-P vacuum source `4e^{−2φ}` (never vanishes ⇒ the flux
DRIFTS, `hopfion_GP_exterior_probe_results.md`), the EH-frame source ρ_4=(κ_4/4)Y is **COMPACT** ⇒ the mass
flux PLATEAUS at 2E_4, cutoff-free. **The cleanness is a property of the (CONDITIONAL-DERIVED) EH frame**, not
a native Branch-P result.

## Adversarial note on the EH-action premise (per Charles's steer)
The geometric term ∫√−g R/(2κ_g) is Lovelock-unique among **metric-only, local, ≤2-derivative** actions in 4D
(up to the overall κ_g and a Λ term); **Λ=0 is the local-room asymptotic-flatness scope** (dispatch §6), a
scoped choice, not a fitted coefficient. So closing Phase C needs **no** preferred-coframe invariant and **no**
unchosen coefficient beyond κ_g ⇒ **no `BLOCKED_ACTION_FORK` at this phase.** BUT: EH is CONDITIONAL-DERIVED
(it is *assumed* metric-only/local/2-derivative, not re-derived from positional dilation), and it is exactly
the standard self-gravitating-soliton (ADM) structure — so the clean mass M_N=2E_4 is **conditional on that
frame**, not an unconditional UDT derivation. Whether the metric-only EH action survives against the native
positional-dilation geometric action is the open frame question (D/E + Charles).

## Pre-registered gate status
- **Phase A:** PASS (baseline reproduced; axisymmetry flagged ~10%).
- **Phase C (linear lapse):** **PASS** — source/flux identity converges, cutoff-independent, correct sign.
- **Phase B (Hessian instability):** **NOT RUN** — the critical make-or-break gate (`FAIL_H3_INSTABILITY` if a
  localized negative mode converges). REQUIRED before `PASS_LOCAL_MASS_BRANCH`.
- **Phase D (full linear metric), Phase E (continuation):** NOT RUN.

## Verdict (this checkpoint)
**`PHASE_A_C_PASS_CONDITIONAL`** — under the frozen EH+physical-coupling action, the H3 carrier has a clean,
positive, cutoff-independent local mass M_N = 2E_4 = E_2+E_4 (weak field), resting on the machine-verified
positivity ρ+S=2ρ_4≥0. **This is NOT yet `PASS_LOCAL_MASS_BRANCH`** (needs Phase B stability + D + E) and is
**CONDITIONAL on the EH-action premise** (CONDITIONAL-DERIVED, not native-dilation-derived).

## NOT claimed
- NOT: an unconditional UDT-derived mass — it is conditional on the EH/metric-only action premise.
- NOT: `PASS_LOCAL_MASS_BRANCH` — Phase B (no localized negative mode), D, E are unrun.
- NOT: a particle label, measured-mass comparison, or fitted coupling (κ_g free; ξ=κ_4=1 gauge).
- NOT: axisymmetry imposed (measured ~10% residual; Phase E must go full-3D or re-examine).
- NOT: G=8πT smuggled — the geometric term is Lovelock-unique metric-only, Λ=0 local-room scope, κ_g the only normalization.
