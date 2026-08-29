# G292 repair report

Date: 2026-08-28
Scope: external-review repairs R1--R4 only

## Implemented

1. The aggregate verifier now fails closed if `sympy` is unavailable and always reruns the symbolic
   production derivation before reporting `PASS`.
2. The run record declares `sympy`, uses a writable bytecode-cache prefix, and instructs sealed
   reviewers to replay from a writable ephemeral copy.
3. The exact report now distinguishes the complete abstract orientable metric-connection theorem
   from the single explicit metric-realization family. No all-history realization theorem is
   claimed.
4. External-review status is recorded as `ACCEPT_WITH_REPAIRS`; final premise, package, and
   repository replays are required before status closure.

No scientific formula, witness parameter, tolerance, omission, or landing token changed.

## Internal verification

- repaired aggregate: `PASS`, with all 22 symbolic checks freshly replayed;
- no-`sympy` hostile replay: failed closed with the registered dependency error;
- current scientific premises: `PASS`, 274 rows;
- repository suite: `195 passed, 1 xfailed` in 129.69 seconds;
- repair verifier: recorded separately in `REPAIR_VERIFICATION_RESULT.json`;
- repair-only external follow-up: `ACCEPT_G292_REPAIRS`, no remaining defects.

## Final banking verification

After adding G292 to the exact registry and updating the bounded startup surface, the 275-row premise
verifier passed and the complete repository suite passed with `195 passed, 1 xfailed` in 134.91
seconds. The expected xfail is the pre-existing matter-sector habit-pin gate.
