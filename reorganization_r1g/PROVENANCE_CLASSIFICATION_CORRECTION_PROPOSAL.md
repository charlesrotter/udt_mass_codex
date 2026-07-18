# Provenance-classification correction proposal

Status: **proposal only; not applied**. B02 and B03 remain unauthorized.

## Reproduced defect

In the fixed R1C builder, the branch beginning with
`lower.startswith(("cascade_", ...))` returns `LEGACY_FROZEN` and
`PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE`. It runs without establishing the
artifact's operator lineage. R1E then maps that legacy label to
`archive/pre_2026-07-01/`. This conflates three independent questions.

1. **Operator provenance**: `PRE_NATIVE`, `NATIVE_2026-07-01`, `MIXED`, or
   `OPEN`, established from operator-bearing commits and primary records.
2. **Scientific lifecycle**: `ACTIVE`, `SUPERSEDED`, `HISTORICAL`, or `FROZEN`,
   established from the current controls and result status.
3. **Path-migration safety**: a separate dependency, manifest, frozen-path,
   collision, and pointer-closure decision.

A historical artifact is not thereby pre-native. A post-July artifact is not
thereby native. A byte-safe standalone script is not thereby safe to place in
a provenance-specific archive.

## Proposed fail-closed precedence

1. Apply hard-frozen and manifest path constraints without inferring operator
   provenance.
2. Classify operator provenance from explicit path/family lineage. A
   `PRE_NATIVE` ruling requires a path-history commit at or before the parent of
   `f766478`; a prefix is never evidence.
3. Classify `MIXED` when native and imported/reference operators coexist.
4. Classify insufficient evidence as `OPEN`.
5. Determine lifecycle independently from current controls and result records.
6. Determine migration safety independently from the complete dependency and
   immutability closure.

The proposed machine rules are
[CORRECTED_CLASSIFIER_RULES.json](CORRECTED_CLASSIFIER_RULES.json).

## Proposed destination taxonomy

- `archive/pre_2026-07-01/`: only artifacts with explicit, path-specific
  `PRE_NATIVE` operator lineage.
- `archive/native_2026-07-01/`: historical or superseded artifacts explicitly
  descended from the July 1 native operator, partitioned by lane/family.
- `archive/post_2026-07-01/`: historical `MIXED` or `OPEN` artifacts,
  partitioned by lane/family so the uncertainty is visible.
- `research/<lane>/`: active artifacts only after a separately authorized,
  dependency-closed migration.
- current path: frozen or manifest-constrained artifacts absent separate
  authority.

All 32 B02/B03 rows are presently
`BLOCKED_PROVENANCE_CORRECTION_REQUIRED`; the destinations in the exact table
are proposals, not move authority. The frozen Stage-D preregistration in the
121-file census remains at its current immutable path.

## Catch-proof contract

The independent verifier rejects:

- a post-July `cascade_*` row labeled `PRE_NATIVE` without explicit lineage;
- the removal of required pre-native lineage evidence from an otherwise valid
  fixture;
- any `archive/pre_2026-07-01/` destination whose operator provenance is not
  proven `PRE_NATIVE`;
- missing or duplicate adjudication rows.

These checks are exercised, not merely asserted, in
[INDEPENDENT_VERIFY_RESULT.json](INDEPENDENT_VERIFY_RESULT.json).
