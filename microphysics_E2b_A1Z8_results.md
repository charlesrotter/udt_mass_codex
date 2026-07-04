# E2b SWEEP — BRACKET 1 (A1 m=3, Z=8): results (OBSERVE mode)

**Date:** 2026-07-03 (late). **Status: PROVISIONAL — sweep agent output, NOT verified, NOT
banked.** Contract: `microphysics_E2_battle_plan.md` (APPROVED AS WRITTEN). Machinery:
`cell_solver_composite.py` @ commit 17678d6, UNCHANGED (imported; harness 25/25). Data-blind:
no particle masses/data anywhere. Everything below is WHAT THE COUPLED SYSTEM DID — no merit
gating; non-convergence recorded as first-class data.

**Headline observation (scoped to this bracket, this grid, these seeds): the coupled
composite converged NOWHERE in the swept window — 0 of 62 phase-1 solves and 0 of 17 phase-2
flooring solves reached the pre-committed floor max|F| ≤ 1e-8. The dominant behavior is not a
residual plateau but a RUNAWAY: the LM runs BOTH free boundaries outward at the trust-cap speed,
approximately preserving the seed's ambient-shell width, until r_sU presses the trust guard —
while the outer-fold rows stay satisfiable (q_fold ≈ banked 12.6245) and the seal C2 row
self-tunes to E_ang(r_p) ≈ 2 = the plateau's U. The rows that will NOT close are C1c
(f_r(r_p,θ) = 0), the f-PDE interior, and (small-coupling controls) C2. H_cell — the free
consistency gate — reads O(1)–O(1e9) on every end state: none of these states is anywhere near
a solution; the residual "floors" (~1e-4–1e-2 in max|F|) are LM stagnation points of a system
that appears to have no attractor in the swept window.**

Sections: 1 setup/premises · 2 phase-1 outcome table · 3 phase-2 flooring + wide-guard ·
4 residual anatomy (where the mass sits) · 5 characterization of the runaway direction ·
6 pre-committed failure reading (solver-first order) · 7 coverage statement · 8 conditioning
notes for the next brackets · files.

## 1. Setup and premise ledger (chose-or-derived; additions to the E1 ledger #1–#17, which is
inherited UNCHANGED)

