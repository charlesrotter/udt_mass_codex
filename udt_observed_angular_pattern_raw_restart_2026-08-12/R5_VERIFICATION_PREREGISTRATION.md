# R5 independent verification — preregistration before replay

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_CORRECTED_ASSEMBLY__BEFORE_INDEPENDENT_REPLAY`

No R5 spectrum, overlap, or covariance-subspace outcome has been interpreted.

## Independent method

- reconstruct all 2,328 curves and 9,286 relations without importing the production module;
- use SciPy `svd(..., lapack_driver="gesvd")` for every full view basis;
- use SciPy symmetric `eigh(..., driver="evr")` for every transformed covariance;
- reconstruct every singular spectrum and spectral-boundary gap;
- reconstruct every ranked overlap and corrected covariance-subspace field where the corresponding
  top-`k` projector is numerically owned;
- reconstruct summaries from the full raw saved atlas and verify every manifest hash;
- preserve all numerically ambiguous boundaries rather than dropping or repairing them.

## Frozen numerical ownership rule

Let the relative singular boundary gap be

```text
g = (sigma_k - sigma_{k+1}) / sigma_1.
```

The full-dimensional projector is always owned. At smaller ranks, independent projector comparison
is required only when both participating views have

```text
g >= sqrt(eps_float64).
```

For a resolved comparison use

```text
tol = max(2e-10, 8192 * eps_float64 / min(gaps)).
```

as both relative and absolute tolerance for bounded projector quantities. This is a numerical
conditioning rule, not a mode-selection or physics threshold. Unresolved rows must remain finite,
bounded, counted, and gap-labelled, but their basis-dependent projector value is not independently
certified.

For transformed covariance range projectors, apply the same `sqrt(eps)` rule to the relative gap
between the numerical rank threshold and its neighboring eigenvalues. Zero- and full-rank range
projectors are owned exactly. Covariance traces and difference-projection norms require only the
global singular boundary; range overlap requires both boundaries.

## Fixed comparison gates

- singular values, energy fractions, and gaps: `rtol=5e-11`, `atol=5e-12`;
- direct covariance scalars and thresholds at resolved global boundaries: the gap-conditioned rule
  above, never looser than `2e-10`;
- integer counts, dimensions, ranks, IDs, and keys: exact;
- summary reconstruction from the complete saved raw atlas: `rtol=5e-13`, `atol=5e-14`;
- all full-dimensional overlaps: one within `5e-12`;
- any mismatch outside these rules stops before a verification result is written.

## Required return

The verifier must report:

- exact output censuses;
- maximum singular-value discrepancy;
- resolved and unresolved overlap-row counts;
- resolved and unresolved covariance-subspace row counts;
- maximum resolved projector/covariance discrepancy and maximum allowed gap-conditioned bound;
- every summary and manifest check;
- `PASS` only if all owned comparisons and all structural gates succeed.
