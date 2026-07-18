# R1A inbound-reference correction preregistration

- Date: 2026-07-18
- Correction base: `65b7f861ccbffc6b8623ea73035050b3d62fff92`
- Literal comparison base: `4c98e32d7b8af0dc3159706d18006d673566d721`
- Branch: `codex/reorg-r1a-2026-07-18`
- Trigger: an independent audit found that the original right-boundary regex
  treated sentence punctuation `.` as a filename-continuation character.

## Historical-evidence firewall

The original preregistered R1A adjudication and migration artifacts remain
unchanged as the exact historical record of the first run. In particular, do
not rewrite or regenerate in place:

- `ADJUDICATION_SUMMARY.json`;
- `CANDIDATE_ADJUDICATION.tsv`;
- `ELIGIBLE_BATCH.txt`;
- `INBOUND_REFERENCES.tsv`;
- `POINTER_REWRITE_PLAN.tsv`;
- `PREMOVE_HASHES.tsv`;
- `PREMOVE_ADJUDICATION_REPORT.md`;
- `PREMOVE_VERIFY_RESULT.json`;
- `MOVE_MAP.tsv`; or
- `POSTMOVE_POINTER_CENSUS.tsv`.

The correction must add separately named corrected/consolidated tables under
this directory. Only the five enumerated live pointer sources and the R1A
audit report/index may be edited.

## Expected correction claim

The independent audit reports 14 omitted occurrences. The corrected base
census is expected to contain exactly:

- 815 occurrences;
- 92 distinct source paths; and
- 16 occurrences whose source is formally `FROZEN_EVIDENCE` under the R0
  classification/prefix rule.

These are audit expectations, not values to force. A scanner and an independent
literal `git grep -F` implementation must reproduce them exactly at `4c98e32`,
or the correction stops without pointer mutation.

## Boundary contract

For a candidate filename token:

- `file.md.` must match (`.` is sentence punctuation at end or before
  non-filename punctuation/space);
- `file.md)` must match; and
- `file.md.bak` must not match because the following dot begins an
  alphanumeric filename suffix.

The corrected implementation must include executable catch-proofs for all
three cases. It must independently compare every corrected occurrence key
`(target, source, line, column)` with literal `git grep` results from the fixed
base.

## Fixed omission dispositions

Exactly five omitted occurrences are expected to be stale non-frozen live
pointers and are authorized for path-only substitution:

1. `HANDOFF_ARCHIVE.md`: `PROVENANCE_AUDIT_2026-06-30.md`;
2. `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md`:
   `STEP2_timelive_matter_results.md`;
3. `HANDOFF_ARCHIVE.md`: `coupled_timelive_VERIFIER.md`;
4. `archive/tier_d_round3_contract.md`: `lepton_ladder_test_results.md`; and
5. `NEGATIVES_REGISTRY.md`: `weld_discriminator_results.md`.

The occurrence in
`archive/pre_native_coupled/timelive_nonround_native_solve_results.md` pointing
to `timelive_nonround_VERIFIER.md` is expected to be an intentional reference
to the co-located archived copy and requires no rewrite. The remaining eight
omissions are expected to name retained targets and therefore require no path
change. Every omission receives an explicit row and disposition.

## Revalidation gates

Before banking the correction:

1. original historical tables are byte-identical to correction base `65b7f86`;
2. the corrected census is exactly 815/92/16 and agrees occurrence-for-
   occurrence with literal Git grep at `4c98e32`;
3. the three boundary catch-proofs pass and fail red under their corresponding
   deliberate mutations;
4. exactly the five authorized live pointer tokens change, with no other byte
   changes in those sources;
5. the co-located archive reference is present, intentional, and unchanged;
6. all eight other omitted occurrences point to retained targets;
7. all 17 moved files remain eligible under the corrected census;
8. every moved destination still has its original Git blob/SHA-256 payload;
9. all six frozen package manifests and complete tracked package states remain
   identical to R0;
10. the corrected post-move audit finds zero stale non-frozen pointers;
11. the original dirty checkout still matches the 54-row metadata-only census;
12. `python3 -m pytest tests/` remains at 69 passed, 1 xfailed, and the one
    known hygiene-header failure; and
13. the report/index carries a prominent correction layer without erasing the
    original counts.

Maximum conclusion: the R1A archive move remains topology-safe after repairing
the reference-census blind spot. This correction changes no physics status and
does not authorize R1B.
