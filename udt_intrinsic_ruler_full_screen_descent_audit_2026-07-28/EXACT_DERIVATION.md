# Exact derivation — intrinsic ruler and full-screen Hopf descent

## 1. Scope

This is stationary, off-shell geometry in the chosen twisted `R x S3` control:

```text
theta0=exp(-phi)(c_E dt+alpha sigma3),
theta1=exp(+phi)sigma3,
(theta2,theta3)^T=P(sigma1,sigma2)^T,
g=-theta0^2+theta1^2+theta2^2+theta3^2.
```

`phi` and the reciprocal weights are founded. The global `S3`, stationarity, and the displayed
block-screen coframe are chosen existence controls. `P` is every smooth invertible full screen,
including both metric shears. No action, source, carrier, field equation, density, bootstrap value,
boundary law, or dynamics is loaded. As in the parent family, `c_E`, `kappa`, and the twist amplitude
`alpha` are constants; promoting `alpha` to a field is outside this audit.

## 2. The ruler alignment survives every full screen

Let `K=partial_t`. It is a supplied Killing field throughout this stationary family, although that
fact alone does not make its line metric-selected. In the orthonormal coframe,

```text
K_flat=-c_E exp(-phi) theta0,
dtheta0=-dphi wedge theta0+t0 theta2 wedge theta3,
t0=alpha kappa exp(-phi)/det(P).
```

Direct exterior multiplication gives

```text
K_flat wedge dK_flat
  =c_E^2 alpha kappa exp(-3phi)/det(P)
     theta0 wedge theta2 wedge theta3.
```

Therefore, up to spacetime orientation,

```text
omega_K=star(K_flat wedge dK_flat)
       =plus_or_minus c_E^2 alpha kappa exp(-3phi)/det(P) theta1.
```

For `alpha*kappa !=0`, finite `phi`, and invertible `P`, the twist line is exactly the reciprocal
ruler line. Both screen shears can change the nonzero coefficient through `det(P)`, but they cannot
rotate the line away from `theta1`. Rescaling `K` rescales the twist quadratically and likewise
does not change its line.

This is universal inside the registered general-screen coframe for a supplied `K`. Calling it a
metric-intrinsic ruler additionally requires the metric to select `K` rather than coordinates to
supply it.

## 3. The old metric-intrinsic clock certificate persists on open full-screen neighborhoods

The six parent configurations C01–C06 have exact nonzero determinants of the three curvature-
invariant spatial gradients. That rank-three certificate forces the complete continuous Killing
algebra to be the single line `span(K)`.

A curvature-invariant gradient depends continuously on the metric through its third jet. Its `3 x
3` determinant is therefore continuous in the `C3` metric topology. Since each frozen determinant
is exactly nonzero, every C01–C06 configuration has a `C3`-open neighborhood in which it remains
nonzero. Regular logarithmic screen coordinates supply independent perturbations along both shear
tangents in those neighborhoods.

Thus the earlier same-metric clock/ruler result was not a measure-zero diagonal-screen accident:

```text
open general-screen neighborhoods with both shears
  -> rank-three unique K persists
  -> nonzero twist selects theta1.
```

This is an open-neighborhood theorem, not a universal statement about all smooth `P`. On the
rank-deficient strata the old certificate is inconclusive; its failure is not a proof that no other
metric-intrinsic clock selector can exist.

## 4. The spacetime ruler and orbit-space Hopf generator are related but not identical

Let `V` be the registered diagonal Hopf lift with `sigma3(V)=1`, `dt(V)=0`, and period `2 pi` on the
stationary orbit space. Evaluating `theta0,theta1` on `(K,V)` and inverting gives

```text
E0=exp(phi)/c_E K,
E1=exp(-phi)(V-alpha/c_E K),
V =exp(phi) E1+alpha/c_E K.
```

The twist-selected spacetime ruler vector `E1` therefore has a stationary-time component when
`alpha !=0`; its spacetime integral curves are not the closed Hopf fibers. After quotienting by the
stationary `K` flow,

```text
pi_* E1=exp(-phi) V.
```

Its projected line is the Hopf line. The founded one-form normalization is

```text
alpha0=exp(-phi)theta1=sigma3.
```

With

```text
sigma3=cos(eta)^2 dxi1+sin(eta)^2 dxi2,
xi1,xi2 each of period 2 pi,
```

`sigma3(V)=1`, its fiber integral is `2 pi`, and the normalized base curvature flux has magnitude
one. Hence the regular free Hopf bundle is still exact on the chosen `S3` orbit space. This does not
yet say the complete orbit metric is invariant along that circle.

## 5. Necessary and sufficient full-metric descent conditions

The stationary-orbit metric is

```text
q=exp(2phi) sigma3^2 + sigma_screen^T h sigma_screen,
h=P^T P,
sigma_screen=(sigma1,sigma2)^T.
```

