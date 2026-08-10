# Post-review correction

Date: 2026-08-10

The first external reviewer returned `TYPE_FAILURE`. The scientific 120-cell shape was reproduced,
but the review correctly rejected the evidence package because its verifier expected a Git object
store and its atlas carried inherited evidence labels outside the exact source manifest.

The correction makes no scientific promotion or candidate change:

- the 24 identities and five candidate families are unchanged;
- the 24 frozen source bytes and their manifest are unchanged;
- atlas evidence now cites only the consolidated, manifested records actually used by the
  classification;
- Git blob identities are reconstructed directly as `SHA1("blob <size>\\0" + bytes)`;
- all 24 paths, sizes, SHA-256 values, and blob identities are checked from materialized intake
  bytes; and
- production, independent verification, and catch proofs now expose non-mutating `--check` modes.

The corrected local result remains a `LEAD`. It cannot become `VERIFIED-WITH-CAVEATS` unless a fresh
manifest-confined external review accepts the scientific ownership ruling.
