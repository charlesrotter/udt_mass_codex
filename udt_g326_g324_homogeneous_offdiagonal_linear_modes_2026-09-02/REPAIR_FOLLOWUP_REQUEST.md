# G326 repair-only external follow-up request

Fresh-review verdict: `ACCEPT__G326_BOUNDED_OFFDIAGONAL_CENSUS`.

Verify only repairs R1 and R2 in `REPAIR_LEDGER.tsv` and whether the unchanged bounded scientific
landing remains supported. Do not reopen, extend, or continue the research.

## R1 — exact computational-source integrity

1. Confirm that `verify_package.py` pins exact SHA-256 digests for
   `derive_offdiagonal_modes.py`, `verify_offdiagonal_independent.py`, and
   `run_catch_proofs.py`.
2. Confirm that the aggregate verifier executably replaces each of those three sources, one at a
   time, with a canned banked-artifact emitter and requires the mutated package to fail at the
   corresponding `source_integrity:<name>` gate.
3. Confirm these are live rejection proofs rather than string-only assertions.
4. Follow `REPLAY_PRECONDITION.md`, run the four registered commands literally, and confirm exact
   reproduction of all three banked JSON artifacts plus successful aggregate verification.

## R2 — writable ephemeral-copy replay

1. Confirm that `REPLAY_PRECONDITION.md` explicitly preserves the sealed intake as read-only.
2. Confirm that its copy and permission commands create a writable ephemeral copy suitable for the
   registered replay without changing evidence in the intake.
3. Confirm that the scope permits checks only in that ephemeral copy and does not permit evidence
   edits or research continuation.

## Scientific boundary

R1 and R2 must not change the metric, reciprocal kernel, angular sector, adopted field equation,
off-diagonal ODE, solution basis, six-constant classification, combined twelve-constant count, or
any premise. The bounded landing remains limited to homogeneous synchronous first variation. It
does not establish full linear or nonlinear stability, classify nonzero Fourier modes, select a
physical history, topology, occupancy, scale, observation, or `X_max`.

Allowed follow-up outcomes:

- accept R1 and R2 and the unchanged bounded landing;
- identify a concrete incomplete registered repair;
- retain the already accepted bounded scientific grade while recording any remaining evidence
  defect.
