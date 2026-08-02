# Exact derivation — functional persistence of the intrinsic projector

## 1. Scope and type

This is configuration-space geometry in the registered stationary complete off-shell family

```text
theta0 = exp(-phi) (dt+a sigma3),
theta1 = exp(+phi) sigma3,
(theta2,theta3)^T = P(q) (sigma1,sigma2)^T,
g = -theta0^2+theta1^2+theta2^2+theta3^2,
```

on `R x S3`.  The primary centers retain `a=1/64` and the Maurer--Cartan coefficient
`kappa=-2`.  The profile `phi` and full screen `P:S3->GL(2,R)` are released in stationary smooth
functional neighborhoods.  No action, equation of motion, carrier, bootstrap return, density,
source, boundary law, stability condition, or physical label enters.

The six centers are

```text
phi0=F_GENERIC/50,
P0=exp(lambda phi0) I,
lambda=-2,-1,0,1/2,1,2.
```

The result is an open-neighborhood theorem in this bounded family, not an explicit radius and not a
classification of every stationary or time-dependent UDT metric.

## 2. Why all five gates are open

### Intrinsic clock certificate

At every center, the three complete-metric scalar invariants `(I1,I2,I3)` have independent spatial
gradients at the registered north event.  Their exact determinants are nonzero in
`CENTER_NEIGHBORHOOD_ATLAS.tsv`.

The metric and the invariant gradients depend continuously on the `C3` jets of `phi` and `P`.
Therefore each nonzero determinant stays nonzero on some open `C3` neighborhood.  Every member of
that neighborhood remains stationary, so `K=partial_t` is Killing.  The inherited one-jet Killing
argument then makes its line the unique continuous Killing line.

This is a sufficient certificate.  The determinant-zero locus is a **certificate wall**, not a
theorem that no intrinsic clock exists there.

### Global twist-selected ruler

Let `A=dt+a sigma3`.  Since

```text
K_flat = -exp(-2phi) A,
d sigma3 = kappa sigma1 wedge sigma2,
theta2 wedge theta3 = det(P) sigma1 wedge sigma2,
```

direct exterior algebra gives

```text
star(K_flat wedge dK_flat)
  = plus_or_minus [a kappa exp(-3phi)/det(P)] theta1.
```

Thus, throughout the smooth global family, nonzero `a`, nonzero `kappa`, and invertible `P` make the
clock twist span the same global unoriented ruler line `theta1`.  The result is exact throughout the
family, not merely continuous near the centers.

### Projector and screen

Normalize the clock and ruler lines to `u` and `n`.  In the positive rank-three bundle
`E=u_perp`,

```text
P_n = n tensor n_flat,     rank(P_n)=1,
Q   = I_E-P_n,             rank(Q)=2.
```

The signs of `u` and `n` cancel.  The projector and its unique orthogonal complement therefore exist
wherever the two line gates hold.

### Global configuration and displayed slice

Relative to `(dt,sigma3,sigma1,sigma2)`,

```text
det(coframe)=det(P),
det(g)=-det(P)^2.
```

Every finite smooth `phi` and smooth globally invertible `P` gives a smooth global Lorentzian
configuration.  The displayed `t=constant` slice is positive exactly when

```text
exp(4phi)>a^2.
```

At each center, compactness of `S3` supplies uniform positive margins for `det(P)` and the slice
inequality.  Small `C0` perturbations preserve them; a `C3` neighborhood is therefore more than
sufficient.  The equality `exp(4phi)=a^2` degenerates this displayed slice, not the four-metric.

### Nonzero relative projector curvature

The relative curvature of the rank-one reduction is

```text
Omega_rel(X,Y)=Q[(D_X P_n),(D_Y P_n)]Q.
```

It depends continuously on the metric/projector first jets.  Every center has a nonzero exact
north-event component, so every center has an open `C1`, hence `C3`, neighborhood in which
`Omega_rel` is nonzero somewhere.

Together these five facts prove an open functional neighborhood around each C01--C06 center.  They
do not provide a numerical neighborhood radius.

## 3. General first-jet response algebra

Write

