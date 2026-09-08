# BI3 review execution record

All paths below are review-owned evidence. Parent and accepted sources were read only.
Each launcher uses the read existing run_capture.py, 512MiB address space,
60-second CPU/wall limits and one numerical-library thread. Python3.10.12,
SymPy1.13.1. No GPU/grid/evolution process. No duplicate full358 audit or sync.

Source-first seal: 2026-09-08T18:43:30.597780+00:00. Candidate exposure followed
that seal after CANDIDATE_FREEZE.md became available. Tool transcript records
initial inspection/reads, direct primary method retrieval and freeze polling.
No mathematical conclusions were sent before the author freeze became available.

The first authentication failure is preserved; retry changes only read-only
Git invocation to disable preload threading and optional locks. The frozen
candidate had no scientific repair. Deliberate mutant assertion failures are
successful adversarial probes, distinct from the failed authentication launcher.

Exact commands (raw streams and JSON share each capture prefix):

## authentication

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/authentication /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/authenticate.py
```

Observed: exit 1; timeout False; 0.065617103s; child RSS 27212KiB.

## authentication_retry

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/authentication_retry /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/authenticate.py
```

Observed: exit 0; timeout False; 0.065195776s; child RSS 16436KiB.

## source_first_run

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/source_first_run /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/source_first_check.py
```

Observed: exit 0; timeout False; 0.390727065s; child RSS 48868KiB.

## source_first_seal_run

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/source_first_seal_run /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/seal_source_first.py
```

Observed: exit 0; timeout False; 0.017227997s; child RSS 14016KiB.

## preserve_sources_run

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/preserve_sources_run /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/preserve_sources.py
```

Observed: exit 0; timeout False; 0.018021170s; child RSS 15168KiB.

## candidate_authentication

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/candidate_authentication /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/authenticate_candidate.py
```

Observed: exit 0; timeout False; 0.017198026s; child RSS 14976KiB.

## candidate_comparison

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/candidate_comparison /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/compare_candidate.py
```

Observed: exit 0; timeout False; 0.489258551s; child RSS 49008KiB.

## mutation_probe_run

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/mutation_probe_run /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/mutation_probe.py
```

Observed: exit 0; timeout False; 0.457912592s; child RSS 51852KiB.

## author_regression

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/author_regression /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/check_bi3.py
```

Observed: exit 0; timeout False; 0.280443177s; child RSS 49092KiB.

## final_integrity

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/final_integrity /home/udt-admin/udt_mass_codex python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_03/review/final_integrity.py
```

Observed: exit 0; timeout False; 0.062073509s; child RSS 15904KiB.

The completion generator and final seal likewise run under the same launcher;
their exact argument arrays/timestamps are in completion_run.json and
final_seal_run.json. Final seal captures the stable payloads and snapshots;
its own capture stream/receipt are excluded to avoid self-reference.

REVIEW_REPORT.md gives argument audit, omissions and evidence-use limits.
REVIEW_RESULT.json is the machine-readable disposition. FINAL_REVIEW_SEAL.json
records exact final evidence identities; checksums assert correspondence only.
