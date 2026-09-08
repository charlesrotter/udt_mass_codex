# G331 exact derivation — nonsymmetric Ricci eigenlines versus closed Hopf fibres

Date: 2026-09-03

## 1. Scope

G330 established an intrinsic Hopf line on the supplied non-round Berger family

```text
gamma_0 = a^2 (sigma_1^2 + sigma_2^2) + c^2 sigma_3^2,
a > 0, c > 0, a != c.
```

Its spatial Ricci endomorphism has horizontal double eigenvalue and vertical simple eigenvalue

```text
lambda_h = 4/a^2 - 2 c^2/a^4,
lambda_v = 2 c^2/a^4,
Delta_0 = abs(lambda_v-lambda_h) = abs(4(c^2-a^2)/a^4) > 0.
```

Berger symmetry then supplied a second fact: the simple eigenline is tangent to a closed `U(1)`
action, so its leaves are the Hopf circles. G331 tests these two facts separately under smooth
nonhomogeneous metric perturbations. No independent carrier, action, source, matter field, or
physical history is added.

## 2. Uniform eigengap theorem on the complete nearby metric class

Let `gamma` be another positive Riemannian metric on `S3`. There is a unique positive,
`gamma_0`-self-adjoint bundle endomorphism `B` such that

```text
gamma(u,v) = gamma_0(Bu,v).
```

Let `A_gamma=gamma^{-1} Ric(gamma)` be its Ricci endomorphism and put

```text
Ahat_gamma = B^(1/2) A_gamma B^(-1/2).
```

This is self-adjoint in the one fixed metric `gamma_0`. Thus the comparison with
`A_0=gamma_0^{-1} Ric(gamma_0)` is typed on a common inner-product bundle rather than made between
unrelated component matrices.

Ricci depends continuously on a metric and its first two derivatives. Hence

```text
gamma -> gamma_0 in C2  implies  Ahat_gamma -> A_0 uniformly on compact S3.
```

Choose a neighborhood for which

```text
sup_p ||Ahat_gamma(p)-A_0(p)|| < Delta_0/2.
```

The self-adjoint eigenvalue bound places one perturbed eigenvalue inside the interval of radius
`epsilon` around `lambda_v` and the other two inside the interval of radius `epsilon` around
`lambda_h`, with `2 epsilon < Delta_0`. The intervals are disjoint. The first cluster therefore
has rank one at every point.

The associated Riesz/spectral projector `P_gamma` is globally defined and varies continuously. If
`gamma` is smooth, `Ahat_gamma`, `P_gamma`, and the line

```text
L_gamma = image(P_gamma)
```

are smooth. More generally a `Ck` metric gives a `C(k-2)` Ricci projector wherever the simple gap
is open. This two-derivative loss is part of the theorem; a bare `C0` metric perturbation is not
enough.

This proves a full-neighborhood statement. It is not a one-mode or symmetry-reduced test.

## 3. What `S3` topology gives—and does not give

Real line bundles are classified by `H1(-;Z2)`. Because

```text
H1(S3;Z2) = 0,
```

the continued line bundle is trivial. It therefore has a global nonzero section and a global unit
representative after using `gamma`. On connected `S3`, the two representatives `V` and `-V` remain
equally valid; the metric selects no sign.

Every nonvanishing smooth line field integrates to a one-dimensional foliation. Neither line-bundle
triviality nor a Ricci eigengap says that those leaves are periodic, share one period, or form the
fibres of a smooth quotient by `S1`.

## 4. A genuinely nonhomogeneous local tilt

The three-dimensional conformal Ricci law for

```text
gamma_epsilon = exp(2 epsilon f) gamma_0
```

is exact:

```text
Ric(gamma_epsilon)
 = Ric(gamma_0) - Hess(u) + du tensor du
   - (Delta u + |du|^2) gamma_0,
u = epsilon f.
```

At a point `p`, choose a `gamma_0`-orthonormal Ricci eigenframe with `e_3` vertical. A smooth bump
supported in a normal coordinate ball can be chosen so that

```text
f(p)=0,
df(p)=0,
Hess(f)(e_1,e_3)=1,
Delta f(p)=2.
```

For example, multiply `x_1 x_3+x_1^2` by a cutoff which is one near `p`. Then, exactly at `p`,

```text
Ric(gamma_epsilon)(e_1,e_3) = -epsilon,
R(gamma_epsilon)(p) = R(gamma_0)-8 epsilon.
```

Outside the bump support the scalar curvature remains the Berger constant. Therefore every small
nonzero member is nonhomogeneous and is not merely a diffeomorphic copy of `gamma_0`. The old
vertical Hopf direction is not its Ricci eigenline at `p`, while Section 2 guarantees that a nearby
simple eigenline still exists for sufficiently small `epsilon`.

This witness is a spatial metric statement. G331 does not assert that the displayed bump, paired
with an unspecified extrinsic curvature, solves the vacuum constraint equations.

## 5. Explicit nearby metrics with an irregular Ricci eigenflow

The stronger orbit-closure control is metric-owned. Write

```text
S3 = {(z_1,z_2) in C2 : |z_1|^2+|z_2|^2=1},
x = |z_1|^2,
eta_0 = x dphi_1 + (1-x) dphi_2.
```

For positive weights `w_1,w_2`, define

```text
F = w_1 x + w_2(1-x),
eta = eta_0/F,
xi = w_1 partial_phi1 + w_2 partial_phi2,
zeta = (w_2 dphi_1-w_1 dphi_2)/F,
```

