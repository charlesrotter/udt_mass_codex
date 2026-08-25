# G253 repair preregistration

Date: 2026-08-24

Trigger: fresh external `gpt-5.4` adjudication `REPAIRS_REQUIRED` on the sealed intake at
`/tmp/udt_g253_review_xcnll8p9`.

## Frozen scientific landing

The following bounded landing is not being changed by this repair:

```text
MIXED_STATUS_NATIVE_CHAIN_COMPRESSES
__DIRECT_RECIPROCAL_REDSHIFT_IS_CONDITIONAL
__ANGULAR_RESPONSE_IS_A_DISTINCT_SIBLING
__ABSOLUTE_SCALE_ATTACHMENT_IS_DOWNSTREAM
```

No source, premise status, node, edge, formula, historical-control disposition, observational
value, fitted coefficient, physical history, branch population, or protected package may be added
or changed during this repair.

## R1 — dual-layout source resolver

The production replay, independent replay, and package verifier shall resolve each manifest source
from exactly one of two allowed layouts:

1. repository layout: `<root>/<manifest-relative-path>`;
2. sealed layout: `<root>/sources/<manifest-relative-path>`.

Resolution must be hash-aware. No existing candidate whose SHA-256 disagrees with the manifest may
be silently ignored. If both candidates exist, both must match the registered hash or the replay
must fail. Missing or mismatched sources must fail closed.

## R2 — hostile path-resolution coverage

The registered hostile checks shall explicitly prove:

- repository-layout resolution succeeds for a matching source;
- sealed-layout resolution succeeds for a matching source;
- a missing source is rejected;
- a mismatched source is rejected;
- conflicting repository and sealed candidates are rejected.

These are certification tests only and may not alter the scientific result counts except the
registered hostile-catch count.

## R3 — sealed replay closure

Build a fresh sealed intake and run, from that intake:

```text
python3 <package>/derive_native_kernel_compression.py --no-write
python3 <package>/verify_native_kernel_compression_independent.py --no-write
python3 <package>/run_catch_proofs.py --no-write
python3 <package>/verify_package.py
```

All must exit zero. The regenerated production and independent JSON objects must be byte-for-byte
or object-equal to the stored results. The catch result may change only by the preregistered R2
path-resolution catches.

## Maximum repair conclusion

Successful local and sealed replays establish only that the original bounded scientific landing is
reproducible under both repository and sealed source layouts. They do not strengthen it. A fresh
external repair-only follow-up remains required for external verification.
