# E2b SWEEP — BRACKET 3 (A3, Z=8): results (OBSERVE mode)

**Date:** 2026-07-03 (late). **Status: PROVISIONAL — sweep agent output, NOT verified, NOT
banked.** Contract: `microphysics_E2_battle_plan.md` (APPROVED AS WRITTEN). Machinery:
`cell_solver_composite.py` UNCHANGED (imported; same state as brackets 1–2, clean tree). Scripts
adapted (not rewritten) from the bracket-2 sweep per the E2b brief; the ACCUMULATED bracket-1+2
conditioning notes (`microphysics_E2b_A1Z8_results.md` §8 + `microphysics_E2b_A1Z1_results.md`
§8) followed: full matrix without triage, 0.10·r_s caps, ONE wide-guard dilation-exponent run,
H_cell read on EVERY end state, EXTEND-FLOOR on the parked state, ρ_p + U(ρ_p) read on wall end
states (the station-lock cross-family question). Data-blind: no particle masses/data anywhere.
Everything below is WHAT THE COUPLED SYSTEM DID — no merit gating; non-convergence is
first-class data. FIRST A3-FAMILY BRACKET (the ambient slice family switches from A1 to A3
through the same `make_slice` dispatch; nothing else changes).

**Headline observation (scoped to this bracket, this grid, these seeds): the coupled composite
converged NOWHERE — 0 of 62 phase-1 solves, 0 of 16 phase-2 flooring solves, 0 of 1 wide-guard,
0 of 1 extended-floor, 0 of 2 grid cross-checks reached the pre-committed floor max|F| ≤ 1e-8.
The same two behaviors as brackets 1–2, now cross-FAMILY: (1) the dominant cap-speed outward
runaway to the 5·r_s guard (42/62 press it), approximately self-similar with residual ~ r^−1.00
along the dilation orbit; (2) the station-parked ultra-slow outward translation (ncap = 0) on
wall-seeded N=2 κ=1 cells — and, NEW in this bracket, the parked basin is WIDER: it captures the
wall-seeded small-coupling controls (C1, C2) and even W1 at amp 1.5, and the N=2 κ=1 lock
survives amp 1.5 (bracket 2's amp-1.5 seeds broke it). The U = 2.000 seal lock IS present in the
A3 family and is shell-relative — with a SHARPENED diagnosis that partially regrades bracket 2's
wording: on every wall end state (parked AND runaway) ρ_p equals the SEED's shell height
ρ(0.95·r_s) to 5–7 digits (here 1.011441–1.011494 vs seed 1.0114407; station b^{−1/2} =
1.0120927), and a retro-check shows bracket 2's "locked" ρ_p = 1.003689 was ITS seed value
1.0036886 too (station 1.003829). So the lock = the seal PRESERVES its seed shell-relative
height exactly while the whole composite translates; U(ρ_p) ≈ 2 because 0.95·r_s sits on the
U≈2 shoulder. What IS solver-tuned is the C2 row: E_ang(seal) self-tunes to U(ρ_p) (2.001–2.007
on the locked family). The extended floor (4000 further iterations) shows the parked state
CREEPS (pure translation, width 36.0490 → 36.0487, ρ_p frozen at 1.0114454) with Φ still
falling and H_cell pinned at 1.63 — a slow-motion false floor, not a finite-size solution;
station-parking is now confirmed in BOTH families (3 of 3 brackets that have wall-admissible
N=2 κ≈1 cells).**

Sections: 1 setup/premises · 2 phase-1 outcome table · 3 phase-2 flooring + wide-guard/dilation
exponent · 4 the station-lock story (cross-family verdict + regrade) · 5 residual anatomy +
grid cross-check · 6 pre-committed failure reading · 7 coverage statement · 8 conditioning
notes for bracket 4 · files.

## 1. Setup and premise ledger (chose-or-derived; E1 ledger #1–#17 inherited UNCHANGED)

Bracket: A3, Z=8 (banked E0: a* = b = 0.9762462715 HELD, r_s = 720.9907, ρ_s = 2.421082,
q = 11.165535, ρ_c = 1; U_seal = U(ρ_s) = 0.6707 — between bracket 1's 0.052 and bracket 2's
1.409). A3 slice: U = 2ρ²(1+b)/(1+bρ⁴); its U=2 roots are ρ = 1 (core fold) and ρ = b^{−1/2} =
1.0120927 (the wall station; E1: r* = 0.95228·r_s = 686.59, ρ(r*) = 1.0120923). E1 audit: the
N=2 inversion IS present in this bracket (present 3 of 4, absent only A1 Z=8) → the N=2 κ=1
wall-admissible cells are genuine articles. Anchor per plan wording fix: a* HELD; Δφ floats and
is REPORTED (P-E2b3-8, THEORY: E1 ledger #5).

| # | Premise (this run) | Tag |
|---|---|---|
| P-E2b3-1 | Window cells W1–W6, C1, C2 from the E1 `necessary_map` for THIS bracket. W5/W6 = the GENUINE wall-admissible N=2 κ=1 articles (admfrac 0.122/0.114, outer_seal_admissible=True). Controls C1/C2 genuinely admfrac 1.0 — NO substitute flags. ONE flag: W3 (N=1, ξ=1, κ=0.1) has admfrac 0.905 and outer_seal_admissible=False in THIS bracket (was 1.0 in brackets 1–2); kept for cross-bracket comparability. | CHOSE (map-guided) |
| P-E2b3-2 | Slices: plateau-target r_p0 = 100.0 (same absolute value as brackets 1–2; r_p0/r_s ≈ 0.139); wall-target r_p0 = 0.95·r_s = 684.94 (r* = 686.59). Seed placements only; r_p FREE. | CHOSE |
| P-E2b3-3 | Seed amplitudes amp ∈ {0.3, 0.8, 1.5}, bulge = amp·(1−μ²)·sin(π(ζ+1)/2) on the rigid map | CHOSE (banked undersampling lesson; bulge theorem = non-perturbative in θ) |
| P-E2b3-4 | Grids Nr=12, Nθ=8, Na=192, kmap=2.5 (brackets-1/2 choice unchanged); confirm grids reserved for candidates (none arose); grid cross-check run anyway on the two key behaviors (§5) | Category-A conditioning |
| P-E2b3-5 | LM maxit 150 (phase 1) / 2000 (phase 2) / 4000 (extended floor), wall 75/240/300 s; free-boundary per-iteration caps \|Δr_p\|,\|Δr_sU\| ≤ 0.10·r_s (whole-step rescale); validity guard r_p ∈ (1e-6·r_s, r_sU), r_sU < 5·r_s (25·r_s in the one wide-guard run) — reject-step guards, never constraint rows | Category-A trust handling (brackets-1/2 pattern, pre-authorized) |
| P-E2b3-6 | Convergence = max\|F\|∞ ≤ 1e-8 (rows O(1) at seed) | Pre-committed (plan instrument 1) |
| P-E2b3-7 | Continuation seeds: best-Φ W1 end state per slice, re-solved under each other cell's couplings. BOTH donors ended guard-parked (rsU 3572–3605 > 4.5·r_s) → poisoned-donor flag carried per row (`donor_guard_parked: true`), per the bracket-2 conditioning note; no non-guard donor existed among W1 end states to substitute | Plan method + bracket-2 note (flagged) |
| P-E2b3-9 | Budget: coverage-first order; internal 70-min cap; actual total compute ≈ 15 min of the ~90-min ceiling | anti-hang |

Window cells (all from `microphysics_E1_probe_results.json` necessary_map, A3 Z=8):

| cell | N | ξ | κ | provenance |
|---|---|---|---|---|
| W1 | 1 | 0.5 | 0.1 | moderate-ξ plateau (admfrac 1.0); identical to brackets 1–2 → continuation start + comparability |
| W2 | 1 | 0.2 | 0.1 | moderate-ξ plateau neighbor (admfrac 1.0) |
| W3 | 1 | 1.0 | 0.1 | moderate-ξ plateau neighbor — **admfrac 0.905 here, outer_seal_admissible=False (FLAGGED, kept for comparability)** |
| W4 | 1 | 0.5 | 1.0 | κ-continuation neighbor (admfrac 1.0) |
| W5 | 2 | 0.05 | 1.0 | **WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.122, outer_seal_admissible=True) — E1-inversion bracket, genuine |
| W6 | 2 | 0.1 | 1.0 | **2nd WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.114, outer_seal_admissible=True) |
| C1 | 1 | 0.05 | 0.01 | fully-admissible small-coupling control (admfrac 1.0) |
| C2 | 2 | 0.05 | 0.01 | 2nd fully-admissible control (admfrac 1.0 — genuine, no flag) |

