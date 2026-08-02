# Exact derivation — complete FC07 full-screen witnesses

Date: 2026-08-01  
Base: `06858a8e4f9fedfe3921b8083748193f24f945de`

## 1. Scope and selected existence control

This is an exact construction inside the registered `FC07_PERIODIC_TORUS_BUNDLE` class and the
registered direct-sum spectator extension of the founded reciprocal pair. The block extension,
constant depth, zero shift, and zero pair-screen mixing are selected existence controls, not a
unique UDT four-dimensional extension.

No action, variation, source, carrier, density, bootstrap equation, stability condition, desired
filter, or field equation is used.

## 2. Mapping-torus domain

For every registered `M in GL(2,Z)`, define

```text
Sigma_M = ([0,1] x T2) / ((1,y) ~ (0,M y)).
```

Unimodularity makes `y -> M y` a diffeomorphism of `T2`. The quotient is therefore a smooth compact
three-manifold. The determinant-minus-one rows are nonorientable and overlap the registered FC09
description; this overlap does not create another independent family.

Convention: the boundary map `F` sends the `s=1` side to the `s=0` side. For comparison with the
parent graph notation, define `v_minus` as the vector at `s=1` and `v_plus` as its image at `s=0`,
so `v_plus=M v_minus`. Reversing the plus/minus naming would display `M^-1` instead; no geometry or
fiber count changes.

## 3. Full screen metric and smooth seam

Let

```text
h0 = [[a,b],[b,d]],       a>0, ad-b^2>0,
h1 = M^T h0 M.
```

For any nonzero vector `v`,

```text
v^T h1 v = (Mv)^T h0 (Mv) > 0,
```

so `h1` is positive definite. Also

```text
det(h1)=det(M)^2 det(h0)=det(h0).
```

Use the standard smooth flat step. With `eta(u)=0` for `u<=0` and `eta(u)=exp(-1/u)` for `u>0`,
set

```text
chi(s)=eta(s)/(eta(s)+eta(1-s)).
```

Then `chi(0)=0`, `chi(1)=1`, and every positive-order derivative vanishes at both endpoints. Define

```text
h(s)=(1-chi(s))h0+chi(s)h1.
```

The positive-definite cone is convex because

```text
v^T h(s) v=(1-chi)v^T h0 v+chi(Mv)^T h0(Mv)>0.
```

At order zero, the boundary pullback is exactly `h1=M^T h0 M`. Every higher endpoint derivative is
zero on both sides, so every transformed jet matches. This produces a smooth `C-infinity` metric on
the quotient, not merely a local fundamental-domain profile.

## 4. Four-dimensional metric and nondegeneracy

For symbolic `c_E>0`, `L>0`, and finite constant `phi0`, take

```text
g=-c_E^2 exp(-2phi0) dt^2 + L^2 exp(2phi0) ds^2 + dy^T h(s)dy.
```

Its determinant is

```text
det(g)=-c_E^2 L^2 det(h(s))<0.
```

The reciprocal depth factors cancel in the determinant; no numerical scale or depth is selected.
The metric is smooth and Lorentzian everywhere.

## 5. Coframe descent and the orientation split

Choose the positive-oriented square-root screen matrices `P0,P1`, so
`h0=P0^T P0`, `h1=P1^T P1`, and both determinants are positive. Let `A=P0 M`. Since

```text
A^T A=M^T h0 M=h1=P1^T P1,
```

the exact seam factor

```text
O=P1 A^-1
```

obeys `O^T O=I` and `P1=O P0 M`. Its determinant is

```text
det(O)=sign(det(M)).
```

For `det(M)=+1`, `O` lies in connected `SO(2)`. A smooth screen-gauge path from identity to
`O^-1`, flat at its endpoints, converts the square-root coframe into one satisfying
`P(1)=P(0)M`. Thus six registered rows possess global oriented coframes for the same descended
metric.

For `det(M)=-1`, `O` is a reflection and cannot be joined to the identity inside one orientation
component. Those two rows possess smooth complete metrics and local coframes with a reflection
transition, but not a single global oriented coframe.

## 6. Seven metric fibers from eight monodromies

