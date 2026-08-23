# G225 repair R2 preregistration — sealed ancestry proof

Date: 2026-08-22

## Trigger

The R1 follow-up reviewer confirmed the repaired aggregate replay, unchanged science, and all
sealed hashes, but returned `G225_REPAIR_INCOMPLETE` because the sealed intake did not carry
independently verifiable Git ancestry for the repair preregistration and implementation commits.

## Frozen repair R2

The next intake builder will include the raw Git commit payloads for:

1. R1 preregistration commit
   `78818a4818fc20f2e45efbec8b844772f6901cab`;
2. R1 implementation commit
   `6db43e9606acce0bcfc41a5e7557d9f1c514d292`;
3. this R2 preregistration commit; and
4. the intake-builder implementation `HEAD`.

Before building, it will fail closed unless:

- the R1 preregistration is an ancestor of the R1 implementation;
- the R1 implementation is an ancestor of `HEAD`;
- the R2 preregistration is an ancestor of `HEAD`.

The raw commit payloads will be listed in `PAYLOAD_MANIFEST.tsv`. A sealed reviewer must be able to
recompute each Git commit object hash from its raw bytes and inspect its `parent` field. For this
linear repair sequence, the R1 implementation must name the R1 preregistration as its parent, and
the intake-builder implementation commit must name this R2 preregistration as its parent.

## Forbidden changes

Do not alter mathematical scripts, result payloads, counts, theorem wording, premises, the R1
source-resolution repair, or the scientific landing.

## Maximum conclusion

If the raw commit objects validate and the sealed aggregate replay remains exit zero without hash
changes, conclude only:

```text
G225_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
```
