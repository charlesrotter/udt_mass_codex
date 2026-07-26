# Source-manifest correction 01

This is an append-only correction to `SOURCE_MANIFEST_AMENDMENT_01.tsv`.
The original amendment remains unchanged as historical evidence.

Independent source verification found that the S17 SHA-256 value was transcribed
with one missing `b`.  The path, size, source role, and source universe do not
change.  Direct hashing of the working-tree file and `git show` from frozen base
`c1036fb498c8ed009733c82ee86cf96152a5ed6e` both give:

`8337c04d5b5b5aac858e980baa937771060bced8db4eecf8362b630d7815f4df`

All source-integrity verification after this correction must apply
`SOURCE_MANIFEST_CORRECTION_01.tsv` as an overlay to S17.  No generated scientific
classification is changed by this clerical correction.
