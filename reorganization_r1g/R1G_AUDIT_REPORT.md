# R1G provenance-classification audit report

## Verdict

The reported classification defect is reproduced. R1F remains clean, while B02
and B03 are blocked and unauthorized. The fixed R1C rule classified every
eligible `cascade_*` path as pre-native from its prefix, and R1E propagated that
label into a pre-July archive destination without operator-lineage evidence.

No research artifact or research script, fixed R0–R1F record, current registry,
evidence, data file, or manifest was changed by R1G. Only this audit overlay is
corrected.

The current tables include the preregistered readout-provenance correction:
reference-only standard-theory diagnostics are disclosed separately and do not
demote the provenance of the native action/EOM they read. The correction record
is [R1G_READOUT_PROVENANCE_CORRECTION_REPORT.md](R1G_READOUT_PROVENANCE_CORRECTION_REPORT.md).

## Independent census

- The fixed R1C ownership registry contains 138 `cascade_*` rows.
- Exactly 121 carry the prefix-produced pair `LEGACY_FROZEN` /
  `PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE`.
- Git history places 61 introductions on July 2 and 60 on July 3.
- The 121 affected rows resolve into 15 coherent introducing-commit/family
  groups: all 121 are `NATIVE_2026-07-01`; none is `MIXED` or proven
  `PRE_NATIVE`. Five C12 rows separately disclose reference-only GR/MS readout.
- Lifecycle is separately recorded as 120 `HISTORICAL` and one `FROZEN`
  Stage-D preregistration.

The exact per-file census is
[AFFECTED_CASCADE_FILE_CENSUS.tsv](AFFECTED_CASCADE_FILE_CENSUS.tsv); the
family-level evidence and counts are
[AFFECTED_CASCADE_FAMILY_SUMMARY.tsv](AFFECTED_CASCADE_FAMILY_SUMMARY.tsv).

## Exact B02/B03 adjudication

The source plan has exactly 18 B02 and 14 B03 paths. Git history independently
places B02 introductions from July 2 through July 7 and B03 introductions from
July 2 through July 8. The complete table, including every introducing/first/
last commit and date, blob, SHA-256, operator evidence, lifecycle evidence,
owner, secondary consumer, migration-safety ruling, and proposed destination,
is [B02_B03_ADJUDICATION.tsv](B02_B03_ADJUDICATION.tsv).

The totals are:

| Axis | Ruling | Count |
|---|---:|---:|
| Operator provenance | `NATIVE_2026-07-01` | 29 |
| Operator provenance | `MIXED` | 2 |
| Operator provenance | `OPEN` | 1 |
| Operator provenance | `PRE_NATIVE` | 0 |
| Scientific lifecycle | `HISTORICAL` | 32 |
| Primary owner | `FOUNDATIONS` | 27 |
| Primary owner | `MACRO` | 3 |
| Primary owner | `PARTICLE_MASS` | 2 |
| Migration safety | `BLOCKED_PROVENANCE_CORRECTION_REQUIRED` | 32 |
| Comparison readout | `REFERENCE_ONLY` | 3 |
| Imported action/coupling | load-bearing nonzero alpha | 2 |

The two `MIXED` rows are `phi_source_derivation.py` and `homog_alpha_test.py`:
the imported/free nonzero-alpha weight enters the tested matter action and phi
EOM. `cascade_bv16_cas.py`, `cascade_or_energy_cas.py`, and
`verify_universe_bv2_f_einstein.py` remain `NATIVE_2026-07-01`; each separately
discloses `GR_EINSTEIN_TENSOR;MISNER_SHARP` with `role=REFERENCE_ONLY`.
`verify_redshift_profile_derivation.py` is `OPEN`: it is a
post-July kinematic/proper-distance calculation without a field-equation
operator lineage. The remaining 26 explicitly descend from the July 1 native
equations.

## Boundary and proposed correction

The exact ancestry boundary is `f766478`, parent `7893983`, as documented in
[JULY1_NATIVE_FIELD_EQUATION_BOUNDARY.md](JULY1_NATIVE_FIELD_EQUATION_BOUNDARY.md).
The independent concepts, replacement precedence, and destination taxonomy are
specified in
[PROVENANCE_CLASSIFICATION_CORRECTION_PROPOSAL.md](PROVENANCE_CLASSIFICATION_CORRECTION_PROPOSAL.md).
Nothing in R1G applies that proposal to the fixed registries.

## Verification

The external verifier reconstructs the plan and affected universes without
importing the freezer/builder, recomputes every Git history and content
identity, exercises eight provenance/coverage catch-proofs—including the three
readout/action separation guards—replays all six frozen manifests and package
paths/blobs, checks current links
and all 306 frontier rows / 101 unique targets, confirms the known test
baseline, and compares the original dirty checkout's 54 paths by status/lstat
metadata only with contents marked `NOT_READ`.

The results are recorded in
[INDEPENDENT_VERIFY_RESULT.json](INDEPENDENT_VERIFY_RESULT.json), with output
hashes in [OUTPUT_SHA256SUMS.tsv](OUTPUT_SHA256SUMS.tsv).

## Stop condition

B02/B03 migration, classifier application, other migration, physics work, and
GPU work remain unauthorized. R1G stops at the audit/correction proposal.
