# Post-review correction preregistration

Date: 2026-08-05  
Parent: `db862ea4`  
Mutation not yet performed

## Findings to correct

1. The cold reviewer found that source-locator rows `L13`-`L16` describe the frozen pre-mutation
   controls but do not say so. Their line ranges now resolve to corrected current text.
2. Independent post-review inspection found that the date-only `F18_EARLY_POSTJULY_FIELD_SOLVER`
   rule catches three sources in the presently load-bearing founding chain:
   `UDT_NATIVE_ACTION_COLD_PACKET.md`,
   `UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md`, and
   `verify_udt_reciprocal_c_postulate.py`. Calling them
   `HISTORICAL_SUPERSEDED_NO_ACTION` contradicts their registered current use. This repeats the
   provenance-by-date error pattern previously found in the cascade reorganization audit.

## Frozen correction contract

- Preserve the original commits and frozen universe unchanged.
- Add a snapshot-semantics column to the locator table. `L13`-`L16` must point explicitly to base
  `682adb6c9d4cc7c9834cb5ea6a7712a32206650b`; current control locations must be recorded separately.
- Freeze and individually list all 254 rows selected by the old date-only F18 rule before changing
  its effective outcome.
- Reclassify only the three named current founding-chain sources as
  `CONDITIONAL_REINTERPRETATION_ONLY`; their exact algebra is current but all supplied-depth,
  readout, profile and action caveats remain.
- Retain the other 251 F18 rows as `HISTORICAL_SUPERSEDED_NO_ACTION`, with an explicit per-row or
  coherent-family reason rather than date alone.
- No row becomes native physics, move-ready, a selected action/source, or `REDERIVATION_REQUIRED`.
- Update all counts, identity hashes, verifier expectations and current top summaries exactly.
- Make the repository-gate replay use an explicit writable temporary directory without changing
  the tested suite.
- Add mutations that reject reclassification of any named founding-chain source as historical and
  reject a locator that lacks snapshot semantics.

Maximum conclusion: classifier and locator precision repair only. No new physics follows.
