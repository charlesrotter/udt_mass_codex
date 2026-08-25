`ACCEPT_WITH_REPAIRS`

Finding:

- Provenance verification is not fully exact. `verify_package.py` special-cases
  `CURRENT_SCIENTIFIC_PREMISES.tsv` by stripping one `G258` line before recomputing the hash, even
  though `SOURCE_MANIFEST.tsv` pins one exact source hash. That does not break the bounded
  scientific replay, but it weakens strict byte-exact provenance certification and should be
  repaired.

The bounded scientific core passed. The reviewer reran all four registered commands from the
package directory: `derive_inverse_metric_reconstruction.py`, `verify_independent.py`,
`run_catch_proofs.py`, and `verify_package.py`; all exited zero. The package reproduced 12 nodes,
10 positive adjacent changes, one negative adjacent change, maximum algebra residual
`2.220446049250313e-16`, zero saved-radius and covariance residuals, 252 independent Decimal
assertions, and 8/8 hostile catches.

Evidence for the required adjudication:

- The reciprocal identities and determinant-one radial block are the exact registered
  construction: `T=Z^-1`, `L=Z`, `f=Z^-2`, and `TL=1`; the replay checks the radial determinant at
  every knot.
- `theta=5 log10(R/R0)` reconstructs the relative areal radii, and only one positive homothety
  remains.
- The full-covariance adjacent-change calculation reproduces the final
  `-0.3098941412089942 sigma` classification. This remains conditional on G237's chosen zero
  cross-release covariance after de-overlap, not a proof of release independence.
- “Sampled relative primary metric state” is acceptable only at the package's processed,
  conditional, knotwise, non-continuous ceiling.
- No continuous interpolation, derivative law, radiative-transfer derivation, Lambda-CDM distance,
  post-readout orchestra, `X_max`, or fitted UDT coefficient entered.
- W3/G257 are used only as the quiet-GR comparison requirement, not as the SNe cosmological
  profile; the hostile controls catch a static-GR-exterior import.

Scope qualifications:

- Acceptance is conditional on the supplied endpoint-frequency attachment, the G119
  central-spherical branch theorem, imported transparent transfer, the frozen G237 processed state,
  and the chosen block-diagonal cross-release covariance.
- It does not canonize W1 or W3.
- It does not establish a continuous, derivative-level, covariant four-dimensional UDT history;
  it supports only the preregistered bounded knotwise reconstruction.

This repository copy preserves the review's full scientific adjudication while replacing its
ephemeral absolute-path links with stable package-relative references.
