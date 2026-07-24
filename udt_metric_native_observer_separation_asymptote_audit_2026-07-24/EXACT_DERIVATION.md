# Exact derivation

## 1. Reciprocal clock depth

The registered founding chain gives, in its declared reciprocal pair,

```text
theta_clock = exp(-phi) c_E dt
theta_ruler = exp(+phi) dr
```

and the clock-dilation factor relative to a `phi=0` anchor is

```text
T(phi)=exp(phi).
```

This fixes clock dilation as a function of reciprocal depth. It does not by
itself fix the physical distance assigned to that depth.

## 2. Observer-rest geometry from the complete coframe

Use the exact complete triangular coframe already employed by the metric
atlases:

```text
theta0 = u dx0 + b dx1
theta1 = w dx1
theta2 = (r a20+e a30)dx0 + (r a21+e a31)dx1 + r dx2 + e dx3
theta3 = t a30 dx0 + t a31 dx1 + t dx3
```

where `u,w,r,t` are positive. The spacetime metric is

```text
g=-theta0^2+theta1^2+theta2^2+theta3^2.
```

For the observer whose clock leg is `theta0`, an instantaneous
clock-horizontal displacement obeys

```text
theta0=0  =>  dx0=-(b/u)dx1.
```

Define

```text
k2 = r a21+e a31-(b/u)(r a20+e a30),
k3 = t[a31-(b/u)a30].
```

The exact positive spatial line element is then

```text
dell^2
 = (w dx1)^2
 + (k2 dx1+r dx2+e dx3)^2
 + (k3 dx1+t dx3)^2.
```

Its coframe determinant is `w r t`, and its metric determinant is

```text
det(h)=w^2 r^2 t^2>0.
```

This is a direct full-coframe result. The angular directions and all four
base/screen shifts enter before any symmetry reduction.

## 3. The complete spatial gradient of reciprocal depth

Write the coordinate components of `dphi` as

```text
(p0,p1,p2,p3).
```

Its coframe components are

```text
c0 = (p0-a20 p2-a30 p3)/u,
c1 = (p1-a21 p2-a31 p3-b c0)/w,
c2 = p2/r,
c3 = (p3-e p2/r)/t.
```

On `theta0=0`, only the last three components contribute. Therefore the
complete observer-rest squared depth gradient is

```text
B = h^-1(dphi,dphi) = c1^2+c2^2+c3^2.
```

The production derivation independently obtains the same expression by
inverting the complete induced three-metric. This quantity is the exact
metric solder between the reciprocal `phi` sector and the complete
shift/angular orchestra.

## 4. The metric-native distance law

Suppose a physical observer-rest distance from a reference level is a
single-valued function

```text
D=F(phi).
```

A smooth distance function satisfies the spatial eikonal normalization

```text
h^-1(dD,dD)=1
```

away from its cut locus. Since `dD=F'(phi)dphi`,

```text
[F'(phi)]^2 B = 1.
```

Consequently:

```text
dD/dphi = 1/sqrt(B(phi)).
```

This is possible as one universal scalar law only when `B` is positive and
constant on each relevant `phi` level set—equivalently, when

```text
B=B(phi).
```

This is the transnormal condition. If `B` varies around one `phi` level,
different angular locations or gradient curves assign different distance
increments to the same clock dilation. The metric then supplies
path-dependent distances, not one `D(phi)`.

The local eikonal equation also makes the integral curves of `grad(D)`
unit-speed geodesics. Turning this local result into a global distance
requires control of reachability, caustics, cut loci, topology, and event
pairing.

## 5. Infinite-dilation asymptote

When the transnormal condition holds, the metric-native depth reach from
`phi0` to infinite clock dilation is

```text
X_phi = integral(phi0,infinity) dphi/sqrt(B(phi)).
```

It is finite exactly when this integral converges.

For the asymptotic control

```text
B(phi)=C^2 exp(2 alpha phi),
```

the endpoint is finite for positive `alpha`:

