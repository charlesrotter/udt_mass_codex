# Output schema

## `EXTENSION_DIRECTION_LEDGER.tsv`

Exactly seven rows, one for each free generator direction after the founded
reciprocal base generator is fixed. Effects are separated into the founded
pair, aligned local depth, non-aligned local depth, the fixed clock-horizontal
spatial metric, and the full four-dimensional metric.

## `BRANCH_EXTENSION_ATLAS.tsv`

Exactly 84 rows: the Cartesian product of twelve registered finite-cell
completion classes and seven extension directions. `global_descent_status`
is a compatibility status, never a selection. `unresolved_requirement`
records the datum that prevents promotion. `xmax_consequence` is deliberately
fail-closed.

## `MODULATION_CHANNEL_LEDGER.tsv`

Five non-overlapping readings: aligned local depth, non-aligned local depth,
global transverse distance, four-dimensional clock-angular mixing, and the
still-open scalar feedback/selection question.

## JSON results

- `ALGEBRA_RESULT.json`: production exact SymPy calculation.
- `INDEPENDENT_RESULT.json`: independent standard-library rational replay.
- `VERIFICATION_RESULT.json`: schema, cross-product, source, and catch-proof
  verification.
- `REPOSITORY_GATES.json`: repository preservation and baseline checks.

