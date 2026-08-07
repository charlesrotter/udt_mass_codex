# WR-L/Xmax light-cone and observer-frame audit

Date: 2026-07-23

Preregistration commit: `44ebe4c`

Compute: CPU-only exact algebra

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's expectation was correct in its local geometric part:

> The corrected WR-L metric contains an exact Lorentzian light-cone
> structure, and its radial orthonormal observer frames form the connected
> `SO+(1,1)` family without importing an SR transformation or a GR field
> equation.

For

```text
A(r)=1-r/X,
ds2=-A c_E^2 dt2+A^-1 dr2+r2 dOmega2,
```

radial null curves satisfy

```text
dr/dt=+-c_E A.
```

A static coordinate observer therefore sees the coordinate slope approach
zero at `r=X`. But the same observer's proper clock and ruler are

```text
dtau=sqrt(A)dt,
dell=dr/sqrt(A),
```

so the locally measured null speed remains exactly `+-c_E`.

The optical coordinate is

```text
r_star=-X log(1-r/X)=2X phi.
```

It diverges as `r` approaches `X`, and the radial metric becomes

```text
ds2_rad=A[-d(c_E t)^2+dr_star^2].
```

Thus the static clock/optical asymptote and the local Lorentzian cone are
both directly derived.

Two qualifications are load-bearing.

1. `r=X` is a frame-invariant null surface in the recorded geometry, but
   the metric admits regular crossing curves. Static unattainability is not
   universal uncrossability.
2. The older global `phi -> phi-beta` positional-frame homothety does not
   survive the complete WR-L metric with its fixed areal angular sector.
   Local observer reciprocity is derived; global equivalence of all
   observer-centered `X` spheres is still open.

## Exact null surface

The normal to an `r=constant` surface has norm

```text
g^-1(dr,dr)=A.
```

The static Killing field has norm

```text
g(partial_t,partial_t)=-A c_E^2.
```

Both become null at `r=X`. This statement is invariant under a local change
of orthonormal frame.

The surface is not a curvature singularity. Direct four-dimensional
reconstruction gives

```text
Ricci scalar       = 6/(X r) -> 6/X^2,
Kretschmann scalar = 8/(X^2 r^2) -> 8/X^4.
```

The static congruence nevertheless becomes singular: the proper
acceleration required to remain at fixed `r` is

```text
c_E^2/[2X sqrt(A)],
```

which diverges at the surface. Static observers cannot be continued there
as static observers.

## Regular crossing

With the ingoing coordinate

```text
v=c_E t+r_star,
```

the radial metric is

```text
ds2_rad=-A dv2+2 dv dr.
```

Its determinant is `-1`, including at `A=0`. Two explicit local witnesses
are:

```text
dv=0, varying r:
    ds2=0                         (null crossing)

dv=dlam, dr=-kappa dlam, kappa>0:
    ds2=-(A+2kappa)dlam2          (timelike near the surface)
```

Therefore the metric itself does not make `X` an uncrossable positional
speed limit. It makes `X` a null horizon of the static patch. A global UDT
boundary, quotient, observer-dependent horizon construction, or different
complete metric could still prohibit or reinterpret crossing; none is
selected here.

This is the precise point at which the analogy with `c` stops being
automatic. `c_E` bounds timelike directions inside every tangent space. A
null hypersurface is a geometric surface that timelike observers can
cross. Making the latter universally terminal requires additional global
content.

## Local moving and accelerating observers

Let

```text
theta0=sqrt(A)c_E dt,
theta1=dr/sqrt(A).
```

The connected, time- and orientation-preserving transformations that keep

```text
-(theta0)^2+(theta1)^2
```

unchanged are

```text
theta0'=cosh(eta)theta0+sinh(eta)theta1,
theta1'=sinh(eta)theta0+cosh(eta)theta1.
```

Equivalently, for the two null coframes,

```text
theta_plus' = exp(eta) theta_plus,
theta_minus'= exp(-eta)theta_minus.
```

The null lines therefore do not move. This is not an imported Lorentz
formula: it is the connected frame group obtained by preserving the
metric's local `(-,+)` quadratic form.

`eta(t,r)` may be any smooth local rapidity field. In the registered
coframe convention the radial connection changes as

```text
omega' = omega-deta.
```

