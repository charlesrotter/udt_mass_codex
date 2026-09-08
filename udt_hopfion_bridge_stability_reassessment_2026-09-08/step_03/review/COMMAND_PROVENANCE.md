# Execution provenance

Source-first check literal outer command:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_hopfion_bridge_stability_reassessment_2026-09-08/step_03/review/source_first_ratio /home/udt-admin/udt_mass_codex python3 -B udt_hopfion_bridge_stability_reassessment_2026-09-08/step_03/review/independent_ratio_check.py
```

Automatic capture JSON owns the exact child argv, cwd, time, resource limits
and result. Separate stdout/stderr are preserved. The inspected utility
hardcodes a 60-second wall timeout as well as the recorded 60-second CPU cap.
Bookkeeping/source-read commands were short shell/Python operations; their
complete initial raw CLI streams are not separately archived. No full audit
or author replay occurred before seal. The initial missing step_03/WORK_ORDER
read is retained in the requirements; campaign-root scope was read instead.
