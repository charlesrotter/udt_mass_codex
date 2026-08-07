# V-BAO build notes (D3, M2, 2026-08-07)

Binding: PREREGISTRATION.md sections 1, 4, 6; D1_FORMULAS.md 'FOR THE BUILDERS'.
Files: `v_bao.py` (pipeline), `synth_bao.py` (synthetic gates), `test_v_bao.py`
(purity + correctness tests, 16 passing), `m1_spot_verify.py` (+ outputs in
`vbao_outputs/`, quarantined smoke in `smoke_outputs/`). Nothing committed to git
(per dispatch); no real-data verdict number exists anywhere in these outputs.

## 1. M1 spot-verify (F-PEEK-legal: schema/rowcount/z-range/dN/dz only)

All load-bearing M1 recon claims verified EXACTLY against the on-disk files
(`vbao_outputs/m1_spot_verify.json`):

- Row counts match M1's table to the row for all 8 (tracer, cap) data catalogs
  (e.g. BGS_BRIGHT NGC 2,909,876; QSO SGC 430,172). BGS NGC ran_0 = 13,248,857.
- z ranges match (BGS 0.010-0.500, LRG 0.400-1.100, ELG 0.800-1.600,
  QSO 0.800-3.500; QSO SGC max 3.4999).
- Columns RA/DEC/Z, WEIGHT_COMP, WEIGHT_ZFAIL, WEIGHT_SYS present in every data
  AND randoms file. NX and WEIGHT_FKP present-but-avoidable (they exist, we
  never read them). NO `_rec` file anywhere in the directory.
- dN/dz histograms (50 bins per tracer/cap) saved in the JSON.
- NO failed claim.

## 2. What was built (frozen choices restated)

`v_bao.py`:
- **Loader** (`load_columns`/`load_catalog`): the PIPELINE's only read path
  (A6 precision: the blacklist wire covers `load_columns`, the sole path that
  can feed the estimator; the two schema-class scripts `m1_spot_verify.py`
  and `estimate_full_cost` open catalogs directly via astropy with hardcoded
  schema-legal columns — verifier-checked, no leak); column whitelist
  = RA/DEC/Z/WEIGHT_COMP/WEIGHT_ZFAIL/WEIGHT_SYS; blacklist NX/WEIGHT_FKP and
  any `_rec` path enforced BEFORE any I/O (machine-tested: violation raises on a
  nonexistent path, proving no file is touched). Weight = product of the native
  completeness weights; `use_sys=False` variant implements M1's over-correction
  caveat test. Returns tag='real'.
- **Shells** (frozen): dz = 0.05 (BGS/LRG/ELG), 0.15 (QSO) over the M1 ranges;
  floor 5e4 weighted galaxies; dropped shells returned explicitly (no silent
  caps). Gridding convention: edges anchored at z_lo; the last BGS shell
  (0.46-0.51) is truncated by the catalog cut at 0.50 - reported, not hidden.
- **Estimator**: Landy-Szalay w(theta) per shell/cap, native weights in the
  weighted pair products; theta in [0.3, 12] deg, 40 log bins (frozen). Pair
  counting is CPU-exact: cKDTree.count_neighbors (dual-tree) on unit-sphere
  3-vectors, chord = 2 sin(theta/2), weighted, cumulative-then-diff.
  Normalizations: ordered-pair nDD = W_D^2 - sum(w^2) etc.; self-pairs excluded
  automatically by theta_min > 0.
- **Jackknife** (frozen: angular, 24 regions = 3 weighted-dec bands x 8 RA
  slices, boundaries from the randoms): pair counts are REGION-BLOCKED
  (24x24 block matrices), so all 24 leave-one-out samples are exact re-sums at
  ~no extra pair cost. Validated on synthetic (gate JK below).
- **M2 guard** (F-PEEK wire): `ls_w_theta` raises `M2GuardViolation` on any
  tag='real' catalog while `M3_REAL_RUN_AUTHORIZED = False` (flipped only by
  the M3 prereg). Smoke mode: `make_smoke` caps at 2e4 gal / 4e4 randoms
  (frozen) and `run_smoke_shell` writes ONLY to `smoke_outputs/` with a
  DO-NOT-INTERPRET header, persisting timing/row-count/feasibility fields
  ONLY — w(theta)/sigma values are computed transiently and never stored
  (A3). Corrected noise claim (A3, verifier-measured): at the smoke
  subsample the per-bin jackknife sigma at 1.5-8 deg is 0.0037-0.012 vs a
  realistic bump amplitude ~0.002-0.005 — a factor ~1-6 per bin (NOT the
  ~10x originally claimed), total bump S/N <~ 1.5: still unresolvable, so
  no steer is possible, but the margin is thinner than first stated.
