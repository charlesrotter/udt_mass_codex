# Stage-D FROZEN FORECAST — per-rung predictions from the banked quantization-closure law

**Date:** 2026-07-03. **Held OUT of the repo deliberately** (pre-registration payload; the cell
solves that would test it are the TEST, not this forecast). **No cell/shooting solves of the
field equations were run.** Compute used: algebra on the potential family, the universal bottom
γ-system ODE (the law's own machinery, Category-A conditioning), root-finding on the closure.

**Family/scope:** A1 m=3, Z=8, ρ_c=1 gauge, below-stuck side (the Stage-B ladder family).
**Law status carried over:** DERIVED-AT-SECOND-ORDER, scoped N ≳ 8
(`ladder_theta0_accumulation_results.md`); N > 22 rungs here are EXTRAPOLATION beyond the
banked ladder — that is the point of the forecast.

Generator: `stageD_forecast_gen.py` (this scratchpad). Machine-readable:
`stageD_frozen_forecast.json`.

## The chain (faithful reuse of the blind verifier's chain, `cascade_bv10_assembly.py`)

- x_c = 1/1101 (banked anchor).
- Potential family: U(ρ) = 2ρ³·exp(−a(ρ²−1)), a = (3/2)(1−d). Exact symbolic derivatives at
  ρ=1 (closed forms, for the record):
  - U'(1) = 6d  ⟹ **δ̃(d) = U'(1)/4 = 1.5·d**
  - U''(1) = −12 + 6d + 18d²  ⟹ **s̃₁(d) = |U''(1)|/4 = 3 − 1.5d − 4.5d²**
  - ĉ₃ = U'''(1)/(12 s̃₁), ĉ₄ = U''''(1)/(48 s̃₁) (script uses exact sympy derivatives;
    at d≈2e-3: ĉ₃ ≈ −0.4988, ĉ₄ ≈ −0.6230)
