# Stage D SURVEY sweep — RAW results (blind; observe-mode; no comparisons, no verdicts)

**Date:** 2026-07-03. **Agent role:** Stage-D blind SURVEY (rung positions and per-rung
diagnostics only; the pre-registration, the accumulation/Lemma-D/Theorem docs, and all other
`stageD_*` files were NOT read, per the blinding protocol).
**Family:** A1 m=3 (risefall slice, `make_risefall_slice(a, m=3)`), Z=8, ρ_c=1 gauge,
below-stuck side; family coordinate d = 1 − a/1.5 (Stage-B convention).
**Window swept:** d ∈ (1.30e-3, 2.30e-3) — FULLY swept (no throughput cut; total compute ≈ 2 min).
**Origin solver:** `cell_solver_universe_T3.py` (LSODA shooter; root function = ρ'(r_s) at the
φ=0 seal). **Independent second method:** `cascade_bv6_lib.py` (chunked DOP853, own event
location, Illinois root finder, own graduated-floor counter).
**Scripts:** `cascade_stageD_sweep_scan.py` (pass 1), `cascade_stageD_sweep_refine.py` (pass 2).
**Data:** `stageD_scan_pass1.json`, `stageD_refine_pass2.json`, `stageD_sweep_results_raw.json`.

## Method (survey)

1. **Pass 1 (scan):** geometric grid, 1201 points, Δd/d ≈ 4.76e-4 per step, d descending
   2.30e-3 → 1.30e-3. Miss f = ρ'(r_s) recorded per point; brackets = consecutive seal-seal
   sign changes. Dip detector armed for near-zero |f| arcs WITHOUT a sign change (possible
   even-multiplicity pairs): interior |f| local minimum, same sign across a 5-point window,
   flagged if |f|min < 0.05 × flanking |f|.
2. **Multiplicity guard (hazard 1):** every bracket subdivided 8×, interior sign changes
   counted; any bracket holding >1 crossing is split and recursed (cap depth 6).
3. **Method 1 root:** LSODA bisection to bracket width ≤ 1e-12 in d (rtol=1e-10, atol=1e-12,
   the origin-solver defaults).
4. **Characterization:** Stage-B graduated-floor counters verbatim (`cascade_stageB_common.py`):
   relative floors 1e-1 … 1e-12 at 4/decade; a count is banked only from a plateau spanning
   ≥ 2 decades; dense grids 100001 AND 200001 points (both recorded).
5. **Method 2 root (independent):** bv6 chunked-DOP853 shooter (rtol=1e-11, atol=1e-13; failed-
   chunk partial-dense seal scan built in) + Illinois in a-space, xtol=1e-11; bv6's OWN
   graduated-floor counter (floors 1e-4…1e-11, plateau ≥ 3 floors, 20001 + 40001 pts) re-counts
   N_δ and N_ρ' on its own trajectory. A root enters the table only with both methods sealing
   and agreeing.

## RESULTS — 20 rungs found; every root two-method confirmed; zero unresolved, zero failed points

**Counts: 20 rungs in the full window d ∈ (1.30e-3, 2.30e-3); 13 rungs in (1.45e-3, 2.11e-3).**
N runs over consecutive integers 20…39 (N_δ = N_ρ' on every rung, all four counters, both
methods, both grid densities).

