# External-review correction preregistration

Date: 2026-08-10

Trigger: the first manifest-confined external review returned `TYPE_FAILURE`.

## Frozen failure

The first review is preserved verbatim in substance in `EXTERNAL_REVIEW_RAW.md`. Its decisive findings are accepted:

1. the independent verifier must not require a Git object store unavailable to the sealed intake;
2. every generated atlas evidence path must resolve to an exact `SOURCE_MANIFEST.tsv` row;
3. read-only review mode must verify cached outputs without rewriting them; and
4. a cached internal count reproduction is not an external scientific acceptance.

## Authorized correction scope

The correction will:

- add a non-mutating `--check` mode to the production derivation, independent verifier, and catch-proof runner;
- replace Git-object verification with direct SHA-256 and Git-blob reconstruction from the exact materialized manifest paths;
- make every atlas evidence citation resolve to a listed manifest source, using the already-frozen consolidated branch and transition records rather than silently depending on unmanifested ancestors;
- add exercised fail-closed proofs for a missing manifest source, a hash mismatch, an unmanifested atlas citation, an attempted write in check mode, and the original scientific overclaims;
- regenerate the result tables and hashes without changing the preregistered candidate universe or verdict choices; and
- request a fresh external review only from a newly sealed intake containing the corrected package and the same exact 24 manifested private sources.

## Immutable scope

The source base `9eb88898141dc7ada96bdf5a3aca450e1a2b5a46`, 24-row source manifest, 24 branch identities, five candidate families, and original external failure remain historical evidence and will not be rewritten.

No scientific verdict will be banked unless the corrected package passes a fresh external review. A scientific demotion required by that review will be accepted; the correction may not promote any owner beyond the preregistered maximum.
