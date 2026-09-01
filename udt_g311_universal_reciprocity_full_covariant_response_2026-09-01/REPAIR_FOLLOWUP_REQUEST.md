# G311 repair-only external follow-up request

## Frozen scope

The fresh external reviewer returned `G311_REPAIRABLE_DEFECTS` while explicitly upholding the
bounded scientific landing. Verify only preregistered repairs R1--R3 and that the scientific landing
is unchanged. Do not reopen or continue the research.

## Required checks

1. **R1 dependency-free independence.** In a writable ephemeral copy, run
   `python3 -S verify_covariant_response_independent.py`. Confirm that it imports only the Python
   standard library, imports no production module, uses a different rational plane family and
   component ordering, and independently reconstructs the exact metric two-jet curvature witness.
   It must return rank nine, the metric-line annihilator, nonzero trace-free Ricci, zero Weyl, and the
   unchanged conditional degree count.
2. **R2 sealed containment.** Run all four commands in the registered sealed replay. Confirm that
   `verify_package.py` resolves no path above its package, invokes no Git or repository gate, and
   requires no undeclared dependency. The separately listed repository banking commands in
   `COMMANDS.md` must be explicitly outside and unauthorized during the intake-only replay.
3. **R3 evidence grade.** Confirm that `run_catch_proofs.py` is openly described as a shared-code
   regression harness, and that no ledger, report, or verifier counts its 6/6 catches as
   implementation-independent confirmation.
4. **No scientific change.** Compare the retained landing and strongest conditional landing against
   `EXTERNAL_REVIEW_RESPONSE.md` and `REPAIR_PREREGISTRATION.md`. The theorem, counterresponse,
   response-constitution boundary, metric, reciprocal kernel, angular cancellation, and premise
   grades must be unchanged.

Return exactly one of:

- `G311_ACCEPTED_WITH_RESPONSE_CONSTITUTION_BOUNDARY`
- `G311_REPAIRABLE_DEFECTS`
- `G311_SCIENTIFIC_LANDING_CHANGED`

List any remaining defect precisely. Do not edit evidence files, change the scientific question,
continue the research, or select or canonize a response law, history, scale, or `X_max`.