| d (root, method 1) | bisect width | N_δ | N_ρ' | 200k re-check (N_δ/N_ρ') | bv6 counts (N_δ/N_ρ') | a_seal = \|ρ_s−1\| | q | ρ_s (side) | L_proper | \|d₁−d₂\| two-method |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.2843639710e-03 | 5.2e-13 | 20 | 20 | 20/20 | 20/20 | 0.042191 | 0.41520 | 1.042191 (>1) | 38.4169 | 2.8e-10 |
| 2.2039450927e-03 | 1.0e-12 | 21 | 21 | 21/21 | 21/21 | 0.040914 | 0.39658 | 0.959086 (<1) | 40.2213 | 3.1e-10 |
| 2.1288864689e-03 | 9.7e-13 | 22 | 22 | 22/22 | 22/22 | 0.038697 | 0.37967 | 1.038697 (>1) | 42.0223 | 3.3e-10 |
| 2.0577417608e-03 | 9.3e-13 | 23 | 23 | 23/23 | 23/23 | 0.037413 | 0.36404 | 0.962587 (<1) | 43.8278 | 3.1e-10 |
| 1.9910553287e-03 | 9.0e-13 | 24 | 24 | 24/24 | 24/24 | 0.035736 | 0.34974 | 1.035736 (>1) | 45.6304 | 2.2e-10 |
| 1.9277336730e-03 | 8.7e-13 | 25 | 25 | 25/25 | 25/25 | 0.034465 | 0.33643 | 0.965535 (<1) | 47.4369 | 3.3e-10 |
| 1.8681742877e-03 | 8.5e-13 | 26 | 26 | 26/26 | 26/26 | 0.033195 | 0.32417 | 1.033195 (>1) | 49.2409 | 3.4e-10 |
| 1.8115317445e-03 | 8.2e-13 | 27 | 27 | 27/27 | 27/27 | 0.031947 | 0.31271 | 0.968053 (<1) | 51.0483 | 3.2e-10 |
| 1.7580996965e-03 | 8.0e-13 | 28 | 28 | 28/28 | 28/28 | 0.030991 | 0.30208 | 1.030991 (>1) | 52.8535 | 2.9e-10 |
| 1.7072122586e-03 | 7.7e-13 | 29 | 29 | 29/29 | 29/29 | 0.029773 | 0.29210 | 0.970227 (<1) | 54.6616 | 2.3e-10 |
| 1.6590880518e-03 | 7.5e-13 | 30 | 30 | 30/30 | 30/30 | 0.029061 | 0.28280 | 1.029061 (>1) | 56.4678 | 2.7e-10 |
| 1.6131941021e-03 | 7.3e-13 | 31 | 31 | 31/31 | 31/31 | 0.027876 | 0.27403 | 0.972124 (<1) | 58.2765 | 2.1e-10 |
| 1.5696942664e-03 | 7.1e-13 | 32 | 32 | 32/32 | 32/32 | 0.027356 | 0.26582 | 1.027356 (>1) | 60.0836 | 2.5e-10 |
| 1.5281564318e-03 | 6.9e-13 | 33 | 33 | 33/33 | 33/33 | 0.026206 | 0.25807 | 0.973794 (<1) | 61.8928 | 2.5e-10 |
| 1.4887039755e-03 | 6.8e-13 | 34 | 34 | 34/34 | 34/34 | 0.025839 | 0.25077 | 1.025839 (>1) | 63.7006 | 2.4e-10 |
| 1.4509827346e-03 | 6.6e-13 | 35 | 35 | 35/35 | 35/35 | 0.024724 | 0.24385 | 0.975276 (<1) | 65.5104 | 2.4e-10 |
| 1.4150862672e-03 | 6.4e-13 | 36 | 36 | 36/36 | 36/36 | 0.024481 | 0.23732 | 1.024481 (>1) | 67.3188 | 2.4e-10 |
| 1.3807213706e-03 | 6.3e-13 | 37 | 37 | 37/37 | 37/37 | 0.023401 | 0.23112 | 0.976599 (<1) | 69.1290 | 2.4e-10 |
| 1.3479595305e-03 | 6.1e-13 | 38 | 38 | 38/38 | 38/38 | 0.023258 | 0.22524 | 1.023258 (>1) | 70.9380 | 2.4e-10 |
| 1.3165560367e-03 | 6.0e-13 | 39 | 39 | 39/39 | 39/39 | 0.022213 | 0.21964 | 0.977787 (<1) | 72.7485 | 2.1e-10 |

(a_seal ≡ |ρ_s − 1|, the sealing amplitude of δ = ρ − 1 at the seal — the seal is a ρ-extremum
since ρ'(r_s)=0, so this is the terminal lobe amplitude; matches the banked codex convention,
cf. `cascade_bv9_reshoot.py` "banked |rho_s − 1|".)

**Adjacent-root d ratios (observed, per descending d):** 0.96480, 0.96594, 0.96658, 0.96759,
0.96820, 0.96910, 0.96968, 0.97050, 0.97106, 0.97181, 0.97234, 0.97303, 0.97354, 0.97418,
0.97466, 0.97526, 0.97572, 0.97627, 0.97670.

**Per-rung identity/soundness diagnostics (all 20 rungs):** |Δφ − ln(1101)| ≤ 1.1e-14;
|2m/ρ(seal) − 1| ≤ 6.1e-15; H_drift ≤ 8.3e-10; residual |ρ'(r_s)| at the converged root ≤ 7.8e-08.
ρ_s side alternates every rung across all 20 (even N: ρ_s>1, odd N: ρ_s<1, as tabulated —
recorded as observed, no comparison drawn).

## Floor-audit summary (mandatory; hazard 2)

- **N_δ:** plateau spans 10.2–10.8 decades on every rung (stable from relative floor
  ~1.8e-2–5.6e-2 all the way to 1e-12). N_δ never wobbled at any floor on any rung.
- **N_ρ':** plateau spans 7.5–7.8 decades on every rung (stable from ~3.2e-5–5.6e-5 down to
  1e-12). **The loose-floor undercount hazard reproduced live on every rung:** at relative
  floor 1e-1 N_ρ' reads 9–18 LOW (e.g. rung N=39 reads 21 at floor 1e-1, 24 at 5.6e-2, …,
  reaching the true 39 only near 3.2e-5). A naive single-floor count at 1e-2–1e-1 would have
  systematically undercounted every rung in this window. Full 45-floor profiles for every rung
  are in `stageD_refine_pass2.json` (`profiles`).
