# Research registry semantics

The registry supports artifact navigation and repository reorganization. It does not determine
scientific premise meanings or current execution status.

## Relocation table

Despite its historical filename, `CURRENT_ARTIFACT_PATHS.tsv` is the 1,115-row relocation ledger
produced by the repository reorganization. Query it for a known old path. It is not a startup read,
not a current-frontier index, and not guaranteed to include packages created after that snapshot.
Use root `INDEX.md` for the compact current-frontier paths.

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

The pre-zoomout registry orientation is preserved at
`../../archive/startup_surface_2026-08-17_pre_zoomout/research_registry_README.md`; the earlier
verbose version remains at
`../../archive/startup_surface_2026-08-14/research_registry_README_before_cleanup.md`.
