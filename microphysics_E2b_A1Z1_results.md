# E2b SWEEP — BRACKET 2 (A1 m=3, Z=1): results (OBSERVE mode)

**Date:** 2026-07-03 (late). **Status: PROVISIONAL — sweep agent output, NOT verified, NOT
banked.** Contract: `microphysics_E2_battle_plan.md` (APPROVED AS WRITTEN). Machinery:
`cell_solver_composite.py` UNCHANGED (imported; same commit/state as bracket 1). Scripts adapted
(not rewritten) from the bracket-1 sweep per the E2b brief; bracket-1 conditioning notes
(`microphysics_E2b_A1Z8_results.md` §8) followed: full matrix without triage, 0.10·r_s caps,
ONE wide-guard dilation-exponent run, H_cell read on EVERY end state. Data-blind: no particle
masses/data anywhere. Everything below is WHAT THE COUPLED SYSTEM DID — no merit gating;
non-convergence recorded as first-class data.

**Headline observation (scoped to this bracket, this grid, these seeds): the coupled composite
converged NOWHERE in the swept window — 0 of 62 phase-1 solves, 0 of 17 phase-2 flooring solves,
0 of 2 grid cross-checks, 0 of 1 extended-floor runs reached the pre-committed floor
max|F| ≤ 1e-8. The DOMINANT behavior is the same outward runaway as bracket 1 (both free
boundaries at trust-cap speed to the 5·r_s guard, shell width preserved, C1c θ-sawtooth
holdout). THE NOVELTY — the thing this bracket was watched for — is real but is NOT an
attractor: the genuinely wall-admissible N=2 κ=1 cells (W5, W6), wall-seeded, do NOT join the
cap-speed runaway; they translate outward ULTRA-SLOWLY (ncap = 0 throughout; ~100× below cap
speed) with the seal EXACTLY LOCKED to the ambient shell's U=2 station (ρ_p = 1.003689,
U(ρ_p) = 2.000003 on every such end state, while absolute r_p drifts 600 → 642 — the lock is
shell-relative, not positional). Extended flooring (4000 further iterations) shows the creep
does not stop and Φ keeps slowly falling with H_cell pinned at O(1) (≈ 1.9): a slow-motion
false floor of the same runaway family, not a finite-size solution. The bracket-1 "W6 parking"
behavior is thus CONFIRMED, GENERALIZED (it appears exactly where the E1 map said
wall-admissible N=2 κ≈1 cells exist), and DIAGNOSED (it is station-locked slow translation,
not an equilibrium).**

Sections: 1 setup/premises · 2 phase-1 outcome table · 3 phase-2 flooring + wide-guard ·
4 the wall-N=2-κ≈1 story (parking diagnosed) · 5 residual anatomy + grid cross-check ·
6 pre-committed failure reading (solver-first order) · 7 coverage statement · 8 conditioning
notes for brackets 3–4 · files.

## 1. Setup and premise ledger (chose-or-derived; additions to the E1 ledger #1–#17, inherited
UNCHANGED; bracket-1 ledger pattern followed)

