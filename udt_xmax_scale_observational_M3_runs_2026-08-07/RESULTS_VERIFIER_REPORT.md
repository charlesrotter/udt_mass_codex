# M3 BLIND RESULTS-VERIFIER REPORT (2026-08-08)

Fresh-context adversarial pass per prereg §8 + the directed GPU-amendment re-adjudication.
Verifier: blind results-verifier agent (no stake in the runs). Incremental appends.

## Item 1 — DIRECTED RE-ADJUDICATION: amended-v2 GPU-audit criterion

Independent load of `spotcheck_BGS_DR_full.npz` (float64, shape 24x24x40 = 23,040 cells):

| Claim (diagnosis note) | Independently measured | Match |
|---|---|---|
| max per-cell rel diff 2.3e-9 | 2.3023e-9 | YES |
| total rel diff 4.2e-10 | 4.1932e-10 | YES |
| all 22,020 cells <=1e8 counts agree to <=2.4e-2 | n=22,020; max small-cell diff 0.02419 | YES |
| zero small-cell whole-pair diffs (>0.5) | 0 | YES |
| every diff>0.5 cell has >=3.8e8 counts | min cpu among the 171 such cells = 3.817e8 | YES |
| diffs magnitude-proportional (fp signature) | corr(log cpu, log diff) = 0.984 over 5,309 nonzero-diff cells | YES |

(a) READING JUDGED SOUND. The magnitude-proportionality (corr 0.98; log-log slope ~2.2,
between sqrt-accumulation and worst-case linear growth) is the floating-point
accumulation-order signature; a misassigned pair would produce magnitude-INDEPENDENT O(1)
paired jumps, and the small-cell census (22,020/23,040 cells, sensitivity 20-50x below one
pair) shows zero. A real binning-logic bug would not confine itself to the ~1,000 largest
cells — small cells exercise the same code path across all theta bins and regions.

(b) ADVERSARIAL MASKING HUNT — three findings, none fatal:
1. A constant multiplicative bias WOULD pass the per-cell relative bound — but it is capped
   by the total-sum check at <=1e-9, seven orders below the ~1e-2 jackknife errors. Cannot
   hide at a level that matters. (Measured: weighted signed bias -4.2e-10.)
2. NOTED, not previously stated: the total-sum check does NOT detect misassignment
   (misassignment conserves the total); it detects lost/duplicated pairs and bias. The
   checks are complementary: census (b) = misassignment detector; total (c) = loss/bias
   detector; per-cell (a) = gross catch-all. A few LOST pairs on >1e8-count cells are
   invisible to all three — this matches the honestly-stated sensitivity limit.
3. Sign asymmetry observed: 3,868 cells gpu>cpu vs 1,441 gpu<cpu (net -191 counts on
   4.6e11). A systematic rounding drift between backends at ~1e-10 relative amplitude —
   consistent with atomics-vs-tree accumulation, bounded by the total check. Not a pair
   signature.
   CAVEAT recorded: the v2 numeric bounds (1e-8 per-cell, 1e-9 total) are set 2-4x above
   the measured values — data-chased as thresholds. The criterion retains teeth ONLY
   because check (b), the small-cell whole-pair census, is an absolute (not recalibrated)
   detector. Any future recalibration of (b) should be treated as a red flag.

(c) STOP-TWICE HONESTY: `bao_run_log.txt` shows exactly TWO RuntimeError STOP firings
(v0 bound at code line 211; v1 bound at line 229), both on BGS_BRIGHT NGC 0.21-0.26 DR,
then completion under v2 — matching the disclosure (v1 firing + v1's own total-sum
miscalibration both admitted in GPU_SPOTCHECK_DIAGNOSIS.md and the commit messages).
Checkpointed science counts predate the STOPs (timestamps: checkpoints Aug 7, caches
Aug 8) — the counts feeding physics were untouched by the recalibrations.

Spot-check records in both results jsons: the other five (shell,count) audits computed
fresh (cached=False in sys assembly) with margins 2-5 orders INSIDE the bounds
(mrel 1.8e-12..2.1e-10) — only the heaviest cell-count audit (BGS DR, 8.8M randoms)
approaches the bound, as the accumulation-noise model predicts.