```text
X_phi=1/(C alpha)
```

when `phi0=0`. Constant or decaying `B` gives infinite reach. Thus infinite
clock dilation does not alone imply a finite distance; the complete
metric's spatial `phi` gradient decides.

## 6. Exact conditional WR-L realization

In the conditional WR-L slice,

```text
A=exp(-2phi)=1-r/X,
ds_space^2=A^-1 dr^2+r^2 dOmega^2.
```

Differentiating the profile gives

```text
dphi/dr=exp(2phi)/(2X).
```

Therefore

```text
B=A(dphi/dr)^2=exp(2phi)/(4X^2)
```

and the metric-native radial proper distance is

```text
dD/dphi=2X exp(-phi),
D(phi)=2X[1-exp(-phi)],
lim(phi->infinity) D=2X.
```

The same fixed metric has four distinct readings:

```text
coordinate areal radius: r/X       = 1-exp(-2phi)  -> 1,
radial proper distance:  D/X       = 2[1-exp(-phi)] -> 2,
optical depth:           r*/X      = 2phi           -> infinity,
projective readout:      p/X       = tanh(phi)      -> 1.
```

At clock dilation `T=2`, these are respectively

```text
3/4, 1, log(4), 3/5.
```

Thus the direct metric distance in this slice is not the projective `tanh`
readout. The local WR-L parameter `X` is also not thereby the global
observer-pair diameter.

## 7. Why the reciprocal block alone does not select the law

For the radial reciprocal block,

```text
dell=exp(phi)dr.
```

Given any smooth increasing proposed proper-depth law `D(phi)`, choose

```text
dr/dphi=exp(-phi)D'(phi).
```

Then `dell=dD` identically. Three exercised controls have the same origin
and the same local slope:

```text
D1/X=tanh(phi),          finite endpoint X,
D2/X=1-exp(-phi),        finite endpoint X,
D3/X=phi,                infinite endpoint.
```

All are compatible with the reciprocal clock/ruler form under different
profiles. A selected complete metric branch—or a law selecting one—is
therefore necessary to evaluate `B(phi)`.

## 8. Why radial reach is not yet global `X_max`

Take two complete product spatial geometries with the same radial proper
coordinate `ell`, the same clock law

```text
exp(phi)=1/(1-ell/L),
```

and angular periods `2pi`, but different angular radii. For

```text
h=dell^2+R^2 dtheta^2+Q^2 dpsi^2,
```

the diameter supremum is

```text
diameter^2=L^2+(pi R)^2+(pi Q)^2.
```

The controls `(R,Q)=(L,L)` and `(2L,L)` have identical clock dilation and
identical radial asymptote `L`, but their squared diameters differ by

```text
3 pi^2 L^2.
```

These are logical countercontrols, not candidate universes. They prove that
clock dilation plus radial reach does not determine a global pair diameter
without the angular/global completion.

## 9. Observer and scale dependence

A Lorentzian metric alone selects no observer clock leg. A supplied
reciprocal coframe or observer field does. In the exact flat
`beta=3/5`, `gamma=5/4` control, changing the clock-horizontal event pairing
changes a coordinate span `L` to rest-space span `4L/5`. This is ordinary
covariance of different observer simultaneity choices; it is not a failure
of frame reciprocity.

Under a constant common rescaling

```text
g -> Omega^2 g,
```

clock ratios remain the same while every physical distance and endpoint
scales by `Omega`. Therefore an absolute `X_max` requires the calibrated
physical-metric ontology, or a separately derived conformal representative.
The recent CSN audit established that strong local CSN is not derived.

## Exact conclusion

The complete coframe supplies a direct evaluator:

```text
B = h^-1(dphi,dphi),
D = integral dphi/sqrt(B),
```

with a precise transnormal and convergence gate. It does not currently
supply a selected complete branch, global clock/event pairing, or proof
that the resulting depth reach equals the universe-wide observer-pair
diameter.
