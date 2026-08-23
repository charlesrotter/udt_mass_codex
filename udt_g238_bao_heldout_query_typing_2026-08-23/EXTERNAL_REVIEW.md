# G238 fresh external adversarial review

Review model: external Codex reviewer (`gpt-5.4`, high reasoning, web disabled)

Sealed intake: `/tmp/udt_g238_review_k6yotrly`

`REVIEW_SCOPE.json` SHA-256:
`77ca386f108cba936348164cab2d6289203f43985dc87dbe6e7ffa1b63849c00`

Raw returned review SHA-256:
`41b7d01dafbde011a076731c5e3226998b46617cda80deb64ecebe86e704f884`

## Verdict

`G238_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED`

## Load-bearing findings

- The sealed intake supports the package's negative typing result: the frozen G237 object supplies
  only 11 relative `R` values on 12 knots and explicitly lacks interpolation, derivatives,
  complete metric history, and source/branch population, while the BOSS-side target is a
  two-source reference-projected Landy-Szalay statistic requiring complete
  metric/query/branch/source/reference inputs.
- The cited later metric-native artifacts do not close that gap. They own supplied-history
  evaluators, not history selection from G237: G127 is conditional on one supplied metric history,
  G188 on one supplied complete metric and one supplied null branch, G221 on one supplied complete
  coframe and branch, and G226 on supplied null edges/events.
- The two-source obstruction is real: a one-source observation map or one-point Jacobi data does
  not own a physical pair measure or branch population, and the BOSS random catalogue owns survey
  reference semantics rather than a source law. The exact central-spherical bridge also remains
  blocked by reference cancellation.
- The reviewer found no hidden P1, `X_max`, fitted interpolation, feature selection, cosmological
  distance conversion, post-readout orchestra insertion, or BOSS outcome opening in the sealed
  intake's stated contract.

## Replay results

- `REVIEW_SCOPE.json` verified cleanly: 36/36 declared file hashes matched, and the declared tree
  digest recomputed exactly.
- In a fresh ephemeral copy, `py_compile`, `derive_query_typing.py --write`,
  `verify_query_typing_independent.py`, `verify_package.py`, and `run_catch_proofs.py` all passed.
- The reviewer also replayed the counterfamily witness against the actual frozen knot locations,
  not just the normalized template. The between-knot value plus first two derivatives were all
  nonzero, preserving the scientific nonuniqueness theorem after the registered repair.

## Defects or repairs

1. The load-bearing verifier did not anchor the counterfamily witness to the actual frozen knot
   locations. It constructed the witness on normalized roots `0,1/11,...,1` while checking only
   that the real knots were strictly increasing. Repair by building the witness directly from the
   actual frozen knot values in both derivation and verifier.
2. The sealed replay instructions were not fully self-contained. The registered `--write` step
   fails on a truly read-only temp copy unless the ephemeral copy is made writable, and
   `COMMANDS.md` listed `verify_current_scientific_premises.py` even though that verifier was not
   included in the seal. Repair the ephemeral-copy instructions and separate repository-only
   premise verification from the sealed command list.

## Maximum scientific conclusion

The current sealed corpus does not yet own a lawful no-refit forward operator from the frozen G237
`K=12` processed SNe state to the BOSS observer-coordinate angular Landy-Szalay observable. The
complete continuous metric history, populated null-branch/source-pair measure, and full two-source
reference-projected forward map remain open, so BOSS outcomes must stay closed. No BAO origin,
preferred feature, ruler, `X_max`, cosmological-distance, or UDT-validation claim follows.