In the registered Maurer–Cartan convention,

```text
L_V sigma_screen=kappa R sigma_screen,
R=[[0,-1],[1,0]],
L_V sigma3=0.
```

The `dt^2` coefficient of the complete spacetime metric is `-c_E^2 exp(-2phi)`. Since `c_E` is
nonzero, invariance forces

```text
V(phi)=0.
```

The exact screen Lie derivative is

```text
L_V q_screen
 =sigma_screen^T [V(h)+kappa(hR-Rh)] sigma_screen.
```

Consequently, within this constant-`alpha` stationary family, the complete metric is Hopf-fiber
invariant exactly when

```text
boxed:
V(phi)=0,
V(h)+kappa(hR-Rh)=0.
```

These are conditions on the metric. Requiring a particular `P` to be invariant is too strong and
gauge dependent: `P` may change by a left `O(2)` coframe rotation while `h=P^T P` obeys the metric
condition.

Full-screen anisotropy is not itself an obstruction. The global construction is as follows. Let
`pi:S3->S2` be the supplied Hopf projection and choose any smooth positive metric `q_B` on `S2`.
Its pullback is a global positive horizontal tensor on `S3`. Since the global pair
`(sigma1,sigma2)` spans the horizontal cotangent plane, there is a smooth positive matrix `h` with

```text
pi^* q_B=sigma_screen^T h sigma_screen.
```

The pullback is `V`-invariant, so this `h` obeys the exact equivariance equation. Its unique positive
square root is smooth, and choosing `P=h^(1/2)` supplies a global invertible full screen.

To release both shear polarizations, take `q_B=q_round+epsilon T`, where `T` is a generic smooth
trace-free symmetric tensor on `S2`. Compactness makes this positive for sufficiently small
`|epsilon|`; a generic `T` has both local shear components (it may have topology-required zeros).
No global coframe on `S2` is assumed—the construction uses the global horizontal coframe on the
total `S3` space.

In a local fiber trivialization the same global tensor has the explicit form

```text
h(s)=exp(kappa s R) H0 exp(-kappa s R),
```

then

```text
d h/ds+kappa(hR-Rh)=0.
```

Arbitrary unequal eigenvalues and off-diagonal shear are allowed. For `kappa=-2`, this local
representation is periodic after the registered `2 pi` fiber period. The pullback construction,
not periodicity of one local coordinate alone, supplies the global patching. Thus full Hopf descent
admits constructive global two-shear screens; it does not force a round or isotropic screen.

## 6. The exact compatibility obstruction

If the two descent conditions hold, `V` is a second continuous Killing field of the complete
spacetime metric, independent of the stationary `K`. Every scalar curvature invariant is constant
along both fields. Its spatial gradient therefore annihilates the nonzero spatial fiber direction,
so any `3 x 3` matrix of three such gradients has determinant zero and rank at most two.

Therefore

```text
full Hopf metric descent
  -> at least the two Killing directions K and V
  -> the old rank-three/one-Killing-line certificate cannot hold.
```

This is why the open unique-clock neighborhoods and the exactly fiber-invariant stratum do not
overlap under the old certificate. The six original C01–C06 profiles demonstrate the other side
directly. At their north certificate event the exact Hopf derivative is

```text
V(phi)=3/50 !=0,
```

so those configurations retain their metric-intrinsic clock/ruler result but do not admit full
Hopf metric descent.

Causal character alone does not immediately repair the selection. On a positive compact slice,
small constant combinations `K+Omega V` remain globally timelike by continuity, so the symmetry
plane contains more than one timelike Killing line. This does not prove that no metric-intrinsic
selector exists. It proves only that the registered rank-three uniqueness argument—and the bare
word “timelike”—cannot select one on the descended branch.

## 7. Correct classification

The full-screen ruler result strengthens:

- for any supplied stationary `K`, its nonzero twist selects `theta1` for every invertible `P`;
- the metric itself selects that `K` throughout `C3`-open neighborhoods containing both screen
  shears; and
- founded normalization projects the ruler to the same regular Hopf circle on the chosen orbit
  `S3`.

But the strongest old intrinsic-clock certificate and full metric descent occupy different strata:

```text
OPEN_UNIQUE_CLOCK_STRATUM:
  metric selects K by rank three; Hopf bundle exists; full metric generally does not descend.

FIBER_INVARIANT_DESCENT_STRATUM:
  full two-shear metric descends; K and V are both Killing; old unique-K selector fails.
```

The smallest remaining seam is not whether shear destroys the ruler or the Hopf bundle. It is
whether the complete fiber-invariant metric supplies a native way to distinguish the founded clock
line inside its two-dimensional Killing symmetry plane—or whether a global framing/observer rule
is genuinely additional.

No physical branch, topology, carrier, round target, action, source, boundary, density, bootstrap
fixed point, mass, scale, time-live law, signal law, or canon follows.
