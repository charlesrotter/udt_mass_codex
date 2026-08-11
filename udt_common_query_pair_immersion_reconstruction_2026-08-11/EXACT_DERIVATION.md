# Exact derivation and numerical realization

## 1. Declared geometry

For a supplied regular timelike immersion

```text
F:Sigma^2 -> (M^4,g),
```

the first fundamental form is

```text
h_ij=g(F_*partial_i,F_*partial_j).
```

On the calibrated regular stratum `h00<0`, `det(h)<0`, the unique positive decomposition is

```text
h=-T^2(dy+beta ds)^2+L^2 ds^2,
T^2=-h00,
beta=h01/h00,
L^2=h11-h01^2/h00,
kappa_pair=(1/4)log(-det h),
phi_pair=(1/4)log[(-det h)/h00^2].
```

This is an algebraic evaluator on a supplied immersion. It does not construct the immersion.

## 2. Query Q1 — stationary R17 Hopf-cylinder leaf

The exact immersion is

```text
F_R17(y,s)=(0.07+y,1.08,0.31,0.44+2s)
```

in the registered `R17_P1_P` metric (`lambda=1`, `epsilon=0.12`, `a=0.4`). Its image is the
intrinsic integral leaf of `span(T,Z)` through the G63 point. Direct pullback gives

```text
det h=-1,
kappa_pair=0,
phi_pair=phi=0.12431893015094263,
beta_pair=a=0.4.
```

The `s`-ruling is not an ambient geodesic on this witness:

```text
||nabla_s F_s|| = 1.197298079e-2       (independent replay).
```

Therefore this declared query owns the leaf, its second fundamental form, normal connection, and
surface loops, but it does not own the G63-style geodesic Jacobi channel. Its registered status is
`NOT_OWNED_BY_QUERY`, not a negative result about other R17 queries.

## 3. Query Q2 — complete time-live Fermi surface

At the registered `TL_P2` point, let `(e0,e1)` be the first two vectors of the inverse complete
coframe. Construct the observer germ as the timelike geodesic `z_A(y)` with initial tangent `e0`,
parallel transport `e1` to a ruler `n(y)`, and define

```text
F_TL(y,s)=Exp_zA(y)[s n(y)].
```

The `s`-rulings are affinely parameterized spacelike geodesics. Because the construction is a
geodesic variation, `J=F_*partial_y` satisfies

```text
nabla_s nabla_s J + R(J,F_s)F_s = 0.
```

The corrected production balance at the three registered outer scales is

```text
scale       ||Jacobi residual||     ||second term||    ||curvature term||
0.004       1.7672e-7               1.176666e-1        1.176668e-1
0.002       1.1830e-7               1.176668e-1        1.176668e-1
0.001       2.3802e-7               1.176668e-1        1.176669e-1
```

The independent fixed-RK4/real-difference replay gives relative balance defect
`8.9671e-7`. The outer production sequence is not monotone, so the claim is numerical consistency
plus independent reproduction, not a formal continuum proof.

At the base of this Fermi query, calibration and parallel/geodesic initial conditions give
numerically

```text
det h=-1.00000000114,
kappa_pair=2.85e-10,
phi_pair=3.78e-10,
beta_pair=-1.18e-10,
||nabla_s F_s||=8.96e-10.
```

This near-Minkowski pair readout is local Fermi calibration at one point. It does not make the
ambient time-live metric flat: all eleven registered scalar/mixing fields have nonzero first-
derivative norm there, and both ambient and normal loop returns are nonidentity.

## 4. Common intrinsic/extrinsic decomposition

With the convention

```text
R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y]Z,
```

write

```text
nabla^M_X Y=nabla^Sigma_X Y+II(X,Y),
nabla^M_X nu=-A_nu X+D^perp_X nu.
```

The implemented Gauss component is

```text
<R^M(X,Y)Z,W>-<R^Sigma(X,Y)Z,W>
 +<II(X,W),II(Y,Z)>-<II(X,Z),II(Y,W)>=0.
```

Codazzi and Ricci are evaluated with the same tangent/normal frame and curvature convention. On
Q1 all three corrected production residuals decrease by approximately four when the outer scale
is halved:

```text
scale       Gauss         Codazzi       Ricci
0.004       1.027e-6      4.345e-7      3.318e-7
0.002       2.568e-7      1.086e-7      8.295e-8
0.001       6.422e-8      2.716e-8      2.074e-8
```

On Q2, Gauss and Ricci converge to `7.92e-9` and `3.90e-9`. The Q2 Codazzi sequence is nonmonotone
(`1.61e-7`, `5.00e-7`, `2.41e-7`) and is therefore
`NUMERICALLY_UNRESOLVED` under the registered contract. It is not converted into a negative or a
positive certification.

## 5. Finite loops from the same surfaces

For each query, ambient transport and metric-projected normal transport were evaluated around the
same shrinking rectangles in `Sigma`. Path-ordered transport used `8`, `16`, and `32` subdivisions
per edge. Both quadrature differences decrease by approximately four, and ambient metric defects
remain at or below `3.9e-10`.

The finite-loop return divided by area approaches the independently reconstructed curvature
generator. At the smallest loop:

```text
query        ambient relative difference   normal relative difference
Q1 R17       6.12e-4                       7.39e-4
Q2 TL        2.25e-5                       7.85e-7
```

Thus endpoint depth, ambient transport, and normal transport coexist on one typed surface without
being identified as one scalar.

## 6. Extrinsic nonuniqueness control

In Minkowski space, the plane

```text
F0(t,s)=(t,s,0,0)
```

and cylinder

```text
FR(t,s)=(t,R cos(s/R),R sin(s/R),0)
```

both induce `h=-dt^2+ds^2`, but `II_F0=0` and `II_FR(ss)=-n/R`. The independent replay uses
`R=1.7` and obtains `II_ss=-0.5882352941` with exactly equal first fundamental forms.

Therefore `h`, and hence `(kappa,phi,beta)`, cannot reconstruct the extrinsic channels. The common
object is the supplied immersion/query realization, not its terminal two-metric alone.

## 7. Exact bounded landing

The two query classes own different channel sets:

```text
Q1 exact intrinsic leaf:
  h + endpoint readout + II + normal connection + surface holonomy;
  no geodesic Jacobi channel for its declared nongeodesic ruling.

Q2 Fermi/exponential surface:
  h + endpoint readout + II + normal connection + query-owned Jacobi field
  + ambient and normal surface holonomy.
```

The primary preregistered landing is therefore

```text
QUERY_CLASS_DEPENDENT_CHANNEL_ARCHITECTURE
```

with the secondary scoped result

```text
COMMON_QUERY_CHANNELS_COMPATIBILITY_LINKED_WITH_RETAINED_EXTRINSIC_DATA.
```

This is a bounded geometric result. It selects no physical query or branch.

