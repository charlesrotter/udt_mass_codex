# Evidence gates — complete-geometry SNe replay

Date: 2026-08-15

1. **Preregistered: PASS.** The interface and computation contract were committed at `65f9940e`
   before numerical output. The exact-anchor verifier repair was committed at `670aa041` before its
   corrected rerun; no tolerance or scientific input changed.
2. **Full or bounded: PASS FOR DECLARED TILE ONLY.** The complete nonlinear null/screen/Jacobi path
   and full observed redshift range are covered for one stationary axial G79 control and one chosen
   outward query. Other geometries, directions, skies, histories, branches, caustics, transfer laws,
   and source models are not covered.
3. **Independent verification: PASS WITH CAVEATS.** The direct-loop Christoffel plus
   finite-difference neighboring-ray implementation agrees at five frozen redshifts. An explicit
   covariance-inverse likelihood independently reproduces the production likelihood. A fresh sealed
   `gpt-5.4` reviewer rebuilt the complete curve with explicit endpoint root-finding, reproduced all
   30 payload hashes and the raw likelihood, and found no blocking error. Its direct-anchor caveat is
   retained: only the neighboring-ray side is implementation-distinct.
4. **Premises audited: PASS.** Geometry, query, transfer, catalog, covariance, fitted
   offset, all-sky comparison, physical history, `X_max`, EM/particle theory, and downstream claims
   are separately stamped.

Final bounded grade:

```text
VERIFIED_WITH_CAVEATS__ONE_CONTROL_STRONGLY_SNE_INCOMPATIBLE
```
