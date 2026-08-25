# G260 preregistration — GR-quiet angular non-discard audit

Date: 2026-08-25

## Frozen question

On the complete primary static-spherical metric, determine whether the G257/G259 GR-quiet vacuum
closure retains rather than deletes the native angular sector.

## Preregistered exact checks

1. Derive the full four-dimensional mixed Einstein components directly from the metric, retaining
   the areal `S^2` through the entire Christoffel-to-Ricci calculation.
2. Independently derive the curvature at an equatorial event from metric jets, without importing
   the production residual formulas or reading their result file.
3. Rewrite the G201 amplitudes in `f,f',f''` variables and test their exact relation, if any, to the
   full Einstein residuals for arbitrary smooth positive `f`.
4. Substitute the entire G257 family `f=1+C/r`. Require the full Einstein tensor to vanish while
   recording whether each angular amplitude is individually zero or nonzero.
5. Classify every local `f` for which the sum of the two G201 amplitudes vanishes. Do not discard
   additional branches because they are not vacuum.
6. Express the same identities through the G259 mass aspect `mu=r(1-f)/2`.
7. Run two corruption controls:
   - the isolated two-dimensional clock-radius Einstein tensor;
   - the same warped calculation with angular curvature `k=0` instead of the primary `k=1`.
8. Add hostile mutations that must fail when the angular sector is falsely called inactive, when
   the two-dimensional base is allowed to select `f`, or when quiet-regime scope is widened to the
   loud/global theory.

## Outcome classes

- `FULL_METRIC_CANCELLATION_WITH_ACTIVE_ANGULAR_SECTOR`: the full residual vanishes on the G257
  family, the native angular modes remain individually active, and deletion/flattening corrupts
  the result.
- `ANGULAR_SECTOR_ACTUALLY_INACTIVE_ON_QUIET_BRANCH`: both native angular modes vanish throughout
  every nonflat G257 member.
- `G201_G257_G259_INCONSISTENT`: the independently computed full tensor, G201 amplitudes, and
  registered residuals cannot satisfy one exact common identity.
- `BOUNDED_AUDIT_INCONCLUSIVE`: the independent implementation or corruption controls do not
  distinguish retention from deletion.

No retuning is permitted after the first outcome is observed.

## Certification contract

- production symbolic derivation from the full metric;
- independent standard-library exact-rational tensor replay from metric jets;
- exact arbitrary-jet and named-family assertions;
- at least three hostile mutations with demonstrated red outcomes;
- package verifier, current 242-row premise verifier, and full repository test suite;
- fresh adversarial review before any claim stronger than a repository `LEAD`.

## Maximum conclusion

At most, G260 may establish whether the angular sector is mathematically indispensable and active
inside the bounded primary static-spherical GR-quiet comparison. It may expose an exact identity
joining the G201 amplitudes to the imported Einstein residuals. It may not derive Einstein dynamics
from UDT, select the global parent law, choose a source/history, or extend the quiet cancellation
to loud, time-live, nonspherical, or `X_max` regimes.
