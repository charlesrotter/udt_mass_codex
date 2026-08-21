# G202 audit report — quiet overlap and profile anchors

Date: 2026-08-21

## Landing

```text
QUIET_OVERLAP_FORCES_SECOND_ORDER_FLATNESS
__TWO_SIDED_GROWTH_HAS_INFINITE_NATIVE_PROFILES
__ANCHORS_CALIBRATE_BUT_DO_NOT_DERIVE_HISTORY
```

Grade: `INDEPENDENTLY_VERIFIED_WITH_CAVEATS`

## Result first

The primary metric now gives an exact definition of a genuinely quiet middle.  In logarithmic
radius \(s=\log(r/r_0)\), it requires

\[
\boxed{\phi=0,\qquad \phi_s=0,\qquad \phi_{ss}=0.}
\]

For an analytic profile that changes sign, the first active term must therefore be odd and at least
cubic.  The simplest control \(\phi=a s^3\) works, but it is not unique: infinitely many positive
odd-coefficient profiles share the same quiet overlap and two-sided reciprocal growth.

## What anchors can do

A finite set of observations can fix values or coefficients inside an independently declared
finite-dimensional profile family.  It cannot select a unique unrestricted smooth history;
explicit decaying perturbations preserve any finite set of anchor jets while changing the profile
between them.

`c_E` and `G_obs` also do not determine the radial reference scale by themselves.  A mass anchor
allows the dimensional combination \(G_{\rm obs}M/c_E^2\); a density anchor allows
\(c_E/\sqrt{G_{\rm obs}\rho}\).  These are candidate dimensional scales, not derived UDT laws.

## Why this is progress rather than the old history loop

The open item is now sharply downstream of the kernel:

- the pair law and channel interlocking are retained;
- quiet overlap has an exact metric criterion;
- two-sided growth is demonstrably compatible with infinitely many native profiles;
- the remaining choice is profile-class ownership and calibration, not a missing observer-pair
  mechanism.

## Evidence

- preregistered and pushed at `8503a413`;
- 32/32 symbolic assertions after replacing an ambiguous symbolic nonnegative-coefficient limit by
  its exact lower-bound factorization;
- 20,000 independent exact odd-profile cases;
- 1,000 independent finite-anchor counterfamilies;
- 170,003 independent assertions;
- independent dimensional-exponent verification;
- no production import or artifact read;
- hostile catches, source hashes, no-write replay, premise verifier, repository tests, and diff
  checks are recorded in `EVIDENCE_GATES.md`.

## Maximum conclusion

G202 derives the necessary quiet-overlap jet and classifies the information supplied by finite
anchors.  It does not select the physical profile, its scale, an observational fit, `X_max`,
transfer, source, action, matter, mass dynamics, bootstrap, or signalling.
