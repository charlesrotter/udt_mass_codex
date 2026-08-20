# G194 repair-only external follow-up

Date: 2026-08-20

Reviewer: fresh external Codex `gpt-5.4`, high reasoning, web disabled, read-only sealed intake.

## Landing

`G194_REPAIRS_REJECTED`

## Findings

1. `R1` failed.  Pinning `tempfile.tempdir` bypassed discovery, but the exact registered replay
   still exited nonzero when a downstream Torch import called `tempfile.TemporaryDirectory()` and
   attempted to create a directory on the read-only filesystem.  `.review_runtime` remained empty.
2. `R2` passed within the sealed intake.  The package verifier no longer executes the ambient
   repository premise verifier and reads repository-root evidence only through the frozen source
   manifest.
3. `R3` passed.  The exact machine-readable independence grade
   `METRIC_JET_RIEMANN_SPOTCHECK_PLUS_FORMULA_DRIVEN_MATRIX_IVP` is present and matches the original
   review qualification.
4. The original bounded scientific landing was unchanged.  The failure was packaging-only and did
   not refute the arbitrary-symmetric-matrix theorem in its declared family and germ.

## Replay result

The exact registered no-write command failed during the independent verifier because Torch's lazy
distributed-module import attempted a real temporary-directory creation.  No workaround was used.

## Maximum conclusion

The repair cycle remains rejected until the exact sealed read-only replay passes.  `R2`, `R3`, and
the bounded G194 scientific landing are retained; `R1` must be superseded by a separately
preregistered verifier-only repair.
