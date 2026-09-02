# G323 exact derivation — local refoliation and global compact quotient

Date: 2026-09-01
Grade: `INTERNALLY_VERIFIED_PENDING_FRESH_EXTERNAL_REVIEW`

## Bounded landing

```text
REGISTERED_G320_PROFILES_EMBED_AS_CAUCHY_GRAPHS_IN_ONE_LOCAL_RICCI_FLAT_TAUB_FORM
__INTEGER_MODES_HAVE_STRICTLY_DISTINCT_COMPACT_LATTICE_MODULI_AND_THUS_DISTINCT_UNMARKED_QUOTIENTS
__OPPOSITE_K_SIGNS_ARE_ONE_TIME_UNORIENTED_METRIC_WITH_OPPOSITE_TIME_ORIENTATIONS
__NO_OCCUPANCY_SELECTION
```

This is restricted to the G320/G321 `d=Lambda=0`, `J0>0`, one-coordinate, locally rotationally
symmetric compact data. It neither selects an occupied spacetime nor classifies the full UDT
solution space.

## 1. Frozen G320 data

For a smooth positive periodic profile `psi`, G319/G320 give

\[
\gamma=\psi^4(dx^2+dy^2+dz^2),
\]

\[
B=\epsilon\psi^{-3}\sqrt{36(\psi')^2+J_0},\qquad
F=12\psi''\psi^{-5},\qquad A=F/B,
\]

and

\[
K^x{}_x=\frac{3A-B}{6},\qquad
K^y{}_y=K^z{}_z=\frac B3.
\tag{1}
\]

G320 proved that different integer modes are not related by a spatial diffeomorphism of this
chosen slice. G321 and G322 deliberately left open whether the slices belong to the same unmarked
spacetime.

## 2. The common local spacetime

Set

\[
\mu=J_0/9,\qquad R=\psi^2.
\]

Consider

\[
\boxed{
g_\mu=-\frac R\mu dR^2+\frac\mu R dX^2+R^2(dy^2+dz^2)
},\qquad R>0.
\tag{2}
\]

The nonzero Christoffel symbols, up to lower-index symmetry, are

\[
\Gamma^R{}_{RR}=\frac1{2R},\qquad
\Gamma^R{}_{XX}=-\frac{\mu^2}{2R^3},\qquad
\Gamma^R{}_{yy}=\Gamma^R{}_{zz}=\mu,
\]

\[
\Gamma^X{}_{RX}=-\frac1{2R},\qquad
\Gamma^y{}_{Ry}=\Gamma^z{}_{Rz}=\frac1R.
\tag{3}
\]

Direct substitution gives

\[
R_{ab}=0,
\qquad
R_{abcd}R^{abcd}=\frac{12\mu^2}{R^6}.
\tag{4}
\]

Production reconstructs (3)--(4) by exact rational index loops at three unrelated rational
points; it does not call the metric Ricci-flat by analogy. The independent route reconstructs (3)
from the metric and differentiates the nonzero entries separately.

## 3. Exact embedding of the complete data

Define

\[
X'=-\frac{3B\psi^6}{J_0}.
\tag{5}
\]

Since `J0>0`, `B` and `X'` never vanish on a fixed-sign branch. With

\[
R'=2\psi\psi',
\]

the induced longitudinal metric is

\[
-\frac R\mu(R')^2+\frac\mu R(X')^2
=-\frac{36\psi^4(\psi')^2}{J_0}
+\frac{\psi^4[36(\psi')^2+J_0]}{J_0}
=\psi^4.
\tag{6}
\]

The other two induced components are immediately `R^2=psi^4`, so the pullback of (2) is exactly
the complete G320 intrinsic metric.

A unit normal along the graph is

\[
n=\frac{\mu X'}{R^2}\partial_R+\frac{R'}\mu\partial_X.
\tag{7}
\]

It obeys `g(n,n)=-1` and is orthogonal to the graph. Using the G321 convention
`K=-1/2 L_n gamma`, equations (3), (5), and the G319 identity

\[
B'=3\frac{\psi'}\psi(A-B)
\]

give

\[
K^y{}_y=K^z{}_z=-\frac{\mu X'}{R^3}=\frac B3,
\]

\[
K^x{}_x=\frac{3A-B}{6}.
\tag{8}
\]

Thus both the first and second fundamental forms agree. The arbitrary positive profile is a Cauchy-
graph shape inside (2), not a change of the local four-geometry.

Because `R` has timelike gradient and the quotient spatial directions are compact, every constant-
`R` torus is Cauchy. Since `X'` is nonzero, the embedded slice is a smooth spacelike graph over the
compact `X` circle and is Cauchy as well.

## 4. The forced global quotient period

Injectivity fixes the primitive `X` period to the total graph advance

\[
\boxed{
L_X[\psi]
=\frac3{J_0}\int_0^{2\pi}
\psi^3\sqrt{36(\psi')^2+J_0}\,dx
}.
\tag{9}
\]

Using a divisor of (9) repeats the same profile phase at the same `X` point and destroys the
embedding. Thus (9) is global data, not an arbitrary coordinate-period choice after the complete
datum is fixed.

The exact local isometry

\[
R_*=aR,\quad X_*=X/a,\quad y_*=y/a,\quad z_*=z/a,
\quad\mu_*=a^3\mu
\tag{10}
\]

rescales all three compact coordinate periods by `1/a`. It cannot change

\[
\boxed{\mathcal Q_X=L_X/\sqrt{L_yL_z}}.
\tag{11}
\]

This is intrinsic to the compact spacetime quotient. To see why an isometry cannot mix away the
`X` direction, use the curvature-defined constant-`R` leaves. Their shape operator has one
eigenvalue proportional to `-1/2` along `X` and a repeated eigenvalue proportional to `+1` in the
`y,z` plane. Hence the one-dimensional lattice and the two-dimensional lattice covolume in (11)
are invariantly separated. Changes of basis inside the `y,z` lattice preserve its covolume.

For `psi_n=p+a_0 cos(nx)`, periodic substitution gives

\[
L_X(n)=\frac3{J_0}\int_0^{2\pi}(p+a_0\cos u)^3
\sqrt{J_0+36a_0^2n^2\sin^2u}\,du.
\tag{12}
\]

The integrand is pointwise nondecreasing in positive integer `n` and strictly increases wherever
`sin(u)` is nonzero. Therefore

\[
\boxed{L_X(n+1)>L_X(n)}.
\tag{13}
\]

For the registered controls, production obtains

```text
n=1  L_X=6.554516685020806
n=2  L_X=6.623226427457768
n=3  L_X=6.735440496746481
n=4  L_X=6.888083020830009
```

The `n=1` and `n=2` data therefore have the same local metric form but inequivalent compact
unmarked quotients. This is the whole-spacetime meaning hidden behind G320's slice values
`1,4,9,16`.

## 5. Maximal-development boundary

The curvature invariant (4) diverges at `R=0`, excluding a smooth curvature extension there. The
three translation momenta give causal radial motion

\[
\dot R^2=p_X^2+\frac{\mu(p_y^2+p_z^2)}{R^3}
-\kappa\frac\mu R,
\tag{14}
\]

where `kappa=-1` for timelike and `0` for null curves. Equation (14) has infinite affine/proper
reach as `R->infinity`; no causal endpoint is hidden there. Together with the Cauchy foliation,
this supplies the explicit maximal-GH interface for the registered quotient. Identification with
the per-datum MGHD retains G322's imported-theorem ownership and does not claim arbitrary
Lorentzian inextendibility.

## 6. Opposite `K` signs

Changing `epsilon` reverses `B`, `A`, and every component of `K`. It also sends `X'` to `-X'` while
leaving `L_X` unchanged. Reflection `X->-X` identifies the two embedded graphs in the same
underlying quotient metric, with the unit normal reversed. Therefore:

- after forgetting time orientation, the two signs are the same unmarked metric spacetime;
- retaining time orientation, they are the two opposite orientations of that spacetime.

Moreover, (4) has a nonzero timelike gradient throughout `R>0`. As the gradient of a scalar, it is
preserved—not negated—by every isometry. It gives a canonical oriented timelike line, so there is
no time-orientation-preserving isometry between the two opposite choices. They are distinct only
in the time-oriented category.

## 7. Exact status

- `DERIVED_CONDITIONAL_IN_REGISTERED_FAMILY`: explicit local Ricci-flat form and complete Cauchy
  embedding.
- `DERIVED_CONDITIONAL_IN_REGISTERED_FAMILY`: strictly mode-dependent compact quotient modulus.
- `DERIVED_CONDITIONAL_IN_REGISTERED_FAMILY`: opposite-`K` time-orientation classification.
- `IMPORTED_MATHEMATICAL_METHOD_RETAINED`: G322 maximal-development uniqueness interface.
- `OPEN_NOT_SELECTED`: physical topology, quotient, orientation, data, scale, and occupancy.

The field equation remains owner-adopted provisional and the metric/kernel/angular sector are
unchanged.

