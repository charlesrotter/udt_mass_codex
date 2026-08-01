# Append-only preregistration amendment — transitive evidence closure

Date: 2026-08-01

Base: `686336343878e8a9e39a4b72df08d23754243631`

This amendment was registered after the initial 172-path freeze and before semantic route
adjudication. The initial `PREREGISTRATION.md`, `SOURCE_PATHS.txt`, `SOURCE_INVENTORY.tsv`,
`SOURCE_MANIFEST.sha256`, and `PREREG_SNAPSHOT.json` remain immutable historical records.

## Why the amendment is required

The first source trace found that the initial freeze contained current summaries of load-bearing
Cartan/coframe, finite-cell, selector, variation-domain, and boundary audits without containing all
of the underlying audit packages. Grading a route from summaries alone could make a negative result
an incomplete-source result. This amendment closes that transitive evidence gap without changing
the 20 premises, 14 route candidates, stage gates, falsifiers, or fixed outcome classes.

## Frozen package scope

`TRANSITIVE_PACKAGE_SCOPE.tsv` names ten exact package directories and the route cells for which
they are admitted. `build_transitive_source_freeze.py` enumerates every tracked file in those
directories at the preregistered base, removes any path already present in the original 172-path
freeze, and writes a deterministic additions-only freeze.

The governing source universe for all later adjudication is the exact union of:

1. the immutable original 172 paths; and
2. `TRANSITIVE_SOURCE_PATHS.txt`.

No generated result from this derivation program may enter either set. The package-level freeze is
evidence closure, not authority to import a conditional action, carrier, boundary, topology, field
equation, or scientific verdict.

## Fail-closed rules

- Every scoped directory and every frozen path must exist in the exact base tree.
- Every transitive path must be absent from the original 172-path set.
- The combined set must be unique, deterministic, and hash-verified against the exact base.
- Removing a scoped package file, inserting a current-program output, changing a hash, or creating
  an original/transitive overlap must fail verification.
- This amendment cannot broaden the conclusion ceiling or alter the Stage-3 launch guard.

