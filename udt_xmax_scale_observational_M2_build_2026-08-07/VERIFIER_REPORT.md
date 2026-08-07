# M2 BLIND ADVERSARIAL VERIFIER REPORT

Date 2026-08-07 | blind verifier agent (zero prior context; judged against PREREGISTRATION.md).
Scope: D1 formulas, D2 V-SNe, D3 V-BAO, D4 purity wiring, all captured outputs. Repo left
byte-identical (md5-verified restores) except this file; `__pycache__/*.pyc` refreshed by re-runs
(volatile bytecode, same sources).

## 1. RE-RUNS (my runs, not the captured files)

- `formulas_d1.py`: 52 checks, ALL TRUE, 0.6 s. Output diff vs captured `formulas_output.txt`
  on all KEY/CHECK lines: IDENTICAL.
- `pytest test_v_sne.py test_v_bao.py`: **22/22 PASSED** (6 SNe + 16 BAO), 0.6 s — matches the
  claimed counts.
- `synth_sne.py` (full gate, 25 s): A-analog 9/9, C-analog 9/9, coverage 12/20, GATE PASS.
  Re-run output byte-identical to captured lines 1–31 (deterministic confirmed). See finding A2.
- `synth_bao.py` (full gate, 27 s): gate JK 1.217 PASS, gate A (det 60/60, centers 98.3%,
  FP 6.5%) PASS, gate B PASS. JSON byte-identical to captured except `total_runtime_s`.

## 2. F-PEEK SWEEP (purity)

- Grepped every package output (notes, txt, json, smoke) for real-data verdict numbers: **no
  real-data chi², no bump statistic, no fit result, no preferred-profile statement anywhere.**
  `m1_spot_verify.json` = schema/rowcount/z-range/dN-dz (legal class); `m3_cost_estimate.json`
  = footprint + per-shell counts (schema class).
- Live guard probes (written outside the package, run, deleted):
  - Real Pantheon+ mode-A fit via `DataVector.from_real` → RuntimeError (F-PEEK). BLOCKED.
  - Real DESI LRG shell through `ls_w_theta` → M2GuardViolation. BLOCKED.
  - `load_columns` on the REAL file with NX / WEIGHT_FKP / lowercase `nx` → BlacklistViolation
    before I/O; `_rec` path refused before I/O. ALL BLOCKED.
- Sanctioned-touch lists in both notes match what the code actually reads (real z columns, real
  cov + Cholesky, real mBERR/x1ERR/cERR scales; real m_b_corr/mB/x1/c values never enter any
  mock or fit — verified in `synth_sne.py` source).
- One letter-tension found: finding A3 (smoke w(θ) vector stored).

## 3. F-IMPORT-LCDM

- Package-wide grep (code, docs, outputs) for r_d/fiducial/comoving/acoustic/sound-horizon/
  template/Planck/omega_m/H0/astropy.cosmology/camb: **clean** (only self-referential mentions
  in purity prose). The only geometry in `v_bao.py` is θ = ell/r(z) from the frozen menu.
- Blacklist verified by direct test on real files (above), not just the shipped tests'
  nonexistent-path checks.

## 4. MUTATION PROBES (all mutations restored; md5 of all sources verified = originals)

- **M1 — P1 model sign flip** in `v_sne.ln_g` (P1 → P3-form): CAUGHT by
  `test_p1_n1_reproduces_banked_z_zplus2` (1 failed / 5 passed). The banked n=1 cross-check is
  load-bearing and real.
- **M2 — injected bump amplitude mis-scaled** 5σ → 0.5σ in `synth_bao.gate_a`: CAUGHT —
  gate A FAILS (detection 11.7%, centers 23%). The detection gate is not vacuous.
- **M3 — weight product removed** from `pair_count_blocks` (unweighted counts, weighted norms):
  **NOT CAUGHT — 16/16 tests pass and ALL THREE gates pass** (JK 1.208 PASS, A PASS, B PASS).
  Mock weights are position-independent i.i.d., so ignoring them is statistically invisible.
  → finding A1.
- Follow-up positive check (mine): exact weight-duplication identity — a w=2 point vs the point
  duplicated at w=1 gives **binned DD counts identical to 0.0**; the residual 1e-4 w(θ) shift is
  purely the standard nDD = W²−Σw² self-pair convention (O(1/N), ~1e-5 at real shell sizes).
  The shipped weighted path is CORRECT — it is merely unguarded (A1).