**VERDICT Item 1: AMENDMENT-SUSTAINED** (with the recorded caveat on data-chased numeric
bounds; the census check is the load-bearing detector and must not be weakened in future).

## Item 2 — SNe full re-run + attacks

Full re-run of all 18 fits (modes A/B/C/D x P1/P2/P3) from the committed code + on-disk
Pantheon+ data, ~16 s: **every chi2, shape, offset, shape-interval, and X_eff interval
reproduces with zero relative difference** vs sne_results.json / SNE_RESULTS.md. Headline
shifts reproduce exactly (C-A P1 = 0.004384; D zHD = 0.019822; D zHEL = 0.000204).

(a) P2/P3 CATASTROPHE IS REAL, NOT A FITTER FAILURE.
- P2 has NO optimizer at all: its chi2 (4412.17) is a closed-form profiled-offset
  quadratic (Cholesky linear algebra) — convergence failure is structurally impossible.
  Independently recomputed: 4412.169. The P1-vs-P2 separation is Delta-chi2 ~ 3151.
- P3: independent 100-point geometric scan of chi2(inv_alpha) over the full frozen bounds
  [1e-4, 40] is monotone increasing away from the lower bound — the best fit at the grid
  edge 1e-4 IS the global minimum, i.e. P3 runs to its P2 limit (chi2 4412.90 -> 4412.17
  as inv_alpha -> 0; the 0.73 residual is the finite-1e-4 distance from the limit). The
  interval is honestly flagged lo_open=True (one-sided), and the .md marks it.
- P1: independent 161-point scan over the full bounds + bounded refinement confirms the
  global minimum at inv_n = 0.94703, chi2 = 1260.848 — no missed basin.

(b) THE HONEST n=1 EXCLUSION (computed exactly, inv_n frozen at 1, offset profiled):
- Mode A/zCMB: Delta-chi2 = 7.94 -> **2.82 sigma** (1 dof).
- Mode D/zHD:  Delta-chi2 = 15.16 -> 3.89 sigma.
- Mode D/zHEL: Delta-chi2 = 7.98 -> 2.83 sigma.
CORRECTION TO A BRIEF/README FRAMING RISK: the zHD shift (inv_n 0.947 -> 0.927) moves
AWAY from inv_n = 1, so the flow-correction sensitivity does NOT erode the n=1 exclusion
— it strengthens it. The honest summary: **n=1 (the banked L member) is disfavored at
~2.8 sigma in the primary mode, robust-or-strengthened under both z-column swaps.** This
is a statistical statement under the frozen menu + diagonal-of-cov caveats; 2.8 sigma is
suggestive, not decisive — any write-up language stronger than that would be F-STEER.

(c) ANCHOR PROPAGATION VERIFIED: offset interval half-widths (0.00810, 0.00811 mag)
combined in quadrature with the frozen M_B err 0.027 and translated 10^((B-25-M_B)/5)
independently reproduce X_eff = 2086.0 [2059.1, 2113.2] Mpc exactly. Note the anchor
term DOMINATES the interval (0.027 vs 0.008 stat) — the F-ANCHOR premise carries ~3.3x
the statistical weight; correctly tagged everywhere.

(d) COV/CUTS PER PREREG: cut z > 0.023 applied on the MODE'S z column (verified in
load_mode_data: mask built from tab[zcol]); calibrators (IS_CALIBRATOR==1) excluded from
every fit vector including mode B (anchoring is via the external M_B only); cov subset by
np.ix_ on the same mask (A/B/D); mode C diagonal-only by frozen design; cov symmetrized
against text round-off. n_data/ndof arithmetic consistent across all 18 fits.

**VERDICT Item 2 (SNe leg): SUSTAINED** — all numbers reproduce; the two attacks fail;
one framing correction owed (zHD strengthens, not erodes, the n=1 statement).

## Item 3 — BAO spot-recompute + assembly reproduction

