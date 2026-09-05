# G351 internal aggregate-verifier repair preregistration

Date: 2026-09-05
Trigger: first registered aggregate replay returned 23/26 because three exact-phrase checks did not
match line-wrapped or differently phrased statements already present in the frozen scientific
evidence.

## Frozen failures

- `caustic_boundary`: verifier searched the exact phrase `no finite pointwise`, while the evidence
  says `does not ... extend A^-1 as a finite pointwise scalar`.
- `metric_kernel_unchanged`: verifier searched one single-line phrase split by Markdown wrapping.
- `observer_weight_open_lay`: verifier searched `does **not** tell us`, while the lay report says
  `does not decide among them`.

## Authorized mechanical repair

Change only these three semantic assertions in `verify_package.py` so they match the existing
meaning-bearing phrases. Do not alter the derivation, premise, saved calculation results, exact
landing, scientific scope, or any frozen preregistration/source file.

## Acceptance contract

- The repaired aggregate replay must pass 26/26.
- Production remains 56,316/56,316.
- Independent verification remains 11,115/11,115.
- Hostile mutations remain 10/10 caught.
- The aggregate replay changes no package bytes and emits no bytecode.

Maximum conclusion: mechanical verifier phrase repair only; no scientific claim changes.