## 5. GATE HONESTY

- V-SNe truths (inv-shapes 0.08–1.8) are NOT in the frozen start grid (0.25, 0.75, 1.5, 3.0);
  multi-start, wide bounds; intervals tight (±0.01–0.03) so PASS is not tolerance-vacuous;
  PASS-3sig rule frozen in-file pre-run with the coverage check as the calibration.
- Coverage seeds (5000–5019) were re-used after the bisection fix. Independent check (mine,
  seeds 7000–7019, same pipeline): **16/20 covered** — inside [9,19]; the fix generalizes, not
  seed-tuned. The bisection fix itself is genuinely Category-A (Δchi²-crossing root-finding;
  no physics term touched).
- Gate A threshold calibrated on seed+1 null mocks, FP rate tested on independent seed+2 mocks —
  no same-realization circularity.
- Gate B: pair-splitting ring is deliberately strong (Δchi² ~ 80) — it validates end-to-end
  plumbing + θ(z) geometry, while amplitude/significance sensitivity is carried by gate A
  (mutation M2 proves it). Recovered centers are both ~2% LOW vs injection (sharp ring vs
  Gaussian template) — inside the 15% gate; gate A's median is unbiased (1.98/2.00). Note only.
  P2/P3 joint-fit s-intervals in the gate-B JSON are grid-resolution-limited (61-point span;
  P2 interval degenerates to a point) — conditioning nit, truth-profile gating unaffected.
- D3 mock redesign (patch → full sphere) verified as a MOCK-design fix (edge-dropped companions
  imprint a data/randoms selection mismatch); pipeline code untouched by it; disclosed with two
  honest M3 cautions extracted.
- Diagonal-covariance caveat (task adjudication): the 24-region jackknife cov of 40 bins is rank
  ≤ 23; diagonal chi² with the SAME diagonal in the null-mock calibration is self-consistent FOR
  M2's build-validation purpose (M2 proves sensitivity). For M3 real data, bin-bin correlations
  are real and the independent-bin null calibration will NOT carry — the notes flag this
  honestly; it CONDITIONS M3 (correlated null mocks or a modeled cov needed) without
  invalidating M2.

## 6. PREREG CONFORMANCE

- Frozen choices verified in code against §2/§3/§4: menu P1/P2/P3 exact (D1 forms re-derived and
  matched line-by-line in `ln_g`/`shape_g`); z > 0.023; calibrator exclusion; full STAT+SYS cov
  via Cholesky; 4 modes incl. own-Tripp (diagonal, stated) and z-column swap (mode-D-only,
  machine-enforced); shells dz 0.05/0.15; 5e4 floor; θ ∈ [0.3°,12°], 40 log bins; cubic-in-lnθ
  null + Gaussian bump; FULL-window search (no LCDM center anywhere); ell free with s = ell/X_eff
  honestly reported as the identified combination. Class (iii) not fitted (per §2). F-STEER: no
  n=1/α=2 in any default, grid, or truth (machine-tested in test_v_bao).
- **Per-cap vs per-tracer 5e4 floor (adjudication):** §4 freezes the estimator "per shell, per
  cap" and the floor as "a shell enters only if it holds ≥ 5·10⁴ weighted galaxies". Since the
  estimated object is per-cap, per-(tracer,cap,shell) is the more natural reading, but the text
  does not say "per cap" for the floor — genuinely ambiguous. D3 built the binner
  catalog-agnostic (supports both) and FLAGGED the choice to the M3 gate instead of deciding:
  conforming, F-SHOP-safe handling. The choice is material (per-cap drops all ELG/QSO SGC
  shells) and MUST be settled in the M3 prereg.
- Mode B and calibrators: §3's cuts parenthetical ("used only by the anchored mode") vs the
  implementation (calibrators excluded everywhere; B anchors via the EXTERNAL M_B per §3's own
  mode-B definition and CP4). Consistent with the mode-B definition; disclosed in the notes. OK.

## 7. FINDINGS / AMENDMENTS OWED (none blocking; ranked)

- **A1 (moderate — validation hole):** the weighted pair-count path is exercised but UNVALIDATED:
  removing the weight product passes every test and every gate (mutation M3). Weights are
  load-bearing frozen design for M3. My duplication probe shows the shipped path is exact, but
  the package must not rely on a verifier's one-off. AMEND: add a weight-sensitivity test (the
  w=2-vs-duplicated-point identity on binned counts is exact and cheap) before M3.
