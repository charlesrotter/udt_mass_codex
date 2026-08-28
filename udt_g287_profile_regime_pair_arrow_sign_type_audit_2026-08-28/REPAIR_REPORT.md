# G287 external-review repair report

Date: 2026-08-28
Status: `R1_R3_EXTERNALLY_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`

## R1 — executable hostile mutations

`run_catch_proofs.py` now applies six actual semantic/algebraic mutants. It verifies correct
baselines, requires the exact six-name mutation registry, and fails if any mutant survives or the
registry is emptied. The frozen result records 6/6 caught.

## R2 — aggregate replay

`verify_package.py` now requires and executes production, independent, hostile, repair-hostile,
source-manifest, and review-intake builders. It verifies exact frozen results, rebuilds and compares
the source manifest, verifies the new intake's manifest/scope/detached seal, and replays the four
load-bearing commands from the sealed intake. A broken review builder is rejected.

## R3 — complete dependency-source enforcement

Every one of the 22 dependency rows now carries a sealed evidence path and normalized marker.
Production requires exactly the frozen dependency names, uniqueness, source-manifest membership,
and successful resolution of all 22 markers. G269/G270 resolve through their exact rows in
`CURRENT_SCIENTIFIC_PREMISES.tsv`.

## Hostile repair evidence

`run_repair_catch_proofs.py` uses bounded disposable source/package copies. It confirms rejection
of:

- an empty mutation registry;
- a surviving profile-reversal mutant;
- a broken review-intake builder;
- a changed dependency marker;
- a missing G286 dependency row.

All 5/5 probes pass. No scientific formula, source, premise, or conclusion changed.

The repair-only external follow-up independently replayed the seven registered commands and direct
hostile variants, then returned
`REPAIRS_ACCEPTED__BOUNDED_G287_LANDING_UNCHANGED`. No scoped repair remains.

## Retained landing

```text
PROFILE_REGIME_SIGN_AND_PAIR_ARROW_ORIENTATION_ARE_ALREADY_TYPE_DISTINCT
__NO_NATIVE_KERNEL_REGRESSION
__RECENT_EXPLANATION_CONFLATED_THEM
```
