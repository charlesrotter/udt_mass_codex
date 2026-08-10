# Post-review correction layer

Date: 2026-08-10

Preregistered by `REVIEW_CORRECTION_PREREGISTRATION.md` before repair.

## Corrections made

### Constructive independent verifier

`verify_integrability_independent.py` now obtains every load-bearing local quantity from its
inputs:

- it inverts the coframe by standard-library exact-rational Gauss--Jordan elimination;
- differentiates the inverse with `dF=-F(dA)F`;
- reconstructs brackets from the base Maurer--Cartan structure constants and directional
  derivatives;
- pulls the leaf metric back from the coframe and derived tangent columns; and
- repeats the audit for both Maurer--Cartan sign conventions and all six supplied `lambda` strata.

It neither imports the production controller nor assigns the final bracket or leaf-metric
coefficients. The corrected independent result is 72/72 exact `Fraction` checks.

### Dimensional terminology

All active scientific statements now call `H` a nonintegrable rank-two normal bundle in the full
four-dimensional spacetime. Its restriction to a spatial `S3` slice is the contact plane
`ker(sigma3)`. Historical preregistration and dispatch text is preserved.

### Catch-proof

`verify_audit.py` now rejects a verifier state that assigns a final bracket or leaf metric. The
complete exercised set passes 14/14 catches.

## Result after correction

The correction changes the strength of the evidence, not the scientific landing. The accepted
bounded result remains:

```text
GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN
```

No new physical premise was added and no action, source, matter, bootstrap law, `X_max`, CMB,
signalling, or dynamics conclusion was introduced.

## External-review boundary

The corrected sealed intake was constructed locally with 43 files, zero writable paths, 27/27
package-manifest checks, and the unchanged exact 15-source manifest. It was not transmitted because
the permission service rejected reuse of the first payload authorization. No workaround was used.
