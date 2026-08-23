# G225 exact derivation — shared-event normal-screen carry

Date: 2026-08-22

## Primary bounded landing

```text
METRIC_AND_SHARED_CLOCK_DEFINE_POSITIVE_INCIDENT_SCREEN_PLANES
__CANONICAL_LEAST_TURNING_DIRECT_SCREEN_ISOMETRY_EXISTS_OFF_ANTIPODES
__THREE_DIRECTION_COMPOSITION_RETAINS_FINITE_O2_HOLONOMY_AND_NO_GLOBAL_ENDPOINT_ONLY_FLAT_SCREEN_CARRY_EXISTS
__G188_JACOBI_TRANSPORT_REMAINS_SEPARATE
```

Status: `DERIVED_CONDITIONAL__INTERNALLY_VERIFIED__FRESH_EXTERNAL_REVIEW_PENDING`.

The metric, observer germ, marked shared event, and incident future-null directions are supplied.
The result classifies their local screen geometry; it does not select those data physically.

## 1. From the observer clock to the incident screen

Let `(V,g)` be the Lorentz tangent space at the shared event, with signature `(-+++)`, and let `U`
be the metric-unit future observer clock. For a nonzero future-null vector `k`, define

\[
\omega=-g(U,k)>0,
\qquad
N=\frac{k}{\omega},
\qquad
n=N-U.
\]

Then

\[
g(U,n)=0,
\qquad
g(n,n)=1,
\qquad
N=U+n.
\]

Thus `n` is one point of the observer's unit celestial sphere in the positive Euclidean rest space

\[
H=U^\perp.
\]

The observer screen is

\[
\boxed{E_n=\{x\in H:g(x,n)=0\}.}
\]

It is a positive two-plane. It is canonically isometric to the G188 quotient screen
`k^perp/<k>`. For `X in k^perp`, the unique representative orthogonal to `U` is

\[
j_U[X]=X+\frac{g(U,X)}{\omega}k.
\]

This representative lies in `E_n`; adding a multiple of `k` to `X` does not change it, and the
quotient inner product is preserved. G222's normal screen and this observer-rest screen are
therefore two metric sections of the same positive quotient object on the supplied incidence.

## 2. Canonical least-turning comparison off antipodes

Let `n,m` be two incident unit sight directions in `H`, and put

\[
c=g(n,m).
\]

For `c>-1`, define the skew endomorphism

\[
A=m\otimes n^\flat-n\otimes m^\flat
\]

and

\[
\boxed{
R_{m\leftarrow n}
=I+A+\frac{A^2}{1+c}.}
\]

Direct algebra gives

\[
R_{m\leftarrow n}n=m,
\qquad
R_{m\leftarrow n}^TR_{m\leftarrow n}=I,
\qquad
\det R_{m\leftarrow n}=1.
\]

Every vector orthogonal to both `n` and `m` is fixed pointwise. Hence `R` is the unique proper
orthogonal transformation that sends `n` to `m` and fixes their common perpendicular subspace.
It is continuous from the identity and is covariant under every passive `O(H)` transformation:

\[
R_{Qm\leftarrow Qn}=Q R_{m\leftarrow n}Q^{-1}.
\]

Its restriction

\[
\boxed{C_{m\leftarrow n}=R_{m\leftarrow n}|_{E_n}:E_n\to E_m}
\]

is therefore a metric-natural direct screen isometry on the non-antipodal stratum. In passive
screen bases its matrix transforms as

\[
C\longmapsto Q_m^T C Q_n,
\qquad Q_n,Q_m\in O(2).
\]

This is also celestial-sphere Levi-Civita transport along the unique short great-circle arc from
`n` to `m`. It is a local geometric evaluator; no physical spacetime relation has been selected by
writing it down.

## 3. Orthogonal projection is not the answer

The raw orthogonal projection from `E_n` to `E_m` is canonical but generally not an isometry. In
adapted screen bases its matrix is

\[
\operatorname{diag}(c,1).
\]

