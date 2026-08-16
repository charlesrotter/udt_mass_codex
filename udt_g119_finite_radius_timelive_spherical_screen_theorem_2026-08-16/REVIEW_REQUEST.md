# Fresh adversarial review request — G119

Cold-review the proposed finite-radius time-live central-spherical screen theorem. Do not defend it.

The claimed result is conditional on a supplied smooth time-oriented warped metric

\[
g=h_{ab}(x)dx^a dx^b+R(x)^2d\Omega^2,
\]

a regular center, central observer, normalized radial null point-observer exponential query, and one
finite branch. It claims that spherical rotational variations and an independent mixed-curvature
calculation prove

\[
D_{\rm sky}=R O,\quad O\in O(2),\quad |\det D_{\rm sky}|=R^2
\]

at arbitrary finite radius on every regular branch, with rank-zero but phase-surviving spherical
caustics.

Audit all of the following:

1. Is a lifted rotational Killing field exactly the unit-sky-normalized point-observer Jacobi
   field, or is a hidden factor of affine frequency, endpoint lapse, or observer calibration missing?
2. Is `E=Xi/R` actually parallel along every radial geodesic of an arbitrary time-dependent
   spherical warped product?
3. Reconstruct the sign and index placement of
   `R^theta_{a theta b} K^a K^b = -Rdd/R` independently.
4. Does the result survive arbitrary orbit-metric cross terms, not just the diagonal chart used by
   the executable? Distinguish a coordinate check from the covariant warped-product proof.
5. Classify coincidence, areal turning points, finite caustics, orientation reversal, passage through
   another regular center, multiple preimages, and lack of global screen section.
6. Is “no rank-one caustic” correct in precisely the declared exact central-spherical class?
7. Does the radiometric corollary preserve the G94 ownership boundary and avoid deriving transfer?
8. Does the SNe regrade remove only an independent tensor screen while retaining `R/sqrt(T)` and
   release-frequency/source conditionals?
9. Re-run both scripts and compare their stdout byte-for-byte with the saved JSON artifacts.
10. Hunt any overclaim of history, query, branch, transfer, global, or observational selection.

Return one of:

- `VERIFIED_WITH_CAVEATS`;
- `REPAIRABLE_SCOPE_OR_ALGEBRA_DEFECT`;
- `THEOREM_FALSE_IN_DECLARED_CLASS`; or
- a more precise landing.

List mandatory repairs separately from optional improvements. Do not edit files or continue the
research.