- 200k-point re-check equals the 100k count on every rung, both counters; bv6's independent
  counter (own floors, own trajectory, 20k + 40k pts) equals both on every rung.

## Hazards encountered / guarded

1. **Dense clusters (hazard 1):** NONE found. Every pass-1 bracket held exactly one crossing
   under 8× subdivision; inter-root spacing (2.3–3.5% of d) is 50–70× the pass-1 grid step
   (0.048%); dip detector found zero deep same-sign arcs (no evidence of unresolved even pairs).
2. **Loose-floor undercount (hazard 2):** live on every rung; defeated by the ≥2-decade plateau
   discipline (see floor audit above).
3. **Failed-chunk-contains-seal (hazard 3):** the bv6 shooter's partial-dense scan was armed; no
   failed chunks occurred in this window.
4. **Failed points (hazard 4):** ZERO — all 1201 scan shots + all refine shots returned status
   `seal`; no collapse, no no-seal, no non-finite miss. Nothing was interpolated over.

**Unresolved spans: none. Un-swept spans: none (window fully covered).** Edge coverage: above
the top rung, 14 grid points to d=2.30e-3 with no sign change (min |f| = 4.4e-3); below the
bottom rung, 26 grid points to d=1.30e-3 with no sign change (min |f| = 3.9e-3).

## Shot ledger

Pass-1 scan 1201 (LSODA) + multiplicity guard & bisection 581 (LSODA) + bv6 122 (DOP853) =
**1904 shots**, wall ≈ 92 s total. Single process throughout; no GPU; no background polling.

## Premise ledger (chose-or-derived)

Inherited from the task/Stage-B family definition (not chosen here): slice family risefall m=3
(CHOSE at Stage B), Z=8 (FREE-and-explored, Route-B probe value), ρ_c=1 (gauge WLOG,
homothety-covariance THEORY per T3), φ_c=−ln(1101) (OBSERVATIONAL PIN, canon), U(ρ_c)=2
(THEORY + ruling), potential-only φ-blind matter (CHOSE, T3 slice family), d = 1−a/1.5
coordinate (Stage-B convention, kept for comparability), below-stuck side (task).

Category-A conditioning chosen by this survey (soundness record, no physics content):
pass-1 grid 1201 geometric points (Δd/d≈4.76e-4); dip-detector threshold 0.05× flank;
multiplicity guard 8× subdivision, recursion cap 6; bisection width cap 1e-12 in d (≤45 steps);
LSODA rtol=1e-10/atol=1e-12 (origin defaults); bv6 DOP853 rtol=1e-11/atol=1e-13, Illinois
xtol=1e-11 in a, maxit=30; counter grids 100001/200001 (Stage-B) and 20001/40001 (bv6); floor
schedules as in the two harnesses (verbatim reuse). No agreement threshold was pre-set for the
two-method check; the raw |d₁−d₂| is reported per rung (max 3.4e-10).

## Blinding statement

Not read: `cascade_stageD_prereg.md`, any other `stageD_*` file, `ladder_theta0_accumulation_results.md`,
`ladder_lemmaD_sealing_amplitude_results.md`, `ladder_theorems_AB_C_results.md`. No rung
positions were predicted or extrapolated from any law; the grid was uniform-geometric over the
whole window and every root was found by sign change only. Files read for method: Stage-B
results METHODS/hazards, `cascade_stageB_*.py`, `cascade_stageB_common.py`, `cascade_bv6_lib.py`,
`cell_solver_universe_T3.py`, plus a grep for the `a_seal` definition line in
`cascade_bv9_reshoot.py` (definition only).