Because `d(deta)=0`, a variable frame—including an accelerating one—does
not create curvature. The metric supplies the connection transformation,
but it supplies no equation selecting `eta`, an observer worldline, or an
acceleration history.

At the horizon the static coframe itself degenerates. A regular crossing
frame is not related to it by a finite boost at the limiting surface; its
relative rapidity diverges. This is why “all finite local boosts preserve
the static cone” and “a regular observer can cross the horizon” are
consistent statements.

## The angular obstruction

Using the corrected WR-L relation

```text
r=X(1-exp(-2phi)),
```

the complete metric becomes

```text
ds2 =
  exp(-2phi)[-c_E^2dt2+4X^2dphi2]
  +X^2[1-exp(-2phi)]^2dOmega2.
```

Under the older constant depth re-centering `phi' = phi-beta`, the
time-radial block receives the common factor

```text
exp(2beta).
```

The angular block instead receives

```text
[(1-exp(-2(phi-beta)))/(1-exp(-2phi))]^2,
```

which depends on position and is not the common factor. The exact witness

```text
phi=log(2), beta=log(2)/2
```

gives

```text
time-radial ratio = 2,
angular ratio     = 4/9.
```

Therefore the old constant-depth shift is not a full WR-L metric
homothety when the areal angles are fixed.

This does not refute every possible global UDT frame transformation. It
proves that the angular sector is load-bearing and that the previous
projective-frame answer belonged to a different warped metric family,
whose transverse radius scaled as `C exp(phi)` rather than the WR-L areal
radius.

## Regrade of earlier frame work

The earlier full-frame, dynamic-frame, and accelerating-Cartan packages
remain exact in their declared reciprocal warped-product representative.
They are not silently reusable as the global frame mechanics of WR-L.

What survives:

- positive common rescaling preserves null cones;
- local orthonormal frame changes preserve the metric;
- variable frame rapidity contributes only pure-frame connection terms;
- acceleration does not manufacture curvature;
- the metric cone does not by itself prove a material signalling law.

What is withdrawn as an implication for WR-L:

- `x=X tanh(phi)` as its physical position law;
- `phi -> phi-beta` as a complete WR-L homothety;
- the old transverse scaling `R=C exp(phi)` as the WR-L areal sector; and
- a completed global observer-reciprocity theorem.

The full table is in `PRIOR_WORK_REGRADE.tsv`.

## What this means for `Xmax`

Three statements must now be kept separate:

1. **Derived:** every local orthonormal frame at a given WR-L event shares
   the same null cone.
2. **Derived:** every such frame identifies the same geometric `r=X` null
   surface of that fixed solution.
3. **Open:** observers with different positional origins have equivalent
   `X`-radius domains under a complete UDT frame symmetry.

The owner postulate of one common `Xmax` remains coherent, but the third
statement is not yet realized by this simple spherical metric. Its angular
sector exposes the missing join.

## Four evidence gates

1. **Preregistered:** yes, commit `44ebe4c` before source adjudication and
   algebra.
2. **Full or bounded scope:** complete for the exact radial null
   characteristics, local connected orthonormal radial frames, arbitrary
   smooth local rapidity, both regular null charts, and the specified
   constant-depth-shift/full-angular obstruction on the recorded WR-L
   branch. Other complete metrics and transformations are outside scope.
3. **Independent verification:** a separate standard-library rational
   implementation recomputed the cone, frame group, crossing witnesses,
   source hashes, and angular mismatch without importing the production
   module.
4. **Premises audited:** static/spherical/areal slice, WR-L conditions,
   owner `Xmax`, local observer definition, free rapidity, global boundary,
   angular completion, action, source, and material signals are explicit.

The grade remains `VERIFIED-WITH-CAVEATS` because no fresh external
semantic agent was launched.

## Maximum conclusion

> The WR-L metric directly derives a frame-invariant local Lorentzian cone,
> an invariant null `X` surface, and exact static clock/optical
> unattainability. Its regular ingoing chart also admits crossing curves,
> so universal uncrossability is not metric-derived. The corrected areal
> angular sector blocks the older constant-depth global frame homothety.
> Completing observer reciprocity therefore requires the complete angular
> transformation or another globally completed metric/boundary.

No Hopf carrier, action, source, physical signal law, global boundary,
canonization, navigation change, or GPU work follows.