- **Bump machinery** (frozen): null = cubic in ln(theta); alt = null + Gaussian
  in ln(theta) (center theta_b, width sigma_b, amplitude free, either sign);
  search = ALL 40 bin centers x width grid {0.10,0.20,0.35,0.60} over the FULL
  window (F-STEER: no seeded center) + Nelder-Mead refine (width clamped to
  [0.03,1.5]). Trials: null-mock calibration - M realizations of N(0, sigma^2),
  same full-window grid search, max-dchi2 distribution (vectorized via
  projection quadratic forms; machine-tested identical to the grid search).
  Conditioning statement: chi^2 uses DIAGONAL jackknife variances - the
  24-region jackknife covariance of 40 bins is rank <= 23 (not invertible);
  the null-mock calibration uses the SAME diagonal, so the trials-corrected
  significance is self-consistent. Carried honestly: residual bin-bin
  correlations are not modeled at M2; M3 review point.
- **UDT joint shape fit**: theta_BAO(z) = ell/r(z) per D1; (X_eff, shape)
  coordinates with g(shape, L): P1 (-expm1(-2sL))/s, P2 2L, P3 expm1(2sL)/s;
  the identified combination is s = ell/X_eff (ell and X_eff are exactly
  degenerate in theta alone - reported as s, F-SCOPE-honest). s is linear at
  fixed shape (closed-form); shape from a 24-point geometric grid on [0.05, 5]
  that contains NEITHER 1/n=1 nor 1/alpha=0.5 (F-STEER machine test) + bounded
  scalar refine; profile-likelihood intervals on s (dchi2 <= 1 and <= 4).

## 3. Synthetic gate results (all PASS; `vbao_outputs/synth_gate_results.json`)

- **Gate JK** (jackknife validation): median(jk sigma / empirical scatter over
  8 independent uniform mocks) = 1.22 - mildly conservative, in band [0.6,1.8].
- **Gate A** (bump injection into w(theta) vectors; noise at the
  jackknife-estimated level from synthetic, scaled to the 6e4-per-shell
  regime): threshold = 95th pct of null max-dchi2 = 10.5; detection rate
  60/60; 98.3% of centers within 25%; median recovered theta_b = 1.98 deg
  (true 2.0), sigma_b = 0.248 (true 0.25); false-positive rate on 200
  independent null mocks = 6.5% vs 5% expected (inside the 3-sigma binomial
  band). PASS.
- **Gate B** (end-to-end mini-mock, 1.2e5 points): pair-splitting catalog,
  truth = P1 with n=1.6 (arbitrary validation truth; NOT n=1 - F-STEER),
  s_truth = ell_inj/X_eff = 0.05 rad = 2.8648 deg; two frozen LRG shells
  (0.40-0.45, 0.45-0.50; 6e4 each; 12 empty shells correctly reported
  dropped); randoms 2x with shuffled z. Both shells detected at
  trials-corrected p < 1/300 (dchi2 = 86.6, 76.9), centers 4.909/4.572 deg vs
  injected 5.005/4.653 deg (within 2%, inside the 15% gate). Joint fit
  (truth profile): s_best = 2.754, 1-sigma [2.34, 3.24], 2-sigma [1.90, 3.47]
  - covers s_truth (gated at 2-sigma, stated). P2/P3 fits reported alongside
  (chi2 2.3/2.4 vs 0.0): two close shells cannot discriminate profiles -
  expected and honest; the M3 leverage is the full z range. PASS.

## 4. Mock-design finding (first iteration, documented)

The first gate-B mock used a 1160 deg^2 patch and DROPPED companions falling
outside it. That imprints a real density gradient in the data that the uniform
randoms do not share => a broad spurious w ~ 0.007 at all theta swamping the
ring, plus jackknife regions (~48 deg^2) comparable to the 5-deg scale inflate
sigma. This is a MOCK artifact, not a pipeline flaw (real DESI randoms share
the data's footprint selection, so no such mismatch exists there). Fix: the
gate-B mock runs on the FULL SPHERE (edge-free; no dropping; companion
fraction 0.25). Two real-data cautions extracted for M3: (i) at theta ~ 5-12
deg the 24-region jackknife regions on a per-cap footprint are not much larger
than the scale - jackknife errors at the largest bins may be unreliable;
(ii) any data/randoms selection mismatch mimics broad w power.

## 5. M3 full-run cost estimate (honest; `vbao_outputs/m3_cost_estimate.json`)

Measured throughput (this CPU, region-blocked weighted dual-tree, patch-density
regime): ~2.5e8 pairs/s; estimate uses 2e8 conservatively. Footprints measured
from occupied 1-deg cells (schema-level read). With randoms = 1 file (~4x data):

- Kept shells (floor applied PER CAP, unweighted proxy): 62. Total ~ 3.2 CPU-hr
  (BGS NGC 1.7 hr worst tracer; worst single shell BGS NGC z 0.16-0.21,
  N=532k, ~25 min). Jackknife adds ~nothing (region-blocked). Bump + trials
  machinery: seconds per shell. NOT prohibitive: a full M3 pass is < half a day
  single-core, embarrassingly parallel over shells if needed.
- Using all 4 random files (~18x data) scales RR by ~20x => roughly 40-60
  CPU-hr. Proposed bounded default for the M3 gate: 1 random file for all
  shells + a spot-check shell with 4 files to quantify the RR-noise cost.
- FLAG for the M3 gate (prereg interpretation point, not decided here): the
  5e4 floor applied per (tracer, cap, shell) drops ALL ELG SGC and QSO SGC
  shells and half the QSO NGC shells; applied per tracer (caps combined) they
  survive. `bin_shells` supports either (it bins whatever catalog it is
  given); the choice belongs to Charles's M3 gate.

## 6. Purity statement

- **F-IMPORT-LCDM (machine-wired)**: NX/WEIGHT_FKP unreturnable and `_rec`
  unopenable through the pipeline's read path (`load_columns`; A6: the two
  schema-class scripts read directly, hardcoded legal columns); tests prove the
  violation fires BEFORE I/O. No acoustic scale, no r_d, no comoving distance,
  no fiducial cosmology, no template anywhere in the module: the only
  geometry is theta = ell/r(z) from the frozen native menu.
