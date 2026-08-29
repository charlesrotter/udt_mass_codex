# G292 repair-only external follow-up request

Review only the corrected sealed G292 intake. Verify only preregistered repairs R1--R4 and that the
bounded scientific landing is unchanged. Do not continue the research.

1. Compare the corrected `verify_package.py`, `RUN_RECORD.md`, `EXACT_DERIVATION.md`, and
   `EVIDENCE_GATES.md` against their copies under `ORIGINAL_SEALED_G292/`.
2. Confirm that the aggregate now fails closed when `sympy` is unavailable. Run the registered
   no-`sympy` hostile check or `verify_repairs.py` from a writable ephemeral copy.
3. Confirm the replay documentation declares `sympy`, a writable copy, and a writable bytecode
   cache rather than attempting to write into the sealed mount.
4. Confirm the scope now separates the general abstract supplied metric-connection theorem from
   the single explicitly realized global metric family.
5. Confirm the original external verdict is recorded accurately, the 274-row premise replay and
   `195 passed, 1 xfailed` repository replay are reported, and no pending status was silently called
   closed before this follow-up.
6. Confirm no formula, free parameter, tolerance, omitted stratum, or exact landing token changed.

Return exactly one verdict:

- `ACCEPT_G292_REPAIRS`
- `REJECT_G292_REPAIRS`

List any remaining repair defect precisely. Do not reopen or extend the scientific question unless
a repair itself changed the scientific landing.
