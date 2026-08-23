# G232 whiteboard synthesis

Date: 2026-08-23

## Primary conference landing

```text
FIXED_MEMBER_CARTAN_DESCENT_IS_EVALUATIVE
__FINITE_PROFILE_FAMILY_CLOSURE_IS_CONDITIONAL
__UNRESTRICTED_PRIMARY_PROFILE_FINITE_JET_CLOSURE_REQUIRES_EXACT_OBSTRUCTION_TEST
__VALUED_PAIR_NETWORK_ENCODES_BUT_DOES_NOT_GENERATE_THE_PROFILE
```

Status: `PONDER_CONVERGENCE__NEXT_TEST_PREREGISTERED`, not a banked obstruction theorem.

## What was hiding in plain sight

The static-spherical “physical history gap” is much smaller than recent language made it sound. It
is principally the function \(\phi(r)\).

Once one complete valued \(\phi(r)\) is supplied, the metric already plays the local score. Areal
radius is its one-dimensional symmetry-reduced Cartan coordinate, the radial derivative is fixed,
and every local invariant follows. No additional reciprocal-kernel mechanism or second metric
selector is missing at that level.

What current identities do not do is compose the whole function \(\phi(r)\) from \(c_E\),
Reciprocity, composition, and finitely many anchors. Calling that distinction “missing history”
made one precise functional freedom sound like a swarm of missing physical mechanisms.

## Exact ownership levels

### One supplied metric member — `DERIVED_CONDITIONAL`

For

\[
f(r)=e^{-2\phi(r)},
\qquad
g=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\]

the regular static-spherical member is locally cohomogeneity one. Its reduced derivative operator
is

\[
e_{\hat r}=\sqrt f\,\partial_r=e^{-\phi}\partial_r.
\]

This is a finite local Cartan law whose coefficient functions are read from the already supplied
member. “Finite classifying space” does not mean “predicted from finitely many constants.” Centers,
space-form points, and isotropy-changing radii require separate strata.

### One finite declared family — `CONDITIONAL/CHOSE`

For fixed odd \(n\) in the G204 control family,

\[
\phi(x)=\frac{a}{2^n}x^2(x^2-1)^n,
\qquad x=r/r_0,
\]

the reduced state \((x,a,r_0;n)\) closes conditionally:

\[
e_{\hat r}x=\frac{e^{-\phi(x;a,n)}}{r_0},
\qquad e_{\hat r}a=e_{\hat r}r_0=e_{\hat r}n=0.
\]

That is useful finite closure, but it inherits the chosen profile family and does not select
\(a,r_0,n\).

### The unrestricted profile family — exact test required

For every proposed finite jet order, smooth or analytic profiles can agree through that order at a
regular orbit and differ at the next. The G231-ceiling witness should preserve the metric fourth jet
and \((R,\nabla R,\nabla^2R)\), then vary the metric fifth jet and \(\nabla^3R\).

If the preregistered invariant replay succeeds, the negative is limited to **local, finite-order,
natural autonomous laws uniform over the unrestricted primary profile family**. It says nothing
against a nonlocal law, an infinite-state law, or a separately founded smaller family.

## Why this is progress

This is not another narrowing around an undefined hole. It removes a false binary:

- UDT does not need a mysterious extra mechanism to evaluate a complete supplied metric or valued
  relation network.
- UDT also has not derived an unrestricted radial profile from finite anchors merely because that
  profile can be evaluated everywhere.

The next calculation is one exact two-profile discriminator, not another broad jet census or a new
physical mechanism.
