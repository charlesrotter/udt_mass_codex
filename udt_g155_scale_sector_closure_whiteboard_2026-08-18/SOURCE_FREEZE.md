# Source-freeze interpretation

The 41 paths in `SOURCE_MANIFEST.tsv` are frozen by their recorded SHA-256 and byte count at the
preregistration commit `2f5cf474`.

`CURRENT_SCIENTIFIC_PREMISES.tsv` and `CURRENT_RESEARCH_PROGRAM.md` are live authority files and
may lawfully change after this package is banked. Reproducibility therefore means checking the
recorded payloads from Git commit `2f5cf474`, not requiring a future worktree copy of a live file to
retain its preregistration hash. The derivation and independent verifier use that immutable Git
snapshot. This is a packaging clarification only; no source, role, result, or landing changed.
