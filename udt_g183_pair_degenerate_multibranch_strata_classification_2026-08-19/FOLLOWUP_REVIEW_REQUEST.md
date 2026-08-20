# G183 repair-only follow-up request

Review only the registered packaging repair. Do not continue the science.

1. Confirm the original `G183_REPAIR_REQUIRED` review is preserved.
2. Run exactly `python3 verify_package.py` in the sealed read-only package directory, with no
   environment variable. It must return zero and change no package hash.
3. Run exactly `python3 verify_default_read_only_entrypoint.py`. It must return zero and report
   `hashes_unchanged: true`.
4. Confirm result writing now requires explicit `UDT_WRITE_VERIFICATION_RESULT=1`.
5. Confirm no theorem, witness, numerical count, source, landing, or conclusion ceiling changed.

Return exactly one:

- `G183_REPAIR_ACCEPTED`
- `G183_REPAIR_REJECTED`
