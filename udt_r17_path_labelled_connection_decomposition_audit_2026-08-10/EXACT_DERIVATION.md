# Exact derivation — complete R17 path-labelled normal connection

Date: 2026-08-10

Current status after fresh external review: `VERIFIED-WITH-CAVEATS`; the reviewer independently
reconstructed the load-bearing algebra and returned `VERIFIED_AS_STATED`.

## 1. Supplied geometry and types

On the preregistered regular stationary R17 family,

```text
theta0=u^-1(dt+a sigma3), theta1=u sigma3,
theta2=v sigma1,          theta3=v sigma2,
u=exp(phi), v=exp(lambda phi), T(phi)=0,
```

the orthonormal frame is

```text
e0=u T, e1=u^-1(Z-aT), e2=v^-1 X, e3=v^-1 Y.
```

The pair-leaf tangent bundle and its metric normal bundle are

```text
E=span(e0,e1)=span(T,Z),
H=span(e2,e3)=span(X,Y).
```

The previous result restricted the induced normal connection to directions in `E`. Here the
connection is defined for every vector field `W` by

```text
D_W s=P_H(nabla^LC_W s),  s in H.
```

This is a globally typed metric connection on `H`: projection preserves the Leibniz rule, and the
discarded `E` components are orthogonal to normal sections, so metricity follows from metricity of
the Levi--Civita connection. No GR observer mechanics, action, or physical path law is imported.

## 2. Compatible scalar jets

Use the Maurer--Cartan sign `epsilon=+1` or `-1`:

```text
[X,Y]=2 epsilon Z, [Y,Z]=2 epsilon X, [Z,X]=2 epsilon Y.
```

Set

```text
p1=Z(phi), p2=X(phi), p3=Y(phi),
q21=X(Z(phi)), q31=Y(Z(phi)),
q22=X(X(phi)), q33=Y(Y(phi)).
```

The production and independent derivations enforce, rather than ignore, the scalar commutators;
for example

```text
Z(X phi)-X(Z phi)=2 epsilon Y(phi),
Z(Y phi)-Y(Z phi)=-2 epsilon X(phi),
X(Y phi)-Y(X phi)=2 epsilon Z(phi).
```

## 3. Complete connection

For an oriented local normal frame `(e2,e3)`, let `A(W)=g(D_W e2,e3)`. Direct coframe inversion,
noncoordinate bracket reconstruction, and the Koszul formula give

```text
A(e0)= epsilon a/(u v^2),
A(e1)= epsilon(2/u-u/v^2),
A(e2)=-lambda p3/v,
A(e3)= lambda p2/v.
```

The first two entries reproduce the banked leafwise connection. The last two are the released
horizontal components; they vanish identically at `lambda=0` but not generically elsewhere.
Under an oriented normal-frame rotation `A` changes by an exact gauge term. Under reflection its
signed representative reverses. The connection, not one chosen one-form representative, is the
global object.

## 4. All six curvature planes

Because the oriented normal group is `SO(2)`, `F=dA`. Exact exterior differentiation in the
noncoordinate frame gives

```text
F01 = 2 epsilon a(1+lambda)p1/(u^2 v^2),
F02 = 2 epsilon a(1+lambda)p2/(u v^3),
F03 = 2 epsilon a(1+lambda)p3/(u v^3),

F12 = 2 epsilon(1-lambda)p2 u/v^3 - lambda q31/(u v),
F13 = 2 epsilon(1-lambda)p3 u/v^3 + lambda q21/(u v),

F23 = lambda(q22+q33)/v^2
      +2u^2/v^4-4/v^2-2a^2/(u^2 v^4).
```

This is the complete vertical/horizontal decomposition in the declared arena:

- `F01` is leafwise;
- `F02,F03,F12,F13` are mixed;
- `F23` is horizontal.

The `O(2)`-safe local summaries are the curvature tensor up to normal-frame conjugation and, for
the metric-owned `E/H` split, the three squares

```text
F01^2,
F02^2+F03^2+F12^2+F13^2,
F23^2.
```

## 5. Three distinct special roles

The six-stratum atlas yields three clean but inequivalent simplifications:

1. `lambda=-1`: `F01=F02=F03=0`, so `i_e0 F=0`; all clock-legged curvature vanishes. The
   ruler--screen and horizontal terms remain generically nonzero, so the complete connection is
   not flat.