On the three independent screen-metric components `(a,b,d)`, congruence by
`M=[[p,q],[r,s]]` acts linearly as

```text
a' = p^2 a + 2pr b + r^2 d,
b' = pq a + (ps+qr)b + rs d,
d' = q^2 a + 2qs b + s^2 d.
```

Exact comparison of all eight registered operators gives 27 distinct pairs and one collapsed pair:

```text
C_I = C_-I.
```

Hence the realized local **metric** endpoint fibers form seven classes. The identity and central
sign mapping tori remain different global monodromy/topology data, but the metric's quadratic
readout cannot distinguish their endpoint congruence. This refines rather than contradicts the
parent abstract `Graph(M)` census: eight linear presentations become seven after metric readout.

The exact generic control `h0=[[2,1/3],[1/3,5]]` gives seven different endpoint metrics, one for
each congruence class. It is an arithmetic distinction control, not a physical screen choice.

The fiber law is lattice-basis covariant. Under `y=B y'`,

```text
M'=B^-1 M B,       h'=B^T h B,
C_M'(h')=B^T C_M(h)B.
```

This identity was checked exactly for every frozen row with exchange and shear basis changes. The
seven-class count is a count of the frozen representatives' metric congruence operators, not an
exhaustive classification of `GL(2,Z)` conjugacy classes or mapping-torus diffeomorphism types.

## 7. Which monodromies force screen variation?

Solving `M^T h0 M=h0` on the full symmetric screen gives:

| monodromy | invariant symmetric form | positive-definite member? |
|---|---|---|
| identity | `(a,b,d)` | yes, full cone |
| minus identity | `(a,b,d)` | yes, full cone |
| order four | `(d,0,d)` | yes |
| order six | `(d,d/2,d)` | yes |
| parabolic | `(0,0,d)` | no |
| hyperbolic | `(-d,d/2,d)` | no |
| exchange | `(d,b,d)` | yes when `d>|b|` |
| reversing glide | `(2b,b,d)` | yes when `b>0,d>b/2` |

Thus six monodromies admit constant-screen subfamilies. Parabolic and hyperbolic monodromy admit no
positive-definite fixed screen, so every positive complete witness must change its screen metric
somewhere around the base circle. This is forced geometric variation, not dynamics or physical
time evolution.

## 8. Global projector and nonparallelism

The full transition on `(t,s,y)` is `T=diag(1,1,M)`. The screen projector

```text
Pi=diag(0,0,1,1)
```

obeys `T Pi=Pi T`; it therefore descends globally for all eight witnesses. Both its vertical
`T2` distribution and the complementary `(t,s)` distribution are integrable.

This does not make the split parallel. Where `dh/ds` is nonzero,

```text
Gamma^a_(s b)=1/2 (h^-1 h')^a_b,
Gamma^s_(a b)=-1/(2 L^2 exp(2phi0)) h'_ab,
```

so the Levi-Civita connection mixes the two blocks. Parabolic and hyperbolic monodromies force such
mixing somewhere in every positive witness in this block class. The other six allow both constant
and varying screen members. No parallelism premise is imposed.

## 9. Completeness

`Sigma_M` is compact and its constructed spatial metric is smooth positive definite. Hopf-Rinow
therefore makes the spatial metric geodesically complete.

The four-metric is the direct product of a constant timelike line with that spatial metric. Its
geodesic equations split into `d2t/dlambda2=0` and the spatial geodesic equation. The time solution
extends for every affine parameter, and spatial completeness extends the other component.
Therefore all eight constructed four-metrics are Lorentzian geodesically complete.

## Maximum conclusion

```text
FC07_COMPLETE_OFFSHELL_FULL_SCREEN_METRIC_WITNESS_FAMILY_EXISTS
SEVEN_FROZEN_REPRESENTATIVE_ENDPOINT_CONGRUENCE_FIBERS_FROM_EIGHT_REGISTERED_MONODROMIES
SIX_GLOBAL_ORIENTED_COFRAMES_PLUS_TWO_LOCAL_TRANSITION_COFRAMES
NO_PHYSICAL_SELECTION_DYNAMICS_STABILITY_BOOTSTRAP_OR_MATTER
```
