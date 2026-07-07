# OWED-FIRST — blind adjudication of the Class-B rung-resonance load-bearing identities

**Date:** 2026-07-07 · **Mode:** VERIFY / adjudicate (blind, neutral) · **Author:** Claude Opus 4.8 (1M).
**Status:** PROVISIONAL — identities BLIND-CONFIRMED; two reconstruction refinements surfaced (below). Gates the
per-rung `(q_N, Δφ_N, I_{r,req}(N), A_N)` classification in `classB_rung_resonance_prebuild_test_DESIGN.md` §OWED FIRST.

## What was owed
The DESIGN doc TRANSCRIBED Charles's Der 1–7; the R4/R5 identities (`I_{r,req}(N)`, `A_N`) and the old no-band
numbers were cited, not independently re-derived. Since the entire rung classification rests on those identities
being exactly right, run a blind pass FIRST: (i) independently re-derive `π_ρ'` → `I_{r,req}(N)` and `E_ang` → `A_N`
from the NATIVE ACTION (not the DESIGN/classB docs), and (ii) re-confirm the old two-branch numbers. Frame NEUTRALLY
(adjudicate, don't confirm — this session's residual-artifact lesson, [[verifier-framing-and-residual-artifacts]]).

## Method (two independent blind agents, run in parallel)
- **Agent A** (`aa57c76dbdf2a0c01`) — blind derivation. Walled off from `classB_rung_resonance_prebuild_test_DESIGN.md`,
  `embedded_classB_mini_MAP.md`, `verify_classB_derivations.py`, `cell_solver_f2d_classB_run_results.md`,
  `classB_embedded_rung_gatecheck_results.md`, LIVE/HANDOFF/memory. Allowed: the UPSTREAM native-action sources only
  (`f_rtheta_free_field_MAP.md §2`, `f2d_virial_step0_results.md`, `round_matter_reduction_results.md`,
  `native_field_equations_constrained_two_player_results.md`, `seal_matching_junction_results.md`, and
  `cell_solver_f2d.py`/BUILDNOTES for conventions only). Told to report whatever its own derivation yields, not to
  reproduce any target.
- **Agent B** (`a68053f66ae7859aa`) — numbers re-confirmation. Re-ran `verify_classB_derivations.py` (CAS) + its OWN
  bounded seeded-`I_r` coupled solves (Nr=16, Nθ=12, single clean process). Adjudicate CONFIRMED/REFUTED/PARTIAL.

## RESULT 1 — the identities are BLIND-CONFIRMED (transcription faithful, nothing smuggled)
| Object | DESIGN doc (transcribed) | Agent A (blind, native action) | Verdict |
|---|---|---|---|
| **R4** | `π_ρ' = Zρφ'² − ξρI_r + κN_w²I_{4θ}/ρ³` | **identical**; CAS-confirmed; the `2φ'ρ'` cross-term cancels EXPLICITLY (product-rule `+8φ'ρ'e^{−2φ}` vs EOM `−8φ'ρ'e^{−2φ}`); `π_ρ=−4e^{−2φ}ρ'` convention CONFIRMED in-source (virial §V5), not assumed | ✅ EXACT (SOLID) |
| **I_{r,req}** | `[q_N²/(Zρ_s³)+κN_w²I_{4θ}/ρ_s³−π'_{ρ,amb}]/(ξρ_s)` | **identical** algebra, using `Zρ_sφ'_s²=q²/(Zρ_s³)` via `φ'_s=q/(Zρ_s²)` | ✅ EXACT (SOLID) |
| **A_N** | `E_ang,natural − m_amb(N)` (E_ang not written out) | derived the EXPLICIT `E_ang=(ξ/2)(I_θ+N_w²I_s)+(κN_w²/2)I_{4θ}/ρ²`; natural (rigid f=θ, I_θ=I_s=I_4θ=1) → `E_ang,natural=(ξ/2)(1+N_w²)+κN_w²/(2ρ_s²)` | ✅ structure confirmed + SHARPENED |

Per-term signs (ρ>0; Z,ξ,κ>0; I_r,I_4θ≥0): `+Zρφ'²≥0` (= `π_φ²/(Zρ³)`, the flux term), `−ξρI_r≤0` (the ONLY
possibly-negative term; the radial-structure channel), `+κN_w²I_{4θ}/ρ³≥0` (angular-skin). `I_r=½∫sinθ f_r²dθ≥0` is
an integral of a square ⇒ realizability requires `I_{r,req}≥0`.

