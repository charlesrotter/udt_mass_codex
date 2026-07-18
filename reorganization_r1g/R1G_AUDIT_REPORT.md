# R1G provenance-classification audit report

## Verdict

The reported classification defect is reproduced. R1F remains clean, while B02
and B03 are blocked and unauthorized. The fixed R1C rule classified every
eligible `cascade_*` path as pre-native from its prefix, and R1E propagated that
label into a pre-July archive destination without operator-lineage evidence.

No research artifact, fixed R0–R1F record, current registry, script, evidence,
data file, or manifest was changed by R1G. This directory is an additions-only
correction overlay.

## Independent census

- The fixed R1C ownership registry contains 138 `cascade_*` rows.
- Exactly 121 carry the prefix-produced pair `LEGACY_FROZEN` /
  `PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE`.
- Git history places 61 introductions on July 2 and 60 on July 3.
- The 121 affected rows resolve into 15 coherent introducing-commit/family
  groups: 116 `NATIVE_2026-07-01` and 5 `MIXED`; none is proven `PRE_NATIVE`.
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
| Operator provenance | `NATIVE_2026-07-01` | 26 |
| Operator provenance | `MIXED` | 5 |
| Operator provenance | `OPEN` | 1 |
| Operator provenance | `PRE_NATIVE` | 0 |
| Scientific lifecycle | `HISTORICAL` | 32 |
| Primary owner | `FOUNDATIONS` | 27 |
| Primary owner | `MACRO` | 3 |
| Primary owner | `PARTICLE_MASS` | 2 |
| Migration safety | `BLOCKED_PROVENANCE_CORRECTION_REQUIRED` | 32 |

The mixed rows are `cascade_bv16_cas.py`, `cascade_or_energy_cas.py`,
`phi_source_derivation.py`, `homog_alpha_test.py`, and
`verify_universe_bv2_f_einstein.py`. They combine the native lineage with,
respectively, reference Einstein/Misner-Sharp readouts or imported alpha/source
conventions. `verify_redshift_profile_derivation.py` is `OPEN`: it is a
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
identity, exercises the three provenance catch-proofs plus coverage checks,
replays all six frozen manifests and package paths/blobs, checks current links
and all 306 frontier rows / 101 unique targets, confirms the known test
baseline, and compares the original dirty checkout's 54 paths by status/lstat
metadata only with contents marked `NOT_READ`.

The results are recorded in
[INDEPENDENT_VERIFY_RESULT.json](INDEPENDENT_VERIFY_RESULT.json), with output
hashes in [OUTPUT_SHA256SUMS.tsv](OUTPUT_SHA256SUMS.tsv).

## Stop condition

B02/B03 migration, classifier application, other migration, physics work, and
GPU work remain unauthorized. R1G stops at the audit/correction proposal.
