# G79 path-evidence banking correction preregistration

Date: 2026-08-11

Base: `c69fb470e3e541093aa34478deae90981fdd256a`

## Defect

`PATH_EVIDENCE.npz` was present in the G79 working package, included in the sealed external-review
intake, and recorded in `REVIEW_MANIFEST.tsv`, but the repository-wide NPZ ignore rule prevented it
from entering commit `3aada07d`.

The reviewed bytes are already fixed by the sealed row:

```text
path   = udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/PATH_EVIDENCE.npz
sha256 = 3f61f35f57b06f4407a7c9b98a75e37c929a6ce71fe180f7fe93d2e3ba765cd7
size   = 120575 bytes
```

## Authorized additions-only repair

1. Add exactly those already-reviewed bytes with a forced Git add.
2. Add a correction report and a fail-closed verifier that require the path to be tracked and its
   SHA-256 to equal the existing sealed-manifest row.
3. Do not regenerate, modify, or reinterpret the NPZ.
4. Do not rewrite the G79 preregistration, result, review, adjudication, or existing manifests.
5. Re-run the G79 external-review verifier, premise guards, tests, frozen manifests, and current
   path checks.

## Maximum conclusion

This may close only a repository-banking/reproducibility defect. It cannot strengthen or alter the
G79 scientific status.
