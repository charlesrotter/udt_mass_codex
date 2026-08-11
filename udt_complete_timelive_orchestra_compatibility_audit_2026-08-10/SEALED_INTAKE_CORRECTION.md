# Sealed-intake path correction

The authorized external intake contained 24 package files plus exactly 13 manifest-listed sources.
For isolation, those 13 sources were placed below `sources/` while their manifest identities
retained repository-relative paths. The historical `verify_preregistration.py` resolves only a
repository checkout and therefore failed in that transport layout.

No manifest row, source byte, preregistration artifact, or scientific result is changed.
`verify_sealed_intake.py` is the additions-only transport verifier. It accepts exactly one complete
layout:

- repository: `PARENT / manifest_path`; or
- sealed intake: `PARENT / sources / manifest_path`.

It fails if neither layout is complete, if any digest differs, or if a protected/stopped source is
named. The corrected sealed replay checks all 13 rows.
