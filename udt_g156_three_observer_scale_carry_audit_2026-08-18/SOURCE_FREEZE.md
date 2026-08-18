# G156 source freeze

- Frozen source-payload commit: `b42c771d`
- Preregistration commit: `7075abcc`
- Frozen source count: 19
- Source identity: exact path, byte count, and SHA-256 in `SOURCE_MANIFEST.tsv`
- Protected local packages: excluded and untouched
- Observational outcomes: excluded

Later edits to live startup documents do not alter this source universe. Any source drift invalidates
the registered run until it is explicitly reconciled.

All 19 manifest payloads are byte-identical at the source-payload and preregistration commits. The
production and independent verifiers intentionally read them from `b42c771d`.
