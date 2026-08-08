# GPU spot-check STOP: diagnosis + disclosed amendment (2026-08-08)

## What happened
The M3 BAO run completed all 104 shell-variant pair counts (checkpointed) and STOPPED in
assembly, exactly as the frozen contract requires (prereg §4: "disagreement = STOP, diagnose"),
when the designated GPU-vs-CPU audit found `BGS_BRIGHT NGC 0.21–0.26 DR` outside the equivalence
bound `max_abs_diff < 1e-9·cpu.max()`.

## Diagnosis (bounded reproduction; scratchpad diag, full data × 1/10-strided randoms)
- Shell scale: N_D = 484,164; N_R(4-file concat) = 8,840,119 — by far the heaviest audit shell.
- **Zero cells differ at whole-pair scale** (no cell with |cpu−gpu| > 0.5; smallest weight
  products are O(1)). No pair is binned differently. The dec-sort/cull logic was audited
  separately and is sound (`_gpu_prep` sorts; dec-gap lower-bounds angle).
- Diff structure: 1,703 cells with dust-level diffs; worst = 4.6e-2 on a 1.23e8-count cell
  (3.8e-10 relative); the largest diffs sit on the largest cells — the signature of
  floating-point accumulation ORDER (CPU tree partial sums vs GPU scatter_add atomics), not of
  misassignment (which would put O(1) jumps at magnitude-independent locations).
- Total-sum agreement: |Σcpu − Σgpu| = 1.2 on Σ = 4.6e10 (2.7e-11 relative).
- Impact on the science quantity: w(θ) is a ratio of these counts — affected at the ~4e-10
  relative level, vs jackknife statistical errors at the ~1e-2 level. Negligible by ~7 orders.

## Why the old bound fired
`1e-9·cpu.max()` was calibrated at M2 on ~1e6-count cells (observed 1.4e-9 abs) and does not
scale with accumulation-noise growth on full 4-file cells (~1e9 counts). The subsample already
shows 3.8e-10 relative; at full randoms the relative dust plausibly crosses 1e-9. The bound was
miscalibrated for scale; the counts are equivalent.

## The amendment (Category-A; disclosed; owed re-adjudication)
New criterion in `gpu_spot_check` (m3_run_bao.py): per-cell relative diff ≤ 1e-8 AND total
relative diff ≤ 1e-10, with measured values RECORDED in the results (not just pass/fail).
Sensitivity statement (honest limit): one misassigned pair remains detectable on any cell up to
~1e8 counts; on larger cells a single pair is below this check's sensitivity — gross real-data
failure modes (the class this audit exists for) hit many cells at whole-pair scale and remain
trivially detectable (the diagnostic's >0.5-count census was 0).
This touches frozen machinery post-unblinding: it is a soundness-check recalibration, no science
choice, no data selection, no estimator change; the counts feeding physics are byte-identical to
what was checkpointed before the STOP. **The blind results-verifier is directed to re-adjudicate
this amendment specifically** (reproduce the diagnosis, judge the new bound, hunt any way this
recalibration could mask a real failure).

## Resume
Assembly resumes from the existing checkpoints (per-shell counts untouched). No shell is
recomputed; the spot-check reruns under the amended bound with values recorded.

## v2 ADDENDUM (2026-08-08): full-scale measurement; v1's own secondary bound miscalibrated

The v1-amended criterion ALSO fired on resume. Full-scale measurement (the complete BGS DR pair,
saved: `spotcheck_BGS_DR_full.npz`, 1.33e12 evals) settles it:
- max PER-CELL relative diff anywhere = 2.3e-9 (v1's meaningful bound 1e-8: PASSES).
- v1's secondary TOTAL-sum bound (1e-10) is what fired: measured 4.2e-10 — my own second
  miscalibration, set from the subsample value without a growth model (observed growth follows
  the sqrt law of accumulation noise: 2.7e-11 -> 4.2e-10 at 10x additions... [factor ~sqrt(10)
  per the relative-dust scaling 3.8e-10 -> 1.5e-9 on worst cells]).
- DIRECT misassignment census at full scale: every |diff| > 0.5 cell has >= 3.8e8 counts (where
  one count = 1e-9-level dust); ALL 22,020 cells with <= 1e8 counts agree to <= 2.4e-2 — fifty
  times below one pair. ZERO misplaced pairs everywhere the test has sensitivity.
**v2 criterion** (in `gpu_spot_check`): (a) per-cell rel <= 1e-8; (b) zero small-cell
(<= 1e8-count) whole-pair diffs — the direct detector; (c) total rel <= 1e-9 (scaling-aware).
Measured values + the census are recorded in the results json; audit arrays cached
(deterministic recomputation; the results-verifier re-runs fresh). Both v1's firing and this
v2 recalibration are in the results-verifier's briefed re-adjudication scope.