and the global weighted contact metric

```text
g_w = dx^2/[4x(1-x)F] + [x(1-x)/F] zeta^2 + eta^2.
```

The apparently singular angular coordinates are only a chart presentation. The construction from
the global standard contact distribution extends smoothly across `x=0,1`. Directly,

```text
eta(xi)=1,
i_xi d eta=0,
g_w(xi,xi)=1.
```

Thus `xi` is the Reeb field of the weighted contact form. The metric is the corresponding
three-dimensional Sasaki metric. The Sasaki curvature identity, also recomputed directly from the
displayed coordinate metric in both implementations, is

```text
Ric(g_w)^sharp
 = lambda_h(x) I + [2-lambda_h(x)] xi tensor eta,
lambda_h(x) = [R(g_w)(x)-2]/2.
```

Therefore `xi` is an exact spatial-Ricci eigenvector with eigenvalue `2`. For unequal weights its
scalar curvature is nonconstant, so the metric is nonhomogeneous.

This family approaches every non-round Berger metric. If the desired Berger radii are `(a,c)`, set

```text
w = a^2/c^2,
mu = a^4/c^2.
```

At equal weights,

```text
mu g_(w,w) = a^2 H + c^2 eta_0^2 = gamma_0,
```

where `H` is the standard horizontal round metric. The scaled vertical Ricci eigenvalue is

```text
2/mu = 2c^2/a^4,
```

exactly G330's `lambda_v`. Since `a!=c`, the base gap is nonzero. Compactness and continuity then
keep the `xi` line simple for all weights sufficiently near `(w,w)`.

The flow is explicit:

```text
(z_1,z_2) -> (exp(i w_1 t) z_1, exp(i w_2 t) z_2).
```

On every torus with `z_1 z_2 != 0`, its orbit closes exactly when `w_1/w_2` is rational. Irrational
ratios are dense. For example, weights proportional to

```text
(1+sqrt(2)/n, 1-sqrt(2)/n)
```

approach equal weights and have irrational ratio. Their generic orbits are dense on invariant
two-tori; only the two coordinate-axis orbits remain closed. Consequently these arbitrarily close,
nonhomogeneous metrics retain a simple metric-defined Ricci eigenline but do not define a circle
fibration by that line.

This is stronger than a free-vector-field counterexample: the nonclosed flow is itself the exact
Ricci eigenline of the displayed metric. It is still a geometric configuration-space result. G331
does not claim this weighted family has been embedded into the active vacuum constraint manifold.

## 6. Exact boundary of the G330 integer

G330 used every leaf's closed metric orbit and common fibre length to define

```text
eta_normalized = (2 pi/ell_fibre) alpha
```

and then obtained absolute helicity one. In the irrational weighted family, generic leaves have no
period and the orbit space is not a smooth `S2` quotient. There is no common `ell_fibre`. G330's
period-normalized connection and its registered integer are therefore unavailable.

The contact volume `integral eta wedge d eta` still exists, and other framed or contact invariants
may be studied. Substituting one of those would be a new mathematical object and cannot be used to
claim that G330's exact invariant survived.

Hence the perturbation boundary is sharp:

- a uniform simple Ricci eigenline is `C2`-open;
- closed Hopf fibres and the G330 period normalization are not open in the surrounding spatial
  metric space.

## 7. Conditional local dynamics

Suppose a smooth Cauchy datum is independently known to satisfy the active provisional vacuum
constraints and its spatial metric lies in the gap-open neighborhood. Conditional on the imported
smooth Einstein-Cauchy theorem, its local development gives a smooth family of induced spatial
metrics in a chosen local foliation. Uniform gap continuity then supplies a nonzero interval on
which the rank-one Ricci line persists.

Unlike G330, no `U(2)` symmetry inheritance is used. Accordingly no closed-orbit or Hopf-fibration
carry follows. The exact bump and weighted metrics above are not promoted to lawful Cauchy data:
their constraint embedding remains open. No energetic, orbital, nonlinear long-time, or maximal
development stability is claimed.

## 8. Controls and ownership

- At `a=c`, `Delta_0=0`; the perturbation theorem does not choose a continuation through the round
  degeneracy.
- A diffeomorphic pullback carries the projector and fibres covariantly and is only a gauge control.
- A common homothety rescales Ricci eigenvalues but not the eigenline.
- `V` and `-V` describe the same line; no orientation is selected.
- Other spatial topologies do not inherit the `H1(S3;Z2)=0` step automatically.
- The weighted contact/Sasaki family is a mathematical test family, not a UDT field, action,
  source, matter model, or occupancy premise.

## 9. Bounded landing

```text
UNIFORM_RICCI_GAP_PRESERVES_GLOBAL_SMOOTH_EIGENLINE
__ARBITRARILY_CLOSE_NONHOMOGENEOUS_METRICS_CAN_HAVE_IRREGULAR_NONCLOSED_RICCI_EIGENFLOW
__HOPF_FIBRATION_AND_G330_PERIOD_NORMALIZATION_ARE_NOT_PERTURBATION_OPEN
__LOCAL_DYNAMIC_CARRY_REMAINS_CONSTRAINT_COMPATIBLE_AND_GAP_CONDITIONAL
```

Maximum pre-external-review grade:

```text
DERIVED_CONDITIONAL__INTERNAL_EXACT_AND_INDEPENDENT_CHECKS_ONLY
```