GPU discipline: V100 torch float64; GPU-vs-CPU seed-residual spot-check rel maxdiff 6.85e-12
(JSON `notes`); no batched-triangular-solve anywhere; anatomy recomputed on CPU from saved
fields — **18/18 states match GPU to machine precision** (§5; no overflow exception this
bracket — the extreme states here run φ_cell NEGATIVE/deep, e^{2φ} underflow direction, which
does not amplify device rounding the way bracket 2's φ ~ +50 overflow states did).

## 2. Phase-1 outcome table (62 solves: 8 cells × 2 slices × 3 amps + 14 continuation)

Statuses: **CONVERGED 0 / stalled 38 / iter-or-wall-capped 24 / throughput-limited 0.**
Top-holdout-row census over all 62: C1c f_r(seal) 34, f-PDE 12, C2 10, amb phi-ODE 2,
seal [rho] 2, cell rho-ODE 1, C1b 1 — **C1c is still the wall** (34/62 vs 25/62 bracket 2).
Free boundaries: 46/62 ended with r_sU > 2·r_s; 42/62 pressed the 5·r_s guard (3605.0).
H_cell_max ≥ 0.99 on every one of the 62 end states (median ≈ 2.0, max 5.4e27): nothing is
near a true composite solution anywhere. Bold rows = the parked (ncap = 0, finite-r_p) family
— NOTE it now includes the CONTROLS and a W1 amp-1.5 row, not just the wall-admissible N=2 κ=1
cells.

| run (cell/slice/seed) | status | Φ_end | max\|F\| | iters | ncap | r_p → | r_sU → | top residual row | H_cell_max |
|---|---|---|---|---|---|---|---|---|---|
| W1/plateau/bulge-amp0.8 | stalled | 2.1e-03 | 1.1e-02 | 47 | 88 | 100→2904 | 721→3557 | f-PDE (1.1e-02) | 2.7e+18 |
| W1/wall/bulge-amp0.8 | stalled | 2.7e-04 | 9.1e-03 | 76 | 94 | 685→3569 | 721→3605 | C1c f_r(seal) (9.1e-03) | 1.5e+00 |
| W2/plateau/bulge-amp0.8 | stalled | 9.7e-04 | 1.4e-02 | 66 | 96 | 100→2914 | 721→3605 | C1c f_r(seal) (1.4e-02) | 1.8e+00 |
| W2/wall/bulge-amp0.8 | iter/wall-capped | 1.1e-03 | 1.8e-02 | 150 | 21 | 685→1660 | 721→1696 | C1c f_r(seal) (1.8e-02) | 2.0e+00 |
| W3/plateau/bulge-amp0.8 | stalled | 7.1e-04 | 9.2e-03 | 48 | 90 | 100→2911 | 721→3534 | amb phi-ODE (9.2e-03) | 2.9e+00 |
| W3/wall/bulge-amp0.8 | stalled | 1.7e-04 | 5.4e-03 | 66 | 90 | 685→3544 | 721→3580 | C1c f_r(seal) (5.4e-03) | 9.9e-01 |
| W4/plateau/bulge-amp0.8 | stalled | 6.4e-03 | 5.1e-02 | 48 | 100 | 100→2880 | 721→3580 | cell rho-ODE (5.1e-02) | 1.7e+02 |
| W4/wall/bulge-amp0.8 | iter/wall-capped | 5.6e-04 | 1.3e-02 | 150 | 8 | 685→1096 | 721→1132 | C1c f_r(seal) (1.3e-02) | 1.6e+00 |
| W5/plateau/bulge-amp0.8 | stalled | 2.0e-04 | 5.8e-03 | 51 | 103 | 100→2884 | 721→3588 | amb phi-ODE (5.8e-03) | 1.9e+00 |
| **W5/wall/bulge-amp0.8** | iter/wall-capped | 3.5e-04 | 8.4e-03 | 150 | **0** | 685→688 | 721→724 | C1c f_r(seal) (8.4e-03) | 1.9e+00 |
| W6/plateau/bulge-amp0.8 | iter/wall-capped | 2.2e-03 | 1.8e-02 | 150 | 19 | 100→598 | 721→1219 | C1c f_r(seal) (1.8e-02) | 1.8e+00 |
| **W6/wall/bulge-amp0.8** | iter/wall-capped | 1.5e-02 | 3.2e-02 | 150 | **0** | 685→689 | 721→725 | C1b (3.2e-02) | 3.5e+01 |
| C1/plateau/bulge-amp0.8 | stalled | 2.9e-01 | 5.4e-01 | 50 | 82 | 100→2954 | 721→3594 | C2 (5.4e-01) | 2.5e+01 |
| **C1/wall/bulge-amp0.8** | iter/wall-capped | 3.6e-02 | 1.0e-01 | 150 | **0** | 685→886 | 721→922 | C1c f_r(seal) (1.0e-01) | 2.0e+00 |
| C2/plateau/bulge-amp0.8 | stalled | 4.9e-02 | 2.0e-01 | 47 | 86 | 100→2941 | 721→3566 | C2 (2.0e-01) | 1.9e+00 |
| **C2/wall/bulge-amp0.8** | iter/wall-capped | 5.0e-02 | 7.9e-02 | 150 | **0** | 685→695 | 721→731 | C1c f_r(seal) (7.9e-02) | 1.4e+02 |
| W1/plateau/bulge-amp0.3 | stalled | 8.3e-04 | 1.1e-02 | 48 | 89 | 100→2903 | 721→3572 | C1c f_r(seal) (1.1e-02) | 1.2e+01 |
| W1/wall/bulge-amp0.3 | stalled | 2.7e-04 | 9.1e-03 | 74 | 94 | 685→3569 | 721→3605 | C1c f_r(seal) (9.1e-03) | 1.5e+00 |
| W2/plateau/bulge-amp0.3 | stalled | 8.6e-04 | 1.4e-02 | 72 | 93 | 100→2984 | 721→3605 | C1c f_r(seal) (1.4e-02) | 1.8e+00 |
| W2/wall/bulge-amp0.3 | stalled | 6.8e-04 | 1.9e-02 | 87 | 95 | 685→3569 | 721→3605 | C1c f_r(seal) (1.9e-02) | 1.9e+00 |
| W3/plateau/bulge-amp0.3 | stalled | 2.4e-04 | 6.2e-03 | 49 | 93 | 100→2980 | 721→3589 | C1c f_r(seal) (6.2e-03) | 7.4e+19 |
| W3/wall/bulge-amp0.3 | stalled | 9.4e-05 | 5.4e-03 | 78 | 95 | 685→3569 | 721→3605 | C1c f_r(seal) (5.4e-03) | 9.9e-01 |
| W4/plateau/bulge-amp0.3 | stalled | 3.0e-03 | 1.3e-02 | 49 | 81 | 100→2902 | 721→3546 | f-PDE (1.3e-02) | 1.8e+12 |
| W4/wall/bulge-amp0.3 | iter/wall-capped | 1.1e-04 | 6.3e-03 | 150 | 30 | 685→1881 | 721→1917 | C1c f_r(seal) (6.3e-03) | 2.0e+00 |
| W5/plateau/bulge-amp0.3 | stalled | 1.2e-04 | 3.8e-03 | 50 | 77 | 100→2842 | 721→3540 | seal [rho] (3.8e-03) | 1.9e+00 |
| **W5/wall/bulge-amp0.3** | iter/wall-capped | 1.5e-04 | 6.2e-03 | 150 | **0** | 685→688 | 721→724 | C1c f_r(seal) (6.2e-03) | 1.6e+00 |
| W6/plateau/bulge-amp0.3 | iter/wall-capped | 1.5e-02 | 3.6e-02 | 150 | 1 | 100→326 | 721→947 | seal [rho] (3.6e-02) | 5.2e+01 |
| **W6/wall/bulge-amp0.3** | iter/wall-capped | 6.7e-04 | 1.6e-02 | 150 | **0** | 685→761 | 721→797 | C1c f_r(seal) (1.6e-02) | 1.6e+00 |
| C1/plateau/bulge-amp0.3 | stalled | 3.1e-01 | 5.6e-01 | 48 | 80 | 100→2947 | 721→3580 | C2 (5.6e-01) | 2.8e+00 |
| C1/wall/bulge-amp0.3 | stalled | 3.7e-03 | 2.5e-02 | 73 | 89 | 685→3504 | 721→3545 | C1c f_r(seal) (2.5e-02) | 1.9e+00 |
| C2/plateau/bulge-amp0.3 | stalled | 5.1e-02 | 2.1e-01 | 47 | 84 | 100→2934 | 721→3563 | C2 (2.1e-01) | 4.4e+00 |
| C2/wall/bulge-amp0.3 | iter/wall-capped | 1.5e-03 | 1.5e-02 | 150 | 90 | 685→3544 | 721→3580 | C1c f_r(seal) (1.5e-02) | 5.4e+27 |
| W1/plateau/bulge-amp1.5 | stalled | 1.5e-02 | 4.8e-02 | 48 | 93 | 100→2961 | 721→3584 | f-PDE (4.8e-02) | 3.9e+10 |
| **W1/wall/bulge-amp1.5** | iter/wall-capped | 7.6e-03 | 4.6e-02 | 150 | **0** | 685→705 | 721→741 | C1c f_r(seal) (4.6e-02) | 1.6e+00 |
| W2/plateau/bulge-amp1.5 | stalled | 4.5e-03 | 1.9e-02 | 49 | 95 | 100→2984 | 721→3604 | f-PDE (1.9e-02) | 4.1e+04 |
| W2/wall/bulge-amp1.5 | iter/wall-capped | 3.0e-03 | 3.0e-02 | 150 | 9 | 685→1275 | 721→1312 | C1c f_r(seal) (3.0e-02) | 2.0e+00 |
| W3/plateau/bulge-amp1.5 | stalled | 3.5e-03 | 1.6e-02 | 48 | 96 | 100→2917 | 721→3543 | f-PDE (1.6e-02) | 3.3e+00 |
| W3/wall/bulge-amp1.5 | stalled | 9.4e-05 | 5.4e-03 | 98 | 94 | 685→3569 | 721→3605 | C1c f_r(seal) (5.4e-03) | 1.0e+00 |
| W4/plateau/bulge-amp1.5 | iter/wall-capped | 1.2e-04 | 5.9e-03 | 150 | 95 | 100→2984 | 721→3605 | C1c f_r(seal) (5.9e-03) | 1.5e+00 |
| W4/wall/bulge-amp1.5 | iter/wall-capped | 2.5e-04 | 1.0e-02 | 150 | 3 | 685→1136 | 721→1172 | C1c f_r(seal) (1.0e-02) | 2.0e+00 |
| W5/plateau/bulge-amp1.5 | iter/wall-capped | 1.1e-03 | 1.7e-02 | 150 | 71 | 100→2071 | 721→2692 | f-PDE (1.7e-02) | 1.4e+02 |
| **W5/wall/bulge-amp1.5** | iter/wall-capped | 3.0e-03 | 3.9e-02 | 150 | **0** | 685→688 | 721→724 | f-PDE (3.9e-02) | 2.0e+00 |
| W6/plateau/bulge-amp1.5 | iter/wall-capped | 1.4e+00 | 4.6e-01 | 150 | 24 | 100→22 | 721→654 | f-PDE (4.6e-01) | 9.6e+02 |
| **W6/wall/bulge-amp1.5** | iter/wall-capped | 7.1e-02 | 7.9e-02 | 150 | **0** | 685→687 | 721→723 | f-PDE (7.9e-02) | 9.5e+01 |
| C1/plateau/bulge-amp1.5 | stalled | 3.2e-01 | 5.6e-01 | 49 | 83 | 100→2920 | 721→3557 | C2 (5.6e-01) | 1.9e+00 |
| C1/wall/bulge-amp1.5 | iter/wall-capped | 3.4e-03 | 2.5e-02 | 150 | 59 | 685→2738 | 721→2774 | C1c f_r(seal) (2.5e-02) | 5.6e+00 |
| C2/plateau/bulge-amp1.5 | stalled | 4.5e-02 | 1.9e-01 | 47 | 87 | 100→2899 | 721→3538 | C2 (1.8e-01) | 7.0e+00 |
| **C2/wall/bulge-amp1.5** | iter/wall-capped | 5.2e-02 | 8.4e-02 | 150 | **0** | 685→693 | 721→729 | C1c f_r(seal) (8.4e-02) | 8.5e+01 |
| W2/plateau/cont-W1 | stalled | 9.5e-04 | 1.6e-02 | 19 | 8 | 2903→2935 | 3572→3605 | C1c f_r(seal) (1.6e-02) | 1.8e+00 |
| W2/wall/cont-W1 | stalled | 1.2e+00 | 1.0e+00 | 1 | 0 | 3569→3569 | 3605→3605 | C2 (1.0e+00) | 1.8e+00 |
| W3/plateau/cont-W1 | stalled | 1.5e-04 | 6.9e-03 | 23 | 6 | 2903→2935 | 3572→3605 | C1c f_r(seal) (6.9e-03) | 9.9e-01 |
| W3/wall/cont-W1 | stalled | 3.3e+00 | 1.7e+00 | 1 | 0 | 3569→3569 | 3605→3605 | C2 (1.7e+00) | 1.7e+00 |
| W4/plateau/cont-W1 | stalled | 1.9e-04 | 6.6e-03 | 24 | 6 | 2903→2935 | 3572→3605 | C1c f_r(seal) (6.6e-03) | 1.5e+00 |
| W4/wall/cont-W1 | stalled | 4.0e+01 | 4.3e+00 | 1 | 0 | 3569→3569 | 3605→3605 | f-PDE (4.3e+00) | 2.7e+00 |
| W5/plateau/cont-W1 | iter/wall-capped | 6.2e-05 | 3.6e-03 | 150 | 6 | 2903→2929 | 3572→3599 | C1c f_r(seal) (3.6e-03) | 1.9e+00 |
| W5/wall/cont-W1 | stalled | 7.7e+02 | 1.9e+01 | 1 | 0 | 3569→3569 | 3605→3605 | f-PDE (1.9e+01) | 1.0e+01 |
| W6/plateau/cont-W1 | iter/wall-capped | 9.4e-05 | 4.6e-03 | 150 | 6 | 2903→2935 | 3572→3605 | C1c f_r(seal) (4.6e-03) | 3.1e+00 |
| W6/wall/cont-W1 | stalled | 7.8e+02 | 1.9e+01 | 1 | 0 | 3569→3569 | 3605→3605 | f-PDE (1.9e+01) | 1.0e+01 |
| C1/plateau/cont-W1 | stalled | 4.8e-03 | 3.3e-02 | 39 | 9 | 2903→2936 | 3572→3605 | C1c f_r(seal) (3.3e-02) | 1.9e+00 |
| C1/wall/cont-W1 | stalled | 3.2e+00 | 1.8e+00 | 1 | 0 | 3569→3569 | 3605→3605 | C2 (1.8e+00) | 2.0e+00 |
| C2/plateau/cont-W1 | stalled | 3.3e-03 | 2.3e-02 | 46 | 9 | 2903→2936 | 3572→3605 | C1c f_r(seal) (2.3e-02) | 1.8e+03 |
| C2/wall/cont-W1 | stalled | 3.6e+00 | 1.6e+00 | 1 | 0 | 3569→3569 | 3605→3605 | C2 (1.6e+00) | 1.9e+00 |

Notes: (a) Continuation = the bracket-2 pattern EXACTLY (both W1 donors ended guard-parked →
`donor_guard_parked: true` on all 14 rows; wall-side rows 1-iteration C2/f-PDE-jump stall,
plateau-side rows descend normally to the same C1c-held floors; W5/plateau/cont-W1 = the
sweep's lowest Φ, 6.2e-5). The poisoned-donor mechanism is now seen in all three brackets.
(b) The inward-collapse curiosity recurs: W6/plateau/amp1.5 ran INWARD (r_p 100 → 22, residual
0.46, not a floor) — bracket 2 had W5+W6 inward; here only W6 (W5/plateau/amp1.5 ran outward).
(c) The small-coupling controls on the PLATEAU slice hold C2 as top row with E_ang(seal) unable
to reach 2 (C1: 1.46, C2: 1.82) — same signature as brackets 1–2. On the WALL slice, however,
the controls PARK (ncap = 0, r_p → 886/695) with E_ang(seal) ≈ 1.991 — nearly paying U = 2 —
and hold out on C1c instead: a bracket novelty (bracket 2's controls joined the fast runaway).

## 3. Phase-2: flooring (maxit 2000) + the wide-guard / dilation-exponent run

Best phase-1 config per (cell × slice) re-run at maxit=2000, wall 240 s; then ONE widened-guard
run (r_sU < 25·r_s, per-iteration caps unchanged) on the best guard-presser (W3/wall/amp0.3).
Gate columns read on END states.

| run | status | Φ_end | max\|F\| | iters | ncap | r_p → | r_sU → | ρ_p | U(ρ_p) | Δφ_float | H_cell_max | q_fold | q_seal | E_ang_seal | top row |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P2/C1/plateau/amp0.8 | stalled | 2.9e-01 | 5.4e-01 | 50 | 82 | →2954 | →3594 | 0.996302 | 1.999767 | 4.16 | 2.5e+01 | 11.1863 | −0.296 | 1.4647 | C2 (5.4e-01) |
| P2/C1/wall/amp1.5 | iter/wall-capped | 2.6e-03 | 2.2e-02 | 2000 | 59 | →3118 | →3155 | 1.011432 | 2.000030 | 10.48 | 1.1e+01 | 11.1660 | 0.279 | 1.9978 | C1c (2.2e-02) |
| P2/C2/plateau/amp1.5 | stalled | 4.5e-02 | 1.8e-01 | 47 | 87 | →2899 | →3538 | 1.000161 | 2.000008 | 6.18 | 7.0e+00 | 11.1880 | −0.738 | 1.8154 | C2 (1.8e-01) |
| P2/C2/wall/amp0.3 | iter/wall-capped | 1.5e-03 | 1.5e-02 | 2000 | 90 | →3544 | →3580 | 1.010617 | 2.000062 | 41.35 | 5.4e+27 | 11.1660 | 0.211 | 1.9997 | C1c (1.5e-02) |
| P2/W1/plateau/amp0.3 | stalled | 8.3e-04 | 1.1e-02 | 48 | 89 | →2903 | →3572 | 1.015593 | 1.999786 | 5.09 | 1.2e+01 | 11.1696 | 0.247 | 1.9998 | C1c (1.1e-02) |
| P2/W1/wall/amp0.8 | stalled | 2.7e-04 | 9.1e-03 | 76 | 94 | →3569 | →3605 | 1.011441 | 2.000029 | 4.64 | 1.5e+00 | 11.1657 | 0.279 | 1.9999 | C1c (9.1e-03) |
| P2/W2/plateau/amp0.3 | stalled | 8.6e-04 | 1.4e-02 | 72 | 93 | →2984 | →3605 | 0.998051 | 1.999891 | 4.80 | 1.8e+00 | 11.1656 | 0.025 | 1.9997 | C1c (1.4e-02) |
| P2/W2/wall/amp0.3 | stalled | 6.8e-04 | 1.9e-02 | 87 | 95 | →3569 | →3605 | 1.011441 | 2.000029 | 9.13 | 1.9e+00 | 11.1657 | 0.279 | 1.9999 | C1c (1.9e-02) |
| P2/W3/plateau/amp0.3 | stalled | 2.4e-04 | 6.2e-03 | 49 | 93 | →2980 | →3589 | 1.001490 | 2.000063 | 30.71 | 7.4e+19 | 11.1664 | 0.142 | 1.9996 | C1c (6.2e-03) |
| P2/W3/wall/amp0.3 | stalled | 9.4e-05 | 5.4e-03 | 78 | 95 | →3569 | →3605 | 1.011439 | 2.000029 | 2.60 | 9.9e-01 | 11.1657 | 0.279 | 2.0000 | C1c (5.4e-03) |
| P2/W4/plateau/amp1.5 | stalled | 1.2e-04 | 5.9e-03 | 168 | 95 | →2984 | →3605 | 0.999746 | 1.999988 | 1.20 | 1.5e+00 | 11.1656 | −0.552 | 1.9999 | C1c (5.9e-03) |
| P2/W4/wall/amp0.3 | iter/wall-capped | 1.0e-04 | 6.3e-03 | 2000 | 30 | →1885 | →1921 | 1.011431 | 2.000030 | 1.70 | 2.0e+00 | 11.1657 | 0.278 | 2.0000 | C1c (6.3e-03) |
| P2/W5/plateau/amp0.3 | stalled | 1.2e-04 | 3.8e-03 | 50 | 77 | →2842 | →3540 | 1.001195 | 2.000052 | 5.77 | 1.9e+00 | 11.1640 | −0.208 | 2.0011 | seal [rho] (3.8e-03) |
| **P2/W5/wall/amp0.3** | iter/wall-capped | 1.5e-04 | 6.2e-03 | 2000 | **0** | →688 | →724 | 1.011445 | 2.000029 | 2.72 | 1.6e+00 | 11.1658 | 0.279 | 2.0013 | C1c (6.2e-03) |
| P2/W6/plateau/amp0.8 | iter/wall-capped | 1.8e-03 | 1.9e-02 | 2000 | 19 | →602 | →1222 | 1.000167 | 2.000008 | 2.99 | 1.8e+00 | 11.1657 | −1.937 | 2.0037 | C1c (1.9e-02) |
| **P2/W6/wall/amp0.3** | iter/wall-capped | 6.6e-04 | 1.6e-02 | 2000 | **0** | →761 | →797 | 1.011494 | 2.000027 | 0.62 | 1.6e+00 | 11.1660 | 0.278 | 2.0028 | C1c (1.6e-02) |
| P2b-wideguard/W3/wall/amp0.3 | (wide) | 4.3e-05 | 2.7e-03 | 255 | 605 | →17982 | →18018 | 1.011444 | 2.000029 | 7.66 | 9.9e-01 | 11.1656 | 0.279 | 2.0000 | f-PDE (2.7e-03) |

**Reading:** (a) NOTHING converges at 2000 iterations — floors at max|F| ~ 3.8e-3 to 0.54, far
above the 1e-8 contract floor. (b) **Wide-guard / dilation exponent:** freed to 25·r_s, the
W3/wall runaway ran the WHOLE way to the widened bound in 255 iterations (r_p → 17982 =
24.94·r_s) with Φ falling (4.3e-5) and no floor. Comparing the guard-parked parent (r_p 3568.9)
to the wide state (r_p 17981.6, dilation ×5.038): the C1c residual vector keeps sign and shape
(θ-sawtooth, antisymmetric across the equator) and scales by 5.047 ± 0.101 across the 8 θ-nodes
→ **residual ~ r^−1.00 along the dilation orbit** (exponent −1.0011; node scatter ±2%).
Cross-bracket: −1.31 (A1 Z=8, node-uniform ±1e-4), −0.99 (A1 Z=1, ±6%), **−1.00 (A3 Z=8, ±2%)**.
The exponent does NOT track the family (A3 Z=8 matches A1 Z=1, not A1 Z=8) and does not track Z
(Z=8 gives −1.31 in A1 but −1.00 in A3); on three points it correlates with U_seal (0.052 →
−1.31; 0.671 → −1.00; 1.409 → −0.99) / with having wall-admissible N=2 cells (A1 Z=8 = the one
bracket without them = the outlier). Bracket 4 (A3 Z=1) discriminates. (c) H_cell is O(1) on
every end state (≈ 1.0–2.0 on the runaway and locked families; up to 5.4e27 on extreme states
where Δφ_float → 41): every falling Φ is a false floor. (d) q_fold reads the banked
11.1640–11.1887 on every end state (banked 11.16554); Δφ floats 0.23–41.35 (vs anchor 7.004) —
unconstrained, as expected off-solution.

## 4. The station-lock story (the cross-family question, answered — with a regrade)

**Verdict asked for by the brief: the U = 2.000 seal lock IS PRESENT in this A3 bracket, and it
is SHELL-RELATIVE, not positional — the station-lock is FAMILY-UNIVERSAL as a behavior.** But
this bracket's data sharpens WHAT the lock is, and the sharpened reading partially regrades
bracket 2's wording:

- **The lock = seed-height preservation, exactly.** On EVERY wall-slice end state — parked AND
  fast-runaway alike — ρ_p = 1.011431–1.011494, i.e. the SEED's shell-relative height
  ρ(0.95·r_s) = 1.0114407 to 5–7 digits, while absolute r_p lands anywhere from 687 to 3569.
  U(ρ_p) = 2.000029 = U(seed height), not the exact station value 2.000000 (station ρ =
  b^{−1/2} = 1.0120927 sits 0.00065 higher in ρ). The extended floor pins this: over 4000
  iterations ρ_p is frozen at 1.0114454 (7 digits) while r_p creeps 687.80 → 692.12.
- **Retro-check on bracket 2 (one line of arithmetic, as the §8 note prescribed):** A1 Z=1's
  "locked" ρ_p = 1.003689 IS its seed value ρ(0.95·r_s) = 1.0036886 (U = 2.0000031); its
  station was 1.003829. So in BOTH brackets the solver does not TUNE ρ_p to the U=2 root — it
  PRESERVES the seed's shell height under rigid translation, and that height carries U ≈ 2
  because the 0.95·r_s wall seed sits on the profile's U≈2 shoulder just below the station.
  Bracket 2's "self-tuned exactly to the U=2 station (ρ_p → station at 3e-6)" is therefore
  better read as "shell-height-preserving, seed-height ≈ station": the lock is real and
  shell-relative, the "tuned to the station" attribution is owed a verifier regrade. What IS
  genuinely self-tuned is the C2 row: E_ang(seal) moves to U(ρ_p) (2.0008–2.0068 on the locked
  family; the C2 residual is ~1e-3 while C1c holds at 6e-3–8e-2).
- **The parked basin is WIDER in this bracket (the novelty):** ncap = 0 finite-size parking
  captures not only the genuine wall-admissible N=2 κ=1 cells (W5, W6 — at ALL THREE
  amplitudes; bracket 2's amp-1.5 seeds broke the lock, these don't) but also the wall-seeded
  small-coupling CONTROLS (C1 amp0.8; C2 amp0.8/1.5, r_p → 886/695/693) and W1 at amp1.5
  (r_p → 705). Wall-seeded W2/W4 show intermediate slow runaway (ncap 3–30). A raw correlate:
  this bracket's controls CAN nearly pay U = 2 at the seal (E_ang(seal) ≈ 1.991) where bracket
  2's could not (1.15/1.65) — consistent with the wall slice here being "softer" (U_seal 0.671,
  E1 ξN wall bound 0.671 vs plateau 2.0).
- **But parking is still NOT an attractor (extended-floor diagnosis, 4000 iters on
  P2/W5/wall):** r_p creeps 687.797 → 692.117 with the shell width EXACTLY preserved (36.0490 →
  36.0487 — pure translation, zero dilation), ρ_p frozen (above), Φ still falling (1.46e-4 →
  1.385e-4), max|F| 6.23e-3 → 6.22e-3 (the C1c sawtooth barely moving), H_cell pinned at 1.63.
  The creep DECELERATES here (a fast 4.2-unit adjustment in the first ~200 iterations, then
  ~3e-5 r-units/iteration — ~250× slower than bracket 2's steady creep) but does not stop, and
  H_cell = O(1) says the state is nowhere near a true composite solution regardless. Same
  family as bracket 2's diagnosis: station-locked slow outward translation = a slow-motion
  false floor.
- **Interior fields on the locked states are large-amplitude but DEEP rather than tall:**
  ρ_cell up to 3.19 (W5) / 3.47 (W6), φ_cell −10.9 to −1.9 (W5) — the cell pays the seal price
  with a deep-φ interior (e^{2φ} UNDERflow direction; bracket 2's locked cells ran φ up to
  +1.6). σ cross-checks on the locked family read max_rel ≈ 5.9 (cell) / 0.053 (ambient) —
  fully off-solution, raw.

## 5. Residual anatomy + grid cross-check (artifact controls)

`sweep_E2b_A3Z8_anatomy.py` → `microphysics_E2b_A3Z8_anatomy.json` (18 saved .pt states; CPU
recompute reproduces the GPU max|F| on **18 of 18** states to ≤ 4e-16 relative — no overflow
exception this bracket; the extreme state P2/C2/wall (H_cell 5.4e27, Δφ_float 41.35) also
matches, its φ_cell being deep-negative rather than large-positive).

- **The C1c holdout is the same grid-scale θ-sawtooth as brackets 1–2** — f_r(r_p, θ_k)
  alternates sign node-to-node (P2/W5/wall: [+6.2e-3, −1.9e-3, +1.4e-3, −1.1e-3, +1.1e-3,
  −1.4e-3, +1.9e-3, −6.2e-3] — antisymmetric across the equator, pole-dominant), with u forming
  the seal-hugging boundary layer (u_seal alternating ±0.004–0.041 on the locked state) that
  buys E_ang(seal) ≈ U(ρ_p) but cannot simultaneously flatten f_r.
- **Runaway self-similarity:** §3(b) — residual ~ r^−1.00, C1c sign/shape preserved under
  ×5.04 dilation.
- **Shell rigidity:** wall-seeded runs preserve the seed's 36.05 ambient-shell width almost
  exactly (fast runaway AND parked translation; the extended floor preserves it to 4 decimal
  places); plateau-seeded runs preserve their 621.0 width loosely (end widths 553–669, ±10%).
- **Grid cross-check** (`sweep_E2b_A3Z8_gridcheck.py`, Nr=16, Nθ=12, Na=256, maxit 400):
  W1/wall/amp0.8 → same cap-speed runaway to the guard (r_p → 3568.9), same C1c holdout
  (1.2e-2), stalled; W5/wall/amp0.3 → same station-parked state (r_p → 688.4, ncap = 0,
  ρ_p = 1.011442, U(ρ_p) = 2.000029), floors max|F| 1.4e-2 (seal-[ρ] top at this grid). Both
  behaviors persist at finer resolution — not coarse-grid artifacts.

## 6. Pre-committed failure reading (plan order, solver-first — NO mechanism)

1. **Seeds/coverage:** 3 amplitudes (far-from-rigid included), both slices, 8 window cells
   spanning the necessary-map INCLUDING the genuine wall-admissible N=2 κ=1 cells and two
   genuine fully-admissible controls, plus (ξ,κ)-continuation both slices: 62 + 16 + 1 + 1 + 2
   solves. Every trajectory joins one of THREE behaviors: the cap-speed outward runaway
   (dominant), the station-parked slow outward translation (wall slice — WIDER basin here:
   N=2 κ=1 at all amps + controls + W1 amp1.5), or the inward-collapse direction at one extreme
   plateau amp (W6, residual 0.46, not a floor). No unexplored basin is indicated by any
   observed structure.
2. **Grid/conditioning:** trust caps, 2000-iteration floors, the 25·r_s wide guard (run the
   whole way to 24.94·r_s), a finer grid (Nr 16/Nθ 12/Na 256), and a 4000-iteration extended
   floor — behavior unchanged and CHARACTERIZED: an approximately self-similar scale-runaway
   (residual ~ r^−1.00) plus a station-locked decelerating-but-nonstop translation, both with
   O(1) H_cell violations at every point. LM stagnation/creep of a system with no attractor in
   the swept window, not conditioning floors.
3. **Frame-level statement (SCOPED, provisional — this is the THIRD of four brackets):** within
   this bracket's swept window (N ∈ {1,2}, ξ ∈ [0.05,1], κ ∈ [0.01,1], both neighborhoods,
   static concentric L2+L4 cell, a* held), the coupled system shows NO finite-size solution.
   The cross-family news: every qualitative behavior of the A1 brackets — the dilation runaway,
   the C1c θ-sawtooth wall, the shell-relative U≈2 seal lock, the poisoned-donor continuation
   stall, the parked-family creep — reproduces under the A3 slice family, with the parked basin
   WIDER here. The obstruction is family-independent in everything measured so far. Per the
   plan this is NOT yet the E2 scoped negative — that verdict needs all four brackets + the
   blind verifier. The pre-named escape ladder (ω ≠ 0 internal rotation) remains a REFRAME
   decision with Charles, never a patch — nothing here licenses reaching for it unilaterally.

## 7. Coverage statement

RUN: all 8 window cells × 2 slices × 3 amplitudes (48) + 14 continuation seeds (62 total,
phase 1); 16 flooring re-runs + 1 wide-guard run (phase 2); 1 extended-floor run (4000 it) on
the parked W5/wall state; 2 grid cross-checks; anatomy on all 18 saved states. THROUGHPUT-
LIMITED REMAINDER: NONE — the full pre-registered matrix ran (total compute ≈ 15 min of the
~90-min budget). NOT swept (out of contract scope for this bracket, for the record): N ≥ 3;
ξ > 1.9 (ξN < 2 enforced); κ > 1; anchor_mode='exact' (unwired branch, needs Charles's ruling);
off-center cells (E1 scope); ω ≠ 0.

## 8. Conditioning notes for bracket 4 (A3 Z=1)

- Everything in the bracket-1+2 §8 notes held here (dense-LM ~0.02 s/it at n=506; caps
  essential; H_cell on every end state; C2 self-tunes toward U(ρ_p) except plateau-slice
  small-coupling controls where E_ang_max < 2 and C2 itself holds out). Keep all of it.
- **NEW — read ρ_p against the SEED height, not just the station.** The sharp identity is
  ρ_p(end) = ρ_seed(0.95·r_s) to 5–7 digits on every wall end state (both brackets checked).
  For bracket 4 compute BOTH numbers up front (seed height vs station root ρ = b^{−1/2}) and
  report ρ_p against each; that one line settles "preserved vs tuned" per bracket and is the
  cleanest cross-family diagnostic. (A verifier regrade of bracket 2's "tuned to the station"
  wording is owed at E2-verdict time; the .pt states exist.)
- **NEW — expect the parked basin to be WIDE in A3 Z=1 if the wall is soft:** here parking
  captured the CONTROLS and an amp-1.5 W1, not just N=2 κ=1 cells; the correlate to watch is
  whether E_ang(seal) can reach ~2 for small-coupling cells (it could here, 1.991; it could
  not in bracket 2's controls). A3 Z=1 has wall-admissible N=2 cells (E1: inversion present)
  → expect the locked family; check amp-1.5 lock survival (survived here, broke in bracket 2).
- **Dilation exponents so far: −1.31 (A1 Z=8), −0.99 (A1 Z=1), −1.00 (A3 Z=8).** Not family,
  not Z; on three points it tracks U_seal (or "has wall-admissible cells": A1 Z=8 is the
  outlier on both). A3 Z=1 (U_seal between — U(1.353) ≈ 1.4, wall-admissible cells present)
  should read ≈ −1.0 if the correlate is right; a −1.3-class reading would break it.
- The wide-guard run here reached the FULL 25·r_s bound in 255 iterations (the runaway is
  faster/cleaner in this bracket); if bracket 4 does the same, the exponent measurement is
  cheap. ncap accounting: the wide run pressed the (rescaled) cap 605 times — cap-press count
  is not comparable across guard widths, don't read it as speed.
- CPU/GPU: 18/18 matched here (no e^{2φ} overflow — this bracket's extreme states run φ deep
  NEGATIVE, not positive; the bracket-2 overflow caveat stays for states with Δφ_float ≳ 25
  AND positive φ excursions).
- Poisoned continuation donors again unavoidable (both W1 end states guard-parked); rows are
  flagged `donor_guard_parked` in the JSON. If bracket 4 wants a clean donor, the only
  candidates would be parked (ncap=0) states — but those are exactly the forbidden donation
  source per the bracket-2 note (they poison the opposite slice). Recommend keeping the
  flagged-donor protocol as-is for cross-bracket comparability.

## Files

- `sweep_E2b_A3Z8.py` (phase 1) / `sweep_E2b_A3Z8_phase2.py` / `sweep_E2b_A3Z8_extfloor.py` /
  `sweep_E2b_A3Z8_gridcheck.py` / `sweep_E2b_A3Z8_anatomy.py` (all adapted from the bracket-2
  scripts); log `sweep_E2b_A3Z8.log`.
- `microphysics_E2b_A3Z8_results.json` (62 runs, full diagnostics + gates + ρ_p/U(ρ_p) per
  run); `microphysics_E2b_A3Z8_phase2.json` (17); `microphysics_E2b_A3Z8_extfloor.json` (1);
  `microphysics_E2b_A3Z8_gridcheck.json` (2); `microphysics_E2b_A3Z8_anatomy.json` (18).
- Saved fields (recompute-on-saved): `E2b_A3Z8_P2_*.pt` (16), `E2b_A3Z8_P2b_wideguard_W3_wall.pt`,
  `E2b_A3Z8_P2c_extended_W5_wall.pt` (18 total).
- NOT committed (per brief); blind verifier pass still owed before any banking.