ASSEMBLY-LEVEL (all 52 shells x 2 variants, from checkpointed w/sig, committed
look_elsewhere.py, seed 20260807): the ENTIRE look-elsewhere block reproduces
bit-identically for BOTH variants — every local max-dchi2, every local p, global max
(44.420049 sys / 41.674504 nosys), global p (0.0 = <1/300 both), joint stat
(235.2494 sys / 226.2547 nosys, p 0.0 all three profiles), and the joint best-combo
parameters including the instability itself: sys (P1, shape 1.00767, s_rad 0.030885) vs
nosys (P1, shape 5.0 = SHAPE_GRID edge, s_rad 0.009136). The .md's Headline 3 parameter
table is exact, and the "no BAO-alone X-range" consequence follows.

RAW-CATALOG END-TO-END (committed pipeline, from the DESI FITS catalogs):
- Strong shell LRG 1.00-1.05 sys: DD/DR/RR pair counts, w(theta), sig ALL bit-identical
  to the checkpoint (max rel diff 0.0); bump (dchi2 45.9624, theta_b 2.4383, sigma_b
  0.2521, A_b 0.01532), local_p 0.0, null 95th 10.4839, trigger True — all exact.
- Null shell ELG_LOPnotqso 1.20-1.25 sys: DD/DR/RR, w, sig ALL bit-identical to the
  checkpoint (max rel diff 0.0); bump (dchi2 1.5489, theta_b 0.3901), local_p 0.9967,
  null 95th 9.5456, trigger False — all exact. A genuine null shell, correctly non-
  triggering.

Both raw-catalog recomputes (one strong, one null; ~350 s and ~1137 s pair counting)
reproduce the pipeline exactly from the DESI FITS catalogs — the committed counts, w,
and per-shell statistics are faithful, and the deterministic seeds reproduce.

Checkpoint census: 104 shell-variant npz+json pairs on disk, matching 52 shells x 2
variants; dropped-shell list = the 6 high-z QSO shells (floor), matching the commit.
M2 validator suites re-run: 38/38 pass.

## Item 4 — Prereg conformance + language scan (both legs)

FROZEN-CHOICE AUDIT (all honored):
- SNe: z>0.023 on the mode's z column; calibrators out; STAT+SYS cov subset (A/B/D);
  mode C diagonal by design; anchor -19.253+/-0.027 as frozen; no post-hoc menu change.
- BAO: theta window 0.3-12 deg / 40 log bins; SHELL_DZ per tracer; 5e4 weighted floor
  (52 kept + 6 high-z QSO dropped — census json matches the commit claim); NX/WEIGHT_FKP
  blacklist + `_rec` path refusal live in the loader; 4-file split-RR; sys/nosys both run;
  300 null mocks; global threshold 0.01; SHAPE_GRID [0.05,5]x24 (the nosys joint edge hit
  at 5.0 is honestly called grid-edge in the .md).
- ORDER VERIFIED FROM GIT: SNe results committed a40127cc 2026-08-07 10:58; earliest BAO
  checkpoint 11:15 the same day; SNE_RESULTS.md/sne_results.json have exactly ONE commit,
  never touched after BAO unblinding. Post-unblinding diffs to m3_run_bao.py (dbc81989,
  c2ea7f5e) touch ONLY the gpu_spot_check criterion + caching — no science path.
- F-PEEK/guard: authorize_m3 tied to prereg hash in both runners; dry-runs never flip.

F-SHOP: one deviation found, honestly disclosed, not a shop: the RADIAL LEG triggered
(9 shells sys / 8 nosys — the .md says "9 shells", minor imprecision) but the estimator
was never built, so the frozen "attempt-only" attempt DID NOT HAPPEN. This is a
contract gap carried openly as OWED; it contaminates nothing else. No other post-hoc
choice found.

F-STEER / the consistency observation ("stated, not fitted") — independently quantified:
implied ell across the 2.3-2.4 deg thread (SNe P1 curve, R_w=2202.6, inv_n=0.947) =
58.7 / 63.9 / 69.1 Mpc at z 0.725/0.925/1.025 — a ~16% spread. At the 9.7%-wide bin
resolution the thread IS near a constant-ell curve, but the observed drift DIRECTION
(theta rising with z) is OPPOSITE to the predicted gentle fall (ell=65: 2.63->2.29 deg)
by ~1-1.5 bins. "Sits near" is fair at current resolution; the drift direction is NOT
confirmed — recommend that one clause travel with the observation so it cannot be
over-read. Outliers: implied ell 245.6 / 33.7 / 23.7 Mpc — the .md's "factors 2-3 off"
slightly understates the 8.8-deg shell (3.8x). Both directions are reported; temperature
is even; no reconciliation was attempted (F-STEER held).

