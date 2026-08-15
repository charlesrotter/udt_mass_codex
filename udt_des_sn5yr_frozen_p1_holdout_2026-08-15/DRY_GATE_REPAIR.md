# Dry-gate sample-count repair

Date: 2026-08-15

Status: source-schema repair committed before any P1 residual or likelihood

## What stopped

The first schema-only dry run stopped because the original preregistration expected `1635` rows
with `IDSURVEY == 10`. That number came from the DES-SN5YR release description of the upstream
quality-cut sample.

The exact frozen Dovekie Hubble diagram at upstream commit
`c9a4fcafc4cbd19bd750dee47fc76194a45c181f` instead contains:

```text
1820 total rows
1623 IDSURVEY == 10 rows
197 rows in the other registered survey identifiers
```

The frozen source is a later Dovekie vector, not the original 1829-object DES5YR-plus-low-z vector.
Its own README registers 1820 total rows. The Hubble-diagram file and compact precision matrix both
have dimension 1820.

## Exposure boundary

Before this repair:

- source hashes and NPZ keys/shapes were read;
- the table schema, survey identifiers, counts, and redshift ranges were parsed;
- the full precision matrix passed Cholesky factorization;
- the first five public table rows were displayed to confirm SNANA parsing, as already disclosed in
  `EXECUTION_CLARIFICATION.md`;
- no P1 prediction, residual, chi-square, aggregate magnitude statistic, or shape optimization was
  computed.

## Repair

Only the expected DES row count changes from `1635` to `1623`. The source commit, file hashes,
`IDSURVEY == 10` filter, frozen P1 shape, covariance rule, statistic, thresholds, secondary tests,
forbidden inputs, and conclusion ceiling do not change.

This is a preregistered-source schema correction, not an outcome-driven retuning.
