# E2b SWEEP — BRACKET 4 (A3, Z=1): results (OBSERVE mode) — FINAL bracket of the E2 contract

**Date:** 2026-07-04. **Status: PROVISIONAL — sweep agent output, NOT verified, NOT banked.**
Contract: `microphysics_E2_battle_plan.md` (APPROVED AS WRITTEN). Machinery:
`cell_solver_composite.py` UNCHANGED (imported; same state as brackets 1–3, clean tree). Scripts
adapted (not rewritten) from the bracket-3 sweep per the E2b brief; the ACCUMULATED bracket-1+2+3
conditioning notes (`microphysics_E2b_A1Z8_results.md` §8 + `microphysics_E2b_A1Z1_results.md`
§8 + `microphysics_E2b_A3Z8_results.md` §8) followed: full matrix without triage, 0.10·r_s caps,
ONE wide-guard dilation-exponent run, H_cell on EVERY end state, extend-floor on the parked
state, and — the bracket-3 regrade instruction — **the seed shell height AND the exact station
root computed UP FRONT, ρ_p read against BOTH on every wall end state**. Data-blind: no particle
masses/data anywhere. Everything below is WHAT THE COUPLED SYSTEM DID — no merit gating;
non-convergence is first-class data.

**Headline observation (scoped to this bracket, this grid, these seeds): the coupled composite
converged NOWHERE — 0 of 70 phase-1 solves, 0 of 19 phase-2 flooring/wide-guard solves, 0 of 1
extended-floor, 0 of 1 wide-guard continuation, 0 of 2 grid cross-checks reached the
pre-committed floor max|F| ≤ 1e-8. Zero convergence is now FOUR-FOR-FOUR across the full E2
bracket matrix (264 phase-1 solves total). The same two base behaviors appear — the dominant
outward runaway (59/70 press the 5·r_s guard) and the wall-seeded finite-size parking (ncap = 0)
— but with THREE bracket-4 novelties, each stated raw: (1) PRESERVED-vs-TUNED IS SETTLED,
CLEANLY: this bracket's geometry separates the two readings for the first time (r* = 0.94801·r_s
< 0.95·r_s, so the wall seed sits OUTSIDE the station and its shell height carries U < 2) — and
every wall end state (parked, runaway, wide-guard, grid-check) reads ρ_p = the SEED's shell
height 1.0037706 to 1e-6..1e-7 with U(ρ_p) = 1.999998 BELOW 2, never the station root 1.0036152
(U = 2 exactly, 1.6e-4 away). The lock is seed-height PRESERVATION under rigid translation;
nothing is tuned to the U = 2 root. (2) THE DILATION ORBIT IS NOT SELF-SIMILAR HERE AND
DECELERATES: the wide-guard run did NOT sprint to the 25·r_s bound (bracket 3: 255 iterations to
24.94·r_s; here 2000+6000 iterations reach only r_p = 4654 = 5.9·r_s, final speed ~0.006
r-units/iter with ZERO cap presses), and the C1c residual keeps sign but NOT shape (per-node
exponents +0.09 to −4.64; effective max|F| exponent ≈ −1.40 over ×1.20 dilation). The
pre-registered discrimination therefore comes out NEGATIVE BOTH WAYS: this bracket has the
HIGHEST U_seal (1.686) and the MOST wall-admissible N=2 cells (3), so both candidate correlates
predicted ≈ −1.0 — neither a clean −1.0 nor a clean −1.3 exists; the exponent-correlate question
DISSOLVES (the "exponent" is not a bracket constant, it is a property of how far along the
deceleration the orbit is measured). (3) THE
PARKED BASIN IS THE NARROWEST AND SHALLOWEST OF THE FOUR: only the three N=2 κ=1 cells park, ONLY at amp 0.3 (amp 0.8 and 1.5 both break the lock —
opposite of bracket 3, stricter than bracket 2), the controls do NOT park despite paying
E_ang(seal) ≈ 1.997 (which BREAKS bracket 3's "controls-can-pay ⇒ wide basin" correlate), and
the extended floor does not creep — the parked state ESCAPES at cap speed (r_p 857 → 3524 in 35
iterations, seed-height lock breaking to ρ_p = 1.0105) then stalls. Parking here is a transient
waypoint on the runaway, not a quasi-stationary creep. H_cell is O(1)-or-worse on every end
state (min 0.99 over all 70): nothing anywhere is near a true composite solution.**

Sections: 1 setup/premises · 2 phase-1 outcome table · 3 phase-2 flooring + wide-guard/dilation
exponent · 4 preserved-vs-tuned (settled) + the parked-basin story · 5 residual anatomy + grid
cross-check · 6 pre-committed failure reading · 7 coverage statement · 8 notes for the E2
verdict / blind verifier (no bracket 5) · files.

## 1. Setup and premise ledger (chose-or-derived; E1 ledger #1–#17 inherited UNCHANGED)

Bracket: A3, Z=1 (banked E0: a* = b = 0.9928086030 HELD — this is the E0 FRESH-CONVERGED
`a_reshot`; A3 Z=1 was Stage-A budget-cut so `a_banked` is None and `load_bracket`'s documented
fallback to the blind-verified fresh value IS the banked number, per the E0 table note; r_s =
784.4148, ρ_s = 1.352957, q = 1.0717828, ρ_c = 1; U_seal = U(ρ_s) = 1.68623 — the HIGHEST of
the four brackets: 0.052 A1Z8, 1.409 A1Z1, 0.671 A3Z8, 1.686 here; it equals the E1 ξN wall
bound). A3 slice: U = 2ρ²(1+b)/(1+bρ⁴); U=2 roots are ρ = 1 (core fold) and ρ = b^{−1/2} =
**1.0036152090** (the exact station root). E1: r* = 0.94801·r_s = 743.63, ρ(r*) = 1.0036152 —
the station root to 7 digits. **Up-front discriminators (computed BEFORE any solve, per the
bracket-3 §8 note):** the 0.95·r_s wall seed sits at r = 745.19 > r* — OUTSIDE the station, a
first — and its shell height is ρ_seed(0.95·r_s) = **1.0037706012** with U(seed height) =
**1.9999977 < 2**. Separation seed-height − station = +1.554e-4: preserved ⇒ ρ_p ≈ 1.0037706,
U just below 2; tuned ⇒ ρ_p ≈ 1.0036152, U = 2.000000 exactly. E1 audit: the N=2 inversion IS
present and this bracket has THREE N=2 κ=1 wall-admissible cells (admfrac 0.110/0.102/0.094 —
the most of any bracket) → W7 added per the E2b brief. Anchor per plan wording fix: a* HELD;
Δφ floats and is REPORTED (P-E2b4-8, THEORY: E1 ledger #5).

| # | Premise (this run) | Tag |
|---|---|---|
| P-E2b4-1 | Window cells W1–W7, C1, C2 from the E1 `necessary_map` for THIS bracket. W5/W6/W7 = the three GENUINE wall-admissible N=2 κ=1 articles (outer_seal_admissible=True). W3 has admfrac 1.0 HERE (bracket 3's W3 flag does not apply). Controls C1/C2 genuinely admfrac 1.0. NO substitute flags anywhere. | CHOSE (map-guided) |
| P-E2b4-2 | Slices: plateau-target r_p0 = 100.0 (same absolute value as brackets 1–3; r_p0/r_s ≈ 0.127); wall-target r_p0 = 0.95·r_s = 745.19 (r* = 743.63 — seed OUTSIDE the station, first bracket). Seed placements only; r_p FREE. | CHOSE |
| P-E2b4-3 | Seed amplitudes amp ∈ {0.3, 0.8, 1.5}, bulge = amp·(1−μ²)·sin(π(ζ+1)/2) on the rigid map | CHOSE (banked undersampling lesson; bulge theorem = non-perturbative in θ) |
| P-E2b4-4 | Grids Nr=12, Nθ=8, Na=192, kmap=2.5 (brackets-1/2/3 choice unchanged); confirm grids reserved for candidates (none arose); grid cross-check run anyway on the two key behaviors (§5) | Category-A conditioning |
| P-E2b4-5 | LM maxit 150 (phase 1) / 2000 (phase 2) / 4000 (extended floor) / 6000 (wide-guard continuation), wall 75/240/300/240 s; free-boundary per-iteration caps \|Δr_p\|,\|Δr_sU\| ≤ 0.10·r_s (whole-step rescale); validity guard r_p ∈ (1e-6·r_s, r_sU), r_sU < 5·r_s (25·r_s in the wide-guard runs) — reject-step guards, never constraint rows | Category-A trust handling (brackets-1/2/3 pattern, pre-authorized) |
| P-E2b4-6 | Convergence = max\|F\|∞ ≤ 1e-8 (rows O(1) at seed) | Pre-committed (plan instrument 1) |
| P-E2b4-7 | Continuation seeds: best-Φ W1 end state per slice, re-solved under each other cell's couplings. BOTH donors ended guard-parked (r_sU = 3922.1 = the 5·r_s bound) → poisoned-donor flag carried per row (`donor_guard_parked: true`); no non-guard donor existed among W1 end states | Plan method + bracket-2 note (flagged) |
| P-E2b4-8 | a* HELD at 0.9928086030 (= a_reshot, the banked number for this budget-cut bracket); Δφ floats, REPORTED | THEORY (E1 ledger #5) |
| P-E2b4-9 | Budget: coverage-first order; internal 70-min cap; actual total compute ≈ 12 min of the ~90-min ceiling | anti-hang |
| P-E2b4-10 | ONE deviation-class addition, flagged: the wide-guard run was CONTINUED from its own saved end state for 6000 further iterations (same run, extended iteration budget — Category-A, same class as the extend-floor) because 2000 iterations did not produce the dilation travel the exponent protocol needs (bracket 3 note assumed a sprint; this bracket decelerates). No knob changed; the continuation is reported as part of the one wide-guard observation. | Category-A (flagged addition) |

Window cells (all from `microphysics_E1_probe_results.json` necessary_map, A3 Z=1):

| cell | N | ξ | κ | provenance |
|---|---|---|---|---|
| W1 | 1 | 0.5 | 0.1 | moderate-ξ plateau (admfrac 1.0); identical to brackets 1–3 → continuation start + comparability |
| W2 | 1 | 0.2 | 0.1 | moderate-ξ plateau neighbor (admfrac 1.0) |
| W3 | 1 | 1.0 | 0.1 | moderate-ξ plateau neighbor (admfrac 1.0 in THIS bracket — no flag) |
| W4 | 1 | 0.5 | 1.0 | κ-continuation neighbor (admfrac 1.0) |
| W5 | 2 | 0.05 | 1.0 | **WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.110, outer_seal_admissible=True) |
| W6 | 2 | 0.1 | 1.0 | **2nd WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.102, outer_seal_admissible=True) |
| W7 | 2 | 0.2 | 1.0 | **3rd WALL-ADMISSIBLE N=2 κ=1** (admfrac 0.094, outer_seal_admissible=True) — BRACKET NOVELTY, E1 found 3 here (most of any bracket) |
| C1 | 1 | 0.05 | 0.01 | fully-admissible small-coupling control (admfrac 1.0) |
| C2 | 2 | 0.05 | 0.01 | 2nd fully-admissible control (admfrac 1.0 — genuine, no flag) |

GPU discipline: V100 torch float64; GPU-vs-CPU seed-residual spot-check rel maxdiff 1.06e-11
(JSON `notes`); no batched-triangular-solve anywhere; anatomy recomputed on CPU from saved
fields — **19/19 phase-2 states match GPU to ≤ 6.2e-12 relative** (+ the extended-floor and
wide-continuation states match by hand; §5). As bracket 3 predicted for the underflow direction:
this bracket's extreme states run φ_cell deep NEGATIVE (to −37), no e^{2φ} overflow, all clean.

## 2. Phase-1 outcome table (70 solves: 9 cells × 2 slices × 3 amps + 16 continuation)

Statuses: **CONVERGED 0 / stalled 60 / iter-or-wall-capped 10.**
Top-holdout-row census over all 70: C1c f_r(seal) 21, f-PDE 19, C2 19, seal [rho] 5,
amb phi-ODE 1, amb rho-ODE 1, cell rho-ODE 1, cell phi-ODE 1, C1b 1, core rho' 1 —
**C1c still leads but with the SMALLEST margin of the four brackets** (21/70 vs 38/62, 25/62,
34/62). Free boundaries: 60/70 ended with r_sU > 2·r_s; 59/70 pressed the 5·r_s guard (3922.07)
— the runaway is the most dominant of the four brackets. H_cell_max ≥ 0.99 on every one of the
70 end states (median ≈ 7.9, max 1.9e17): nothing is near a true composite solution anywhere.
Bold rows = the parked (ncap = 0, finite-r_p) family — NOTE it is ONLY the three N=2 κ=1 cells
and ONLY at amp 0.3 (see §4).

| run (cell/slice/seed) | status | Φ_end | max\|F\| | iters | ncap | r_p → | r_sU → | top residual row | H_cell_max |
|---|---|---|---|---|---|---|---|---|---|
| W1/plateau/bulge-amp0.8 | stalled | 2.5e-02 | 4.7e-02 | 47 | 85 | 100→3180 | 784→3869 | f-PDE (4.7e-02) | 2.3e+14 |
| W1/wall/bulge-amp0.8 | stalled | 2.4e-04 | 8.3e-03 | 76 | 92 | 745→3883 | 784→3922 | C1c f_r(seal) (8.3e-03) | 1.5e+00 |
| W2/plateau/bulge-amp0.8 | stalled | 3.0e-02 | 1.1e-01 | 47 | 85 | 100→3144 | 784→3849 | C2 (1.1e-01) | 2.0e+01 |
| W2/wall/bulge-amp0.8 | stalled | 7.4e-04 | 1.5e-02 | 73 | 93 | 745→3883 | 784→3922 | C1c f_r(seal) (1.5e-02) | 2.1e+00 |
| W3/plateau/bulge-amp0.8 | stalled | 1.9e-02 | 4.2e-02 | 47 | 90 | 100→3161 | 784→3845 | f-PDE (4.2e-02) | 3.0e+11 |
| W3/wall/bulge-amp0.8 | stalled | 8.0e-05 | 4.9e-03 | 82 | 93 | 745→3883 | 784→3922 | C1c f_r(seal) (4.9e-03) | 9.9e-01 |
| W4/plateau/bulge-amp0.8 | stalled | 1.3e-01 | 1.3e-01 | 47 | 96 | 100→3155 | 784→3851 | cell rho-ODE (1.3e-01) | 1.4e+00 |
| W4/wall/bulge-amp0.8 | stalled | 5.5e-05 | 3.9e-03 | 84 | 94 | 745→3883 | 784→3922 | C1c f_r(seal) (3.9e-03) | 1.6e+00 |
| W5/plateau/bulge-amp0.8 | stalled | 3.3e-04 | 8.5e-03 | 88 | 131 | 100→3238 | 784→3922 | f-PDE (8.5e-03) | 1.8e+01 |
| W5/wall/bulge-amp0.8 | stalled | 1.8e+01 | 2.6e+00 | 42 | 102 | 745→3883 | 784→3921 | cell phi-ODE (2.6e+00) | 1.0e+03 |
| W6/plateau/bulge-amp0.8 | stalled | 9.1e-03 | 4.7e-02 | 113 | 104 | 100→3238 | 784→3922 | f-PDE (4.7e-02) | 8.1e+02 |
| W6/wall/bulge-amp0.8 | iter/wall-capped | 2.0e-03 | 1.8e-02 | 150 | 7 | 745→1045 | 784→1084 | seal [rho] (1.8e-02) | 1.3e+00 |
| W7/plateau/bulge-amp0.8 | stalled | 7.5e-02 | 1.3e-01 | 50 | 120 | 100→3173 | 784→3857 | C2 (1.3e-01) | 2.1e+00 |
| W7/wall/bulge-amp0.8 | iter/wall-capped | 4.1e-01 | 9.1e-02 | 150 | 72 | 745→832 | 784→840 | amb rho-ODE (9.1e-02) | 4.2e+01 |
| C1/plateau/bulge-amp0.8 | stalled | 9.0e-01 | 9.5e-01 | 50 | 85 | 100→3237 | 784→3919 | C2 (9.5e-01) | 1.9e+00 |
| C1/wall/bulge-amp0.8 | stalled | 1.6e-03 | 1.8e-02 | 102 | 89 | 745→3883 | 784→3922 | C1c f_r(seal) (1.8e-02) | 2.0e+00 |
| C2/plateau/bulge-amp0.8 | stalled | 2.5e-01 | 4.7e-01 | 47 | 90 | 100→3220 | 784→3904 | C2 (4.7e-01) | 1.9e+00 |
| C2/wall/bulge-amp0.8 | stalled | 1.3e-03 | 1.4e-02 | 68 | 93 | 745→3883 | 784→3922 | C1c f_r(seal) (1.4e-02) | 1.2e+01 |
| W1/plateau/bulge-amp0.3 | stalled | 3.2e-03 | 1.8e-02 | 48 | 84 | 100→3215 | 784→3896 | C2 (1.8e-02) | 2.0e+08 |
| W1/wall/bulge-amp0.3 | stalled | 2.3e-04 | 8.3e-03 | 72 | 95 | 745→3883 | 784→3922 | C1c f_r(seal) (8.3e-03) | 1.5e+00 |
| W2/plateau/bulge-amp0.3 | stalled | 2.5e-02 | 1.4e-01 | 48 | 84 | 100→3167 | 784→3851 | C2 (1.4e-01) | 1.8e+00 |
| W2/wall/bulge-amp0.3 | stalled | 7.4e-04 | 1.5e-02 | 71 | 95 | 745→3883 | 784→3922 | C1c f_r(seal) (1.5e-02) | 1.4e+02 |
| W3/plateau/bulge-amp0.3 | stalled | 1.9e-03 | 1.2e-02 | 48 | 87 | 100→3187 | 784→3905 | f-PDE (1.2e-02) | 3.6e+06 |
| W3/wall/bulge-amp0.3 | stalled | 7.9e-05 | 4.9e-03 | 119 | 94 | 745→3883 | 784→3922 | C1c f_r(seal) (4.9e-03) | 9.9e-01 |
| W4/plateau/bulge-amp0.3 | stalled | 1.4e-02 | 2.4e-02 | 50 | 93 | 100→3164 | 784→3851 | f-PDE (2.4e-02) | 2.0e+00 |
| W4/wall/bulge-amp0.3 | stalled | 6.0e-05 | 4.2e-03 | 89 | 94 | 745→3883 | 784→3922 | C1c f_r(seal) (4.2e-03) | 1.5e+00 |
| W5/plateau/bulge-amp0.3 | stalled | 4.5e-03 | 1.4e-02 | 51 | 103 | 100→3224 | 784→3878 | f-PDE (1.4e-02) | 4.8e+02 |
| **W5/wall/bulge-amp0.3** | iter/wall-capped | 3.7e-03 | 3.1e-02 | 150 | **0** | 745→813 | 784→852 | C1b (3.1e-02) | 3.7e+01 |
| W6/plateau/bulge-amp0.3 | stalled | 2.9e-02 | 5.3e-02 | 49 | 101 | 100→3140 | 784→3857 | amb phi-ODE (5.3e-02) | 1.6e+01 |
| **W6/wall/bulge-amp0.3** | iter/wall-capped | 2.9e-02 | 5.2e-02 | 150 | **0** | 745→793 | 784→833 | core rho' (5.2e-02) | 4.6e+01 |
| W7/plateau/bulge-amp0.3 | iter/wall-capped | 1.5e-02 | 6.5e-02 | 150 | 22 | 100→388 | 784→1071 | C1c f_r(seal) (6.5e-02) | 3.7e+01 |
| **W7/wall/bulge-amp0.3** | iter/wall-capped | 4.8e-02 | 4.1e-02 | 150 | **0** | 745→772 | 784→811 | f-PDE (4.1e-02) | 6.2e+00 |
| C1/plateau/bulge-amp0.3 | stalled | 1.0e+00 | 1.0e+00 | 48 | 83 | 100→3208 | 784→3886 | C2 (1.0e+00) | 1.9e+00 |
| C1/wall/bulge-amp0.3 | stalled | 2.8e-03 | 2.3e-02 | 48 | 79 | 745→3859 | 784→3898 | C1c f_r(seal) (2.3e-02) | 2.0e+00 |
| C2/plateau/bulge-amp0.3 | stalled | 2.8e-01 | 4.9e-01 | 47 | 87 | 100→3205 | 784→3896 | C2 (4.9e-01) | 2.5e+01 |
| C2/wall/bulge-amp0.3 | stalled | 4.5e-03 | 2.3e-02 | 54 | 90 | 745→3813 | 784→3851 | f-PDE (2.3e-02) | 3.2e+01 |
| W1/plateau/bulge-amp1.5 | stalled | 9.7e-02 | 1.0e-01 | 47 | 91 | 100→3157 | 784→3858 | f-PDE (1.0e-01) | 1.5e+00 |
| W1/wall/bulge-amp1.5 | stalled | 2.3e-04 | 8.4e-03 | 78 | 94 | 745→3883 | 784→3922 | C1c f_r(seal) (8.4e-03) | 1.5e+00 |
| W2/plateau/bulge-amp1.5 | stalled | 6.1e-02 | 8.6e-02 | 47 | 84 | 100→3173 | 784→3865 | C2 (8.6e-02) | 6.0e+15 |
| W2/wall/bulge-amp1.5 | stalled | 7.1e-04 | 1.7e-02 | 70 | 95 | 745→3883 | 784→3922 | C1c f_r(seal) (1.7e-02) | 1.8e+00 |
| W3/plateau/bulge-amp1.5 | stalled | 1.5e-01 | 1.2e-01 | 47 | 95 | 100→3183 | 784→3869 | f-PDE (1.2e-01) | 1.0e+00 |
| W3/wall/bulge-amp1.5 | stalled | 1.9e-04 | 6.0e-03 | 87 | 72 | 745→3207 | 784→3245 | C1c f_r(seal) (6.0e-03) | 1.0e+00 |
| W4/plateau/bulge-amp1.5 | stalled | 8.2e-01 | 2.6e-01 | 47 | 101 | 100→3196 | 784→3904 | f-PDE (2.6e-01) | 1.9e+17 |
| W4/wall/bulge-amp1.5 | stalled | 1.1e-03 | 2.4e-02 | 114 | 87 | 745→3883 | 784→3918 | seal [rho] (2.4e-02) | 3.8e+00 |
| W5/plateau/bulge-amp1.5 | stalled | 1.1e+00 | 9.3e-01 | 63 | 119 | 100→3238 | 784→3922 | f-PDE (9.3e-01) | 2.7e+01 |
| W5/wall/bulge-amp1.5 | iter/wall-capped | 1.5e-01 | 1.9e-01 | 150 | 23 | 745→1376 | 784→1415 | f-PDE (1.9e-01) | 5.7e+00 |
| W6/plateau/bulge-amp1.5 | iter/wall-capped | 8.6e-01 | 4.2e-01 | 150 | 27 | 100→68 | 784→752 | f-PDE (4.2e-01) | 1.1e+03 |
| W6/wall/bulge-amp1.5 | iter/wall-capped | 1.3e+00 | 5.8e-01 | 150 | 22 | 745→1029 | 784→1068 | f-PDE (5.8e-01) | 1.2e+01 |
| W7/plateau/bulge-amp1.5 | iter/wall-capped | 3.3e+00 | 6.1e-01 | 150 | 33 | 100→27 | 784→709 | f-PDE (6.1e-01) | 1.1e+03 |
| W7/wall/bulge-amp1.5 | stalled | 4.6e+00 | 1.0e+00 | 45 | 107 | 745→3810 | 784→3849 | f-PDE (1.0e+00) | 5.7e+00 |
| C1/plateau/bulge-amp1.5 | stalled | 8.2e-01 | 8.9e-01 | 49 | 98 | 100→3215 | 784→3898 | C2 (8.9e-01) | 2.1e+00 |
| C1/wall/bulge-amp1.5 | stalled | 2.0e-03 | 2.4e-02 | 63 | 85 | 745→3820 | 784→3859 | C1c f_r(seal) (2.4e-02) | 2.0e+00 |
| C2/plateau/bulge-amp1.5 | stalled | 2.1e-01 | 4.3e-01 | 47 | 92 | 100→3191 | 784→3874 | C2 (4.3e-01) | 1.9e+00 |
| C2/wall/bulge-amp1.5 | stalled | 1.5e-03 | 1.3e-02 | 60 | 83 | 745→3861 | 784→3899 | C1c f_r(seal) (1.3e-02) | 4.2e+00 |
| W2/plateau/cont-W1 | stalled | 1.8e-03 | 1.1e-02 | 18 | 12 | 3215→3240 | 3896→3922 | C1c f_r(seal) (1.1e-02) | 1.9e+08 |
| W2/wall/cont-W1 | stalled | 1.1e+00 | 1.0e+00 | 1 | 2 | 3883→3883 | 3922→3922 | C2 (1.0e+00) | 1.8e+00 |
| W3/plateau/cont-W1 | stalled | 4.4e-04 | 5.9e-03 | 21 | 9 | 3215→3240 | 3896→3922 | C1c f_r(seal) (5.9e-03) | 2.0e+08 |
| W3/wall/cont-W1 | stalled | 2.9e+00 | 1.7e+00 | 1 | 0 | 3883→3883 | 3922→3922 | C2 (1.7e+00) | 1.7e+00 |
| W4/plateau/cont-W1 | stalled | 1.9e-02 | 3.4e-02 | 22 | 10 | 3215→3240 | 3896→3922 | f-PDE (3.4e-02) | 1.8e+08 |
| W4/wall/cont-W1 | stalled | 6.6e+00 | 2.6e+00 | 1 | 0 | 3883→3883 | 3922→3922 | C2 (2.6e+00) | 2.6e+00 |
| W5/plateau/cont-W1 | stalled | 1.3e-03 | 2.2e-02 | 26 | 9 | 3215→3240 | 3896→3922 | seal [rho] (2.2e-02) | 1.8e+08 |
| W5/wall/cont-W1 | stalled | 9.4e+01 | 9.6e+00 | 1 | 0 | 3883→3883 | 3922→3922 | C2 (9.6e+00) | 9.6e+00 |
| W6/plateau/cont-W1 | stalled | 1.8e-03 | 2.3e-02 | 27 | 9 | 3215→3240 | 3896→3922 | seal [rho] (2.3e-02) | 1.6e+08 |
| W6/wall/cont-W1 | stalled | 1.0e+02 | 9.9e+00 | 1 | 0 | 3883→3883 | 3922→3922 | C2 (9.9e+00) | 9.9e+00 |
| W7/plateau/cont-W1 | stalled | 6.5e-03 | 2.6e-02 | 26 | 9 | 3215→3240 | 3896→3922 | seal [rho] (2.6e-02) | 1.4e+08 |
| W7/wall/cont-W1 | stalled | 1.2e+02 | 1.0e+01 | 1 | 0 | 3883→3883 | 3922→3922 | C2 (1.0e+01) | 1.0e+01 |
| C1/plateau/cont-W1 | stalled | 1.3e-02 | 6.2e-02 | 24 | 13 | 3215→3240 | 3896→3922 | C1c f_r(seal) (6.2e-02) | 1.8e+08 |
| C1/wall/cont-W1 | stalled | 3.2e+00 | 1.8e+00 | 1 | 4 | 3883→3883 | 3922→3922 | C2 (1.8e+00) | 2.0e+00 |
| C2/plateau/cont-W1 | stalled | 1.3e-02 | 2.4e-02 | 22 | 12 | 3215→3240 | 3896→3922 | C1c f_r(seal) (2.4e-02) | 1.8e+08 |
| C2/wall/cont-W1 | stalled | 3.5e+00 | 1.6e+00 | 1 | 3 | 3883→3883 | 3922→3922 | C2 (1.6e+00) | 1.9e+00 |

Notes: (a) Continuation = the brackets-1/2/3 pattern EXACTLY (both W1 donors guard-parked →
`donor_guard_parked: true` on all 16 rows; wall-side rows 1-iteration C2-jump stall, plateau-side
rows descend normally to C1c/seal-[ρ]-held floors). Poisoned-donor mechanism now seen in ALL
FOUR brackets. (b) The inward-collapse curiosity recurs at TWO cells this time: W6 and W7
plateau amp1.5 ran INWARD (r_p 100 → 68 and 100 → 27, residuals 0.42/0.61, not floors) —
bracket 2 had two (W5+W6), bracket 3 one (W6). (c) Plateau-slice small-coupling controls hold C2
as top row with E_ang(seal) unable to reach 2 (C1: 0.98–1.11, C2: 1.51–1.57) — the same
signature in all four brackets. (d) Wall-slice controls here reach E_ang(seal) ≈ 1.997–1.999
(CAN nearly pay U = 2) yet do NOT park — they join the runaway with C1c holding out; this breaks
bracket 3's proposed correlate (§4). (e) TWO wall novelty end states at amp 0.8: W5/wall
(cell phi-ODE 2.6, Φ INCREASED overall, H 1e3 — a bad-basin excursion, deep-φ interior) and
W7/wall (r_p → 832 with ncap 72, ρ_p = 1.0365 — the one wall end state that BREAKS the height
lock in phase 1; its ambient shell narrowed to width 8.1 vs the seed's 39.2).

## 3. Phase-2: flooring (maxit 2000) + the wide-guard / dilation-exponent observation

Best phase-1 config per (cell × slice) re-run at maxit=2000, wall 240 s (18 runs); then ONE
widened-guard run (r_sU < 25·r_s, per-iteration caps unchanged) on the best guard-presser
(W4/wall/amp0.8), CONTINUED once from its own end state (P-E2b4-10, flagged). Gate columns on
END states. dev(seed) = ρ_p − 1.0037706012 (seed shell height); dev(stn) = ρ_p − 1.0036152090
(exact station root).

| run | status | Φ_end | max\|F\| | iters | ncap | r_p → | r_sU → | ρ_p | U(ρ_p) | dev(seed) | dev(stn) | Δφ_float | H_cell_max | q_fold | q_seal | E_ang_seal | top row |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P2/C1/plateau/amp1.5 | stalled | 8.2e-01 | 8.9e-01 | 49 | 98 | →3215 | →3898 | 1.000209 | 2.000003 | −3.6e-03 | −3.4e-03 | 8.04 | 2.1e+00 | 1.07348 | −0.001 | 1.1095 | C2 (8.9e-01) |
| P2/C1/wall/amp0.8 | stalled | 1.6e-03 | 1.8e-02 | 102 | 89 | →3883 | →3922 | 1.003768 | 1.999998 | −2.3e-06 | +1.5e-04 | 8.62 | 2.0e+00 | 1.07184 | 0.029 | 1.9995 | C1c (1.8e-02) |
| P2/C2/plateau/amp1.5 | stalled | 2.1e-01 | 4.3e-01 | 47 | 92 | →3191 | →3874 | 1.001014 | 2.000011 | −2.8e-03 | −2.6e-03 | 7.26 | 1.9e+00 | 1.07433 | −0.041 | 1.5728 | C2 (4.3e-01) |
| P2/C2/wall/amp0.8 | stalled | 1.3e-03 | 1.4e-02 | 68 | 93 | →3883 | →3922 | 1.003771 | 1.999998 | +6.1e-07 | +1.6e-04 | 8.35 | 1.2e+01 | 1.07178 | 0.029 | 1.9997 | C1c (1.4e-02) |
| P2/W1/plateau/amp0.3 | stalled | 3.2e-03 | 1.8e-02 | 48 | 84 | →3215 | →3896 | 0.999946 | 1.999999 | −3.8e-03 | −3.7e-03 | 17.52 | 2.0e+08 | 1.07273 | −0.008 | 1.9817 | C2 (1.8e-02) |
| P2/W1/wall/amp0.3 | stalled | 2.3e-04 | 8.3e-03 | 72 | 95 | →3883 | →3922 | 1.003765 | 1.999998 | −6.0e-06 | +1.5e-04 | 6.04 | 1.5e+00 | 1.07180 | 0.029 | 1.9999 | C1c (8.3e-03) |
| P2/W2/plateau/amp0.3 | stalled | 2.5e-02 | 1.4e-01 | 48 | 84 | →3167 | →3851 | 1.001163 | 2.000011 | −2.6e-03 | −2.5e-03 | 4.37 | 1.8e+00 | 1.07337 | −0.040 | 1.8560 | C2 (1.4e-01) |
| P2/W2/wall/amp1.5 | stalled | 7.1e-04 | 1.7e-02 | 70 | 95 | →3883 | →3922 | 1.003761 | 1.999998 | −9.7e-06 | +1.5e-04 | 2.07 | 1.8e+00 | 1.07179 | 0.029 | 1.9999 | C1c (1.7e-02) |
| P2/W3/plateau/amp0.3 | stalled | 1.9e-03 | 1.2e-02 | 48 | 87 | →3187 | →3905 | 0.984785 | 1.998839 | −1.9e-02 | −1.9e-02 | 14.79 | 3.6e+06 | 1.07154 | 0.044 | 1.9988 | f-PDE (1.2e-02) |
| P2/W3/wall/amp0.3 | stalled | 7.9e-05 | 4.9e-03 | 119 | 94 | →3883 | →3922 | 1.003771 | 1.999998 | +1.5e-07 | +1.6e-04 | 3.63 | 9.9e-01 | 1.07181 | 0.029 | 1.9999 | C1c (4.9e-03) |
| P2/W4/plateau/amp0.3 | stalled | 1.4e-02 | 2.4e-02 | 50 | 93 | →3164 | →3851 | 1.000490 | 2.000006 | −3.3e-03 | −3.1e-03 | 5.39 | 2.0e+00 | 1.07184 | −0.006 | 1.9998 | f-PDE (2.4e-02) |
| P2/W4/wall/amp0.8 | stalled | 5.5e-05 | 3.9e-03 | 84 | 94 | →3883 | →3922 | 1.003758 | 1.999998 | −1.3e-05 | +1.4e-04 | 0.54 | 1.6e+00 | 1.07180 | 0.029 | 2.0000 | C1c (3.9e-03) |
| P2/W5/plateau/amp0.8 | stalled | 3.3e-04 | 8.5e-03 | 88 | 131 | →3238 | →3922 | 1.000669 | 2.000008 | −3.1e-03 | −2.9e-03 | 5.54 | 1.8e+01 | 1.07178 | −0.074 | 2.0015 | f-PDE (8.5e-03) |
| **P2/W5/wall/amp0.3** | iter/wall-capped | 3.2e-03 | 2.9e-02 | 2000 | **0** | →857 | →897 | 1.003774 | 1.999998 | +3.3e-06 | +1.6e-04 | 0.60 | 3.3e+01 | 1.07170 | 0.029 | 2.0005 | C1b (2.9e-02) |
| P2/W6/plateau/amp0.8 | stalled | 9.1e-03 | 4.7e-02 | 113 | 104 | →3238 | →3922 | 1.000376 | 2.000005 | −3.4e-03 | −3.2e-03 | 7.49 | 8.1e+02 | 1.07159 | −0.134 | 2.0014 | f-PDE (4.7e-02) |
| P2/W6/wall/amp0.8 | iter/wall-capped | 9.5e-04 | 1.8e-02 | 2000 | 7 | →1045 | →1085 | 1.003803 | 1.999997 | +3.2e-05 | +1.9e-04 | 1.60 | 1.3e+00 | 1.07183 | 0.029 | 2.0015 | seal [rho] (1.8e-02) |
| P2/W7/plateau/amp0.3 | iter/wall-capped | 5.1e-03 | 3.7e-02 | 2000 | 22 | →792 | →1476 | 0.999986 | 2.000000 | −3.8e-03 | −3.6e-03 | 7.30 | 5.4e+00 | 1.07225 | −0.031 | 2.0085 | C1c (3.7e-02) |
| **P2/W7/wall/amp0.3** | iter/wall-capped | 2.3e-02 | 4.0e-02 | 2000 | **0** | →773 | →812 | 1.003771 | 1.999998 | +6.3e-07 | +1.6e-04 | 1.99 | 6.3e+00 | 1.07163 | 0.029 | 2.0097 | C1c (4.0e-02) |
| P2b-wideguard/W4/wall/amp0.8 | (wide, 2000 it) | 3.4e-05 | 3.1e-03 | 2000 | 112 | →4619 | →4659 | 1.003755 | 1.999998 | −1.5e-05 | +1.4e-04 | 3.07 | 2.0e+00 | 1.07176 | 0.029 | 2.0000 | C1c (3.1e-03) |
| P2b-wideguard-CONT/W4/wall | (wide, +6000 it) | 3.3e-05 | 3.0e-03 | 6000 | 0 | →4654 | →4694 | 1.003755 | 1.999998 | −1.6e-05 | +1.4e-04 | — | 2.0e+00 | 1.07176 | 0.029 | 2.0000 | C1c (3.0e-03) |

**Reading:** (a) NOTHING converges at 2000 iterations — floors at max|F| ~ 3.9e-3 to 0.89, far
above the 1e-8 contract floor. (b) **Wide-guard / dilation exponent — the bracket-4 novelty:**
freed to 25·r_s, the runaway does NOT sprint to the bound (bracket 3: 255 iterations to
24.94·r_s). 2000 iterations reach r_p = 4619 (5.9·r_s), and 6000 FURTHER iterations add only 35
r-units (4619.5 → 4654.4, ~0.006 r-units/iter, ncap = 0 — genuinely small steps, not
cap-limited; Φ 3.39e-5 → 3.30e-5, still falling; not stalled). The outward motion DECELERATES
smoothly with no floor. Comparing the guard-parked parent (r_p 3882.9, max|F| 3.92e-3) to the
wide end state (r_p 4654.4, max|F| 3.04e-3, dilation ×1.199): the C1c residual keeps its SIGN
pattern at every θ-node but NOT its shape — per-node effective exponents run +0.09 (node 2,
barely growing) to −4.64 (node 8), mean −2.29 ± 1.56; on max|F| the effective exponent is
**−1.40**. Contrast
bracket 3: shape preserved node-uniform to ±2% at ×5.04 dilation, exponent −1.0011. **The
pre-registered discrimination comes out NEGATIVE BOTH WAYS: no −1.0, no −1.3 — this bracket has
no self-similar dilation orbit to carry a single exponent.** The exponent series is therefore
−1.31 (A1 Z=8), −0.99 (A1 Z=1), −1.00 (A3 Z=8), NO-CLEAN-EXPONENT/−1.4-class-on-max|F| (A3 Z=1)
— and BOTH candidate correlates from bracket 3 §8 break: U_seal here is the HIGHEST (1.686 —
the U_seal-monotone reading predicted the cleanest −1.0) and wall-admissible N=2 cells are the
MOST numerous (3 — the wall-admissible reading also predicted −1.0). Raw statement for the
verifier: the "dilation exponent" is not a bracket constant; in this bracket it is a property of
where along a decelerating, shape-changing orbit one measures. (c) H_cell is O(1) on every end
state: every falling Φ is a false floor. (d) q_fold reads the banked 1.07155–1.07433 on every
end state (banked 1.0717828); Δφ floats 0.54–17.5 (vs anchor 7.004) — unconstrained, as
expected off-solution. (e) σ cross-checks on representative wall end states (raw, off-solution):
cell max_rel 2.0–8.3, ambient max_rel 8e-4–7.8 — fully off-solution, consistent with H_cell.

## 4. Preserved-vs-tuned: SETTLED. And the parked basin: narrowest, shallowest, not an attractor

**The verdict the brief asked for: on every wall end state of every kind — parked, fast-runaway,
guard-parked, wide-guard (out to r_p = 4654 = 5.9·r_s), and both grid-check states — ρ_p reads
the SEED's shell height 1.0037706 to between 1.5e-7 and 3.2e-5, never the station root
1.0036152 (which sits 1.6e-4 away, ~10–1000× the observed deviations), and U(ρ_p) = 1.999998 <
2 (= U at the seed height, NOT the exact 2.000000 of the root). "Station lock" = SEED-HEIGHT
PRESERVATION under rigid translation, full stop.** This bracket is decisive where brackets 2–3
were merely consistent: there the seed height sat 1e-4 BELOW the station on the U≈2 shoulder
(preserved and tuned were near-degenerate); here the wall seed lies OUTSIDE the station
(r* = 0.948·r_s < 0.95·r_s), the seed height is on the far side with U strictly below 2, and the
lock follows the SEED, not the root. The solver-tuned quantity remains what brackets 1–3 saw:
the C2 row drives E_ang(seal) → U(ρ_p) (1.9995–2.0097 across the wall family). The bracket-2
"self-tuned exactly to the U=2 station" wording is hereby CONFIRMED as owed the regrade bracket
3 flagged (its own retro-check already showed ρ_p = its seed value): three brackets of wall end
states now read seed-height-preserved; zero read station-tuned.

**The parked basin (ncap = 0, finite size) is the NARROWEST of the four brackets:**

- Membership: ONLY the three wall-admissible N=2 κ=1 cells (W5, W6, W7), ONLY at amp 0.3.
  Amp 0.8: W5 excursions into a bad basin (Φ rose, cell phi-ODE 2.6), W6 slow-runs away
  (ncap 7 → r_p 1045), W7 runs to 832 while BREAKING the height lock (ρ_p 1.0365, shell width
  collapses 39.2 → 8.1 — the only lock-breaking wall end state in the matrix). Amp 1.5: all
  three N=2 cells slow-run away (ncap 22–23; W7 amp1.5 breaks height too, ρ_p 1.017). Bracket 2
  broke the lock only at amp 1.5; bracket 3 held it at ALL amps and parked its CONTROLS too;
  here even amp 0.8 unparks. The trend does NOT follow U_seal monotonically (basin width:
  narrow at U_seal 1.409, widest at 0.671, narrowest at 1.686).
- **Bracket 3's proposed correlate BREAKS:** its §8 note predicted a WIDE basin here if
  small-coupling controls can nearly pay E_ang(seal) ≈ 2. They CAN (C1: 1.9995, C2: 1.9997 —
  closer to 2 than bracket 3's 1.991) — and they do NOT park (both controls join the fast
  runaway at every amplitude). Paying the seal price is evidently necessary-not-sufficient for
  parking; whatever selects the parked family among payers is not captured by E_ang(seal) alone
  (raw observation: the three cells that park are exactly the E1 wall-admissible N=2 κ=1
  articles in every bracket that has them — the necessary-map correlate survives where the
  E_ang-payment correlate fails).
- **Parking is NOT an attractor, and here it is not even a creep — it ESCAPES (extended floor,
  4000-iter budget on P2/W5/wall):** restarted from the saved parked state (r_p 857.4, width
  39.224), the LM run left the parked configuration at CAP SPEED — r_p 857.4 → 3524.4 in 35
  iterations (ncap 69), the seed-height lock BREAKING en route (ρ_p → 1.01054, dev(seed)
  +6.8e-3, width → 34.3), then stalled at Φ 1.8e-4 with H_cell_max 3.3. Contrast: bracket 2
  crept steadily, bracket 3 crept deceleratingly (~3e-5 r-units/iter, lock frozen to 7 digits);
  here the same protocol UNPARKS. Within-phase-2 evidence agrees: the ncap = 0 "parked" states
  are still translating fast by bracket-3 standards (W5/wall 745 → 857 over 2000 capless
  iterations ≈ 0.056 r-units/iter, ~2000× bracket 3's terminal creep). The parked family in
  this bracket is a slow WAYPOINT on the runaway, not a quasi-stationary state. H_cell O(1)
  throughout says none of it is near a solution in any case.
- Interior fields on the parked states: deep-φ direction as in bracket 3 (φ_cell −21 (W5
  parked) to −37 (post-escape); ρ_cell up to 4.02) — e^{2φ} UNDERflow direction, CPU/GPU clean.

## 5. Residual anatomy + grid cross-check (artifact controls)

`sweep_E2b_A3Z1_anatomy.py` → `microphysics_E2b_A3Z1_anatomy.json` (21 saved .pt states; CPU
recompute reproduces the GPU max|F| on **19/19 phase-2 states to ≤ 6.2e-12 relative** — the
extended-floor and wide-continuation states also match their GPU JSON values by inspection. No
overflow exception: extreme states run φ deep-negative, as bracket 3's underflow note said).

- **The C1c holdout is the same grid-scale θ-sawtooth as brackets 1–3** — f_r(r_p, θ_k)
  alternates sign node-to-node (P2/W5/wall: [+2.2e-3, −9.6e-4, +7.6e-4, −5.5e-4, +5.5e-4,
  −7.6e-4, +9.6e-4, −2.2e-3] — antisymmetric across the equator, pole-dominant), with u forming
  the seal-hugging boundary layer (u_seal ±0.004–0.029 on the parked state) that buys
  E_ang(seal) ≈ U(ρ_p) but cannot simultaneously flatten f_r. Same object, fourth bracket.
- **Runaway self-similarity FAILS here** (§3b): sign preserved, shape not; per-node exponents
  +0.09…−4.64 under ×1.20 dilation; the orbit decelerates with no cap presses. This is the one
  qualitative anatomy difference from brackets 1–3.
- **Shell rigidity:** wall-seeded runs preserve the seed's 39.221 ambient-shell width to ≤ 1%
  on 20 of 27 bulge rows (runaway AND parked; the wide continuation preserves 39.219 at
  r_p 4654); mild exceptions 1.3–3.3% (W5/amp0.8, C2/amp0.3, W3/W7/C2 amp1.5), W4/wall/amp1.5
  9.3% (35.6), and ONE collapse: W7/wall/amp0.8 → 8.15 (the height-lock breaker). Plateau-seeded runs preserve their 684.4 width loosely (end widths
  654–718, ±5%; even the W7/plateau slow-runner at r_p 792 keeps width 684).
- **Grid cross-check** (`sweep_E2b_A3Z1_gridcheck.py`, Nr=16, Nθ=12, Na=256, maxit 400):
  W1/wall/amp0.8 → same cap-speed runaway to the guard (r_p → 3882.8), same C1c holdout
  (1.1e-2), dev(seed) −1.6e-5; W5/wall/amp0.3 → same parked state (r_p → 771.4, ncap = 0,
  ρ_p = 1.0037706, dev(seed) = +1.8e-7 — the seed height to SEVEN digits at the finer grid),
  floors max|F| 1.8e-2 (seal-[ρ] top at this grid). Both behaviors persist at finer resolution
  — not coarse-grid artifacts.

## 6. Pre-committed failure reading (plan order, solver-first — NO mechanism)

1. **Seeds/coverage:** 3 amplitudes (far-from-rigid included), both slices, 9 window cells
   spanning the necessary-map INCLUDING all three genuine wall-admissible N=2 κ=1 articles and
   two genuine fully-admissible controls, plus (ξ,κ)-continuation both slices: 70 + 18 + 1 + 1
   + 1 + 2 solves. Every trajectory joins one of THREE behaviors: the outward runaway (dominant,
   59/70 to the guard; now known to DECELERATE when freed), the wall-seeded finite-size parking
   (three N=2 κ=1 cells at amp 0.3 only; escapes under extended flooring), or the
   inward-collapse direction at extreme plateau amps (W6, W7; residuals 0.4–0.6, not floors).
   No unexplored basin is indicated by any observed structure.
2. **Grid/conditioning:** trust caps, 2000-iteration floors, the 25·r_s wide guard + 6000-iter
   continuation, a finer grid (Nr 16/Nθ 12/Na 256), and a 4000-iteration extended floor —
   behavior unchanged and CHARACTERIZED: a decelerating, non-self-similar outward drift plus a
   transient parked waypoint, both with O(1) H_cell violations at every point. LM stagnation of
   a system with no attractor in the swept window, not conditioning floors.
3. **Frame-level statement (SCOPED — the LAST of the four brackets; the E2 verdict now goes to
   the blind verifier):** within this bracket's swept window (N ∈ {1,2}, ξ ∈ [0.05,1],
   κ ∈ [0.01,1], both neighborhoods, static concentric L2+L4 cell, a* held), the coupled system
   shows NO finite-size solution. With this bracket the pre-registered E2 sweep is COMPLETE:
   0 convergences in 264 phase-1 solves + all flooring/wide/extended/grid instruments across
   all four brackets (guardrail 1 satisfied — no family/Z dependence in the existence verdict;
   the OBSTRUCTION is family-universal, its ANATOMY varies per bracket as recorded).
   Per the plan the scoped negative ("no static concentric embedded L2+L4 cell in the real
   ambient") may only be banked AFTER the blind verifier passes the whole E2 output; the
   pre-named escape ladder (ω ≠ 0 internal rotation, Charles's φ-angular hunch) remains a
   REFRAME decision with Charles, never a patch.

## 7. Coverage statement

RUN: all 9 window cells × 2 slices × 3 amplitudes (54) + 16 continuation seeds (70 total,
phase 1); 18 flooring re-runs + 1 wide-guard run + 1 wide-guard continuation (phase 2); 1
extended-floor run (4000-iter budget) on the parked W5/wall state; 2 grid cross-checks; anatomy
on all 21 saved states. THROUGHPUT-LIMITED REMAINDER: NONE — the full pre-registered matrix ran
(total compute ≈ 12 min of the ~90-min budget). NOT swept (out of contract scope, for the
record): N ≥ 3; ξ > 1.9 (ξN < 2 enforced); κ > 1; anchor_mode='exact' (unwired branch, needs
Charles's ruling); off-center cells (E1 scope); ω ≠ 0.

## 8. Notes for the E2 verdict stage / blind verifier (no bracket 5)

- **Four-bracket uniformities (what the verifier should find in every bracket):** zero
  convergence (0/264 phase-1 + all instruments); C1c f_r(seal) as the leading holdout row
  (38/62, 25/62, 34/62, 21/70) with the same equator-antisymmetric pole-dominant θ-sawtooth
  anatomy; outward drift of the whole composite from every seed class; wall end states
  preserving the SEED's shell-relative height (ρ_p = ρ_seed(0.95·r_s) to 1e-5..1e-7 — brackets
  2, 3, 4 measured directly; bracket 2 retro-checked) with C2/E_ang(seal) self-tuning to U(ρ_p);
  wall-seeded shell width preserved under translation; H_cell O(1)-or-worse on every end state
  (all Φ floors are false floors); the poisoned-donor 1-iteration continuation stall; plateau
  small-coupling controls unable to pay E_ang(seal) = 2 with C2 as their holdout; parking (where
  present) never an attractor.
- **Four-bracket variations (what varies and how, raw):** (i) dilation-orbit character — clean
  self-similar with exponents −1.31 / −0.99 / −1.00 in brackets 1–3 vs NON-self-similar,
  decelerating, −1.4-class-on-max|F| here; BOTH bracket-3 correlate candidates (U_seal
  monotone; wall-admissible-cells-present) are broken by bracket 4 — the exponent question
  dissolves rather than resolves. (ii) parked-basin width — none (A1 Z=8, no wall-admissible
  cells) / N=2-only, amps ≤ 0.8 (A1 Z=1) / WIDE incl. controls + W1, all amps (A3 Z=8) /
  N=2-only, amp 0.3 only (A3 Z=1); the E1 wall-admissible N=2 κ≈1 cells are the parking family
  wherever parking exists — the necessary-map correlate SURVIVES all four brackets. (iii)
  extended-floor fate of the parked state — steady creep (b2) / decelerating creep (b3) /
  cap-speed ESCAPE with lock breakage (b4). (iv) extreme-state φ direction — positive/overflow
  (A1 Z=1) vs deep-negative/underflow (both A3 brackets); CPU/GPU mismatch only ever on the
  overflow direction.
- **The bracket-2 regrade is now OWED formally:** its "ρ_p self-tuned exactly to the U=2
  station" line should be regraded to "seed shell height preserved (≈ station by coincidence of
  the 0.95·r_s seed sitting on the U≈2 shoulder)" — bracket 4's outside-the-station geometry is
  the discriminating measurement (dev(seed) ≤ 3e-5 everywhere; dev(station) = +1.5e-4 uniform;
  U(ρ_p) < 2). The .pt states for all brackets exist for the verifier to recompute.
- **Protocol caveat to carry:** bracket 4's exponent numbers are NOT protocol-comparable to
  brackets 1–3 (×1.20 available dilation vs ×5; decelerating orbit vs cap-speed sprint;
  shape-changing vs shape-preserved residual). The comparable statement is "no self-similar
  orbit exists in A3 Z=1", not "the exponent is −1.4".
- The wide-guard continuation (P-E2b4-10) is the one addition beyond the bracket-3 protocol —
  same run, iteration budget extended, no knob changed; flagged for the verifier.

## Files

- `sweep_E2b_A3Z1.py` (phase 1) / `sweep_E2b_A3Z1_phase2.py` / `sweep_E2b_A3Z1_extfloor.py` /
  `sweep_E2b_A3Z1_gridcheck.py` / `sweep_E2b_A3Z1_anatomy.py` (all adapted from the bracket-3
  scripts); log `sweep_E2b_A3Z1.log`; the wide-guard continuation script ran from the session
  scratchpad (its full parameters are in P-E2b4-10 and its output JSON below).
- `microphysics_E2b_A3Z1_results.json` (70 runs, full diagnostics + gates + ρ_p/U(ρ_p)/
  dev-from-seed/dev-from-station per run); `microphysics_E2b_A3Z1_phase2.json` (19);
  `microphysics_E2b_A3Z1_extfloor.json` (1); `microphysics_E2b_A3Z1_wideguard_cont.json` (1);
  `microphysics_E2b_A3Z1_gridcheck.json` (2); `microphysics_E2b_A3Z1_anatomy.json` (21).
- Saved fields (recompute-on-saved): `E2b_A3Z1_P2_*.pt` (18), `E2b_A3Z1_P2b_wideguard_W4_wall.pt`,
  `E2b_A3Z1_P2b_wideguard_CONT_W4_wall.pt`, `E2b_A3Z1_P2c_extended_W5_wall.pt` (21 total).
- NOT committed (per brief); blind verifier pass owed on the WHOLE E2 output (all four brackets)
  before any banking.
