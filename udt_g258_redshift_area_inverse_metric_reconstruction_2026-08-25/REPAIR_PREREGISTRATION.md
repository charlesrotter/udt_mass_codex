# G258 external-review repair preregistration

Date: 2026-08-25

The fresh external `gpt-5.4` reviewer returned `ACCEPT_WITH_REPAIRS`. It accepted the bounded
scientific core and identified one provenance-certification weakness: `verify_package.py`
reconstructed the preregistration-era `CURRENT_SCIENTIFIC_PREMISES.tsv` hash by deleting the later
`G258` row when run in the live repository. The review found no algebraic, covariance, typing,
scientific-scope, or conclusion-ceiling defect.

## Frozen repair

R1. Replace every synthesized line-deletion compatibility path with exact byte retrieval:

- a sealed intake must hash its included source file byte-for-byte against `SOURCE_MANIFEST.tsv`;
- a live-repository replay may resolve the historical source only as the exact Git object
  `a9f96360:CURRENT_SCIENTIFIC_PREMISES.tsv`;
- the intake builder must copy that exact Git object rather than reconstructing it from the current
  registry;
- no verifier or builder may delete, filter, or rewrite registry rows to manufacture the frozen
  hash.

## Certification contract

1. The exact historical Git object must match the already frozen manifest hash
   `83b00d923de6163fa17c6f336b73baa977f8588e6ab2fd98c57ce17e1e78f441`.
2. Live-repository package verification must pass using exact-object resolution.
3. A newly built sealed intake must pass all manifest entries and all four registered replays.
4. Mutating one byte of the sealed premise source must make strict package verification fail.
5. The five regenerated scientific artifacts must remain byte-identical to their pre-repair forms.
6. The scientific landing, numerical values, premise grades, and conclusion ceiling may not change.

Maximum repair conclusion:

```text
G258_R1_EXACT_HISTORICAL_SOURCE_RESOLUTION_REPAIRED
__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED
__EXTERNAL_REPAIR_ONLY_FOLLOWUP_REMAINS_OPEN
```
