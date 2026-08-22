# G223 repair implementation

Date: 2026-08-22

Repair preregistration commit: `8d502ec5`.

## R1 — true read-only replay

Both production scripts now accept `--check-only`. They execute the complete registered algebra and
construct their result payloads in memory without opening any evidence file for writing.
`verify_package.py` invokes only those check-only paths.

The registered verifier was then run from a fresh intake after write permission was removed from
every intake file and directory. It passed.

## R2 — nonvacuous independent fiber integration

The former `density == density` loop was removed. For 1,000 independent exact-rational controls,
the verifier now samples positive `a`, two independent affine fiber parameters, and an arbitrary
base offset, then checks

\[
(a\lambda_2+s_0)-(a\lambda_1+s_0)=a(\lambda_2-\lambda_1).
\]

The total independent count remains 361,001 because each repaired assertion replaces one vacuous
assertion.

## R3 — sealed source containment

Manifest paths are rejected if absolute or parent escaping. Every resolved source must remain
beneath the verifier root. The intake builder records that frozen sources are copied at
repository-relative paths inside the intake root, allowing the unchanged verifier to resolve all
seven sources without leaving the sealed intake. Two hostile path controls—one absolute and one
parent escaping—are rejected.

## Grade

```text
FRESHLY_ADVERSARIALLY_VERIFIED_AFTER_REPAIRS
```

The sealed repair-only follow-up returned `REPAIRS_ACCEPTED`. The bounded scientific landing and
all premise ceilings are unchanged.