- **A2 (minor — provenance):** `v_sne_synth_results.txt` lines 33–36 ("Degeneracy observations")
  are not produced by the shipped `synth_sne.py` (a re-run drops them). The numbers match the
  notes' §3 claims but their generating code is absent. AMEND: ship the snippet or mark the
  section as ad-hoc post-gate exploration.
- **A3 (minor — F-PEEK letter):** `smoke_outputs/*.json` stores a REAL w(θ) vector over the full
  analysis θ range (quarantined, DO-NOT-INTERPRET). It contains no fit/bump/verdict number and
  BAO-scale content is unresolvable — but the prereg says smoke tests "produce NO science
  numbers", and the notes' "~10× below noise" claim is overstated: measured per-bin jk σ at
  1.5–8° is 0.0037–0.012 vs a realistic bump ~0.002–0.005 (factor ~1–6 per bin; total bump S/N
  ≲ 1.5 — still unresolvable, so no steer is possible). AMEND: correct the notes' factor; either
  strip the w vector from the M2 smoke output or explicitly ledger why it is retained.
- **A4 (minor — M3 gap):** §4 requires trials accounting "over the full θ search window AND over
  shells". Only per-shell trials calibration exists; no cross-shell look-elsewhere machinery.
  Owed before any M3 significance statement.
- **A5 (record):** no radial-leg Δz_BAO estimator code exists in `v_bao.py` (D1 derived the exact
  forms; §4 wording "built as … evaluated per profile" is ambiguous; radial is ATTEMPT-ONLY at
  M3). Building it is M3-attempt work; state this in the M3 prereg.
- **A6 (nit):** "single read path" claim — `estimate_full_cost` and `m1_spot_verify.py` open
  catalogs directly via astropy (hardcoded RA/DEC/Z, schema class; no leak found); the blacklist
  wire covers only `load_columns`. Tighten the claim or route through the loader.
- **A7 (nit):** `_check_guard`'s smoke cap uses max(SMOKE_MAX.values()) = 4e4, so a hand-tagged
  'smoke' DATA catalog of 3e4 (> the 2e4 data cap) would pass the guard; `make_smoke` itself
  enforces correctly.

## FINAL VERDICT: **CLEAN-AMENDED** (A1–A7; A1 is the substantive one)

Both legs re-ran deterministically to their claimed results; every purity guard held under live
attack on real files; two of three deliberate breaks were caught by the shipped gates and the
third (A1) is a documented validation hole around a path independently verified correct; the
disclosed fixes are genuinely Category-A; no F-PEEK verdict number and no LCDM import exists in
the package. M2 may be recorded as M2-BUILT once the amendments are acknowledged (A1's test
added now or explicitly owed at M3 wiring).

---

# FOCUSED PASS — AMENDMENT-GPU + cap-combine (same blind verifier, 2026-08-07, second dispatch)

Scope: the Category-A amendment only (GPU pair-count backend, cap-combine option, A1/A3/A7
amendment closures riding along). Repo left byte-identical (md5 vs the amended state received);
only this section added.

## Per-item verdicts

1. **RE-RUNS (mine): CONFIRMED.** `pytest test_v_sne.py test_v_bao.py`: **32 passed** (6 SNe +
   the claimed 26 BAO, incl. 6 GPU-marked + 2 cap-combine + the new A1 weight test x2 backends +
   the A7 per-role cap test). GPU synthetic gates re-run by me (backend="gpu"): **all three
   PASS** — JK 1.21702557888263 (ref ...516: fp-order), gate A detection 1.0 / centers 98.3% /
   FP 6.5% (identical to ref), gate B centers/intervals match the shipped GPU json to ~1e-8
   (scatter_add accumulation order) and match the ORIGINAL CPU results to ~7 decimals.
2. **CATCH-PROOF REPLAYS: BOTH POSITIVE.** (a) `GPU_DTYPE_NAME="float32"` → precision-guard test
   FAILED as claimed (plus 3 equivalence/e2e failures; note the smallest equivalence case
   [500-8192] alone would NOT catch float32 — the dedicated edge-binning guard is what carries
   the catch at all sizes: layered, working). (b) weight product dropped in the GPU path only →
   `test_weight_sensitivity_duplication_identity[gpu]` FAILED while `[cpu]` PASSED. Restored
   byte-identical both times (md5-verified); suite back to 32/32 green.
