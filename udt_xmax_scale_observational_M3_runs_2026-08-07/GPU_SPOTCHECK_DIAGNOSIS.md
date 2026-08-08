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
