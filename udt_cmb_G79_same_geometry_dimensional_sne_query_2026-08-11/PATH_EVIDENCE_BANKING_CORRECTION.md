# G79 path-evidence banking correction

Date: 2026-08-11

Status: `REPOSITORY_BANKING_DEFECT_CLOSED__SCIENTIFIC_STATUS_UNCHANGED`

The ignored local file `PATH_EVIDENCE.npz` is now tracked without regeneration or byte changes.
Its SHA-256 remains
`3f61f35f57b06f4407a7c9b98a75e37c929a6ce71fe180f7fe93d2e3ba765cd7`, exactly matching the
pre-existing `REVIEW_MANIFEST.tsv` row transmitted to and verified by the external reviewer. Its
size remains `120575` bytes.

The correction is additions-only. No G79 scientific prose, result, preregistration, sealed
manifest, raw review, or adjudication was rewritten. G79 remains
`VERIFIED_WITH_CAVEATS__BOUNDED_SAME_GEOMETRY_REDSHIFT_AND_ANGULAR_DISTANCE_QUERY`.

`verify_banked_path_evidence.py` independently checks Git tracking, byte length, SHA-256, and the
sealed-manifest identity. The repair closes only fresh-clone availability of the saved path field.
