# G233 audit report — primary-profile Cartan closure discriminator

Date: 2026-08-23

## Primary landing

```text
FIXED_MEMBER_CARTAN_DESCENT_IS_EVALUATIVE
__FINITE_G204_CLOSURE_IS_FAMILY_CONDITIONAL
__UNRESTRICTED_PRIMARY_PROFILE_HAS_NO_UNIVERSAL_FINITE_JET_AUTONOMOUS_CLOSURE
__VALUED_PAIR_NETWORK_ENCODES_BUT_DOES_NOT_GENERATE_PROFILE
```

Grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__LOCAL_FINITE_ORDER_FAMILY_OBSTRUCTION`.

## What was learned

The G231 state does not close the unrestricted primary profile family. Two exact analytic primary
metrics can have identical metric four-jets—and therefore identical full
`(R,nabla R,nabla^2 R)`—at one regular quiet orbit, while their next invariant derivative differs.

For

\[
\phi_b=s^3+c s^4+b s^5,
\]

the invariant separator is

\[
\Delta[(\nabla^3\mathcal R)(n,n,n)]
=240\,\Delta b/r_0^5.
\]

The same principal-symbol construction works at every finite order. This is an exact obstruction
to one **local finite-order natural autonomous law uniform over the unrestricted profile family**.
It does not obstruct a nonlocal/global law, infinite-state closure, or a smaller metric-derived
family.

The positive controls survive. One fully valued profile already has a native cohomogeneity-one
Cartan evaluator. The fixed-`n` G204 family has conditional finite closure on `(x,a,r0;n)`, but the
family is `CHOSE` rather than derived.

## Evidence

- prior committed preregistration at `b3ef212e`;
- direct full four-dimensional metric Christoffel/Ricci/scalar computation;
- exact symbolic metric-jet and invariant calculation;
- arbitrary-order principal coefficient checked through seven consecutive orders;
- separate standard-library Fraction-series replay with different exact values;
- initial independent truncation-boundary guard failure preserved and narrowly repaired under a
  written preregistration;
- fresh sealed gpt-5.4 adversarial review: `VERIFIED_WITH_CAVEATS`, no scientific repair;
- the review's sole packaging caveat, a corrupted `\frac`, preregistered and repaired without
  changing the formula;
- no protected path inspected or cited.

## What is not claimed

G233 does not derive the physical profile, select G204, supply a global observer population,
exclude time-live or nonspherical closure, derive dynamics, prove a nonlocal no-go, determine
`X_max`, or add a physical mechanism.

## Banking status

All four gates pass for the declared bounded scope. The result may be banked only as a local
finite-order obstruction over the unrestricted primary static-spherical profile family.
