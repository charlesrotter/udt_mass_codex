# Research registry semantics

The registry supports artifact navigation and repository reorganization. It does not determine
scientific premise meanings or current execution status.

## Current-path table

Use `CURRENT_ARTIFACT_PATHS.tsv` to locate current artifacts. Its entries are operational pointers,
not scientific verdicts.

## Immutable historical tables

R0-R1C ownership, readiness, census, preregistration, and verification records are fixed snapshots
of the evidence state in which they were created. Do not rewrite them to point at newer layouts or
to make a historical package appear current.

## Precedence

1. Root `LIVE.md` controls current status.
2. Root `CURRENT_SCIENTIFIC_PREMISES.tsv` controls exact premise classification and cites its
   load-bearing sources.
3. A package's own preregistration, raw evidence, and verification control its bounded result.
4. Registry paths only answer where an artifact lives.

If these roles are confused or a path is missing, stop and report the mismatch. Do not infer a new
scientific conclusion from registry housekeeping.

The verbose pre-cleanup registry orientation is preserved at
`../../archive/startup_surface_2026-08-14/research_registry_README_before_cleanup.md`.
