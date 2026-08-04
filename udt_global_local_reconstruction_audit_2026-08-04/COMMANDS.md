# Replay commands

Run from repository root:

```bash
python3 udt_global_local_reconstruction_audit_2026-08-04/derive_reconstruction.py
python3 udt_global_local_reconstruction_audit_2026-08-04/independent_reconstruction.py
python3 udt_global_local_reconstruction_audit_2026-08-04/verify_audit.py
python3 verify_current_scientific_premises.py
python3 udt_global_local_reconstruction_audit_2026-08-04/verify_repository_gates.py
python3 udt_global_local_reconstruction_audit_2026-08-04/verify_package_manifest.py
```

The fresh external review used `gpt-5.4`, medium reasoning, disabled web search, a read-only
repository sandbox, and no authorization to edit or continue the research. Its exact request and
verbatim verdict are preserved in `ADVERSARIAL_REVIEW_REQUEST.md` and
`FRESH_ADVERSARIAL_REVIEW.md`.
