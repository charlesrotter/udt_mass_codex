# Fourth-review evidence-closure correction preregistration

Date: 2026-07-22

The final closure review returned `FAIL`. It independently preserved the repaired covariance,
toric/seed evidence, 29 mutation catches, scientific premise ledger, and `LEAD` status. It found two
evidence-banking defects:

1. the committed closure state omitted the generated atlas results, registry, and compressed raw
   ledgers required by `verify_package.py`;
2. `build_correspondence_atlas.py` still emitted the older eight-row lineage table, while the
   corrected validator and current package require ten rows including the two direct production
   source manifests.

## Frozen correction scope

No scientific calculation, raw row, count, premise, status, tolerance, or maximum conclusion may
change. The correction is limited to:

- add the exact amplitude-volume and joint-invariant source-manifest hashes already present in the
  corrected `SOURCE_LINEAGE.tsv` to the production builder's source table;
- preserve their role as `DIRECT_PRODUCTION_SOURCE_MANIFEST` while all other roles remain
  `FROZEN_SOURCE`;
- freeze every generated result, raw ledger, transcript, adjudication, and package document needed
  for a clean committed-tree replay;
- generate a complete package SHA-256 manifest;
- require a clean `git archive` of the resulting commit to run `verify_package.py` without copying
  any untracked evidence into it;
- test that the builder's lineage-generation function yields the exact current ten-row table without
  rerunning the expensive atlas solely for this metadata correction.

The complete atlas need not be recomputed because its source inputs, algorithms, and saved outputs
are unchanged; the builder edit affects only the separately written lineage table and preflight hash
checks.

## Maximum allowed conclusion

Unchanged:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The correspondence remains `LEAD`. A final fresh review must distinguish reproducible package
closure from any scientific promotion.
