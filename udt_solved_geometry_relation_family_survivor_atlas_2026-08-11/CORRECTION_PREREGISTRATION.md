# Post-review correction preregistration

Date: 2026-08-11

The external reviewer accepted the scientific landing and found two transport/replay defects:

1. repository-root source paths are relocated beneath `sources/` in the sealed intake, while the
   repository verifiers understand only the first layout;
2. `run_catch_proofs.py` regenerates evidence and therefore cannot be run in a read-only intake.

Before repair, this record freezes an additions-only correction:

- preserve all original preregistration, numerical scripts, outputs, tables, classifications, and
  source-manifest rows byte-identically;
- add a read-only verifier accepting exactly one complete source layout: repository-root or sealed
  `sources/`, rejecting mixed/partial resolution;
- add a read-only verifier for the already-generated catch-proof records; do not pretend this
  independently re-executes the mutating catch generator;
- freeze and replay the exact original 50-file intake inventory and hashes;
- record the external review and adjudication;
- change no scientific result, threshold, sample, path, field, or landing.

Catch conditions:

- a missing, duplicate, extra, hash-mismatched, protected, or stopped-draft intake path fails;
- a mixed repository/sealed source layout fails;
- a mutated catch-proof row or summary fails;
- the original 28 package files and 22 source files in the reviewed intake remain exact.
