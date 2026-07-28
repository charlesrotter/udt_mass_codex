# Run log

All commands were run from repository root on CPU.

```text
python3 -m py_compile \
  udt_native_global_coframe_definition_audit_2026-07-28/derive_global_definition.py \
  udt_native_global_coframe_definition_audit_2026-07-28/verify_global_definition.py

python3 udt_native_global_coframe_definition_audit_2026-07-28/derive_global_definition.py
python3 udt_native_global_coframe_definition_audit_2026-07-28/verify_global_definition.py
```

The first production attempt reached all symbolic assertions but failed while serializing SymPy
integer objects in the diagnostic sample spectrum. The serializer was corrected to emit strings;
no algebra, source set, premise, tolerance, candidate, or conclusion class changed.

The first independent-verifier attempt exposed a symbolic matrix-equality normalization issue in
the verifier's group-law check. It was corrected to simplify the residual entry by entry. The
production derivation was not changed.

Final production status: `OPEN_MULTIPLE_INDEPENDENT_SELECTOR_GAPS`.

Final verifier status: `PASS_VERIFIED_WITH_CAVEATS_SAME_SESSION`.

Final catch-proofs: 27/27 pass.

GPU processes launched: zero.
