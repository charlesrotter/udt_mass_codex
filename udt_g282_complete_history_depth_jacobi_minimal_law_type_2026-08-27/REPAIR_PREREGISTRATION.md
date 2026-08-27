# G282 external-review repair preregistration

Date: 2026-08-27

External verdict: `ACCEPT-WITH-REPAIRS`

## Frozen repair scope

R1 only: retype the seven checks implemented by `run_catch_proofs.py` as schematic claim-schema
consistency catches. State explicitly that they do not mutate evidence files, derivation code, or
source-census artifacts and are not an artifact-level mutation replay.

Apply this regrade consistently to the script label, saved catch result, package-verifier label,
verification count, command description, audit report, and evidence-gate language. Preserve the
original preregistration as a historical record and append a post-review interpretation note rather
than rewriting the preregistered contract.

## Invariants that must not change

- scientific landing;
- both fixed mathematical witnesses and their outputs;
- exact derivation checks;
- independent RK4 cases, assertions, and error bounds;
- frozen 18-source ownership universe and source hashes;
- three allowed homes for the missing information;
- no-import ledger and scientific ceiling.

## Certification contract

1. All five registered no-write replays still pass after the wording repair.
2. A repository search finds no current G282 claim that the schematic guard mutates artifacts.
3. The package verifier labels the layer as claim-schema catches.
4. The complete package retains the exact scientific landing and all numerical evidence.
5. A sealed repair-only follow-up intake is built for external verification before the external
   grade is promoted from `ACCEPT-WITH-REPAIRS`.

No new physics, law, fit, observation, scale, profile, action, source, or `X_max` statement is
authorized by this repair.
