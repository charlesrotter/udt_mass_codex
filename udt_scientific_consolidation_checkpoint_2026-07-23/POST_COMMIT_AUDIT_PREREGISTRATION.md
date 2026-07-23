# Post-commit adversarial audit preregistration

Date: 2026-07-23

Audited tip: `0b060b4a98164b0959374979203b1fbd81b6d712`

Mode: correction layer and verification strengthening only

## Findings registered before correction

1. Replaying `verify_repository_gates.py` from the committed tip changes only
   `REPOSITORY_GATES.json`: the generated scope list acquires the gate output
   itself. The gate is therefore passing but not byte-deterministic.
2. `verify_checkpoint_independent.py` checks the consolidated status contract,
   source hashes, and evidence-path existence, but it does not mechanically
   resolve every consolidated identity to an exact parent-ledger row. Its
   independence is structural, not yet a complete source-status cross-check.
3. `C10` compresses the parent grade
   `SETTLED_STATIC_FINITE_BOX_CONDITIONAL` to `CONDITIONAL`. This is
   conservative but loses a verified scoped gain.
4. `C22` uses the synthesized label `NOT-IDENTIFIED` where the parent ledger's
   exact status is `OPEN_NOT_JOINED`.
5. The checkpoint prose can state the zero-`dphi` distinction more precisely:
   absence of an intrinsic reduction supplied by `dphi` is exact, while any
   replacement reduction requiring extra structure remains open.
6. `MEMORY.md` correctly subordinates itself to `LIVE.md`, but its top current
   pointer still routes to the superseded July 19 selector instead of the
   consolidation checkpoint.

No underlying evidence package, derivation, equation, numerical result, or
frozen record was found changed by these defects.

## Authorized corrections

- Preserve `PREREGISTERED_STATUS_CONTRACT.tsv`,
  `PREREGISTRATION.md`, and `PREREGISTRATION_CORRECTION.md` unchanged as
  historical evidence.
- Add an append-only machine-readable status-correction overlay.
- Correct only the affected current checkpoint rows and explanatory prose.
- Add an exact source-status binding table covering all 24 checkpoint
  identities.
- Extend the independent verifier and catch-proofs to resolve and check every
  binding against its cited parent TSV row.
- Make the repository-gate output byte-deterministic by excluding its own
  generated output path from its reported input scope.
- Update only the top current pointer in `MEMORY.md`; do not alter its durable
  historical sections.
- Add a post-commit audit report and regenerate only this checkpoint's
  generated verification outputs, manifest, and hashes.

## Prohibited work

- No physics derivation, reinterpretation, action or carrier adoption, solve,
  GPU work, canonization, artifact move, repository reorganization, or edit to
  prior scientific packages.
- No edit to `LIVE.md`, `HANDOFF.md`, `INDEX.md`, `README.md`, `AGENTS.md`,
  `CANON.md`, current registries, frozen packages, scripts, data, or prior
  checkpoint preregistration records.
- No promotion of an open or conditional scientific object.

## Verification contract

- Two corrected status identities, and only those identities, differ from the
  historical preregistered status contract.
- `C10` must equal `SETTLED_STATIC_FINITE_BOX_CONDITIONAL` and retain every
  static finite-box/carrier/action/coefficient/boundary/operator limitation.
- `C22` must equal `OPEN_NOT_JOINED`; no identity between metric `phi` and
  observer rapidity is derived.
- Every one of the 24 current identities must have at least one exact
  parent-ledger binding; source rows, fields, and values must resolve uniquely.
- Catch-proofs must reject a missing binding, duplicate binding identity,
  altered expected source value, loss of all bindings for a current identity,
  C10 promotion beyond its scope, and C22 identity promotion.
- A second repository-gate replay from a clean committed state must leave the
  worktree clean and reproduce the same `REPOSITORY_GATES.json` SHA-256.
- All existing checkpoint catches, parent manifests, six frozen manifests,
  current paths, links/frontier targets, tests, and original dirty-checkout
  metadata gates must still pass.

## Maximum conclusion

`POST_COMMIT_CHECKPOINT_CORRECTION_VERIFIED_WITH_NO_NEW_PHYSICS`