- **γ(d) = 4δ̃(d)² / (Z s̃₁(d)² x_c²)**
- **θ₀(N; d)** self-consistent (bv10 `assemble`): θ₀ = z*_eff(γ) + K·Z(1−x_c)²/(3Θ)
  + (3/2)ĉ₃(δ̃/s̃₁)Θ, with Θ = (N+1)π + θ₀ and K = 2 + (15/16)ĉ₃² − (3/2)ĉ₃ + (3/4)ĉ₄.
  z*_eff(γ) and z_c_eff(γ) come from the universal bottom system
  v_ζζ − p v_ζ + v = 1, ψ_ζ = p, p_ζ = γe^{−2ψ}v_ζ² − p², zero ICs
  (z*_eff = late pair-averaged ρ'-node offset; z_c_eff = late-⟨z·e^{−ψ/2}⟩).
- **Closure: d*(N) solves z_c_eff(γ(d)) = Θ(N)·√x_c** (RHS-form note below); brentq root.
- **a_seal ≈ √Z / Θ(N)** (Lemma D R2 leading form; the (|s̃₁|/Q_s)^{1/4} factor, ≤0.2% on
  banked rungs, needs a solve for Q_s and is deliberately omitted).
- **q = 2Z√|s̃₁|·(1−x_c) / Θ(N)** (s̃₁ at the predicted d*).
- **Parity (below side, Stage-B B3):** odd N → ρ_s < 1; even N → ρ_s > 1.

## CALIBRATION (banked rungs; deviations vs banked d*)

RHS = Θ√x_c (bv10 verifier form — REPRODUCES the banked calibration exactly):

| N  | d_pred        | d_banked        | deviation |
|----|---------------|-----------------|-----------|
| 8  | 0.003902000   | 0.0039170433841 | **−0.38%** |
| 16 | 0.002665640   | 0.0026633943319 | **+0.08%** |
| 22 | 0.002131601   | 0.0021288889610 | **+0.13%** |

(Expected from `ladder_theta0_accumulation_results.md`: −0.38%, +0.08%, +0.13% — exact match.)

RHS variant Θ√x_c/√(1−x_c) (the results-doc wording): −0.41%, +0.05%, +0.09% — a ≤0.05%
d-shift; the bv10 form is used for the forecast since it is the form that produced the banked
calibration numbers.

Free extra checks (not part of the required calibration):
- d*(20): +0.12%, d*(21): +0.14% vs banked.
- q formula vs banked q: N=8 +0.17%, N=22 +0.16%.

Soundness (Category-A conditioning checks): extended γ-grid spline reproduces the calibration
identically (−0.38/+0.08/+0.13); bottom-ODE z_end 400→800 changes z_c_eff by ≤2.1e-4 relative
at the smallest γ used (0.10); lambdified family derivatives agree with bv10's per-call sympy
path to <1e-12.

## FORECAST — all N with predicted d*(N) in the extended range (1.30e-3, 2.30e-3)

Extended range: **N = 20 … 39 (20 rungs)**. Window proper (1.45e-3, 2.11e-3): **N = 23 … 35
(13 rungs)** — cf. Stage-B's rough "≈11 rungs extrapolated" estimate for the aliased window.
(N=20–22 are already banked; their inclusion is a live re-check of the chain.)

| N  | d*(N) predicted | γ(d*)  | θ₀/π    | Θ        | a_seal   | q       | ρ_s parity | window |
|----|-----------------|--------|---------|----------|----------|---------|------------|--------|
| 20 | 2.287198e-03    | 0.7945 | +0.1765 | 66.5273  | 0.042512 | 0.41594 | ρ_s>1      | ext (banked 2.284364e-03) |
| 21 | 2.207016e-03    | 0.7397 | +0.1696 | 69.6465  | 0.040608 | 0.39732 | ρ_s<1      | ext (banked 2.203948e-03) |
| 22 | 2.131601e-03    | 0.6900 | +0.1632 | 72.7681  | 0.038866 | 0.38028 | ρ_s>1      | ext (banked 2.128889e-03) |
| 23 | 2.060559e-03    | 0.6447 | +0.1572 | 75.8918  | 0.037266 | 0.36464 | ρ_s<1      | WINDOW |
| 24 | 1.993544e-03    | 0.6034 | +0.1516 | 79.0175  | 0.035792 | 0.35023 | ρ_s>1      | WINDOW |
| 25 | 1.930249e-03    | 0.5657 | +0.1463 | 82.1449  | 0.034429 | 0.33691 | ρ_s<1      | WINDOW |
| 26 | 1.870395e-03    | 0.5311 | +0.1414 | 85.2739  | 0.033165 | 0.32456 | ρ_s>1      | WINDOW |
| 27 | 1.813737e-03    | 0.4994 | +0.1368 | 88.4043  | 0.031991 | 0.31309 | ρ_s<1      | WINDOW |
| 28 | 1.760049e-03    | 0.4702 | +0.1325 | 91.5361  | 0.030896 | 0.30239 | ρ_s>1      | WINDOW |
| 29 | 1.709125e-03    | 0.4434 | +0.1285 | 94.6690  | 0.029873 | 0.29240 | ρ_s<1      | WINDOW |
| 30 | 1.660779e-03    | 0.4186 | +0.1247 | 97.8031  | 0.028916 | 0.28304 | ρ_s>1      | WINDOW |
| 31 | 1.614840e-03    | 0.3958 | +0.1211 | 100.9382 | 0.028018 | 0.27426 | ρ_s<1      | WINDOW |
| 32 | 1.571151e-03    | 0.3746 | +0.1177 | 104.0742 | 0.027173 | 0.26601 | ρ_s>1      | WINDOW |
| 33 | 1.529567e-03    | 0.3550 | +0.1145 | 107.2112 | 0.026378 | 0.25824 | ρ_s<1      | WINDOW |
| 34 | 1.489955e-03    | 0.3369 | +0.1115 | 110.3489 | 0.025628 | 0.25091 | ρ_s>1      | WINDOW |
| 35 | 1.452191e-03    | 0.3200 | +0.1086 | 113.4874 | 0.024919 | 0.24399 | ρ_s<1      | WINDOW (edge: 0.15% above the 1.45e-3 edge — edge-marginal at the law's ±0.4% accuracy) |
| 36 | 1.416160e-03    | 0.3043 | +0.1060 | 116.6266 | 0.024249 | 0.23743 | ρ_s>1      | ext |
| 37 | 1.381756e-03    | 0.2897 | +0.1034 | 119.7664 | 0.023613 | 0.23122 | ρ_s<1      | ext |
| 38 | 1.348881e-03    | 0.2761 | +0.1010 | 122.9068 | 0.023009 | 0.22532 | ρ_s>1      | ext |
| 39 | 1.317443e-03    | 0.2633 | +0.0987 | 126.0477 | 0.022436 | 0.21972 | ρ_s<1      | ext |

(Θ in radians; a_seal per R2 leading form; q per Lemma D. N=40 predicts d*=1.287357e-03,
just below the extended floor — excluded; edge-marginal there too.)

## Premise ledger (chose-or-derived)

1. **RHS form of the closure = Θ√x_c** — CHOSE between the doc's wording (Θ√x_c/√(1−x_c)) and
   the verifier script's form (Θ√x_c); selected because it reproduces the banked calibration
   numbers EXACTLY (the doc's quoted −0.38/+0.08/+0.13 came from this script). Impact of the
   alternative: ≤0.05% in d*. Effectively pinned-by-provenance of the calibration numbers.
2. **a_seal at R2 leading form √Z/Θ** — CHOSE to omit the (|s̃₁|/Q_s)^{1/4} factor (≤0.2%
   banked) because Q_s requires a cell solve, which is forbidden for this forecast.
3. **θ₀ assembly = bv10's `assemble`** (z*_eff + E-part + δ̂-part, self-consistent) — DERIVED
   (banked, blind-verified construction; reused verbatim).
4. **Extended γ grid down to 0.10 + z_end=400** — Category-A conditioning (CHOSE, soundness-
   checked: z_end convergence 2e-4; calibration invariant under grid extension). NOTE the
   banked law is verified only on γ ∈ [~0.65, 2.4] rungs; forecast rungs N≳31 use γ < 0.4 —
   an extrapolation of the bottom system into a numerically clean but observationally untested
   γ regime.
5. **Parity rule** — carried from Stage-B B3 as an OBSERVED banked regularity (zero exceptions
   in 13 blind-verified rungs), not derived from the closure law itself.
6. **Scope carry-over** — the law is second-order with a named handover sliver (+2.0% of θ₀ at
   N=8 shrinking to +0.9% at N=22, i.e. improving with N); calibration deviations ≤0.4% and
   shrinking with N support ~0.1–0.2%-level d* accuracy for N=23–39, but N>22 is genuine
   extrapolation beyond the banked ladder.
7. Banked pins used ONLY for calibration comparison (d* at N=8/16/20/21/22, q at N=8/22) —
   none entered the forecast computation.

---
**ANCHOR-VALUE STAMP (2026-08-06, canon C-2026-08-06-2):** numeric results in this document ride
the anchor VALUE Delta phi = ln(1101), now demoted to the interpretation-conditional working number
ln(T_emit/T_CMB) with T_emit ~ 3000 K under the CMB emission-surface reading (legacy-interpretation
premise, not native). Structural/impossibility conclusions are value-independent; numeric tables
are conditional on T_emit and re-parameterizable. See `udt_cmb_anchor_provenance_audit_2026-08-06/`.
