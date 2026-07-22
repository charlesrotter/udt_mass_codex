# Commands

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 udt_global_metric_assembly_atlas_2026-07-22/build_global_assembly_atlas.py --workers 8

env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 udt_global_metric_assembly_atlas_2026-07-22/verify_global_assembly_atlas.py

python3 -m pytest tests/
```

The first unbounded-thread pool attempt was manually interrupted and is preserved in
`PRE_THREAD_BOUND_RUN_FAILURE.txt`. The first successful production transcript before the density
ledger/provenance-summary overlay is preserved as `PRE_DENSITY_OVERLAY_ATLAS_TRANSCRIPT.txt`.

The first independent verifier return contained the separately preregistered output-label bug and is
preserved under `PRE_VERIFIER_LABEL_CORRECTION_*`.

The first fresh adversarial review, its completion review, the separately preregistered corrections,
and the final fresh correction-review `PASS` are preserved under `FRESH_*`. The initial correction-
review CLI option-order failure is retained as `PRE_FRESH_CORRECTION_REVIEW_CLI_FAILURE.txt`.