F-ANCHOR: every absolute number in both .md files carries the M_B premise. F-SCOPE: no
"the value of x_max", no M_total; the .md explicitly declines a BAO-alone X-range on the
variant-instability ground (F-SCOPE honored against self-interest). "Feature detected"
used only via the frozen global-p<0.01 criterion; p=0.0 floored as <1/300 at the top of
BAO_RESULTS.md and in the caveat line. The 70.7-deg LRG 0.75-0.80 nominal center (outside
the 12-deg window; local p 0.053) and the radial gap are both carried openly.

STRUCTURAL NOTE (carried caveat, prominence check): the look-elsewhere null mocks are
DIAGONAL Gaussian draws (look_elsewhere.py), so all three significances inherit the
diagonal-jackknife-covariance approximation; correlated bins would inflate apparent
dchi2 vs this null. The caveat is attached to every significance as the M2 verifier
required — but the detection headline's strength rides on it, and the .md's caveat line
says it plainly. Conformant; flagged for M3b (a correlated-null cross-check would
materially harden or soften Headline 1).

Look-elsewhere internal consistency verified: observed and mock statistics go through
the SAME GLS machinery (the per-shell checkpoint dchi2 46.0 for LRG 1.00-1.05 vs the
LE-table 44.42 is a different-statistic pair — detect_bump refine vs bin-center grid —
each self-consistently calibrated against its own null; no apples-to-oranges p).

## FINAL VERDICTS

**Item 1 (GPU-audit amendment): AMENDMENT-SUSTAINED.** The npz-backed diagnosis
reproduces exactly; the accumulation-order reading is sound; the misassignment-census
check (b) is a genuine absolute detector that a multiplicative bias, a lost-pair, or a
binning bug cannot all evade simultaneously; the two STOP firings and both of the
author's own miscalibrations are honestly disclosed in the diagnosis note + commit
messages, and the science counts predate every recalibration. CAVEAT owed: the numeric
bounds (1e-8, 1e-9) are set 2-4x above the measured values (data-chased); teeth reside
in the census check, which must not be weakened in any future recalibration.

**SNe leg: SUSTAINED.** All 18 fits reproduce with zero relative difference. The P2/P3
chi2 catastrophe is structural (P2 closed-form; P3 monotone to its P2 limit at the grid
edge, honestly flagged one-sided), not a fitter failure. P1 global minimum confirmed.

**BAO leg: SUSTAINED.** Two raw-catalog shells (strong + null) and the full 52x2
look-elsewhere assembly reproduce bit-identically; the detection headline, the
weight-robust theta(z) table, the variant-instability of the single-ruler fit, and the
"no BAO-alone X-range" consequence all hold; the consistency observation is fairly
labeled stated-not-fitted.

### Amendments owed (none blocking; all HONESTY-class, not MERIT)
1. n=1 exclusion: quote it as **~2.8 sigma (Delta-chi2 7.9)** in mode A/zCMB, and note
   the zHD swap STRENGTHENS it to 3.9 sigma (does NOT erode) — the current commit-message
   phrasing ("sits just outside the Delta-chi2=1 interval") understates and slightly
   mis-frames the flow-correction direction.
2. Consistency observation: carry the clause that the observed theta-vs-z drift DIRECTION
   is opposite the predicted gentle fall (~1-1.5 bins) so "sits near the SNe curve" cannot
   be over-read as a confirmed thread; and correct "factors 2-3 off" -> up to 3.8x for the
   8.8-deg outlier.
3. Radial count: the .md says "9 shells triggered" but nosys triggers 8 (sys 9); state
   per-variant. The radial estimator was never built — carried as OWED; honest gap.
4. GPU-audit numeric bounds are data-chased above measured values (Item 1 caveat).

None of these change any banked outcome. All are provenance/honesty refinements; no
MERIT judgment was applied (per the governing limit).