- **F-PEEK ledger (every real-data touch this build made)**:
  1. `m1_spot_verify.py` - schema, row counts, z min/max, dN/dz histograms
     (legal class).
  2. `estimate_full_cost` - RA/DEC/Z reads for footprint area + per-shell
     counts (schema-level, legal class).
  3. `run_smoke_shell('LRG','NGC',0.60,0.65)` - I/O feasibility: full-shell
     load (116,653 gal + 752,933 ran0 rows, 0.7 s), then LS on the frozen
     2e4/4e4 smoke subsample (2.4 s), output quarantined in `smoke_outputs/`
     with the DO-NOT-INTERPRET header; the bump machinery was NOT run on it;
     no number from it is cited anywhere. A3: the w(theta)/sigma vectors
     initially stored there were REDACTED post-verifier (redaction noted in
     the file); only timing/row-count/feasibility fields remain.
  No real-data w(theta) at analysis scale, no bump statistic, no fit, no
  verdict number exists in any output of this build.
- **F-STEER**: no LCDM center seeding anywhere - the bump search window is the
  full theta range; the shape grid excludes n=1 and alpha=2; validation truth
  n=1.6 is arbitrary and documented as such; owner hypotheses appear nowhere.
- **F-SHOP**: all thresholds/bins/windows above restate the prereg freeze; the
  two open interpretation points found (per-cap vs per-tracer floor; randoms
  depth) are flagged for the M3 gate, not resolved unilaterally.
- **F-LEGACY**: everything written fresh this session; no archived code.

## 7. Verdict (D3 leg)

V-BAO leg: **M2-BUILT candidate** - synthetic gates all PASS, purity harness
green (16/16 tests), M1 spot-verify clean, M3 cost feasible. Awaits the blind
adversarial verifier pass (prereg section 8) before M2 is recorded.

## 8. AMENDMENTS-APPLIED (verifier CLEAN-AMENDED, 2026-08-07; V-BAO leg)

- **A1**: added `test_weight_sensitivity_duplication_identity` (position-dependent
  weights; w=2-vs-duplicated-point exact identity on binned counts). Catch-proof:
  the verifier's mutation (weight product dropped from `pair_count_blocks`) was
  temporarily applied — the new test FAILED; exact restore verified; full suite
  18/18 passes.
- **A3**: real w(theta)/sigma vectors REDACTED from
  `smoke_outputs/smoke_LRG_NGC_0.60_0.65.json` (redaction noted in-file);
  `run_smoke_shell` amended to never persist w(theta) values (feasibility fields
  only); notes' "~10x below noise" corrected to the verifier's measured ~1-6x
  per bin (total bump S/N <~1.5, still unresolvable).
- **A6**: "single read path" claim softened to what is enforced — the blacklist
  wire covers `load_columns` (the only path feeding the estimator); the two
  schema-class scripts read directly with hardcoded legal columns.
- **A7**: `_check_guard` now enforces the smoke cap PER ROLE at its strictest
  value (data 2e4 / randoms 4e4); a hand-tagged 'smoke' data catalog of 3e4 is
  now caught (new test `test_smoke_data_cap_strict_per_role`).

## 9. AMENDMENT-GPU (Charles's ruling, 2026-08-07; Category-A conditioning)

Technique only — HOW the frozen pair counts are computed, nothing about the
physics, menu, bins, weights or estimator changed; binned counts proven
identical to the CPU path. CPU remains the default backend.

