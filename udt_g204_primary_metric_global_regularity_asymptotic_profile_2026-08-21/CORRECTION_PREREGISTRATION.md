# G204 correction preregistration — smooth-center differentiability

Date: 2026-08-21

## Failure found after the first production replay

The initially registered control

\[
\phi=a x^2(x-1)^n,
\qquad x=r/r_0,
\]

has bounded Kretschmann scalar at the center, but its expansion contains odd powers such as
\(r^3\). A rotation-invariant scalar smooth in Cartesian coordinates must be smooth in \(r^2\).
Therefore the first control proves bounded curvature, not a genuinely smooth center. The original
smooth-center claim is failed closed.

## Preregistered repair control

Before testing the repair, replace only that witness by

\[
\boxed{
\phi_{\rm even}(r)=\frac{a}{2^n}x^2(x^2-1)^n,
\qquad n\ge3\text{ odd},\ a>0.
}
\]

This is analytic in \(r^2\). The factor \(2^{-n}\) is chosen so that its first nonzero
log-areal Taylor coefficient at \(x=1\) remains exactly \(a\), not to fit an outcome.

## Repair checks

The repaired run must verify:

1. an even-power center expansion and smooth Cartesian metric coefficients;
2. \(f=1+O(r^2)\) and finite center curvature;
3. the same quiet crossing order and leading log-areal coefficient \(a\);
4. one negative inner minimum at \(x^2=1/(n+1)\);
5. positive outer growth and curvature decay;
6. survival for every sampled odd \(n\), positive \(r_0\), and positive \(a\).

## Evidence regrade

The final package must preserve both facts:

- the original registered control is `CENTER_CURVATURE_BOUNDED_BUT_NOT_SMOOTH`;
- the even-areal control is `POST_FAILURE_PREREGISTERED_REPAIR_WITNESS`, not a selected profile.

If the even-areal control fails, G204 must land as no smooth-center survivor found in the declared
controls. No further repair family may be introduced in this package.
