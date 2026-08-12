# G76 exact derivation — complete-family whole-sky relation atlas

## Scope

This calculation evaluates the frozen G75 stationary axial profile family under one supplied G74
observer query. It maps the full initial direction sphere at `|X|=1/4` to the first outward crossing
of `|X|=1`. It does not select a physical profile, a last-scattering surface, a source, `R`,
`X_max`, or a CMB observable.

## Cartesian metric

Put `s=X.X`, `rho2=X^2+Y^2`, `A=1+a s`, and

```text
q(s)=c0+c1 s+c2 s^2,
w=q(-Y,X,0).
```

The stationary axial metric used in G75 becomes

```text
g_00=-A,
g_0i=w_i,
g_ij=delta_ij-(a/A)X_i X_j.
```

The symbolic verifier reconstructs the inverse and gives, with

```text
Lz=X pY-Y pX,
B=A+q^2 rho2,
E=p_t-q Lz,
```

the exact null Hamiltonian

```text
H=1/2[p.p+a(X.p)^2-E^2/B].
```

Because `q` varies with `s`, the live gradient is

```text
dq=2 q_s X,
dB=2aX+2q rho2 dq+2q^2(X,Y,0),
dLz=(pY,-pX,0).
```

Hamilton's equations are therefore

```text
dt/dlambda=-E/B,
dX/dlambda=p+a(X.p)X+(E/B)q(-Y,X,0),
dp/dlambda=-a(X.p)p-(E/B)(Lz dq+q dLz)-(E^2/(2B^2))dB.
```

`derive_equations.py` verifies the inverse, Hamiltonian, all variable-`q` gradient terms, the time
equation, 24 exact control evaluations, and the constant-profile limit. All six gates pass.

## Observer query and initial null directions

The observer is fixed at `(1/4,0,0)`. Every unit vector `n` on the registered icosphere is converted
to a future null tangent in the metric-orthonormal observer frame. At the observer, writing
`B=A+q^2/16`, the nonzero components are

```text
k^t=A^(-1/2)+n_3 q(1/4)(A B)^(-1/2),
k^X=n_1 A^(1/2),
k^Y=n_3(A/B)^(1/2),
k^Z=-n_2.
```

The path is integrated without freezing `q_s`. The endpoint is the first outward crossing of the
comparison sphere, found by within-step interpolation and normalized back to the unit sphere.
Turning, missing, nonfinite, negative-orientation, and small-area outcomes remain recorded rather
than filtered.

## Whole-sky diagnostics

For each triangular input face, the oriented spherical solid angle is compared with the oriented
solid angle of its image. Their sum divided by `4*pi` estimates the topological degree. Intrinsic
tangent coordinates at each face center give a `2x2` face map. Its singular values measure angular
stretch and its determinant records local orientation. This is an endpoint tangent-map diagnostic;
it is not G72 path-carried screen rotation or polarization transport.

## Independent formulation

`verify_complete_family_independent.py` does not import the production Hamiltonian RHS. It starts
from the Cartesian metric above, differentiates `g` directly, constructs

```text
Gamma^m_ab=1/2 g^mk(partial_a g_kb+partial_b g_ka-partial_k g_ab),
```

and integrates

```text
dx^m/dlambda=k^m,
dk^m/dlambda=-Gamma^m_ab k^a k^b
```

at 2,048 RK4 steps for 162 directions on one profile from each of the eight exact G75 strata. The
panel contains both lapse extremes and both amplitude extremes. Seven production-resolved rows
replay within `1e-5`; the deliberately included production-unresolved row replays within the
original frozen `5e-5` numerical threshold and remains unresolved. The maximum direct-metric null
residual is `5.425556358351624e-10`.

## Exact bounded result

- frozen profiles: `591/591`;
- frozen shape rays: `49/49`;
- mesh trials: `2,364`;
- level-4 directions per profile: `2,562`;
- `SAMPLED_COMPLETE_ORIENTATION_PRESERVING`: `587`;
- `NUMERICALLY_UNRESOLVED`: `4`;
- sampled missing/nonfinite directions: `0`;
- sampled negative signed-area faces: `0`;
- sampled negative intrinsic face maps: `0`;
- sampled area ratios below `1e-2`: `0`;
- degree range: `0.9999999999999999` to `1.0000000000000002`;
- signed area-ratio range: `0.48488311917529653` to `2.8720295134891574`;
- singular-value range: `0.596894470340065` to `1.8877867031540811`;
- maximum face shear ratio: `1.5944554891818246`;
- maximum Hamiltonian backward error: `3.3559291523488355e-7`;
- maximum G74 replay chord over nine rows: `3.3306690738754696e-16`;
- maximum reflected-partner chord: `0` at the registered coarse audit.

The four unresolved identities are

```text
G75_AM_S03_E100
G75_A0_S03_E100
G75_AP_S03_E100
G75_AM_S24_E100
```

Every non-time-refinement gate passes for all four. Their only failing production gate is the frozen
level-4 `512`-versus-`1024` endpoint chord threshold `5e-5`; the maximum is
`7.99498667241396e-5`. They are not geometric negatives and are not promoted.

## Maximum conclusion

The complete frozen G75 family is sampled as a coherent degree-one, orientation-preserving
whole-sky endpoint relation under this one stationary supplied query, except for four rows retained
as numerical-resolution exceptions. This does not establish continuum global injectivity between
sample points, physical profile selection, a CMB source or endpoint, polarization, scale, or generic
complete-metric behavior.
