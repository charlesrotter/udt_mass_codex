# G281 external-review repair result

Date: 2026-08-27

Landing:

```text
G281_EVIDENCE_AND_GATE_TYPING_REPAIRED__SCIENTIFIC_LANDING_UNCHANGED
```

## R1 — exact sealed source universe

`SOURCE_SCOPE.tsv` now contains exactly the same 32 historical/evidentiary paths as
`SOURCE_MANIFEST.tsv`. Every path must exist and match its frozen SHA-256. The two mutable startup
files are no longer counted as scientific sources. Their alignment is explicitly a separate
repository closure check.

The primary verifier no longer has a mutable-file exemption. It checks exact set equality among the
32 scoped paths, 32 manifested paths, and 32 files whose hashes are verified.

## R2 — history ownership is visible in gate 1

The first of the six route gates is now:

```text
history_metric_owned_or_physically_selected_and_fixed_before_SNe
```

This makes the evaluator/prediction boundary machine-readable. G79 is now `NO` on gate 1 because it
is a supplied control history, while its maximum class remains
`NATIVE_CONDITIONAL_EVALUATION`. No route class changed and no route was promoted.

The preregistration preserves its original six acceptance items and appends a post-review
clarification that “determined independently” includes native ownership/physical selection as well
as pre-SNe freezing; arbitrary outcome-blind controls remain conditional evaluators.

## R3 — replay provenance separated

`COMMANDS.md` identifies the four intake-resident G281/July commands as the sealed command surface.
The G279/G280 no-write checks are explicitly repository-recorded historical evidence, not commands
replayed from the first G281 intake. `AUDIT_REPORT.md`, `EVIDENCE_GATES.md`, and
`VERIFICATION_RESULT.json` now use the same distinction. Saved JSON checking is called a consistency
replay rather than a fresh derivation.

## R4 — filename repair

The stale scan now names `CURRENT_SCIENTIFIC_PREMISES.tsv` rather than the nonexistent `.md` file
and stamps the startup row `REPOSITORY_CLOSURE_CHECK_NOT_SEALED`.

## Noninterference

Unchanged:

- all 24 substantive historical-tile classes;
- all 15 route maximum classes;
- every historical and observational number;
- the metric, reciprocal kernel, direct redshift, optical evaluator, transfer status, P1 status,
  G236/G237 empirical reconstruction, G278 resolution-sensitive holdout, G279 native boundary,
  G280 counterexample, and `X_max`;
- `NO_COMPLETE_NATIVE_SNE_PREDICTION_IN_AUDITED_NONPROTECTED_LINEAGE`.

Fresh internal replay passes. Final grade remains repair-pending until a fresh sealed external
repair-only follow-up accepts R1--R4.
