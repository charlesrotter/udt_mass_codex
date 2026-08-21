# G204 preregistration

Date: 2026-08-21

## Claims to test

1. Direct metric reconstruction gives

   \[
   K=R_{abcd}R^{abcd}
   =f''^2+4(f'/r)^2+4[(1-f)/r^2]^2.
   \]

2. Bounded \(K\) at a positive-areal center forces \(f=1+O(r^2)\), \(f'=O(r)\), and therefore
   \(\phi=O(r^2)\).
3. Every global log-monomial control has a curvature-singular finite-distance center and a
   curvature-decaying infinite-distance outer end.
4. Smooth-center regularity does not select \(n,r_0,a\): the registered \(\phi_{\rm reg}\) family
   survives for every odd \(n\ge3\), positive \(r_0\), and positive \(a\).
5. Each regularized control has one finite negative inner trough at
   \(r/r_0=2/(n+2)\), returns through the G202 quiet crossing, and grows positively outside.
6. A nontrivial negative inner regime joined to both a regular zero-depth center and a zero-depth
   quiet crossing cannot be monotone across the whole inner interval.
7. The outer \(f\to0\), \(K\to0\) limit is not thereby a derived horizon, finite wall,
   \(X_{\max}\), standard asymptotic flatness, or global completion.

## Outcome classes

- `GLOBAL_REGULARITY_SELECTS_ONE_PROFILE`;
- `LOG_MONOMIAL_FAMILY_GLOBALLY_REGULAR`;
- `SMOOTH_CENTER_RESHAPES_INNER_BRANCH__INFINITE_REGULAR_FAMILY_SURVIVES`;
- `ALL_TWO_SIDED_QUIET_PROFILES_EXCLUDED`;
- `TYPE_OR_CURVATURE_FORMULA_FAILURE`.

## Certification contract

- Derive the curvature formula from the full metric, not by importing a named solution.
- Verify it independently from exact metric derivatives or an independently coded connection.
- Check at least 10,000 exact parameter cases for center jets, quiet jets, inner extremum, sign,
  and distinct descriptor survival.
- Check representative high-precision curvature sequences at both boundaries without using them as
  the proof.
- Verify radial spatial-distance convergence/divergence and radial-null affine reach.
- Catch at least ten algebraic or semantic mutations, including promotion of the outer limit to
  \(X_{\max}\) or a horizon.

## Falsification

The anticipated class fails if the curvature identity is wrong, a log-monomial member has bounded
center curvature, the registered regularized family fails center regularity or quiet crossing, or
global regularity fixes the three descriptors after all.

## Maximum conclusion

At most G204 may classify the global positive-areal static branch and prove necessary regularity
conditions. It may not select physical completion, topology, a profile, observations, or dynamics.
