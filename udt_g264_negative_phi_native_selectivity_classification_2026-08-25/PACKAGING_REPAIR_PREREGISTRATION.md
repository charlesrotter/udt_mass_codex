# G264 sealed-replay packaging repair preregistration

## Frozen defect

The external repair follow-up accepted registered scientific repairs R1--R3 but returned
`REJECT_REPAIR` because the sealed repaired package omitted `SOURCE_MANIFEST.tsv`. The registered
`verify_package.py` therefore could not resolve or verify the seven frozen sources from the sealed
intake.

## Bounded repair

Repair only the follow-up intake layout. Do not change the G264 equations, counterfamilies,
thresholds, landing, ownership stamps, or the already accepted metric-first and consistency roles.

The corrected intake will contain a self-contained `replay_root/` with:

1. the repaired G264 package, including `SOURCE_MANIFEST.tsv` and every file read by
   `verify_package.py`;
2. the seven exact source payloads at the repository-relative paths recorded in that manifest;
3. the original intake and both external review records for comparison;
4. a registered command that runs `verify_package.py` from the sealed `replay_root/` without Git,
   repository access, network access, or protected packages.

## Certification contract

Before a corrected intake is offered for authorization:

- copy it to a fresh writable ephemeral directory;
- rerun `derive_selectivity.py`, `verify_metric_first.py`, `verify_independent.py`,
  `run_catch_proofs.py`, `verify_repair_catches.py`, and `verify_package.py` there;
- require all registered counts and the unchanged bounded landing;
- prove fail-closed behavior by removing `SOURCE_MANIFEST.tsv`, altering one frozen source byte, and
  removing one frozen source; all three altered copies must fail;
- record hashes and commands.

## Maximum conclusion

Success establishes only that the R1--R3 repair is reproducibly and independently reviewable from a
self-contained seal. It cannot strengthen the G264 scientific landing or turn negative `phi`, the
alpha-two threshold, the G201 intersection, mass positivity, `X_max`, or a physical history into a
selection law.

