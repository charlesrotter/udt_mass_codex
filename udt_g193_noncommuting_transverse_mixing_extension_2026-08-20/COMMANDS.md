# G193 commands

Run from repository root:

```bash
python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/derive_noncommuting_transverse_mixing.py
python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/verify_noncommuting_transverse_mixing_independent.py
python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/run_catch_proofs.py
python3 verify_current_scientific_premises.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/
git diff --check
```

No-write replay:

```bash
G193_NO_WRITE=1 python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/derive_noncommuting_transverse_mixing.py
G193_NO_WRITE=1 python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/verify_noncommuting_transverse_mixing_independent.py
G193_NO_WRITE=1 python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/run_catch_proofs.py
```

Corrected sealed follow-up replay, from the intake root:

```bash
G193_REVIEW_RUNTIME_REQUIRED=1 TMPDIR=.review_runtime TMP=.review_runtime TEMP=.review_runtime PYTHONDONTWRITEBYTECODE=1 python3 udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/verify_package.py --no-write
```

`.review_runtime` is the only writable intake directory. The package verifier requires it to be
empty before and after replay and hashes every package evidence file across the no-write run.
