# G240 repair preregistration

Date: 2026-08-23

Trigger: fresh external verdict `G240_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED`.

Status: `PREREGISTERED_BEFORE_R1_EXECUTION`

## R1 — one explicit source-root contract

The builder places manifest-bound source evidence under `intake/sources/`, but the delivered
verifier searches from the intake root. Repair only this contract:

1. In the live repository, resolve `SOURCE_MANIFEST.tsv` paths from the repository root.
2. In a sealed intake identified by its root `REVIEW_SCOPE.json`, resolve those paths only from the
   root `sources/` directory.
3. Do not silently probe multiple roots or accept an ambiguous layout.
4. Preserve exact SHA-256 verification of all eleven declared sources.
5. Make the builder execute `verify_package.py --no-write` against the completed intake exactly as
   delivered, with bytecode writes disabled, before reporting the intake as ready.
6. Record the selected source-layout mode in the verification result and add a negative gate proving
   that a sealed intake without its `sources/` root is rejected.

R1 passes only if:

- the repository replay remains green;
- a fresh sealed intake passes the registered no-write replay without mirroring or rearranging files;
- deleting or renaming the sealed `sources/` directory causes the replay to fail closed; and
- manifest, scope, and payload counts are recomputed after the repair.

## Frozen scientific landing and ceiling

The retained G240 landing is unchanged. The repair may not alter the all-image query, operator,
sibling measure, normalization, witnesses, premise stamps, or scientific conclusion.

No observational outcome, fit, physical history, source law, detector/transfer law, branch-selection
law, critical stratum, P1, `X_max`, cosmology, matter, or signalling claim may be opened or added.
