# G236 repair-only follow-up review request

## Frozen prior finding

The fresh reviewer found no scientific, statistical, type, data-provenance, covariance, or hidden-
scaffolding error and independently reproduced every load-bearing G236 number. It returned
`G236_SCIENTIFIC_REPAIR_REQUIRED` solely because the first sealed intake did not carry independently
auditable preregistration chronology.

Do not repeat or broaden the research. Verify only the registered evidence repair and whether the
bounded scientific landing remains byte-identical.

## Required repair checks

1. Recompute the Git object ID of each `GIT_OBJECTS/*_commit_object.txt` with
   `git hash-object -t commit --stdin` and verify exact matches to `184b1a78...` and `318f35de...`.
2. Verify the raw `318f35de...` commit object names `184b1a78...` as its sole parent.
3. Inspect the recursive committed-tree listings and confirm that production code,
   `PRODUCTION_RESULT.json`, `STATE_RECONSTRUCTION.tsv`, and `INDEPENDENT_VERIFICATION.json` are
   absent from both preregistration trees.
4. Inspect `GIT_OBJECTS/318f35de_exact_patch.txt` and confirm the repair commit changed only
   `PREREGISTRATION.md` and added `PREREGISTRATION_REPAIR.md`; it touched no code, data, state, or
   outcome artifact.
5. Independently inspect the production dataflow. Confirm that the state resolutions and scientific
   landing are computed without the `hostile` object, before that object is constructed; the
   repaired hostile is only a certification gate and reported metadata.
6. Verify `CHRONOLOGY_AND_NONINTERFERENCE_PROOF.json` matches these independent checks and retains
   the explicit limit that Git cannot prove the retroactive absence of an untracked private
   computation.
7. Verify the original production, independent, and scientific-landing artifacts are unchanged
   from the first sealed intake hashes recorded in the new scope.

## Required verdict

Return exactly one:

- `G236_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_RETAINED`
- `G236_REPAIR_ACCEPTED_WITH_CAVEATS`
- `G236_REPAIR_INCOMPLETE`
- `G236_REPAIR_INVALIDATES_PRIOR_LANDING`

State explicitly whether any scientific or numerical result changed. Separate required repairs
from optional improvements.
