# Exact derivation: macro phi–angular distance channels

## 1. Founded pair and bounded complete coframe

The founded reciprocal pair remains

```text
theta_clock = exp(-phi) c_E dt,
theta_depth = exp(+phi) dchi.
```

Nothing below changes that pair or the clock-dilation factor `exp(phi)`. The
question is how the remaining coframe changes the physical distance assigned
to the same founded depth.

On the founded clock-horizontal slice, use the exact spatial triangular
coframe convention inherited from the complete-coframe distance audit:

```text
theta1 = w dchi,
theta2 = ell2 dchi + r dy + e dz,
theta3 = ell3 dchi        + t dz,
```

where `w,r,t>0`. In matrix form, with coframe legs as rows,

```text
A = [[w,    0, 0],
     [ell2, r, e],
     [ell3, 0, t]],
h = A^T A,
det(h)=w^2 r^2 t^2 > 0.
```

The three angular-generator directions change `r,e,t`. The two
depth-to-angular directions change `ell2,ell3`. The two clock-to-angular
directions occur in the four-dimensional coframe but vanish from this induced
spatial matrix when `theta_clock=0` for the fixed founded diagonal clock leg.

## 2. Exact local depth norm

Write

```text
dphi = p1 dchi + p2 dy + p3 dz.
```

Solving `A^T c = dphi` gives the orthonormal coframe components

```text
c3 = (p3-e p2/r)/t,
c2 = p2/r,
c1 = [p1-ell2 p2/r-ell3 c3]/w.
```

Therefore the observer-rest squared depth norm is

```text
B = h^-1(dphi,dphi) = c1^2+c2^2+c3^2.
```

This is the exact local coupling of founded depth to the angular and
depth-angular sectors in this chart.

## 3. Aligned branch: no local angular modulation

If the founded depth is aligned with the depth coordinate,

```text
p2=p3=0,
```

then

```text
B=(p1/w)^2.
```

All angular coefficients and both depth-angular shifts cancel exactly. Thus,
on this conditional aligned branch, the complete angular orchestra does not
modify the local clock-depth conversion. It can still change the geometry of
each `phi` level and the complete cell's diameter.

This result is an exact restriction of the metric, not a statement that UDT
selects alignment.

## 4. Non-aligned branch: local angular modulation is possible

When `p2` or `p3` is nonzero, the same exact expression contains `r,e,t` and
the depth-angular shifts. A scalar distance law `D=F(phi)` requires

```text
B=B(phi)
```

on the relevant region. If `B` varies around one `phi` level, one universal
`D(phi)` does not exist there.

An exact local counterwitness takes

```text
phi = x + epsilon sin(y),
w=exp(phi),
r=exp(-k phi),
t=exp(k phi),
e=ell2=ell3=0.
```

Then

```text
B=exp(-2phi)+epsilon^2 cos(y)^2 exp(2k phi).
```

At the same level `phi=log(2)`, with `epsilon=1/10` and `k=1`, the points
`y=0` and `y=pi/2` give

```text
B=29/100  and  B=1/4,
```

a difference of `1/25`. The angular reciprocal direction can therefore
modulate the local depth norm when the founded scalar is not aligned with the
depth foliation.

A depth-angular shift witness with

```text
ell2=s[exp(phi)-1], r=t=1, e=ell3=0
```

gives, at the same level and with `s=1`, the exact values

```text
B=17/80  and  B=1/4,
```

a difference of `-3/80`. These are possibility witnesses, not selected
solutions.

## 5. Global modulation is a separate channel

Even when `p2=p3=0` and the local result is unchanged, angular geometry can
change a complete observer-pair distance. For the conditional flat product

```text
h=dell^2+R^2 dy^2+Q^2 dz^2
```

on an interval of length `L` times two circles of period `2pi`, the squared
diameter is

```text
diameter^2=L^2+pi^2(R^2+Q^2).
```

Changing `R` from `1` to `2` with `L=Q=1` changes the squared diameter by
`3 pi^2`, while the aligned radial norm remains identical. Thus a radial
infinite-dilation reach and the global two-observer maximum separation are
not the same metric quantity.

## 6. Consequence for a distance law and Xmax

Where `B` is positive and constant on `phi` levels, the local metric equation
remains

```text
dD/dphi = 1/sqrt(B(phi)),
X_phi = integral dphi/sqrt(B(phi)).
```

The new audit sharpens its interpretation:

- aligned angular structure may leave `X_phi` unchanged while changing the
  complete cell diameter;
- non-aligned angular structure may make `B` direction-dependent, so there is
  no single scalar `X_phi` to promote to `Xmax`; and
- neither channel supplies the missing global observer comparison, branch
  selection, endpoint/gluing data, or scale closure.

Therefore the metric contains a genuine macro angular modulation mechanism,
but it has not selected the modulation or derived a numerical `Xmax`.

## 7. Twelve-completion descent result

Crossing the seven extension directions with the twelve registered finite-cell
classes gives 84 rows. Every direction is locally available on a regular
chart. None is proven as a selected, globally completed extension across the
whole completion universe.

Only the angular trace and reciprocal directions in FC12 are already
represented conditionally on its regular diagonal toric interior; their
endpoints remain open. Caps require smooth descent, monodromies require
equivariance, mirrors require lift parity, stratified branches require
transition data, and FC11 lacks the complete metric/coframe data needed for a
global decision.

The atlas therefore supplies a compatibility map, not a selector.

