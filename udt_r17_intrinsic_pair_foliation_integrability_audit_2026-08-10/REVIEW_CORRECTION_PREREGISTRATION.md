# External-review correction preregistration

Date: 2026-08-10

External raw-review output SHA-256 before tracked terminal-newline normalization:

```text
cb63e12244103dc92bcc554297b7a44e2a8c7ca425453762c62beff3a885196a
```

Tracked `EXTERNAL_REVIEW_RAW.md` SHA-256 (same text with one terminal newline):

```text
d5a17ecc1d2319218488f91da778251f1ebe9bfe4e11268b622efa82d13eac45
```

The reviewer accepted the preregistered landing at its bounded conditional strength and identified
two repairable evidence/wording defects.

## Frozen corrections

1. Replace the local so-called independent verifier with a genuinely constructive standard-library
   implementation. It must:
   - invert the coframe independently;
   - derive Lie brackets from base structure constants and directional derivatives of the frame
     coefficients rather than assigning the final brackets;
   - derive the leaf pullback metric from the coframe and tangent columns rather than assigning its
     entries; and
   - test both Maurer--Cartan sign conventions across all six supplied `lambda` strata.
2. Restrict `contact` terminology to the spatial `S3` slices. In four dimensions call `H` a
   nonintegrable rank-two normal bundle, not a contact structure.
3. Preserve the raw review verbatim and do not strengthen its accepted landing.
4. Re-run all package, source, repository, frozen-manifest, link, frontier, and test gates.

## Acceptance criteria

- The constructive independent verifier must not import the production controller or assign the
  final pair/screen bracket or leaf-metric coefficients.
- Both Maurer--Cartan signs must leave `E` involutive and `H` nonintegrable.
- The external landing and every open path/reset/arrow/downstream scope must remain unchanged.

No new scientific question, branch, path, action, source, matter, bootstrap law, `X_max`, CMB
physics, signalling, or dynamics is authorized by this correction.