3. **EQUIVALENCE HONESTY: NOT TOLERANCE-VACUOUS.** Bounds: totals rtol 1e-12; per-bin
   |cpu−gpu| < 1e-9·max(cpu) ⇒ absolute tolerance ≤ ~1e-3 of a count at these sizes, vs observed
   ~1e-15 relative diffs and vs 1.0 for a whole pair. Probe: injected ONE unit-weight pair into
   one wrong bin of the GPU result → **all three equivalence cases FAILED**. A single misassigned
   pair is caught; restored, green.
4. **F-PEEK SWEEP OF NEW OUTPUTS: CLEAN.** `gpu_timing_LRG_NGC.json` persists ONLY n/t_s/evals/
   block-cull/throughput/dtype/dec-extent — no counts, no w(θ), no bump-usable number; the code
   `del`s the count array and the positions are the RANDOMS catalog (survey mask only, no
   clustering content). The raised 2e5/4e5 cap: disclosed in-file and in notes §9, timing-only,
   quarantined — ADJUDICATED within the carve-out (the frozen SMOKE_MAX governs the w(θ) smoke
   path, which was not run). `synth_gate_results_gpu.json` is synthetic-only; the
   `four_file_m3` additions are schema-class. Old smoke w(θ) vector confirmed REDACTED (A3),
   disclosed in-file. Residual note: direct `pair_count_blocks_gpu` calls bypass `_check_guard`
   (guard scope = ls_w_theta, unchanged from the CPU era) — the timing path rests on disclosure,
   not a machine wire.
5. **COST TABLE: ARITHMETIC CONFIRMED.** 62 rows; Σt_gpu = 165.6 GPU-hr (claimed 166),
   Σt_cpu = 45.7 CPU-hr (claimed 46); worst shells 25.0 / 5.9 hr as claimed; every row exactly
   t = evals/throughput at the stated 4.5e8 (measured 4.4–4.6e8) and 2e8 (conservative vs
   measured 2.5e8). One ≤5% convention nit: GPU evals count DR once (343·N²·f_cull), CPU pairs
   count DR twice (361·N²) — slightly GPU-favorable, and the honest conclusion (GPU ~3.6×
   slower for the 4-file run) is anti-GPU anyway. No error changes the conclusion.
6. **CAP-COMBINE: DEFAULT OFF CONFIRMED, TEST REAL.** `ls_w_theta(backend="cpu")` default; all
   three gates default cpu; `run_smoke_shell` uses per-cap `bin_shells`; the shipped CPU gate
   json is byte-identical to the pre-amendment results. `test_capcombine_counts_equal_sum_of_caps`
   genuinely constrains the block assembly (disjoint patches, counts==sum at rtol 1e-12) and the
   per-tracer floor test is exact. Caveat carried: the union-region jackknife of the combined
   estimator has no statistical validation gate yet — fine for a default-OFF option; owed if the
   M3 prereg freezes the per-tracer reading.

## New (minor) findings — provenance class only

- **B1:** no shipped code writes `synth_gate_results_gpu.json` (main() writes only the CPU json;
  the GPU gates were invoked ad-hoc). I regenerated it from the shipped gates and it matches —
  content verified; AMEND: add a `--backend gpu` path to `synth_bao.py.__main__`.
- **B2:** no shipped code generates the `four_file_m3` section of `m3_cost_estimate.json`;
  arithmetic independently verified internally exact (item 5). AMEND: ship the generator or note
  it ad-hoc.
- **B3:** the smoke json's `REDACTED` key was hand-edited post-verifier (self-disclosed in its
  own text; future runs write `REDACTION_POLICY` via code). Honest; no action needed.

## FOCUSED-PASS FINAL VERDICT: **CLEAN-AMENDED** (B1, B2 — provenance nits only)

The amendment is genuinely Category-A: technique only (backend selection + a default-OFF option
for a prereg-flagged ambiguity), physics/menu/bins/weights/estimator untouched, CPU default and
original results byte-identical, equivalence machine-enforced and demonstrably sensitive to a
single misplaced pair, both catch-proofs independently replayed, purity of all new outputs
verified. Prior verdict (CLEAN-AMENDED) stands with A1/A3/A7 now CLOSED by this amendment;
A2 closed by the in-run degeneracy generator (noted: its frozen seeds 4100/4200 are new, so the
section is now self-reproducing going forward).
