# Commands

Executed from the clean isolated repository root:

```text
python3 udt_phi_metric_ontology_audit_2026-07-22/build_source_census.py
python3 udt_phi_metric_ontology_audit_2026-07-22/derive_ontology_algebra.py
python3 udt_phi_metric_ontology_audit_2026-07-22/verify_ontology_audit.py
python3 udt_phi_metric_ontology_audit_2026-07-22/freeze_manifest.py
python3 udt_phi_metric_ontology_audit_2026-07-22/verify_repository_gates.py
```

The repository-gate command internally runs the documented CPU-only test baseline with
`CUDA_VISIBLE_DEVICES=` and `PYTHONDONTWRITEBYTECODE=1` and reads the original dirty checkout only
through Git status and filesystem metadata.

No ODE, PDE, relaxation, time-live, or GPU physics process was launched.