Bracket: A1 m=3, Z=8 (banked E0: a* = 1.4813439683 HELD, r_s = 577.5027, ρ_s = 2.26140,
q = 12.62444, ρ_c = 1; U_seal = 0.0522 — the bracket that admits almost nothing at the wall).
Anchor per plan wording fix: a* HELD at banked value; Δφ floats and is REPORTED (P-E2b-8,
THEORY: E1 ledger #5).

| # | Premise (this run) | Tag |
|---|---|---|
| P-E2b-1 | Window cells W1–W6, C1, C2 (table below) selected from the E1 `necessary_map` | CHOSE (map-guided). **FLAG:** this bracket has NO wall-admissible N=2 κ≈1 cells (E1 verified finding) → nearest admissible N=2 cells substituted (W5, W6) per the brief's control spirit. **FLAG:** the plan presumes 2 fully-admissible control cells; this bracket has exactly ONE (admissible_fraction = 1.0: N=1, ξ=0.05, κ=0.01) → C2 = nearest small-coupling N=2 (admfrac 0.911) substituted, flagged. |
| P-E2b-2 | Slices: plateau-target r_p0 = 100.0; wall-target r_p0 = 0.95·r_s = 548.63 (r* = 0.954·r_s = 551.06). Seed placements only; r_p FREE. | CHOSE |
| P-E2b-3 | Seed amplitudes amp ∈ {0.3, 0.8, 1.5}, bulge = amp·(1−μ²)·sin(π(ζ+1)/2) on the rigid map | CHOSE (banked undersampling lesson; bulge theorem = non-perturbative in θ) |
| P-E2b-4 | Grids Nr=12, Nθ=8, Na=192, kmap=2.5 (E2a smoke wall-resolved choice); confirm grids reserved for candidates (none arose) | Category-A conditioning |
| P-E2b-5 | LM maxit 150 (phase 1) / 2000 (phase 2), wall 75/240 s; free-boundary per-iteration caps \|Δr_p\|,\|Δr_sU\| ≤ 0.10·r_s (whole-step rescale); validity guard r_p ∈ (1e-6·r_s, r_sU), r_sU < 5·r_s (25·r_s in the one wide-guard run) — reject-step guards, never constraint rows | Category-A trust handling (pre-authorized by the E2b brief) |
| P-E2b-6 | Convergence = max\|F\|∞ ≤ 1e-8 (rows O(1) at seed; Φ0 ~ 4–650) | Pre-committed (plan instrument 1) |
| P-E2b-7 | Continuation seeds: best-Φ W1 end state per slice, re-solved under each other cell's couplings | Plan method (continuation in (ξ,κ) from best-conditioned cell) |
| P-E2b-9 | Budget: coverage-first order (every cell×slice at amp 0.8, then amp depth, then continuation); internal 70-min cap | anti-hang |

Window cells (all from `microphysics_E1_probe_results.json` necessary_map, this bracket):

| cell | N | ξ | κ | provenance |
|---|---|---|---|---|
| W1 | 1 | 0.5 | 0.1 | moderate-ξ plateau-admissible (admfrac .903); E2a smoke cell → continuation start |
| W2 | 1 | 0.2 | 0.1 | moderate-ξ plateau neighbor (.907) |
| W3 | 1 | 1.0 | 0.1 | moderate-ξ plateau neighbor (.900) |
| W4 | 1 | 0.5 | 1.0 | κ-continuation neighbor, plateau-admissible (.902) |
| W5 | 2 | 0.1 | 0.1 | nearest ADMISSIBLE N=2 (.906); no wall-admissible N=2 κ≈1 exists in this bracket |
| W6 | 2 | 0.05 | 1.0 | literal nearest-to-κ=1 N=2 (admfrac 0.023, thin interior band) |
| C1 | 1 | 0.05 | 0.01 | the bracket's ONLY fully-admissible cell (admfrac 1.0) |
| C2 | 2 | 0.05 | 0.01 | 2nd small-coupling control (nearest N=2, .911) — FLAGGED substitute |

GPU discipline: V100 torch float64; GPU-vs-CPU seed-residual spot-check rel maxdiff recorded in
the JSON (`notes`); no batched-triangular-solve anywhere; anatomy recomputed on CPU from saved
fields (an end-to-end independent-device check).

## 2. Phase-1 outcome table (62 solves: 8 cells x 2 slices x 3 amps + 14 continuation)

Statuses: **CONVERGED 0 / stalled 35 / iter-or-wall-capped 27 / throughput-limited 0.**
Top-holdout-row census over all 62: C1c f_r(seal) 38, C2 12, f-PDE 7, amb phi-ODE 3, C1b 1,
seal [rho] 1. Free boundaries: 48/62 runs ended with r_sU > 2 r_s; 40/62 pressed the 5 r_s trust
guard (2887.5). "stalled" = LM found no downhill step in 40 lambda tries (in almost every case
immediately after r_sU reached the guard — the descent direction WAS the guard-blocked outward
dilation); "iter/wall-capped" = budget hit with Phi still falling.

| run (cell/slice/seed) | status | Φ_end | max\|F\| | iters | caps | r_p → | r_sU → | top residual row |
|---|---|---|---|---|---|---|---|---|
| W1/plateau/bulge-amp0.8 | stalled | 2.3e-03 | 1.4e-02 | 48 | 85 | 100→2370 | 578→2874 | amb phi-ODE (1.4e-02) |
| W1/wall/bulge-amp0.8 | stalled | 3.9e-04 | 1.1e-02 | 93 | 88 | 549→2846 | 578→2875 | C1c f_r(seal) (1.1e-02) |
| W2/plateau/bulge-amp0.8 | stalled | 4.6e-03 | 2.3e-02 | 48 | 91 | 100→2380 | 578→2880 | amb phi-ODE (2.3e-02) |
| W2/wall/bulge-amp0.8 | iter/wall-capped | 1.5e-03 | 1.8e-02 | 150 | 6 | 549→1188 | 578→1217 | C1c f_r(seal) (1.8e-02) |
| W3/plateau/bulge-amp0.8 | iter/wall-capped | 4.4e-04 | 8.0e-03 | 150 | 89 | 100→2367 | 578→2851 | C1c f_r(seal) (8.0e-03) |
| W3/wall/bulge-amp0.8 | stalled | 1.5e-04 | 6.7e-03 | 77 | 95 | 549→2859 | 578→2888 | C1c f_r(seal) (6.7e-03) |
| W4/plateau/bulge-amp0.8 | stalled | 1.4e-03 | 7.1e-03 | 49 | 87 | 100→2300 | 578→2858 | C1c f_r(seal) (7.1e-03) |
| W4/wall/bulge-amp0.8 | iter/wall-capped | 4.6e-04 | 1.3e-02 | 150 | 5 | 549→865 | 578→894 | C1c f_r(seal) (1.3e-02) |
| W5/plateau/bulge-amp0.8 | stalled | 6.3e-03 | 2.2e-02 | 48 | 81 | 100→2355 | 578→2850 | f-PDE (2.2e-02) |
| W5/wall/bulge-amp0.8 | iter/wall-capped | 2.2e-03 | 1.9e-02 | 150 | 20 | 549→1204 | 578→1232 | C1c f_r(seal) (1.9e-02) |
| W6/plateau/bulge-amp0.8 | iter/wall-capped | 2.5e-02 | 1.0e-01 | 150 | 13 | 100→233 | 578→710 | f-PDE (1.0e-01) |
| W6/wall/bulge-amp0.8 | iter/wall-capped | 1.6e-02 | 6.3e-02 | 150 | 0 | 549→552 | 578→581 | f-PDE (6.3e-02) |
| C1/plateau/bulge-amp0.8 | stalled | 2.8e-01 | 5.2e-01 | 50 | 81 | 100→2397 | 578→2885 | C2 (5.2e-01) |
| C1/wall/bulge-amp0.8 | iter/wall-capped | 5.6e-02 | 9.6e-02 | 150 | 0 | 549→561 | 578→590 | C1c f_r(seal) (9.6e-02) |
| C2/plateau/bulge-amp0.8 | stalled | 4.1e-02 | 1.8e-01 | 47 | 85 | 100→2351 | 578→2837 | C2 (1.8e-01) |
| C2/wall/bulge-amp0.8 | iter/wall-capped | 1.1e-02 | 7.5e-02 | 150 | 6 | 549→1202 | 578→1231 | C1c f_r(seal) (7.5e-02) |
| W1/plateau/bulge-amp0.3 | stalled | 6.5e-04 | 1.3e-02 | 94 | 91 | 100→2410 | 578→2888 | C1c f_r(seal) (1.3e-02) |
| W1/wall/bulge-amp0.3 | stalled | 3.9e-04 | 1.1e-02 | 95 | 87 | 549→2859 | 578→2888 | C1c f_r(seal) (1.1e-02) |
| W2/plateau/bulge-amp0.3 | stalled | 1.7e-03 | 1.8e-02 | 48 | 80 | 100→2395 | 578→2881 | C1c f_r(seal) (1.8e-02) |
| W2/wall/bulge-amp0.3 | iter/wall-capped | 1.3e-03 | 1.6e-02 | 150 | 4 | 549→1225 | 578→1254 | C1c f_r(seal) (1.6e-02) |
| W3/plateau/bulge-amp0.3 | stalled | 3.3e-04 | 8.1e-03 | 50 | 82 | 100→2368 | 578→2846 | C1c f_r(seal) (8.1e-03) |
| W3/wall/bulge-amp0.3 | stalled | 1.5e-04 | 6.7e-03 | 84 | 95 | 549→2859 | 578→2888 | C1c f_r(seal) (6.7e-03) |
| W4/plateau/bulge-amp0.3 | iter/wall-capped | 1.7e-04 | 6.6e-03 | 150 | 87 | 100→2407 | 578→2884 | C1c f_r(seal) (6.6e-03) |
| W4/wall/bulge-amp0.3 | iter/wall-capped | 1.1e-04 | 6.3e-03 | 150 | 50 | 549→1915 | 578→1944 | C1c f_r(seal) (6.3e-03) |
| W5/plateau/bulge-amp0.3 | stalled | 2.5e-03 | 1.3e-02 | 48 | 78 | 100→2404 | 578→2877 | C1c f_r(seal) (1.3e-02) |
| W5/wall/bulge-amp0.3 | iter/wall-capped | 2.1e-02 | 7.6e-02 | 150 | 0 | 549→557 | 578→586 | C1b (7.6e-02) |
| W6/plateau/bulge-amp0.3 | stalled | 6.6e-05 | 3.6e-03 | 50 | 77 | 100→2384 | 578→2887 | seal [rho] (3.6e-03) |
| W6/wall/bulge-amp0.3 | iter/wall-capped | 3.0e-04 | 6.3e-03 | 150 | 0 | 549→550 | 578→579 | C1c f_r(seal) (6.3e-03) |
| C1/plateau/bulge-amp0.3 | stalled | 3.2e-01 | 5.6e-01 | 48 | 79 | 100→2340 | 578→2832 | C2 (5.6e-01) |
| C1/wall/bulge-amp0.3 | iter/wall-capped | 5.8e-02 | 9.7e-02 | 150 | 0 | 549→553 | 578→582 | C1c f_r(seal) (9.7e-02) |
| C2/plateau/bulge-amp0.3 | stalled | 3.7e-02 | 1.7e-01 | 47 | 83 | 100→2383 | 578→2873 | C2 (1.7e-01) |
| C2/wall/bulge-amp0.3 | iter/wall-capped | 3.8e-02 | 7.9e-02 | 150 | 0 | 549→714 | 578→743 | C1c f_r(seal) (7.9e-02) |
| W1/plateau/bulge-amp1.5 | stalled | 8.8e-04 | 1.3e-02 | 72 | 92 | 100→2410 | 578→2888 | C1c f_r(seal) (1.3e-02) |
| W1/wall/bulge-amp1.5 | iter/wall-capped | 6.5e-04 | 1.3e-02 | 150 | 68 | 549→2323 | 578→2352 | C1c f_r(seal) (1.3e-02) |
| W2/plateau/bulge-amp1.5 | stalled | 2.5e-03 | 1.7e-02 | 66 | 95 | 100→2410 | 578→2888 | C1c f_r(seal) (1.7e-02) |
| W2/wall/bulge-amp1.5 | iter/wall-capped | 4.9e-03 | 3.9e-02 | 150 | 4 | 549→983 | 578→1012 | C1c f_r(seal) (3.9e-02) |
| W3/plateau/bulge-amp1.5 | iter/wall-capped | 3.8e-04 | 8.2e-03 | 150 | 84 | 100→2381 | 578→2854 | C1c f_r(seal) (8.2e-03) |
| W3/wall/bulge-amp1.5 | iter/wall-capped | 4.0e-03 | 3.2e-02 | 150 | 1 | 549→595 | 578→624 | C1c f_r(seal) (3.2e-02) |
| W4/plateau/bulge-amp1.5 | stalled | 1.8e-03 | 2.0e-02 | 51 | 98 | 100→2320 | 578→2874 | amb phi-ODE (2.0e-02) |
| W4/wall/bulge-amp1.5 | iter/wall-capped | 1.8e-03 | 2.2e-02 | 150 | 0 | 549→629 | 578→658 | C1c f_r(seal) (2.2e-02) |
| W5/plateau/bulge-amp1.5 | stalled | 1.1e-03 | 1.1e-02 | 71 | 95 | 100→2319 | 578→2888 | C1c f_r(seal) (1.1e-02) |
| W5/wall/bulge-amp1.5 | iter/wall-capped | 1.3e-03 | 1.5e-02 | 150 | 31 | 549→1546 | 578→1575 | C1c f_r(seal) (1.5e-02) |
| W6/plateau/bulge-amp1.5 | iter/wall-capped | 3.4e-02 | 1.2e-01 | 150 | 19 | 100→360 | 578→838 | f-PDE (1.2e-01) |
| W6/wall/bulge-amp1.5 | iter/wall-capped | 8.1e-03 | 3.9e-02 | 150 | 0 | 549→550 | 578→579 | f-PDE (3.9e-02) |
| C1/plateau/bulge-amp1.5 | stalled | 2.9e-01 | 5.3e-01 | 49 | 82 | 100→2334 | 578→2833 | C2 (5.3e-01) |
| C1/wall/bulge-amp1.5 | iter/wall-capped | 5.6e-02 | 9.5e-02 | 150 | 0 | 549→563 | 578→592 | C1c f_r(seal) (9.5e-02) |
| C2/plateau/bulge-amp1.5 | stalled | 4.5e-02 | 1.9e-01 | 48 | 86 | 100→2362 | 578→2850 | C2 (1.9e-01) |
| C2/wall/bulge-amp1.5 | iter/wall-capped | 1.0e-02 | 7.2e-02 | 150 | 8 | 549→1247 | 578→1276 | C1c f_r(seal) (7.2e-02) |
| W2/plateau/cont-W1 | stalled | 1.1e+00 | 1.0e+00 | 1 | 6 | 2410→2410 | 2888→2888 | C2 (1.0e+00) |
| W2/wall/cont-W1 | stalled | 7.2e-04 | 1.4e-02 | 26 | 0 | 2846→2859 | 2875→2888 | C1c f_r(seal) (1.4e-02) |
| W3/plateau/cont-W1 | stalled | 3.0e+00 | 1.7e+00 | 1 | 5 | 2410→2410 | 2888→2888 | C2 (1.7e+00) |
| W3/wall/cont-W1 | stalled | 1.4e-04 | 6.6e-03 | 103 | 0 | 2846→2859 | 2875→2888 | C1c f_r(seal) (6.6e-03) |
| W4/plateau/cont-W1 | stalled | 6.6e+00 | 2.5e+00 | 1 | 5 | 2410→2410 | 2888→2888 | C2 (2.5e+00) |
| W4/wall/cont-W1 | iter/wall-capped | 5.8e-05 | 4.2e-03 | 150 | 0 | 2846→2846 | 2875→2875 | C1c f_r(seal) (4.2e-03) |
| W5/plateau/cont-W1 | stalled | 3.6e+00 | 4.9e-01 | 1 | 6 | 2410→2410 | 2888→2888 | f-PDE (4.9e-01) |
| W5/wall/cont-W1 | iter/wall-capped | 2.6e-04 | 1.0e-02 | 150 | 0 | 2846→2859 | 2875→2888 | C1c f_r(seal) (1.0e-02) |
| W6/plateau/cont-W1 | stalled | 9.5e+01 | 9.5e+00 | 1 | 5 | 2410→2410 | 2888→2888 | C2 (9.5e+00) |
| W6/wall/cont-W1 | stalled | 1.1e-01 | 2.0e-01 | 144 | 0 | 2846→2846 | 2875→2875 | f-PDE (2.0e-01) |
| C1/plateau/cont-W1 | stalled | 3.2e+00 | 1.8e+00 | 1 | 8 | 2410→2410 | 2888→2888 | C2 (1.8e+00) |
| C1/wall/cont-W1 | stalled | 4.7e-03 | 3.2e-02 | 33 | 0 | 2846→2859 | 2875→2888 | C1c f_r(seal) (3.2e-02) |
| C2/plateau/cont-W1 | stalled | 3.5e+00 | 1.6e+00 | 1 | 8 | 2410→2410 | 2888→2888 | C2 (1.6e+00) |
| C2/wall/cont-W1 | stalled | 2.5e-03 | 4.0e-02 | 49 | 0 | 2846→2859 | 2875→2888 | C1c f_r(seal) (4.0e-02) |

Notes on the continuation rows (plan method, P-E2b-7): plateau-slice continuation seeds
(re-solving the best W1 plateau end state under each other cell's couplings) all stall in ~1
iteration — the W1 end state sits at the trust guard, and under changed couplings the C2/E_ang
rows jump O(1) with no downhill step available inside the guard. Wall-slice continuation seeds
descend normally to the same C1c-held floors as the direct seeds (W4/wall/cont-W1 reached the
sweep's lowest phase-1 Phi = 5.8e-5 — same holdout row, same runaway position). Continuation
neither found a basin the direct seeds missed nor changed any qualitative behavior.

## 3. Phase-2: flooring (maxit 2000) + the wide-guard observation run

For each (cell x slice), the best phase-1 config re-run with maxit=2000, wall 240 s; then ONE
widened-guard run (r_sU < 25 r_s, per-iteration caps unchanged) on the best guard-presser
(W6/plateau/amp0.3). Gate columns are the plan's instruments read on the END states (owed ~0
only on a true solution — none is one).

| run | status | Φ_end | max\|F\| | iters | r_p → | r_sU → | top row | Δφ_float | H_cell_max | q_fold | q_seal | E_ang_seal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P2/C1/plateau/amp0.8 | stalled | 2.8e-01 | 5.2e-01 | 50 | →2397 | →2885 | C2 (5.2e-01) | 5.07 | 2.2e+01 | 12.6404 | -0.267 | 1.4804 |
| P2/C1/wall/amp1.5 | iter/wall-capped | 3.9e-02 | 8.1e-02 | 2000 | →681 | →709 | C1c f_r(seal) (8.1e-02) | 4.40 | 1.1e+01 | 12.6252 | 0.348 | 1.9854 |
| P2/C2/plateau/amp0.3 | stalled | 3.7e-02 | 1.7e-01 | 47 | →2383 | →2873 | C2 (1.7e-01) | 4.98 | 1.9e+00 | 12.6426 | -0.147 | 1.8298 |
| P2/C2/wall/amp1.5 | iter/wall-capped | 2.2e-03 | 3.4e-02 | 2000 | →2687 | →2716 | C1c f_r(seal) (3.4e-02) | 1.39 | 1.9e+00 | 12.6246 | 0.345 | 1.9997 |
| P2/W1/plateau/amp0.3 | stalled | 6.5e-04 | 1.3e-02 | 94 | →2410 | →2888 | C1c f_r(seal) (1.3e-02) | 24.76 | 2.2e+15 | 12.6245 | 0.045 | 1.9998 |
| P2/W1/wall/amp0.8 | stalled | 3.9e-04 | 1.1e-02 | 93 | →2846 | →2875 | C1c f_r(seal) (1.1e-02) | 1.00 | 1.6e+00 | 12.6246 | 0.356 | 1.9998 |
| P2/W2/plateau/amp0.3 | stalled | 1.7e-03 | 1.8e-02 | 48 | →2395 | →2881 | C1c f_r(seal) (1.8e-02) | 5.27 | 3.8e+00 | 12.6320 | 0.029 | 1.9964 |
| P2/W2/wall/amp0.3 | stalled | 2.4e-04 | 6.7e-03 | 211 | →2859 | →2888 | C1c f_r(seal) (6.7e-03) | 1.00 | 2.0e+00 | 12.6246 | 0.346 | 2.0000 |
| P2/W3/plateau/amp0.3 | stalled | 3.3e-04 | 8.1e-03 | 50 | →2368 | →2846 | C1c f_r(seal) (8.1e-03) | 21.56 | 2.9e+12 | 12.6249 | 0.034 | 1.9994 |
| P2/W3/wall/amp0.3 | stalled | 1.5e-04 | 6.7e-03 | 84 | →2859 | →2888 | C1c f_r(seal) (6.7e-03) | 3.95 | 9.9e-01 | 12.6246 | 0.346 | 2.0000 |
| P2/W4/plateau/amp0.3 | iter/wall-capped | 1.6e-04 | 6.6e-03 | 2000 | →2407 | →2884 | C1c f_r(seal) (6.6e-03) | 4.48 | 1.5e+00 | 12.6244 | 0.088 | 1.9998 |
| P2/W4/wall/amp0.3 | iter/wall-capped | 1.0e-04 | 6.3e-03 | 2000 | →1918 | →1946 | C1c f_r(seal) (6.3e-03) | 0.59 | 2.0e+00 | 12.6245 | 0.346 | 2.0000 |
| P2/W5/plateau/amp1.5 | stalled | 1.1e-03 | 1.1e-02 | 71 | →2319 | →2888 | C1c f_r(seal) (1.1e-02) | 6.90 | 1.8e+02 | 12.6207 | -1.013 | 1.9894 |
| P2/W5/wall/amp1.5 | iter/wall-capped | 1.3e-03 | 1.5e-02 | 2000 | →1547 | →1575 | C1c f_r(seal) (1.5e-02) | 5.18 | 4.9e+00 | 12.6248 | 0.347 | 1.9997 |
| P2/W6/plateau/amp0.3 | stalled | 6.6e-05 | 3.6e-03 | 50 | →2384 | →2887 | seal [rho] (3.6e-03) | 5.85 | 1.9e+00 | 12.6250 | -0.008 | 2.0012 |
| P2/W6/wall/amp0.3 | iter/wall-capped | 1.6e-04 | 6.0e-03 | 2000 | →550 | →579 | C1c f_r(seal) (6.0e-03) | 2.66 | 1.9e+00 | 12.6249 | 0.346 | 2.0017 |
| P2b-wideguard/W6/plateau/amp0.3 | (wide) | 1.6e-06 | 3.7e-04 | 250 | →13889 | →14401 | f-PDE (3.7e-04) | 6.48 | 2.1e+00 | 12.7185 | -0.050 | 1.9985 |

**Reading:** (a) NOTHING converges at 2000 iterations either — floors sit at max|F| ~ 3.6e-3 to
0.5, all far above the 1e-8 contract floor. (b) The wide-guard run is the decisive observation:
freed to 25 r_s, the system kept inflating (r_p -> 13889 = 24.0 r_s, r_sU -> 14401) and Phi kept
FALLING (1.6e-6; max|F| 3.7e-4) with no floor in sight — the residual infimum along this
direction appears to be 0 at INFINITE dilation, i.e. a scale-runaway, not an approach to a
solution. (c) H_cell — the free consistency gate, NOT a residual row — stays O(1) (~ -1.4 to
-2.1, near the flat-cell value E_ang - 2) on EVERY end state including the wide-guard one: small
pointwise EOM residuals over an ever-larger domain integrate to an O(1) conservation violation.
The falling Phi is a FALSE floor; no state on the runaway path is near a true composite
solution. This is exactly the vacuousness-proofing the instruments were built for.

## 4. Residual anatomy (recomputed on CPU from saved fields — also the GPU/CPU cross-check)

`sweep_E2b_A1Z8_anatomy.py` -> `microphysics_E2b_A1Z8_anatomy.json` (17 saved .pt states; CPU
recompute reproduces the GPU max|F| values, e.g. P2/W1/wall 1.09e-2 both — banked GPU
discipline satisfied end-to-end).

- **The C1c holdout is a grid-scale theta-sawtooth**: f_r(r_p, theta_k) alternates sign
  node-to-node at the SH collocation points on essentially every end state (e.g. P2/W1/wall:
  [+1.5e-3, +6.1e-3, -9.1e-3, +1.1e-2, -9.8e-3, +6.3e-3, -3.4e-3, -3.0e-4]). The u field forms
  a seal-hugging boundary layer (u(seal) O(0.3-1.9), u(core) small) that buys E_ang(r_p) ~ 2
  (the C2 row self-tunes to the plateau's U = 2 — read E_ang_seal ~ 2.000 across the table)
  but cannot simultaneously flatten f_r at the seal: C1c and the f-PDE fight, and the residue
  is the sawtooth.
- **The runaway is EXACTLY self-similar**: parent W6/plateau (r_p 2384) vs wide-guard (r_p
  13889, dilation x5.827): the C1c residual vector scales by 10.0410 +/- 0.0001 UNIFORMLY
  across all 8 theta nodes (same signs, same shape) — residual ~ r^-1.31 along a pure dilation
  orbit. The LM is descending a scaling direction of the discretized system, not approaching
  an attractor.
- Wall-seeded runs translate outward preserving the seed's ambient-shell width (28.87) almost
  exactly; plateau-seeded runs preserve their 477.5 width similarly: the ambient shell rides
  along rigidly while the cell inflates.
- The one non-runaway family: W6 (N=2, kap=1) at the wall parks r_p at 551.9 ~ r* = 551.1 (the
  U=2 station) with ncap=0 — the only configuration that stays at finite size — but floors at
  max|F| ~ 6e-3 with the f-PDE itself as holdout: the N=2, kap~1 carrier sits at the wall
  station the E1 inversion pointed to, and its interior PDE still will not close.
- One curiosity, reported raw: W2/wall end states carry max|u| = 3.140 ~ pi (a full extra
  half-winding attempt in the deviation field) — the far-from-rigid seed explored a different
  f-branch and still floored the same way.
- q_fold reads the banked 12.6244-12.64 on every end state (the outer fold rows are easily
  held); q_seal is small (+0.35 wall-slice, ~0 to -1 plateau-slice); dphi_float lands anywhere
  from 0.6 to 25 (vs anchor 7.004) — unconstrained, as expected off-solution.

## 5. Grid cross-check (artifact control)

`sweep_E2b_A1Z8_gridcheck.py` -> `microphysics_E2b_A1Z8_gridcheck.json`: W1/wall/amp0.8 and
W6/plateau/amp0.3 re-run at Nr=16, Nth=12, Na=256 (maxit 400). Same behavior in both: outward
runaway to the guard (r_p -> 2853 / 2287), same holdout rows (C1c 1.5e-2 / seal-[rho] 6.8e-3),
no convergence. The phase-1/2 behavior is not a coarse-grid artifact at the swept resolutions.

## 6. Pre-committed failure reading (plan order, solver-first — NO mechanism)

Plan order for "no convergence anywhere": (1) seeds/continuation coverage -> (2) grid/
conditioning -> (3) then and only then the frame.

1. **Seeds/coverage:** 3 amplitudes (0.3 / 0.8 / 1.5, far-from-rigid included), both slices,
   8 window cells spanning the necessary-map (incl. both N=2 stand-ins and both controls), plus
   (xi,kap)-continuation from the best-conditioned cell: 62 + 17 + 2 solves, every basin found
   is the SAME basin (the dilation runaway) or the same C1c-held floor. Widening seeds further
   is not indicated by any observed structure — every trajectory joins the same two behaviors.
2. **Grid/conditioning:** column-scaled QR/lstsq LM (the E2a-validated driver), trust caps on
   the free boundaries, longer budgets (2000 it), widened guard (25 r_s), finer grid (Nr 16 /
   Nth 12 / Na 256) — behavior unchanged and now CHARACTERIZED: an exactly self-similar
   scale-runaway with residual ~ r^-1.3 and an O(1) H_cell violation all along it. The floors
   are not conditioning floors; they are the LM stagnating where the only descent direction is
   the guard-blocked dilation.
3. **Frame-level statement (SCOPED, provisional — this is ONE bracket):** within this bracket's
   swept window (N in (1, 2), xi in [0.05,1], kap in [0.01,1], both neighborhoods, static
   concentric L2+L4 cell, a* held), the coupled system shows NO finite-size solution; the
   system prefers infinite dilation, and the obstruction rows are the seal's angular set
   (C1c + f-PDE + C2 at small coupling). Per the plan this is NOT yet the E2 scoped negative
   — that verdict needs all four brackets + the blind verifier. It is consistent with the E1
   bulge-theorem tension (the theta-deformation the seal demands cannot be paid at finite
   r_p in this window) and consistent with the necessary-map's warning that THIS bracket
   (U_seal = 0.052) admits almost nothing at the wall.
   The pre-named escape ladder (omega != 0 internal rotation) remains a REFRAME decision with
   Charles, never a patch — nothing here licenses reaching for it unilaterally.

## 7. Coverage statement

RUN: all 8 window cells x 2 slices x 3 amplitudes (48) + 14 continuation seeds (62 total,
phase 1); 16 flooring re-runs + 1 wide-guard run (phase 2); 2 grid cross-checks; anatomy on all
17 saved states. THROUGHPUT-LIMITED REMAINDER: NONE — the full pre-registered matrix ran (total
compute ~12 min of the ~90-min budget; the E2a conditioning fears did not materialize at these
grid sizes on the V100). NOT swept (out of contract scope for this bracket, for the record):
N >= 3; xi > 1.9; kap > 1 (except W6's kap=1); anchor_mode='exact' (unwired branch, needs
Charles's ruling); off-center cells (E1 scope); omega != 0.

## 8. Conditioning notes for the next brackets (A1 Z=1, A3 Z=8, A3 Z=1)

- The V100 dense-LM at Nr=12/Nth=8/Na=192 runs ~0.02-0.06 s/iteration (n=506); a full bracket
  matrix is ~2 min, phase-2 flooring ~5 min. Budget is NOT the binding constraint; run the
  full seed matrix per bracket without triage.
- The free-boundary trust caps (0.10 r_s/iteration, whole-step rescale) are ESSENTIAL: uncapped,
  the E2a smoke wandered; capped, every trajectory is interpretable. Keep the validity-guard
  bound at 5 r_s for the sweep and do ONE 25 r_s wide-guard observation per bracket if the
  guard is pressed — the self-similarity measurement (residual-vs-dilation exponent) is cheap
  and is the sharpest characterization of the runaway.
- Read H_cell on EVERY end state (it is free): it separates "LM found a small-residual
  non-solution" from "near a solution" instantly. Phi/max|F| alone are misleading here.
- Expect the C2 row (E_ang(r_p) = U(rho_p)) to self-tune to U ~ 2 by boundary drift; where U=2
  is NOT attainable (small-coupling controls: E_ang_max < 2) C2 itself becomes the holdout
  (C1/C2 cells here: max|F| ~ 0.1-0.5).
- The Z=1 brackets have U_seal ~ 1.4-1.7 and DO have wall-admissible N=2 kap~1 cells (E1
  verified) — the wall-slice behavior may differ qualitatively there; the W6-at-r* parking
  behavior seen here (the only finite-size attractor-ish behavior in this bracket) is the thing
  to watch.
- GPU/CPU spot-checks: seed-residual rel maxdiff 3.98e-11; anatomy CPU recompute matches GPU
  end states. No batched-triangular-solve used anywhere.

## Files

- `sweep_E2b_A1Z8.py` (phase 1) / `sweep_E2b_A1Z8_phase2.py` / `sweep_E2b_A1Z8_gridcheck.py` /
  `sweep_E2b_A1Z8_anatomy.py`; log `sweep_E2b_A1Z8.log`.
- `microphysics_E2b_A1Z8_results.json` (62 runs, full diagnostics + gates per run);
  `microphysics_E2b_A1Z8_phase2.json` (17); `microphysics_E2b_A1Z8_gridcheck.json` (2);
  `microphysics_E2b_A1Z8_anatomy.json` (17).
- Saved fields (recompute-on-saved): `E2b_A1Z8_P2_*.pt` (16), `E2b_A1Z8_P2b_wideguard_*.pt` (1).
- NOT committed (per brief); blind verifier pass still owed before any banking.