```text
dphi = p1 theta1+p2 theta2+p3 theta3,
L_A  = (E_A P)P^-1,
C    = P R P^-1,
m    = kappa exp(-phi),
t1   = kappa exp(+phi)/det(P).
```

In the screen basis, the connection vectors mixing the ruler with the screen are

```text
v0 = (0,0),
v1 = (-p2,-p3),
v2 = (A,B+t1/2),
v3 = (B-t1/2,D),

A = L1_11+c11 m,
B = [L1_12+L1_21+(c12+c21)m]/2,
D = L1_22+c22 m.
```

The screen endomorphism is two-dimensional, so its oriented scalar components are simply

```text
W_AB = det(v_A,v_B).
```

The three potentially nonzero components are

```text
W12 = p3 A-p2(B+t1/2),
W13 = p3(B-t1/2)-p2 D,
W23 = A D-B^2+t1^2/4.
```

The complete local relative response vanishes at an event exactly when all three vanish.  A zero of
only `W23` is not a complete-response wall.  Under an orientation-preserving screen-frame change,
the `v_A` rotate together and every `W_AB` is unchanged; a reflection changes their common sign but
not the zero/nonzero ruling.

## 4. Exact symmetric screen charts

At the north event, `phi=0` and `P=I`.  For

```text
P=exp[phi M],
M=lambda I+mu S1+nu S2,
```

the exact response is

```text
W12 = (6lambda+6mu-3nu+50)/2500,
W13 = (-3lambda+3mu+6nu+100)/2500,
W23 = 1+(9/2500)(lambda^2-mu^2-nu^2).
```

Consequences:

- Equal screen (`mu=nu=0`): `W23=1+(3lambda/50)^2 >= 1`.  The north-event response is nonzero for
  every real `lambda`; the six sampled values were not special points on that axis.
- One `S1` shear (`nu=0`): there is one complete north-event zero at
  `(lambda,mu)=(25/2,-125/6)`.
- One `S2` shear (`mu=0`): there is one complete north-event zero at
  `(lambda,nu)=(-200/9,-250/9)`.
- Both shears: the complete north-event zero set is the affine line

```text
lambda = 5nu/4+25/2,
mu     = -3nu/4-125/6,
nu     = any real number.
```

These are exact off-shell response-certificate strata.  A zero at the north event does not prove
that the response vanishes elsewhere on the complete configuration, and none of the strata is a
field equation, instability, or physical branch.

## 5. Wall atlas and scope

The released family contains several different kinds of boundary and they must not be conflated:

- `det(P)=0`: actual coframe/four-metric degeneracy;
- `exp(4phi)=a^2`: displayed-slice degeneracy while the four-metric remains Lorentzian;
- `a*kappa=0`: loss of this registered twist ruler selector;
- curvature-fingerprint determinant zero: failure of one sufficient clock certificate;
- all `W12,W13,W23=0` at an event: local relative-response certificate wall;
- `v=0` in polar shear coordinates: a chart failure repaired by regular `log(H)` coordinates.

The complete wall census is `DEGENERACY_WALL_ATLAS.tsv`.  Nothing is discarded because it lacks a
desired shape.

## 6. Relation to the stability and bootstrap hypotheses

The intrinsic-projector geometry is not a fine-tuned property of six isolated configurations.  It
persists on six functional neighborhoods and through the entire equal-screen axis.  This strengthens
its usefulness as a possible geometric ingredient in the stability program.

It does **not** establish energetic or dynamical stability, select the `S2` carrier, integrate the
conditional response as `L2+L4`, or put any configuration on shell.  A separately stated bootstrap
or native field equation may later be intersected with this map.  It may not be retrofitted to choose
the positive region.

Maximum conclusion:

```text
DERIVED_CONDITIONAL_ON_THE_REGISTERED_STATIONARY_COMPLETE_OFFSHELL_FAMILY:
EACH_C01_C06_CENTER_LIES_IN_AN_OPEN_CONFIGURATION_NEIGHBORHOOD_WITH_THE
INTRINSIC_CLOCK_RULER_PROJECTOR_GATES_AND_NONZERO_RELATIVE_CURVATURE_SOMEWHERE.
```

