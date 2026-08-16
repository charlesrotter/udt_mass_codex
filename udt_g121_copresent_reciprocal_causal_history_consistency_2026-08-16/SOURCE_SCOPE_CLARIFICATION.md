# G121 source-snapshot clarification

`SOURCE_MANIFEST.tsv` originally pointed to the live `CURRENT_SCIENTIFIC_PREMISES.tsv` at SHA-256
`db69a4fb...97d7b`. Before adding the G121 registry row, that exact byte-identical file was copied
to `PRE_G121_CURRENT_SCIENTIFIC_PREMISES.tsv`, and the manifest path was changed without changing
the registered hash. This preserves the exact premise state consulted and prevents the package
verifier from depending on a later live-registry edit.
