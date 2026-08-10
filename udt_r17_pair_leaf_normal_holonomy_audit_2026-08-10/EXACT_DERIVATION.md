# Exact derivation — R17 pair-leaf normal connection and holonomy

Date: 2026-08-10

Status ceiling before a fresh external adversarial review: `LOCAL_VERIFIED_LEAD`.

## 1. Supplied geometry and scope

On the regular stationary R17/W01 family,

```text
theta0 = u^-1 (dt + a sigma3)
theta1 = u sigma3
theta2 = v sigma1
theta3 = v sigma2
u = exp(phi) > 0
v = exp(lambda phi) > 0
```

the dual orthonormal frame is

```text
e0 = u T
e1 = u^-1 (Z - a T)
e2 = v^-1 X
e3 = v^-1 Y.
```

Take the Maurer--Cartan convention

```text
[X,Y] = 2 epsilon_MC Z
[Y,Z] = 2 epsilon_MC X
[Z,X] = 2 epsilon_MC Y,
```

where `epsilon_MC=+1` or `-1`.  Write `p1=Z(phi)`, `p2=X(phi)`, and
`p3=Y(phi)`.  The already-derived pair distribution is

```text
E = span(e0,e1) = span(T,Z),
```

and its metric-orthogonal rank-two normal bundle is

```text
H = span(e2,e3).
```

The calculation below derives only the connection induced on `H` by the Levi--Civita connection
of this supplied metric, restricted to directions tangent to `E`.  It does not identify that
connection with a complete physical observer arrow.

## 2. Full bracket reconstruction

Direct differentiation of the inverted coframe gives

```text
[e0,e1] = -(p1/u) e0
[e0,e2] = -(p2/v) e0
[e0,e3] = -(p3/v) e0

[e1,e2] = (p2/v)e1 - (lambda p1/u)e2 + (2 epsilon_MC/u)e3
[e1,e3] = (p3/v)e1 - (2 epsilon_MC/u)e2 - (lambda p1/u)e3

[e2,e3] = (2 epsilon_MC a/(u v^2))e0
          + (2 epsilon_MC u/v^2)e1
          + (lambda p3/v)e2
          - (lambda p2/v)e3.
```

In particular, `[e0,e1]` has no `e2` or `e3` component, so the derived pair leaves remain
involutive.  No bracket coefficient is assigned in either implementation.

## 3. Metric-owned projected normal connection

For an oriented local screen frame `(e2,e3)`, define

```text
D_V s = H(nabla_V s),
A(V) = g(nabla_V e2,e3),    V in E.
```

The exact Koszul formula gives

```text
A(e0) = epsilon_MC a/(u v^2)
A(e1) = epsilon_MC (2/u - u/v^2).
```

In the global leaf basis `(T,Z)`, using `T=e0/u` and
`Z=u e1+(a/u)e0`, this becomes

```text
A_T = epsilon_MC a/(u^2 v^2)
A_Z = epsilon_MC [2 - u^2/v^2 + a^2/(u^2 v^2)].
```

This is a genuine connection one-form, not itself a gauge-invariant observable.  Under a local
screen rotation by `alpha`, `A -> A+d alpha`.

## 4. Curvature on every pair leaf

Because `SO(2)` is abelian, the normal curvature is `F_perp=d_E A`.  Evaluating it on the
orthonormal pair basis gives

```text
F_perp(e0,e1)
  = epsilon_MC 2 a (1+lambda) p1/(u^2 v^2)
  = epsilon_MC 2 a (1+lambda) Z(phi)
      exp[-2(1+lambda)phi].
```

Its orientation-free square is

```text
4 a^2 (1+lambda)^2 [Z(phi)]^2 exp[-4(1+lambda)phi].
```

Three distinct flat strata therefore occur:

```text
lambda = -1;
a = 0;
Z(phi) = 0.
```

For the supplied twisted generic arena (`a != 0`, generic `Z(phi) != 0`), every listed lambda
except `-1` has locally curved normal transport.  This is a classification, not a lambda selector.

## 5. Contractible and wound holonomy are different data

Each pair leaf is a cylinder `R x S1`.  If `C` is a contractible loop bounding a leaf region
`Sigma`, parallel transport in the chosen oriented screen frame is

```text
Hol(C) = exp[-J integral_Sigma F_perp],
```

where `J` is the generator of screen rotations.  This is local curvature holonomy.

For a loop winding `n` times around the Hopf circle, define on a reference fiber

```text
Theta_base = integral_0^(2 pi) A_Z dpsi.
```

Deforming that loop through a region adds the corresponding curvature flux.  Thus the oriented
angle has the form

```text
Theta_n = n Theta_base + curvature_flux       (mod 2 pi).
```

Consequently `lambda=-1` can have a flat connection on each cylinder while retaining nontrivial
winding holonomy.  Flat does not mean globally trivial on `R x S1`.

Under an orientation-preserving screen change, a closed-loop holonomy angle is unchanged modulo
`2 pi`.  Under screen reflection it changes sign.  The full `O(2)`-representative-free datum is
therefore the conjugacy class, equivalently

```text
trace(Hol) = 2 cos(Theta),
```

not the signed angle.  This `SO(2)` normal holonomy must not be conflated with ambient Lorentz
holonomy.

## 6. A second, independent stratification

The normal metric is

```text
q_H = v^2 (sigma1^2 + sigma2^2).
```

The round two-form combination is invariant under Hopf-fiber rotation, so

```text
L_Z q_H = 2 lambda Z(phi) q_H.
```

Thus `q_H` descends unchanged to the Hopf base for arbitrary stationary `phi` when `lambda=0`.
For another lambda it descends only on the fiber-basic stratum `Z(phi)=0`.

This is not the same condition as flat normal connection:

- `lambda=-1` makes `F_perp=0` for every stationary profile;
- `lambda=0` makes the normal metric Hopf-basic for every stationary profile.

The complete metric therefore exposes two clean but different geometric roles.  It does not yet
say that either one is the physical branch, nor that the roles must be carried by the same branch.

## 7. Cross-leaf comparison

On each spatial `S3`, `H=span(X,Y)` is the standard horizontal complement to the Hopf-fiber
direction `Z`.  Once a base path and a starting point are supplied, it gives a horizontal lift.
But the metric data tested here do not choose a unique path between two base points, especially at
global or cut-locus ambiguities.  Hence the audit derives a leafwise connection and
representative-free holonomy data, but not a unique cross-leaf comparison or physical complete
observer arrow.

## 8. Exact landing

```text
CONDITIONAL_METRIC_OWNED_NORMAL_CONNECTION_AND_REPRESENTATIVE_FREE_HOLONOMY_DATA_ON_SUPPLIED_R17_PAIR_LEAVES__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN
```

The result is conditional on the supplied regular stationary R17/W01 coframe family.  It selects
no leaf, path, winding, lambda, profile, action, source, matter law, bootstrap parameter, `X_max`,
CMB observable, signalling law, or dynamics.
