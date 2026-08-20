# G189 external-review repair preregistration

Date: 2026-08-20

## Trigger

The fresh sealed gpt-5.4 review returned:

```text
G189_ACCEPTED_WITH_REPAIRS
```

It retained all four scientific claims requested by the review and identified two evidence-quality
repairs:

1. the DES rows in `SOURCE_MANIFEST.tsv` use host-absolute paths, so the source-integrity check can
   inspect the host copy even when the numerical replay is pointed at sealed `external_data`;
2. the implementation-distinct replay recomputes from raw data but reads `PRODUCTION_RESULT.json`
   and judges its own success by agreement with that artifact.

## Bounded repairs

Before changing the implementation, preregister the following mechanical corrections:

1. Replace the two absolute DES manifest paths by logical `external_data/...` paths. Resolve those
   paths only through the declared `G189_DES_ROOT` data root, including in the intake builder.
2. Remove every read of `PRODUCTION_RESULT.json` from
   `verify_p1_free_flux_independent.py`. That script must calculate its result and internal algebraic
   gates from raw sealed inputs alone.
3. Move production-versus-independent numerical comparison into `verify_package.py`, where the two
   separately produced artifacts are joined explicitly.
4. Preserve the exact production scores, preregistered ceilings, scientific landing, imported
   transfer status, zero shape-parameter count, and regular-center type classification.
5. Bank the verbatim external verdict and a compressed raw transcript. A fresh sealed repair-only
   review remains required before describing the repair findings themselves as externally closed.

## Certification contract

- the production and implementation-distinct scripts must both replay from a fresh sealed intake
  when `G189_DES_ROOT` points to its local `external_data` directory;
- the production source-hash keys must contain no absolute host path;
- the implementation-distinct script source must not contain `PRODUCTION_RESULT.json`;
- independently computed Pantheon+ and DES chi-squares and offsets must agree with production within
  the existing tolerances;
- all original mutation catches, scope guards, source hashes, scores, and bounded landings must be
  unchanged;
- no scientific claim may be strengthened by these repairs.

## Maximum conclusion

At most these repairs can close the two evidence-quality defects named by the external reviewer.
They cannot alter or strengthen the bounded G189 scientific landing.
