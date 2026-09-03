# G334 driver-identified sealed-extra repair preregistration

Date: 2026-09-03
Status: `PREREGISTERED_BEFORE_REPAIR_EXECUTION`

The fresh external reviewer returned
`ACCEPT__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED` with no scientific repairs. During
post-review adjudication, the driver found one independent packaging defect: the preflight package
replay wrote an unmanifested `__pycache__` file inside the already sealed intake. The manifest and
all 36 registered payloads remained byte-exact, and the reviewer replayed from a writable copy, but
the intake contained one extra unregistered file. This is not acceptable as exact sealed closure.

## R1 — exact file-set closure

Repair `verify_review_intake.py` so it rejects both missing/changed registered payloads and every
unmanifested regular file other than `REVIEW_MANIFEST.tsv` and its detached seal.

## R2 — no-bytecode replay

Repair every registered replay command and subprocess invocation to use Python's no-bytecode mode,
so package verification cannot create `__pycache__` beside sealed evidence.

## Frozen repair gates

1. A newly built intake has exactly the builder-declared file count.
2. `verify_review_intake.py` passes the fresh intake.
3. Adding one ephemeral unmanifested file to a disposable copy makes verification fail.
4. Running the aggregate package replay directly inside a disposable intake copy leaves its exact
   regular-file set and all SHA-256 digests unchanged.
5. All 103 scientific aggregate gates still pass and all registered scientific outputs remain
   byte-identical.
6. The external verdict and bounded scientific landing remain unchanged.

Maximum repair conclusion:

```text
G334_SEALED_FILE_SET_AND_NO_BYTECODE_REPLAY_REPAIRED
__SCIENTIFIC_LANDING_UNCHANGED
```

The repair may not change any metric, response formula, branch, candidate classification, premise,
scope boundary, or scientific output.