2. `lambda=0`: `A(e2)=A(e3)=0` in the global left-invariant representative, and the normal metric
   is Hopf-basic. Mixed and horizontal curvature remain generically nonzero.
3. `lambda=1`: the first-gradient pieces of `F12,F13` vanish, leaving crossed Hessian terms there.

No supplied `lambda` makes all six components identically zero on arbitrary compatible stationary
jets. These observations classify the family; they select no branch.

## 6. The pair-leaf bundle and its two connection layers

The inherited completion is

```text
pi: R x S3 -> S2,
```

with fibers `R x S1`, exactly the pair leaves. The plane `H=span(X,Y)` is the Hopf Ehresmann
connection. In terms of `eta=sigma3`,

```text
H=ker(dt) intersect ker(eta),
Omega_H=d eta=-2 epsilon sigma1 wedge sigma2
       =-2 epsilon v^-2 theta2 wedge theta3.
```

Therefore a supplied base path and starting point have a unique horizontal lift. The nonzero
Ehresmann curvature records the failure of horizontal planes to integrate and makes lifted
endpoint phase path-dependent. It does not select a base path or a starting fiber phase.

The second layer is `D`, the metric connection on the normal plane itself. For every supplied
piecewise-smooth total-space path `gamma`, its parallel-transport ODE has a unique solution.
Consequently

```text
PT(identity)=identity,
PT(gamma2 concatenated with gamma1)=PT(gamma2) PT(gamma1),
PT(reverse gamma)=PT(gamma)^-1.
```

Thus the metric derives a path-groupoid functor after a path is supplied. Because `D` is metric,
this functor is isometric normal carry. It cannot by itself be the still-missing non-isometric
observer-pair comparison.

## 7. Chart compatibility and base descent

On Hopf-chart overlaps, local horizontal sections differ by the fiber transition function and
local normal frames differ by `O(2)` gauge. The local connection forms have the standard inhomogeneous
overlap term, while `F` transforms by conjugation. Open-path matrices transform at their endpoints;
closed-loop conjugacy classes and traces are representative-free. Hence the connection is global
even though one preferred global base section is unavailable.

A connection on the total normal bundle need not descend to an endpoint-only connection on `S2`.
A necessary curvature condition is horizontality with respect to the vertical pair directions
`T,Z`. The exact contractions are

```text
F(T,Z)=F01,
F(T,X)=2 epsilon a(1+lambda)p2/(u^2 v^2),
F(T,Y)=2 epsilon a(1+lambda)p3/(u^2 v^2),

F(Z,X)=-lambda q31
       +2 epsilon p2[(1-lambda)u^2+(1+lambda)a^2/u^2]/v^2,
F(Z,Y)= lambda q21
       +2 epsilon p3[(1-lambda)u^2+(1+lambda)a^2/u^2]/v^2.
```

For arbitrary compatible stationary jets, no supplied `lambda` makes all five contractions
identically zero. Therefore the complete `D` curvature is not the pullback of one base two-form in
the general family. `lambda=0` being Hopf-basic for the normal metric is not enough to make the
complete ambiently induced connection base-basic. Restricted jet subloci may satisfy the necessary
conditions, but sufficient global descent would also require compatible vertical holonomy; that
classification remains a separate sublocus question, not a branch selector.

## 8. Finite-cell/global completion

On the supplied smooth positive `R x S3` completion, `E`, `H`, the Hopf connection, and `D` are
global and nonsingular. Spatial compactness closes the declared cell without adding a boundary
functional. This does not prove compatibility with a different seal, quotient, null degeneration,
or time-live completion.

## 9. Local landing

```text
COMPLETE_METRIC_PROJECTED_H_CONNECTION_AND_PATH_FUNCTOR_DERIVED_ON_SUPPLIED_REGULAR_STATIONARY_R17__FULL_CURVATURE_GENERALLY_NONZERO__PATH_SELECTION_AND_PHYSICAL_ARROW_OPEN
```

This derives a complete path-labelled isometric carry layer in the supplied branch family. It
does not derive the path label, path independence, a non-isometric calibration magnitude, the
physical observer arrow, or any downstream dynamics or phenomenology.