## RESULT 2 — the old no-band numbers RE-CONFIRMED (Agent B, own solves)
- `verify_classB_derivations.py` CAS → **PASS** (D1/D2/R4 flux identity + mandatory-`I_r` logic).
- **q closes π_φ:** `q=+3.95287` (N_w=1) / `+3.82057` (N_w=2), `R3~1e-13`, → `π_φ,amb=Z·q_A=8×0.5=4.0`; seed-independent.
- **I_r drains (load-bearing):** seeded `u=f−θ` amp 0.3/0.4/0.5 (`I_r,seed` up to 0.69), coupled solve →
  final `I_r ~ 1e-16…1e-18` (N_w=1, machine zero) / `1.106e-5` (N_w=2, seed-independent fixed point). DRAINED, not
  persisted, every solve. Far below the O(1–10) needed to close R4 (which stays `+10.0`/`+11.2` at ρ'_amb=+1).
- **Two-branch floor:** min‖(R4,R5)‖ = `0.786` (N_w=1; banked 0.774 — 1.5% off, coarser L-grid) / `2.679` (N_w=2;
  banked 2.68). Past the turning point R4 opens (~0.1) but R5 pins at `~0.78`/`~2.68` — the single-signed O(1)
  obstruction. No common zero.

## THE TWO REFINEMENTS the blind pass surfaced (NOT refutations — reconstruction sharpenings; both were DESIGN-doc "reconstruct/flag" items)
**Refinement 1 — the I_r branch is controlled by `π'_{ρ,amb}(N)` (ambient momentum-DERIVATIVE), not `sign(ρ'_amb)`.**
`ρ'_amb` fixes the sign of the momentum VALUE `π_ρ=−4e^{−2φ}ρ'`, but `I_{r,req}` depends on `π'_{ρ,amb}`, whose sign
is set by the AMBIENT's OWN R4 (`π'_{ρ,amb}=Zρ_ampφ'_amp²−ξρ_amp I_{r,amp}+κN²I_{4θ,amp}/ρ_amp³`), not by `ρ'_amb`
alone. Necessary-for-realizability: `π'_{ρ,amb} ≤ q²/(Zρ_s³)+κN_w²I_{4θ}/ρ_s³`; SUFFICIENT for strict `I_r>0`:
`π'_{ρ,amb}≤0`. ⇒ the old "Branch A/B by sign(ρ'_amb)" is a heuristic; the real per-rung control variable is
`π'_{ρ,amb}(N)`, which the classification must reconstruct from the rung's ambient R4.

**Refinement 2 — `m_amb(N)` in `A_N` is genuinely undetermined AND may not vary with the rung.** Agent A derived the
embedded seal condition as `E_ang(r_s)=2+H_amb` (from virial V5: closed cell H=0 ⇒ E_ang(r_s)=2; embedded ⇒
E_ang=2+H_amb; the geometric "2" = √h·R^(2) per 4π balancing E_ang). Gate-check (b) already established `H_amb(N)=0`
for EVERY rung. So IF `m_amb` is that seal target, `m_amb≡2` (constant across rungs), and `A_N` depends on the rung
ONLY through `ρ_s(N)` and the winding `N_w`:
```
A(N_w, ρ_s) = (ξ/2)(1+N_w²) + κN_w²/(2ρ_s²) − 2         [conditional on m_amb≡2; ILLUSTRATIVE, ξ=κ=1]
  N_w=1:  A = 1/(2ρ_s²) − 1     → crosses 0 at ρ_s = 1/√2 ≈ 0.707
  N_w=2:  A = 0.5 + 2/ρ_s²      → > 0 for all ρ_s (never crosses)
```
Whether `m_amb` = the geometric "2", or `H_amb` (=0), or a SEPARATE ambient Misner–Sharp mass at the rung, is an
identification in the embedded-matching files Agent A was walled off from. **This identification decides whether the
`A_N` resonance screen is meaningful and whether it varies with the rung at all — it is Charles's to adjudicate
before any `A_N` column is banked as a build gate.**

## NET verdict
- **OWED-FIRST identities: BLIND-CONFIRMED.** `I_{r,req}(N)` and `A_N` follow exactly from the native action; the old
  two-branch numbers re-confirm. The classification's ALGEBRA is trustworthy.
- **Two reconstruction premises are now the crux** (not the algebra): `π'_{ρ,amb}(N)` (Refinement 1) and `m_amb(N)`
  (Refinement 2). Both were flagged "reconstruct / reconstructed-vs-derived" in the DESIGN doc; the blind pass
  sharpened WHAT they physically are. `m_amb(N)` needs Charles before `A_N` is banked.

## Premise ledger / scope
π₂ static S-Dir tile; Class-B seal; MODEL ambient in the numbers re-confirm (q_A=0.5, μ=1.0, Z=8, ξ=κ=1, Nr≤16,
Nθ≤12, N_w∈{1,2}); DESIGN/PROVISIONAL/Outcome D. `q_N,Δφ_N,Θ(N),x_c=1/1101` DERIVED (Stage-D, canon). `π'_{ρ,amb}(N)`,
`m_amb(N)`, `E_ang,natural`, `ρ_s(N)`, `I_{4θ}` at the rung = RECONSTRUCTED (flag at use). Data-blind on lepton numbers.
Not TARGETING the lepton ladder — OBSERVE which rungs (if any) hit resonance.
