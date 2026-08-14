# R3 patch-cardinality correction — outcome

Date: 2026-08-13
Grade: `VERIFIED__BOUNDED_OPERATIONAL_REPAIR`
Production state: `NOT_RUNNING__FRESH_RESTART_REQUIRED`

## What failed

The guarded R3 run atomically completed `48/194` North selections and stopped on the first South
`DR` component. TreeCorr had accepted a common declared patch count for the data and random
catalogs, then independently replaced it with `max(patch)+1` while loading each per-object patch
array. The first South data catalog lacked the terminal occupied label and therefore reached the
cross-correlation with a smaller inferred patch cardinality than its random catalog.

This was a representation failure inside the numerical engine boundary. It was not an R3 covariance
observation and supplied no feature, scale, or physics result.

## Correction

`run_r3_covariance_atlas.py` now supplies TreeCorr its public list-of-catalogs form: one nonempty
single-patch child for every occupied frozen fine patch. Every child retains:

- its original global integer patch ID;
- the common full registered patch count;
- exactly the original rows and weights for that patch.

No sky position, HEALPix membership, block parent, angular bin, pair estimator, normalization,
covariance formula, rank rule, weight lane, selection, or tolerance changed. New checkpoint metadata
pins the correction preregistration and the representation string
`explicit_nonempty_single_patch_catalog_lists_v1`.

The guarded service wrapper now uses `set -euo pipefail`; a deliberate Python exit `7` propagates as
exit `7` through `python | tee` rather than being reported as success.

## Verification

The final fail-closed verifier pins TreeCorr `5.1.3` and production SHA-256
`a09d287b24ce662ced9e986d0480ffc94caf54962c3205ea81ba2a1e8b2f7840`.

- The legacy whole-catalog construction reproduces the exact cardinality exception.
- Nonconsecutive global labels `{0,2,7}` and `{0,2,5}` exercise internal holes plus data-only and
  random-only patches on a nine-patch atlas.
- Child IDs, cardinality, ordered RA/DEC/weight membership, and exactly-once row coverage pass.
- Central DD/DR/RR integer counts are exact and weighted residuals are zero in the synthetic check.
- Twelve literal deletion checks—four occupied union blocks times DD/DR/RR—are exact with zero
  weighted residual.
- The first South real cell completes all nine central comparisons; maximum relative weighted
  difference from frozen R2 is `8.670449712771705e-10`.
- A North replay reproduces all seven stored central arrays; its maximum relative weighted difference
  from frozen R2 is `2.316075357408534e-10`.
- All `48` legacy checkpoint filenames and metadata were censused. Each has the exact old production
  hash and lacks the two new provenance fields.
- Repository tests pass: `103 passed, 1 xfailed`.

A fresh zero-context adversarial review traced TreeCorr's source, independently tested nonconsecutive
patch IDs, identified two rounds of verifier hardening, and finally returned `VERIFIED` for the closed
harness changes. It did not run the real cells or inspect covariance outcomes; the main verification
run separately executed those preregistered gates.

## Checkpoint and restart decision

The old `48` cells are valid provenance for the stopped program but are not reusable under the exact
checkpoint contract. Every old cell differs from the corrected contract in exactly:

1. production script SHA-256;
2. correction-preregistration SHA-256;
3. explicit TreeCorr patch-representation identifier.

R3 must therefore restart from an empty checkpoint directory. This is deliberate contract honesty,
not a scientific rejection of the completed North cells.

## Evidence gates

1. **Preregistered:** yes, commit `bdd9869f` preceded code changes and tests.
2. **Full or bounded scope:** bounded operational repair; one synthetic adversarial geometry and two
   preregistered real structural cells. No covariance outcome claim.
3. **Independently verified:** yes for the TreeCorr mechanism and representation semantics; real-cell
   gates were executed by the main verifier with an independent North stored-array comparison.
4. **Premises audited:** yes; no scientific or statistical premise changed.

## Maximum conclusion

`VERIFIED`: explicit nonempty single-patch catalog lists preserve R3's frozen global patch atlas and
central/deletion semantics under TreeCorr `5.1.3`, and the service wrapper now reports Python failure.
A fresh complete R3 production run is authorized operationally.

Nothing here establishes an R3 covariance outcome, BAO feature, significance, physical scale, UDT
response, CMB relation, cosmology, or `X_max`.