**What changed** (`v_bao.py`, `synth_bao.py`, `test_v_bao.py`,
`gpu_timing_smoke.py`):
- `pair_count_blocks_gpu`: brute-force block counting, torch float64 on V100
  (`GPU_DTYPE_NAME` guard constant, block 8192, ~2 GB peak); binning on
  cos(theta) via `bucketize(..., right=True)` on ascending cos-edges — the
  edge-tie sides PROVEN to match the CPU `count_neighbors` '<=' convention
  (derivation in the code comment); same API/return (ordered counts,
  self-pairs excluded by the window, Sigma-w^2 normalization untouched);
  exact dec-sort block culling. `ls_w_theta(..., backend=)` selects; a CPU
  spot-check per M3 run is a standing option (same call, backend="cpu").
- CAP-COMBINE OPTION (#5, default OFF = per-cap as frozen):
  `ls_w_theta_capcombine` (NGC+SGC counts summed pre-LS; jackknife over the
  union of caps' regions, block-diagonal) + `bin_shells_combined`
  (per-tracer floor). No science choice made — an OPTION for the M3 prereg.
- Tests 26/26 pass: equivalence (3 sizes incl. multi-block and
  position-dependent weights: totals equal at rtol 1e-12; per-bin max diff
  ~1.4e-9 on counts ~1e6, i.e. ~1e-15 relative — accumulation-order only);
  precision guard (pairs 1e-9 above bin edges must land in the upper bin —
  float32 collapses the ~1e-12 cos margin to a tie and misbins); end-to-end
  ls_w_theta GPU==CPU; weight test parametrized over both backends;
  cap-combine counts == sum of per-cap counts; combined floor logic.
- CATCH-PROOFS (both positive): forcing float32 -> precision test FAILED,
  restored exactly (byte-identical diff), suite green. Dropping the weight
  product in the GPU path only -> weight test [gpu] FAILED while [cpu]
  passed, restored exactly, suite green (26/26).
- RE-GATE with backend=gpu: all three synthetic gates PASS
  (`vbao_outputs/synth_gate_results_gpu.json`; gate JK 1.7 s, gate A 1.1 s,
  gate B 5.3 s — 2.6 s/shell vs 6 s CPU on the sphere mock; gate-B interval
  identical to CPU to ~8 decimals).

**Measured GPU throughput + 4-file M3 estimate** (timing smoke on real LRG
NGC 0.60-0.65 random positions at raised 2e5/4e5 subsamples — quarantined
timing path only, cap-raise stated in-file, counts discarded, only
timing/feasibility persisted: `smoke_outputs/gpu_timing_LRG_NGC.json`):
- 4.5e8 pair-evals/s sustained (float64; bucketize+scatter dominated);
  dec-cull fraction 0.42 at dec extent 89 deg.
- FOUR-file run (randoms ~18x data), all 62 kept shells
  (`vbao_outputs/m3_cost_estimate.json` section `four_file_m3`):
  GPU brute ~166 GPU-hr (worst shell BGS NGC 0.16-0.21: 25 hr) vs CPU
  dual-tree ~46 CPU-hr (worst 5.9 hr) — the tree pays only in-window pairs
  (~4%), the brute GPU pays the culled all-pairs (~42%). HONEST CONCLUSION:
  as-implemented the GPU backend does NOT beat the CPU tree for the 4-file
  M3; it is validated and available. Bounded options flagged for the M3
  gate: (a) tree-RR + GPU DD/DR hybrid; (b) 2D (dec+RA) GPU culling
  (est. 4-5x); (c) per-cap RR reuse across shells (exact in expectation
  under shuffled-z randoms; would need explicit prereg); (d) the 1-file
  default (3.2 CPU-hr) + a 4-file spot-check shell.

**B1/B2/B3 closure (focused verifier pass, provenance class):**
- B1 CLOSED: `synth_bao.py --backend gpu` (shipped `run_gates`) now writes the
  backend-suffixed gates json; regenerated and gate-content-verified against the
  shipped `synth_gate_results_gpu.json` (identical; fp-order only, e.g. JK
  median differs at 1e-12).
- B2 CLOSED: `cost_estimate.py` (shipped, deterministic) regenerates the whole
  `four_file_m3` section; reproduces the shipped totals exactly (GPU 165.557
  GPU-hr; CPU legacy 45.733 CPU-hr) and fixes the DR-counting asymmetry to
  once-on-both (factor 343): corrected CPU total 43.5 CPU-hr (worst shell
  5.6 hr), legacy DR-twice total kept in the json for the audit trail;
  conclusion unchanged (GPU brute ~3.8x slower than the CPU tree).
- B3 acknowledged: the `REDACTED` key in the M2 smoke json was a one-off HAND
  edit post-verifier (self-disclosed in its own text); all future smoke runs
  write the `REDACTION_POLICY` field via code (`run_smoke_shell`), no science
  values persisted.
