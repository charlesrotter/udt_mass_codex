# G253 registered commands

Run from the repository root:

```bash
python3 udt_g253_native_kernel_minimal_dependency_compression_audit_2026-08-24/derive_native_kernel_compression.py
python3 udt_g253_native_kernel_minimal_dependency_compression_audit_2026-08-24/verify_native_kernel_compression_independent.py
python3 udt_g253_native_kernel_minimal_dependency_compression_audit_2026-08-24/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```

The first three commands write only their registered JSON result in the G253 package. The last two
are repository-wide integrity gates.

For a strict read-only replay, append `--no-write` to each of the first three commands.

The production, independent, and package verifiers accept exactly two source layouts: repository
sources at the root or sealed sources under the root `sources/` directory. Every existing candidate
must match its manifest SHA-256; a conflicting duplicate fails closed.
