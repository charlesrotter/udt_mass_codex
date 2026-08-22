# G211 run record

Date: 2026-08-22

## Environment

- repository: `/home/udt-admin/udt_mass_codex`
- branch: `grok`
- preregistration commit: `7220e71f`
- computation: CPU, exact SymPy/Fraction plus 120-digit `mpmath`
- GPU: not used

## Commands

```bash
python3 udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/derive_diagonal_scalar_basis.py
python3 udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/verify_diagonal_scalar_independent.py
python3 udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/run_radial_controls.py
python3 udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/verify_source_manifest_repository.py
python3 udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 \
  udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/verify_core_package.py
```

## Initial results

- production assertions: 29
- independent exact cases: 10,000
- independent assertions: 280,003
- high-precision profiles: 4 at 120 digits
- source-manifest rows verified: 8
- hostile catches: 31
- byte-stable no-write core replay: PASS
- first-run scientific repairs: none
- harness-only repairs: one registered repeated-token deletion-helper correction before any hostile
  result file was written

## External review

- sealed intake: `/tmp/udt_g211_review_efn8o_7v`
- scope SHA-256: `553151874b32f4411ac184eae7d3c8d035b8230e9b87f5d46e3c94c0aea7dbc5`
- tree SHA-256: `1c74daf06c0be362726ff4154abbe42a73dcf12e3b9fc77f6ed43d4162731c26`
- payload hashes: 34/34 passed
- registered no-write replay: passed
- reviewer grade: `VERIFIED_WITH_CAVEATS`
- required repairs: none
- scientific landing: unchanged
- final package no-write replay: passed
