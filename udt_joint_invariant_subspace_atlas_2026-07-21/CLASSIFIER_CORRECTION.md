# Classifier Correction — Repeated Central Eigenspace

The first complete build returned `VERIFICATION_REQUIRED` despite tensor covariance residual
`2.2204460492503131e-16`. It reported 23,994 nonlinear classification disagreements, all confined
to `central_block_ranks` and `central_block_status`; algebra dimension, commutant dimensions,
gradient-orbit dimensions/signatures, and reducibility class had zero disagreements.

Cause: the central-block routine diagonalized an arbitrary floating SVD representative even when
the metric-self-adjoint center was one-dimensional. That center contains only the scalar identity,
but numerical diagonalization chose an arbitrary eigenbasis in its repeated four-dimensional
eigenspace. Tiny basis-dependent complex components caused the same scalar center to alternate
between `4` and `COMPLEX_JORDAN_OR_NUMERIC_OBSTRUCTION` after a coordinate change.

Correction:

1. a one-dimensional self-adjoint center is classified directly as the scalar identity with one
   rank-four block;
2. higher-dimensional real central spectral projectors are constructed as polynomials in the
   central element, not from an arbitrary eigenvector matrix;
3. projector idempotence, metric self-adjointness, centrality, and operator commutation gates remain
   unchanged;
4. no family, configuration, tolerance, chart, or scientific classification target changed.

The failed result and transcript are preserved byte-for-byte as `PRECORRECTION_ATLAS_RESULT.json`
and `PRECORRECTION_ATLAS_TRANSCRIPT.txt` with SHA-256 values
`bf73dbdfd12c9b07bd167725c0f9086bdd9f9539b3c034793a4fca2ff5d6a93e` and
`975299fabd703fd34e6461c96c0502a8d63634250188f800a9ff4a822e3d07ef`.

The corrected complete replay has zero non-uncertain classification disagreements. Its 24
uncertain comparisons remain retained in `NUMERIC_MARGIN_LEDGER.tsv`.