Its determinant is `c`, its Gram matrix is `diag(c^2,1)`, and it becomes singular when the sight
directions are orthogonal. The least-turning map remains a regular isometry there. This separates
screen identification from projected image-area response.

## 4. Exact composition defect

For three pairwise non-antipodal directions `n_0,n_1,n_2`, direct and sequential comparisons are

\[
C_{2\leftarrow0},
\qquad
C_{2\leftarrow1}C_{1\leftarrow0}.
\]

Their defect on the starting screen is

\[
\boxed{
H_{210}
=C_{2\leftarrow0}^{-1}C_{2\leftarrow1}C_{1\leftarrow0}
\in O(E_{n_0}).}
\]

The ambient representative is a proper orthogonal map fixing `n_0`, so its screen restriction is a
proper two-dimensional rotation after an orientation is chosen. It need not be the identity.

An exact rational witness is

\[
n_0=(1,0,0),\quad n_1=(0,1,0),\quad n_2=(0,0,1).
\]

For this octant triangle,

\[
H_{210}=
\begin{pmatrix}
1&0&0\\
0&0&-1\\
0&1&0
\end{pmatrix}.
\]

It fixes `n_0` and rotates its screen by a right angle. By contrast, three directions ordered along
one short great-circle arc compose exactly. In oriented language the general defect angle is the
spherical area enclosed by the direction-space triangle; without a supplied orientation the
invariant object is the `O(2)` conjugacy class.

Therefore the direct least-turning comparisons do not define a thin endpoint pair-groupoid. A
sequence of supplied directions carries genuine angular route memory.

## 5. Global flat endpoint carry is impossible

The screen bundle over the observer celestial sphere is canonically the tangent bundle `TS^2`.
Suppose a continuous family of screen isometries

\[
G_{m\leftarrow n}:E_n\to E_m
\]

were defined for every ordered pair and satisfied identity and exact cocycle laws. Choose one base
direction `n_0` and an orthonormal basis of `E_{n_0}`. Transporting that basis by
`G_{n\leftarrow n_0}` would produce a continuous global orthonormal frame of `TS^2`. The hairy-ball
theorem forbids even one nowhere-zero global tangent vector field, hence forbids this frame.

Thus no continuous global endpoint-only flat screen carry exists. Local trivializations can exist
on restricted direction patches, but their transition rotations are additional carried data, not
a scalar consequence of G224.

## 6. Antipodal precision

When `m=-n`, the screen subspaces coincide as subsets of `H`, so an abstract identity map between
them exists. What fails is a unique continuous least-turning proper ambient rotation extending the
non-antipodal rule. For `n=(1,0,0)`, both

\[
\operatorname{diag}(-1,-1,1),
\qquad
\operatorname{diag}(-1,1,-1)
\]

are proper orthogonal maps sending `n` to `-n`, but they act differently on the common screen.
Approaching the antipode along different great circles produces these different limits. The
antipodal stratum therefore needs a path/axis choice if the least-turning rule is to continue.

## 7. Separation from G224 and G188

G224's line-amplitude switch still composes exactly:

\[
q_{AC}=q_{BC}q_{AB}=(r_{BC}r_{AB})^{-1}.
\]

The screen rotation `H` is an independent matrix channel and does not alter that scalar product.

G188's finite Jacobi map remains separate. It integrates the ambient curvature along each supplied
null ray and can focus, shear, rotate, and become singular at a caustic. The pointwise map `C` above
is an isometry at one shared event and cannot replace that finite propagator. An actual chain uses
the supplied along-edge G188 propagators and the local vertex comparisons in their proper order.

## 8. Landing and ceiling

G225 selects preregistered alternative

```text
B_LOCAL_DIRECT_ISOMETRY_WITH_NONTRIVIAL_COMPOSITION_HOLONOMY
```

in the declared local screen arena. It derives neither a universal null protocol nor a physical
screen transport between arbitrary events. It does not constrain an independently supplied direct
relation, populate observers or branches, select a metric history, or derive `X_max`, transfer,
observations, action, source, matter, bootstrap, mass, or signalling.