Bracket: A1 m=3, Z=1 (banked E0: a* = 1.4942743251 HELD, r_s = 620.4261, ρ_s = 1.36181,
q = 1.480868, ρ_c = 1; U_seal = 1.40875 — a bracket with a REAL wall-admissible window,
contrast bracket 1's U_seal = 0.0522). E1 station: r* = 0.95172·r_s = 590.47, ρ(r*) = 1.003829.
Anchor per plan wording fix: a* HELD at banked value; Δφ floats and is REPORTED (P-E2b2-8,
THEORY: E1 ledger #5).

| # | Premise (this run) | Tag |
|---|---|---|
| P-E2b2-1 | Window cells W1–W6, C1, C2 (table below) selected from the E1 `necessary_map` for THIS bracket | CHOSE (map-guided). This bracket HAS wall-admissible N=2 κ=1 cells (E1 verified) → W5/W6 are the GENUINE articles (no stand-ins). Controls: this bracket has MANY fully-admissible cells; C1 and C2 are both genuinely admfrac = 1.0 — NO substitute flags needed (contrast bracket 1's two flags). |
| P-E2b2-2 | Slices: plateau-target r_p0 = 100.0 (same absolute value as bracket 1 for comparability; r_p0/r_s ≈ 0.16); wall-target r_p0 = 0.95·r_s = 589.40 (r* = 590.47). Seed placements only; r_p FREE. | CHOSE |
| P-E2b2-3 | Seed amplitudes amp ∈ {0.3, 0.8, 1.5}, bulge = amp·(1−μ²)·sin(π(ζ+1)/2) on the rigid map | CHOSE (banked undersampling lesson; bulge theorem = non-perturbative in θ) |
| P-E2b2-4 | Grids Nr=12, Nθ=8, Na=192, kmap=2.5 (bracket-1 choice unchanged); confirm grids reserved for candidates (none arose); grid cross-check run anyway on the two key behaviors (§5) | Category-A conditioning |
| P-E2b2-5 | LM maxit 150 (phase 1) / 2000 (phase 2) / 4000 (extended floor), wall 75/240/300 s; free-boundary per-iteration caps \|Δr_p\|,\|Δr_sU\| ≤ 0.10·r_s (whole-step rescale); validity guard r_p ∈ (1e-6·r_s, r_sU), r_sU < 5·r_s (25·r_s in the one wide-guard run) — reject-step guards, never constraint rows | Category-A trust handling (bracket-1 pattern, pre-authorized) |
| P-E2b2-6 | Convergence = max\|F\|∞ ≤ 1e-8 (rows O(1) at seed; Φ0 ~ 1.1–2079) | Pre-committed (plan instrument 1) |
| P-E2b2-7 | Continuation seeds: best-Φ W1 end state per slice, re-solved under each other cell's couplings | Plan method (continuation in (ξ,κ) from best-conditioned cell) |
| P-E2b2-9 | Budget: coverage-first order (every cell×slice at amp 0.8, then amp depth, then continuation); internal 70-min cap; actual total compute ≈ 10 min of the ~90-min ceiling | anti-hang |

Window cells (all from `microphysics_E1_probe_results.json` necessary_map, A1 m=3 Z=1):

| cell | N | ξ | κ | provenance |
|---|---|---|---|---|
| W1 | 1 | 0.5 | 0.1 | moderate-ξ plateau (admfrac 1.0); identical to bracket-1 W1 → continuation start + cross-bracket comparability |
| W2 | 1 | 0.2 | 0.1 | moderate-ξ plateau neighbor (admfrac 1.0) |
| W3 | 1 | 1.0 | 0.1 | moderate-ξ plateau neighbor (admfrac 1.0) |
| W4 | 1 | 0.5 | 1.0 | κ-continuation neighbor (admfrac 1.0) |
| W5 | 2 | 0.05 | 1.0 | **WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.109, outer_seal_admissible=True) — the priority novelty vs bracket 1 |
| W6 | 2 | 0.1 | 1.0 | **2nd WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.100, outer_seal_admissible=True) |
| C1 | 1 | 0.05 | 0.01 | fully-admissible small-coupling control (admfrac 1.0) |
| C2 | 2 | 0.05 | 0.01 | 2nd fully-admissible control (admfrac 1.0 — genuine; NO flag, contrast bracket 1) |

GPU discipline: V100 torch float64; GPU-vs-CPU seed-residual spot-check rel maxdiff 2.19e-11
(JSON `notes`); no batched-triangular-solve anywhere; anatomy recomputed on CPU from saved
fields (end-to-end independent-device check — one flagged exception, §5).

## 2. Phase-1 outcome table (62 solves: 8 cells × 2 slices × 3 amps + 14 continuation)

Statuses: **CONVERGED 0 / stalled 45 / iter-or-wall-capped 17 / throughput-limited 0.**
Top-holdout-row census over all 62: C1c f_r(seal) 25, C2 15, f-PDE 14, cell phi-ODE 3,
seal [rho] 2, C1b 1, cell rho-ODE 1, amb phi-ODE 1. Free boundaries: 50/62 ended with
r_sU > 2·r_s; 47/62 pressed the 5·r_s trust guard (3102.1). The exceptions cluster EXACTLY
where the E1 map said they would: the wall-seeded wall-admissible N=2 κ=1 cells (bold rows).

| run (cell/slice/seed) | status | Φ_end | max\|F\| | iters | ncap | r_p → | r_sU → | top residual row | H_cell_max |
|---|---|---|---|---|---|---|---|---|---|
| W1/plateau/bulge-amp0.8 | stalled | 1.1e-02 | 3.2e-02 | 48 | 86 | 100→2554 | 620→3101 | f-PDE (3.2e-02) | 1.8e+01 |
| W1/wall/bulge-amp0.8 | stalled | 3.7e-04 | 1.1e-02 | 78 | 95 | 589→3071 | 620→3102 | C1c f_r(seal) (1.1e-02) | 1.5e+00 |
| W2/plateau/bulge-amp0.8 | stalled | 1.6e-02 | 6.4e-02 | 48 | 84 | 100→2536 | 620→3060 | C2 (6.4e-02) | 4.9e+00 |
| W2/wall/bulge-amp0.8 | stalled | 7.6e-04 | 1.3e-02 | 78 | 94 | 589→3071 | 620→3102 | C1c f_r(seal) (1.3e-02) | 3.5e+00 |
| W3/plateau/bulge-amp0.8 | stalled | 5.2e-03 | 2.0e-02 | 48 | 80 | 100→2518 | 620→3043 | f-PDE (2.0e-02) | 1.2e+21 |
| W3/wall/bulge-amp0.8 | stalled | 2.8e-04 | 6.3e-03 | 53 | 93 | 589→3042 | 620→3073 | C1c f_r(seal) (6.3e-03) | 9.9e-01 |
| W4/plateau/bulge-amp0.8 | stalled | 2.3e-02 | 3.2e-02 | 49 | 93 | 100→2609 | 620→3081 | f-PDE (3.2e-02) | 4.0e+22 |
| W4/wall/bulge-amp0.8 | iter/wall-capped | 1.2e-04 | 5.8e-03 | 150 | 66 | 589→2466 | 620→2497 | C1c f_r(seal) (5.8e-03) | 1.7e+00 |
| W5/plateau/bulge-amp0.8 | iter/wall-capped | 1.8e-02 | 8.6e-02 | 150 | 47 | 100→721 | 620→1241 | f-PDE (8.6e-02) | 5.0e+01 |
| **W5/wall/bulge-amp0.8** | iter/wall-capped | 9.9e-04 | 6.9e-03 | 150 | **0** | 589→611 | 620→642 | C1c f_r(seal) (6.9e-03) | 1.9e+00 |
| W6/plateau/bulge-amp0.8 | iter/wall-capped | 4.1e-01 | 4.5e-01 | 150 | 29 | 100→439 | 620→959 | f-PDE (4.5e-01) | 7.0e+01 |
| **W6/wall/bulge-amp0.8** | iter/wall-capped | 5.6e-03 | 3.0e-02 | 150 | **0** | 589→633 | 620→664 | C1b (3.0e-02) | 3.7e+01 |
| C1/plateau/bulge-amp0.8 | stalled | 7.3e-01 | 8.5e-01 | 50 | 83 | 100→2566 | 620→3086 | C2 (8.5e-01) | 1.9e+00 |
| C1/wall/bulge-amp0.8 | stalled | 3.1e-03 | 2.4e-02 | 86 | 85 | 589→3022 | 620→3053 | C1c f_r(seal) (2.4e-02) | 1.2e+01 |
| C2/plateau/bulge-amp0.8 | stalled | 1.6e-01 | 3.7e-01 | 47 | 87 | 100→2525 | 620→3046 | C2 (3.7e-01) | 5.4e+00 |
| C2/wall/bulge-amp0.8 | stalled | 4.7e-03 | 2.0e-02 | 47 | 93 | 589→3032 | 620→3063 | f-PDE (2.0e-02) | 4.3e+00 |
| W1/plateau/bulge-amp0.3 | stalled | 2.0e-03 | 1.1e-02 | 48 | 82 | 100→2515 | 620→3046 | C1c f_r(seal) (1.1e-02) | 1.5e+00 |
| W1/wall/bulge-amp0.3 | stalled | 7.2e-04 | 1.1e-02 | 54 | 95 | 589→3049 | 620→3080 | C1c f_r(seal) (1.1e-02) | 1.5e+00 |
| W2/plateau/bulge-amp0.3 | stalled | 7.2e-03 | 6.6e-02 | 48 | 82 | 100→2529 | 620→3057 | C2 (6.6e-02) | 1.8e+00 |
| W2/wall/bulge-amp0.3 | stalled | 9.3e-04 | 1.3e-02 | 52 | 91 | 589→3046 | 620→3077 | C1c f_r(seal) (1.3e-02) | 1.8e+00 |
| W3/plateau/bulge-amp0.3 | stalled | 7.7e-04 | 6.9e-03 | 49 | 80 | 100→2580 | 620→3101 | C1c f_r(seal) (6.9e-03) | 1.8e+02 |
| W3/wall/bulge-amp0.3 | stalled | 1.3e-04 | 6.2e-03 | 118 | 93 | 589→3071 | 620→3102 | C1c f_r(seal) (6.2e-03) | 9.9e-01 |
| W4/plateau/bulge-amp0.3 | stalled | 6.4e-03 | 1.6e-02 | 49 | 88 | 100→2530 | 620→3055 | f-PDE (1.6e-02) | 1.8e+18 |
| W4/wall/bulge-amp0.3 | stalled | 8.1e-05 | 4.8e-03 | 103 | 92 | 589→3071 | 620→3102 | C1c f_r(seal) (4.8e-03) | 1.5e+00 |
| W5/plateau/bulge-amp0.3 | stalled | 4.2e-03 | 1.6e-02 | 50 | 91 | 100→2519 | 620→3091 | cell rho-ODE (1.6e-02) | 1.9e+00 |
| **W5/wall/bulge-amp0.3** | iter/wall-capped | 2.3e-03 | 1.1e-02 | 150 | **0** | 589→600 | 620→631 | cell phi-ODE (1.1e-02) | 1.9e+00 |
| W6/plateau/bulge-amp0.3 | iter/wall-capped | 4.7e-03 | 1.5e-02 | 150 | 104 | 100→2576 | 620→3097 | f-PDE (1.5e-02) | 1.5e+38 |
| **W6/wall/bulge-amp0.3** | iter/wall-capped | 6.2e-03 | 2.0e-02 | 150 | **0** | 589→600 | 620→631 | C1c f_r(seal) (2.0e-02) | 1.8e+00 |
| C1/plateau/bulge-amp0.3 | stalled | 7.7e-01 | 8.7e-01 | 48 | 81 | 100→2555 | 620→3076 | C2 (8.7e-01) | 1.9e+00 |
| C1/wall/bulge-amp0.3 | stalled | 4.0e-03 | 3.0e-02 | 66 | 90 | 589→3038 | 620→3069 | C1c f_r(seal) (3.0e-02) | 2.0e+00 |
| C2/plateau/bulge-amp0.3 | stalled | 1.8e-01 | 4.0e-01 | 47 | 86 | 100→2549 | 620→3071 | C2 (4.0e-01) | 1.9e+00 |
| C2/wall/bulge-amp0.3 | iter/wall-capped | 2.6e-02 | 5.7e-02 | 150 | 10 | 589→934 | 620→965 | C1c f_r(seal) (5.7e-02) | 1.1e+02 |
| W1/plateau/bulge-amp1.5 | stalled | 7.3e-02 | 7.9e-02 | 48 | 94 | 100→2537 | 620→3057 | f-PDE (7.9e-02) | 2.7e+02 |
| W1/wall/bulge-amp1.5 | stalled | 4.1e-04 | 1.1e-02 | 63 | 77 | 589→3030 | 620→3060 | C1c f_r(seal) (1.1e-02) | 1.5e+00 |
| W2/plateau/bulge-amp1.5 | stalled | 3.4e-02 | 5.3e-02 | 48 | 86 | 100→2526 | 620→3067 | f-PDE (5.3e-02) | 7.1e+05 |
| W2/wall/bulge-amp1.5 | stalled | 6.9e-04 | 1.4e-02 | 89 | 81 | 589→3032 | 620→3065 | C1c f_r(seal) (1.4e-02) | 1.9e+00 |
| W3/plateau/bulge-amp1.5 | stalled | 1.3e-03 | 9.0e-03 | 54 | 105 | 100→2537 | 620→3059 | amb phi-ODE (9.0e-03) | 1.7e+10 |
| W3/wall/bulge-amp1.5 | iter/wall-capped | 2.7e-03 | 2.6e-02 | 150 | 1 | 589→734 | 620→765 | C1c f_r(seal) (2.6e-02) | 1.1e+00 |
| W4/plateau/bulge-amp1.5 | stalled | 6.4e-03 | 2.5e-02 | 52 | 100 | 100→2538 | 620→3060 | f-PDE (2.5e-02) | 1.2e+16 |
| W4/wall/bulge-amp1.5 | iter/wall-capped | 9.0e-03 | 6.4e-02 | 150 | 1 | 589→670 | 620→701 | seal [rho] (6.4e-02) | 7.9e+00 |
| W5/plateau/bulge-amp1.5 | iter/wall-capped | 5.0e-01 | 2.9e-01 | 150 | 25 | 100→27 | 620→549 | cell phi-ODE (2.9e-01) | 1.4e+02 |
| W5/wall/bulge-amp1.5 | iter/wall-capped | 6.0e-03 | 4.7e-02 | 150 | 28 | 589→1309 | 620→1340 | seal [rho] (4.7e-02) | 3.5e+00 |
| W6/plateau/bulge-amp1.5 | iter/wall-capped | 1.2e+00 | 4.0e-01 | 150 | 24 | 100→34 | 620→554 | f-PDE (4.0e-01) | 2.3e+03 |
| W6/wall/bulge-amp1.5 | iter/wall-capped | 5.8e-01 | 3.2e-01 | 150 | 24 | 589→738 | 620→769 | f-PDE (3.2e-01) | 2.4e+01 |
| C1/plateau/bulge-amp1.5 | stalled | 7.4e-01 | 8.5e-01 | 49 | 85 | 100→2541 | 620→3065 | C2 (8.5e-01) | 2.1e+00 |
| C1/wall/bulge-amp1.5 | iter/wall-capped | 3.0e-02 | 7.0e-02 | 150 | 1 | 589→833 | 620→864 | C1c f_r(seal) (7.0e-02) | 2.0e+00 |
| C2/plateau/bulge-amp1.5 | stalled | 1.4e-01 | 3.5e-01 | 47 | 89 | 100→2530 | 620→3054 | C2 (3.5e-01) | 1.6e+01 |
| C2/wall/bulge-amp1.5 | stalled | 1.9e-03 | 1.8e-02 | 75 | 89 | 589→3071 | 620→3102 | C1c f_r(seal) (1.8e-02) | 8.3e+00 |
| W2/plateau/cont-W1 | stalled | 1.2e-03 | 1.6e-02 | 19 | 11 | 2515→2571 | 3046→3102 | C1c f_r(seal) (1.6e-02) | 1.8e+00 |
| W2/wall/cont-W1 | stalled | 1.1e+00 | 1.0e+00 | 1 | 0 | 3071→3071 | 3102→3102 | C2 (1.0e+00) | 1.8e+00 |
| W3/plateau/cont-W1 | stalled | 1.8e-04 | 7.6e-03 | 21 | 8 | 2515→2571 | 3046→3102 | C1c f_r(seal) (7.6e-03) | 9.9e-01 |
| W3/wall/cont-W1 | stalled | 2.9e+00 | 1.7e+00 | 1 | 0 | 3071→3071 | 3102→3102 | C2 (1.7e+00) | 1.7e+00 |
| W4/plateau/cont-W1 | stalled | 1.6e-04 | 7.1e-03 | 24 | 9 | 2515→2571 | 3046→3102 | C1c f_r(seal) (7.1e-03) | 1.5e+00 |
| W4/wall/cont-W1 | stalled | 7.0e+00 | 2.6e+00 | 1 | 0 | 3071→3071 | 3102→3102 | C2 (2.6e+00) | 2.6e+00 |
| W5/plateau/cont-W1 | stalled | 9.5e-05 | 3.2e-03 | 69 | 8 | 2515→2571 | 3046→3102 | cell phi-ODE (3.2e-03) | 1.9e+00 |
| W5/wall/cont-W1 | stalled | 1.0e+02 | 9.7e+00 | 1 | 0 | 3071→3071 | 3102→3102 | C2 (9.7e+00) | 9.7e+00 |
| W6/plateau/cont-W1 | iter/wall-capped | 1.4e-03 | 1.0e-02 | 150 | 8 | 2515→2570 | 3046→3101 | f-PDE (1.0e-02) | 5.7e+01 |
| W6/wall/cont-W1 | stalled | 1.1e+02 | 9.9e+00 | 1 | 0 | 3071→3071 | 3102→3102 | C2 (9.9e+00) | 9.9e+00 |
| C1/plateau/cont-W1 | stalled | 6.4e-03 | 4.0e-02 | 34 | 12 | 2515→2571 | 3046→3102 | C1c f_r(seal) (4.0e-02) | 1.9e+00 |
| C1/wall/cont-W1 | stalled | 3.2e+00 | 1.8e+00 | 1 | 2 | 3071→3071 | 3102→3102 | C2 (1.8e+00) | 1.9e+00 |
| C2/plateau/cont-W1 | stalled | 4.3e-03 | 2.7e-02 | 27 | 12 | 2515→2571 | 3046→3102 | C1c f_r(seal) (2.7e-02) | 3.4e+02 |
| C2/wall/cont-W1 | stalled | 3.6e+00 | 1.6e+00 | 1 | 2 | 3071→3071 | 3102→3102 | C2 (1.6e+00) | 1.9e+00 |

Notes: (a) Continuation behavior is the MIRROR of bracket 1: here the WALL-slice continuation
rows stall in 1 iteration (the W1/wall end state sits at the guard; under N=2 κ=1 couplings its
E_ang(seal) reads ~11.7 vs U ~ 2 → an O(10) C2 jump with no downhill step inside the guard),
while the PLATEAU-slice continuation rows descend normally to the same C1c-held floors
(W5/plateau/cont-W1 reached the sweep's second-lowest Φ = 9.5e-5). In bracket 1 it was the
plateau side that stalled in 1 iteration. Same mechanism (the guard-parked donor state), opposite
slice — continuation again neither found a new basin nor changed any qualitative behavior.
(b) One raw curiosity: W5/W6 plateau amp1.5 ran INWARD (r_p 100 → 27/34, the only inward
trajectories in the sweep) with large residuals (0.3–0.4) — a different unstable direction,
not a floor. (c) The small-coupling controls on the plateau slice hold C2 as top row with
E_ang(seal) unable to reach 2 (C1: 1.15, C2: 1.65) — same signature as bracket 1.

## 3. Phase-2: flooring (maxit 2000) + the wide-guard observation run

For each (cell × slice), the best phase-1 config re-run with maxit=2000, wall 240 s; then ONE
widened-guard run (r_sU < 25·r_s, per-iteration caps unchanged) on the best guard-presser
(W4/wall/amp0.3, the lowest-Φ guard-pressing run). Gate columns read on END states (owed ~0
only on a true solution — none is one).

| run | status | Φ_end | max\|F\| | iters | r_p → | r_sU → | top row | Δφ_float | H_cell_max | q_fold | q_seal | E_ang_seal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P2/C1/plateau/amp0.8 | stalled | 7.3e-01 | 8.5e-01 | 50 | →2566 | →3086 | C2 (8.5e-01) | 4.70 | 1.9e+00 | 1.4819 | -0.023 | 1.1494 |
| P2/C1/wall/amp0.8 | stalled | 3.1e-03 | 2.4e-02 | 86 | →3022 | →3053 | C1c f_r(seal) (2.4e-02) | 15.48 | 1.2e+01 | 1.4809 | 0.037 | 1.9957 |
| P2/C2/plateau/amp1.5 | stalled | 1.4e-01 | 3.5e-01 | 47 | →2530 | →3054 | C2 (3.5e-01) | 13.52 | 1.6e+01 | 1.4819 | -0.072 | 1.6471 |
| P2/C2/wall/amp1.5 | stalled | 1.9e-03 | 1.8e-02 | 75 | →3071 | →3102 | C1c f_r(seal) (1.8e-02) | 4.69 | 8.3e+00 | 1.4809 | 0.035 | 1.9996 |
| P2/W1/plateau/amp0.3 | stalled | 2.0e-03 | 1.1e-02 | 48 | →2515 | →3046 | C1c f_r(seal) (1.1e-02) | 5.72 | 1.5e+00 | 1.4812 | -0.031 | 1.9937 |
| P2/W1/wall/amp0.8 | stalled | 3.7e-04 | 1.1e-02 | 78 | →3071 | →3102 | C1c f_r(seal) (1.1e-02) | 5.74 | 1.5e+00 | 1.4809 | 0.036 | 1.9999 |
| P2/W2/plateau/amp0.3 | stalled | 7.2e-03 | 6.6e-02 | 48 | →2529 | →3057 | C2 (6.6e-02) | 5.53 | 1.8e+00 | 1.4801 | -0.049 | 1.9338 |
| P2/W2/wall/amp1.5 | stalled | 6.9e-04 | 1.4e-02 | 89 | →3032 | →3065 | C1c f_r(seal) (1.4e-02) | 2.04 | 1.9e+00 | 1.4805 | 0.035 | 1.9995 |
| P2/W3/plateau/amp0.3 | stalled | 7.7e-04 | 6.9e-03 | 49 | →2580 | →3101 | C1c f_r(seal) (6.9e-03) | 10.83 | 1.8e+02 | 1.4810 | -0.016 | 1.9993 |
| P2/W3/wall/amp0.3 | stalled | 1.3e-04 | 6.2e-03 | 118 | →3071 | →3102 | C1c f_r(seal) (6.2e-03) | 2.67 | 9.9e-01 | 1.4809 | 0.036 | 1.9999 |
| P2/W4/plateau/amp0.3 | stalled | 6.4e-03 | 1.6e-02 | 49 | →2530 | →3055 | f-PDE (1.6e-02) | 27.43 | 1.8e+18 | 1.4833 | -0.043 | 1.9996 |
| P2/W4/wall/amp0.3 | stalled | 8.1e-05 | 4.8e-03 | 103 | →3071 | →3102 | C1c f_r(seal) (4.8e-03) | 6.93 | 1.5e+00 | 1.4808 | 0.036 | 2.0000 |
| P2/W5/plateau/amp0.3 | stalled | 4.2e-03 | 1.6e-02 | 50 | →2519 | →3091 | cell rho-ODE (1.6e-02) | 5.58 | 1.9e+00 | 1.4845 | 0.033 | 2.0050 |
| **P2/W5/wall/amp0.8** | iter/wall-capped | 2.9e-04 | 6.4e-03 | 2000 | →612 | →643 | C1c f_r(seal) (6.4e-03) | 2.77 | 1.9e+00 | 1.4808 | 0.036 | 2.0014 |
| P2/W6/plateau/amp0.3 | stalled | 4.6e-03 | 1.5e-02 | 302 | →2576 | →3097 | f-PDE (1.5e-02) | 50.37 | 1.4e+38 | 1.4809 | -0.007 | 2.0026 |
| **P2/W6/wall/amp0.8** | iter/wall-capped | 2.3e-03 | 1.7e-02 | 2000 | →634 | →665 | C1c f_r(seal) (1.7e-02) | 2.44 | 2.5e+00 | 1.4807 | 0.036 | 2.0036 |
| P2b-wideguard/W4/wall/amp0.3 | (wide) | 1.9e-05 | 1.9e-03 | 149 | →7481 | →7515 | C1c f_r(seal) (1.9e-03) | 9.67 | 1.5e+00 | 1.4830 | 0.025 | 2.0000 |

**Reading:** (a) NOTHING converges at 2000 iterations — floors sit at max|F| ~ 4.8e-3 to 0.85,
all far above the 1e-8 contract floor. (b) **Wide-guard / dilation exponent:** freed to 25·r_s,
the W4/wall runaway kept inflating (r_p → 7481 = 12.1·r_s) with Φ falling (1.9e-5, max|F|
1.9e-3) and no floor in sight. Comparing the guard-parked parent (r_p 3071) to the wide state
(r_p 7481, dilation ×2.436): the C1c residual vector keeps sign and shape and scales by
2.41 ± 0.14 across the 8 θ-nodes → **residual ~ r^−0.99 (≈ 1/r) along the dilation orbit** —
approximately self-similar scale-runaway. (Bracket 1 measured r^−1.31 with near-exact node
uniformity ±1e-4; here the exponent is shallower and the node scatter is ±6% — same family,
not identical.) (c) H_cell — the free consistency gate — is O(1) on EVERY end state (≈ 1.5 on
the whole runaway family, ≈ 1.9 on the station-locked family, and up to 1e38 on the extreme
plateau states where the cell fields blow up): no state anywhere is near a true composite
solution; every falling Φ is a false floor. (d) q_fold reads the banked 1.4808–1.4845 on every
end state; Δφ floats 2.0–50.4 (vs anchor 7.004) — unconstrained, as expected off-solution.

## 4. The wall-N=2-κ≈1 story (the bracket's priority question, answered)

This bracket has genuine wall-admissible N=2 κ=1 cells and they DO behave differently — but the
difference is SPEED and LOCKING, not existence of a solution:

- **No cap-speed runaway:** wall-seeded W5/W6 at amps 0.3/0.8 never touch the 0.10·r_s trust
  cap (ncap = 0 through 2000+ iterations) while every other configuration presses it 60–100
  times. Their boundary motion is O(1e-3–1e-2) r-units/iteration — ~100× below cap speed.
- **Station-lock (the sharp identity):** on every such end state the seal sits EXACTLY at the
  ambient shell's U=2 station: ρ_p = 1.003689–1.003690, U(ρ_p) = 2.000003, E_ang(seal)
  self-tuned to 2.001–2.004 — while ABSOLUTE r_p varies freely (600, 612, 634, 642; even
  > r_s). The lock is to the shell-relative station (banked profile: ρ(r*) = 1.003829 at
  r* = 590.47), not to a position. This is bracket 1's "W6 parking at r*" made precise: the
  E1 station is a genuine organizing structure of the coupled system's landscape.
- **But it is NOT an attractor (the extended-floor diagnosis, run beyond the bracket-1
  protocol):** re-solving the P2/W5/wall end state for 4000 further iterations, r_p creeps
  612.03 → 642.17 with the shell width EXACTLY preserved (31.019 at both ends — pure
  translation, zero dilation), Φ still slowly falling (2.9e-4 → 1.4e-4), max|F| 6.4e-3 →
  5.8e-3 (C1c sawtooth holdout barely moving), H_cell pinned at 1.90. The station-locked
  family is an ultra-slow outward TRANSLATION of the whole composite — a slow-motion member
  of the same no-attractor runaway, with the seal riding the traveling shell's U=2 station.
- **Amp dependence:** amp 1.5 wall seeds break the lock and rejoin the fast runaway (W5:
  r_p → 1309; W6: → 738 with f-PDE 0.32); the lock has a finite basin in seed amplitude.
- **Interior fields on the locked states are extreme:** ρ_cell reaches 29.0 (W5) / 20.4 (W6),
  φ_cell up to +1.6 (vs ρ_core floor 1.026/1.054, ρ_core actual 2.72/2.09) — the cell pays
  the C2 = U = 2 seal price with a large-amplitude interior, and the f-PDE/C1c still won't
  close (σ cross-checks read max_rel ~ 1–2 on both domains, raw — fully off-solution).

Answer to the brief's question ("parking? convergence? floors?"): **parking = YES as behavior
(robust: 2 cells × 2 amps × 2 grids), diagnosed as station-locked slow translation;
convergence = NO (floors at max|F| ~ 6e-3, C1c θ-sawtooth, H_cell ≈ 1.9); floors = false
floors (Φ falls indefinitely along the slow translation, H_cell never moves).**

## 5. Residual anatomy + grid cross-check (artifact controls)

`sweep_E2b_A1Z1_anatomy.py` → `microphysics_E2b_A1Z1_anatomy.json` (17 saved .pt states; CPU
recompute reproduces the GPU max|F| on 16 of 17 states, e.g. P2/W5/wall 6.36e-3 both).
**Flagged exception (raw):** P2/W6/plateau/amp0.3 reads maxF 1.53e-2 on GPU vs 7.44 on CPU —
this is the H_cell ~ 1.4e38 end state whose cell fields sit in e^{2φ} overflow territory
(Δφ_float 50.4), where device rounding differences amplify enormously; the state is nowhere
near a solution either way, but the cross-check failure on extreme states is a conditioning
fact worth carrying.

- **The C1c holdout is the same grid-scale θ-sawtooth as bracket 1** — f_r(r_p, θ_k)
  alternates sign node-to-node (P2/W5/wall: [+6.4e-3, −2.7e-3, +1.5e-3, −1.3e-3, +1.1e-3,
  −1.5e-3, +2.7e-3, −6.3e-3] — antisymmetric across the equator, pole-dominant), with the u
  field forming the seal-hugging boundary layer that buys E_ang(seal) ≈ 2 but cannot
  simultaneously flatten f_r.
- **Runaway self-similarity:** §3(b) — residual ~ r^−0.99 along the dilation orbit, C1c
  sign/shape preserved.
- **Shell rigidity:** wall-seeded runs preserve the seed's 31.0 ambient-shell width almost
  exactly (both the fast runaway and the slow station-locked translation, which preserves it
  to 31.019 over the whole extended floor); plateau-seeded runs preserve their 520.4 width
  loosely (end widths 472–572, ±10%).
- **Grid cross-check** (`sweep_E2b_A1Z1_gridcheck.py`, Nr=16, Nθ=12, Na=256, maxit 400):
  W1/wall/amp0.8 → same cap-speed runaway to the guard (r_p → 3071), same C1c holdout
  (1.4e-2), stalled; W5/wall/amp0.3 → same station-locked slow translation (r_p → 603.2,
  ncap = 0, E_ang(seal) 2.0056, H_cell 1.9), floors max|F| 2.0e-2 (seal-[ρ] top at this grid).
  Both behaviors persist at finer resolution — not coarse-grid artifacts.

## 6. Pre-committed failure reading (plan order, solver-first — NO mechanism)

1. **Seeds/coverage:** 3 amplitudes (far-from-rigid included), both slices, 8 window cells
   spanning the necessary-map INCLUDING the genuine wall-admissible N=2 κ=1 cells and two
   genuine fully-admissible controls, plus (ξ,κ)-continuation both slices: 62 + 17 + 2 + 1
   solves. Every trajectory joins one of THREE behaviors: the cap-speed outward runaway
   (dominant), the station-locked slow outward translation (wall-admissible N=2 κ=1, wall
   slice, moderate amps), or an inward-collapse direction at extreme plateau amps (large
   residual, not a floor). No basin unexplored by seed widening is indicated — the locked
   family, the one new structure, was found and diagnosed.
2. **Grid/conditioning:** trust caps, 2000-iteration floors, the 25·r_s wide guard, a finer
   grid (Nr 16/Nθ 12/Na 256), and a 4000-iteration extended floor — behavior unchanged and now
   CHARACTERIZED: an approximately self-similar scale-runaway (residual ~ r^−1.0) plus a
   station-locked slow translation, both with O(1) H_cell violations at every point. These are
   LM stagnation/creep behaviors of a system with no attractor in the swept window, not
   conditioning floors.
3. **Frame-level statement (SCOPED, provisional — this is the SECOND of four brackets):**
   within this bracket's swept window (N ∈ {1,2}, ξ ∈ [0.05,1], κ ∈ [0.01,1], both
   neighborhoods, static concentric L2+L4 cell, a* held), the coupled system shows NO
   finite-size solution. The novelty vs bracket 1: the E1 U=2 station is now demonstrated to
   be a real organizing structure (the seal locks to it exactly, ρ_p → the station value at
   3e-6 precision) — but locking the seal is not the same as closing the cell: C1c + f-PDE
   still hold out and the locked composite drifts outward forever. Per the plan this is NOT
   yet the E2 scoped negative — that verdict needs all four brackets + the blind verifier.
   The pre-named escape ladder (ω ≠ 0 internal rotation) remains a REFRAME decision with
   Charles, never a patch — nothing here licenses reaching for it unilaterally.

## 7. Coverage statement

RUN: all 8 window cells × 2 slices × 3 amplitudes (48) + 14 continuation seeds (62 total,
phase 1); 16 flooring re-runs + 1 wide-guard run (phase 2); 1 extended-floor run (4000 it) on
the station-locked state; 2 grid cross-checks; anatomy on all 17 saved states. THROUGHPUT-
LIMITED REMAINDER: NONE — the full pre-registered matrix ran (total compute ≈ 10 min of the
~90-min budget). NOT swept (out of contract scope for this bracket, for the record): N ≥ 3;
ξ > 1.9 (ξN < 2 enforced); κ > 1; anchor_mode='exact' (unwired branch, needs Charles's
ruling); off-center cells (E1 scope); ω ≠ 0.

## 8. Conditioning notes for brackets 3–4 (A3 Z=8, A3 Z=1)

- Everything in the bracket-1 §8 notes held here (dense-LM speed ~0.02–0.06 s/it at n=506;
  full matrix ≈ 2 min; caps essential; H_cell on every end state; C2 self-tunes to U ≈ 2
  except where E_ang_max < 2 — there C2 itself is the holdout). Keep all of it.
- **NEW — extend-floor any "parked" state before describing it as finite-size.** Bracket 1's
  W6-at-r* parking looked like "the only finite-size behavior"; the extended floor here (4000
  extra iterations from the saved end state, ~80 s) showed the parked family CREEPS (pure
  translation, width-preserving, station-locked). Cheap and decisive; recommend retro-applying
  to bracket 1's W6 state (saved .pt exists) at verifier time.
- **NEW — the station-lock identity is the sharp diagnostic for wall behavior:** read ρ_p and
  U(ρ_p) on wall-slice end states. If A3 brackets show the same U(ρ_p) = 2.000 lock, the
  station is family-universal; if not, it is A1-specific. One line of arithmetic per state.
- **NEW — CPU/GPU cross-check fails on e^{2φ}-overflow end states** (H_cell ≳ 1e15,
  Δφ_float ≳ 25): device rounding amplifies; don't read the CPU-GPU mismatch on such states
  as a machinery bug (16/17 clean here, the 1 mismatch is the overflow state). The extreme
  states themselves are data (the plateau runaway drives cell fields to blow-up in this
  bracket much harder than bracket 1: H_cell up to 1e38 vs 1e15).
- The wide-guard dilation exponent is bracket-dependent: −1.31 (Z=8) vs −0.99 (Z=1), node
  scatter ±1e-4 vs ±6e-2. Measure it per bracket; the A3 values will say whether the exponent
  tracks Z, the family, or U_seal.
- Continuation donors that sit ON the guard poison the opposite-slice continuation rows
  (1-iteration C2-jump stalls; seen both brackets, mirrored slices). If a cleaner continuation
  is wanted in brackets 3–4, donate from the best NON-guard-pressing end state instead
  (Category-A choice; flag it if used).

## Files

- `sweep_E2b_A1Z1.py` (phase 1) / `sweep_E2b_A1Z1_phase2.py` / `sweep_E2b_A1Z1_gridcheck.py` /
  `sweep_E2b_A1Z1_anatomy.py` (all adapted from the bracket-1 scripts); log `sweep_E2b_A1Z1.log`.
- `microphysics_E2b_A1Z1_results.json` (62 runs, full diagnostics + gates per run);
  `microphysics_E2b_A1Z1_phase2.json` (17); `microphysics_E2b_A1Z1_gridcheck.json` (2);
  `microphysics_E2b_A1Z1_anatomy.json` (17); `microphysics_E2b_A1Z1_extfloor.json` (1).
- Saved fields (recompute-on-saved): `E2b_A1Z1_P2_*.pt` (16), `E2b_A1Z1_P2b_wideguard_W4_wall.pt`,
  `E2b_A1Z1_P2c_extended_W5_wall.pt` (18 total).
- NOT committed (per brief); blind verifier pass still owed before any banking.

---

## REGRADE (blind verifier a98ce79ecc245b189, 2026-07-04 — supersedes the "station lock" wording above)

Bracket 2's wall end states are NOT "self-tuned exactly to the U=2 station" — ρ_p =
1.003689–1.003690 is the SEED's shell height ρ_seed(0.95·r_s) = 1.0036886 PRESERVED under rigid
translation, sitting 1.40e-4 BELOW the true station root 1.0038293; U(ρ_p) = 2.0000031 ≈ 2 only
because the 0.95·r_s seed lies on the profile's U≈2 shoulder; the solver-tuned quantity is the
C2 row (E_ang(seal) → U(ρ_p)); bracket 4's outside-the-station geometry (dev(seed) ≤ 3.2e-5,
dev(station) +1.5e-4 uniform, U(ρ_p) < 2) settles preserved-over-tuned decisively.
