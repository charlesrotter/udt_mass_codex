# G228 exact derivation — neighboring-event curvature first variation

Date: 2026-08-23

## 1. Object type

Let `p` be one supplied event of a smooth four-dimensional Lorentz metric. The curvature value at
`p` is an algebraic Riemann tensor

\[
R_p\in\mathcal R(V),\qquad \dim\mathcal R(V)=20.
\]

Its covariant first derivative is the tensor

\[
D_{eabcd}=(\nabla_eR)_{abcd}.
\]

For each fixed derivative direction `e`, the last four indices retain the algebraic Riemann
symmetries. Before imposing differential Bianchi, `D` therefore belongs to

\[
V^*\otimes\mathcal R(V),
\]

an 80-dimensional vector space.

The Levi-Civita differential Bianchi identity is

\[
D_{e,ab,cd}+D_{a,be,cd}+D_{b,ea,cd}=0.
\]

It is a compatibility identity for a supplied smooth metric connection. It is not an equation of
motion and does not calculate the numerical value of `D`.

## 2. Exact module calculation

The production and independent implementations separately rebuilt the G227 20-component
algebraic-curvature basis, formed all 80 derivative components, and generated the 24 cyclic
component equations indexed by one derivative-index triple and one curvature bivector.

Exact row reduction gives

\[
\operatorname{rank}B_{\nabla R}=20,
\qquad
\dim\ker B_{\nabla R}=80-20=60.
\]

The production SymPy matrix and the separately written standard-library `Fraction` matrix have the
same canonical SHA-256 digest:

```text
c3d8c8625620751ec1497ce089aa31ae84750581af4518371daffeaece90906d
```

Their 80-by-60 kernel matrices also have the same digest:

```text
a6db92e6f5eced9f2fc6cb6ef5cb5a68152775d39c8e3e5f1509bb4586f6d5f6
```

## 3. Frozen null-tetrad subset census

Use

\[
k=e_0+e_3,\qquad
\ell=\tfrac12(e_0-e_3),\qquad
s_1=e_1,\qquad
s_2=e_2.
\]

Exactly,

\[
k^2=\ell^2=0,\qquad k\cdot\ell=-1,
\qquad s_A\cdot s_B=\delta_{AB},
\]

and the four vectors have determinant `-1`, so they span the tangent space.

For each nonempty frozen subset, restrict a compatible `D` to the linearly independent directional
derivatives in that subset.
The complete exact census is:

| Number of independent directions | Target components | Image rank | Codimension | Number of frozen subsets |
|---:|---:|---:|---:|---:|
| 1 | 20 | 20 | 0 | 4 |
| 2 | 40 | 40 | 0 | 6 |
| 3 | 60 | 54 | 6 | 4 |
| 4 | 80 | 60 | 20 | 1 |

Thus every supplied one-direction derivative and every supplied linearly independent two-direction
pair in the frozen census extends to at least one **algebraic differential-Bianchi-compatible** full
derivative-curvature tensor. Differential Bianchi first becomes a nonidentity restriction on the
frozen linearly independent three-direction tiles, where six exact syzygies survive. The full four-
direction star has twenty.

The result selects preregistered alternative

```text
B_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_THREE_DIRECTIONS
```

The banked statement is the complete frozen null-tetrad census. The calculation is consistent with
the natural general rank pattern under changes of spanning basis, but no broader minimality theorem
over every degenerate or repeated direction arrangement is needed here.

## 4. Why one ray does not choose a history

Let `q(epsilon)` lie on one supplied short geodesic from `p` with initial tangent `v`, and use
Levi-Civita parallel transport to return the neighboring tensor to `p`. Then

\[
\frac{P_{p\to q}^*R_q-R_p}{\epsilon}
\longrightarrow(\nabla_vR)_p.
\]

The one-direction projection has exact rank 20. Consequently, any algebraic-curvature-shaped
first change along that one line can be extended by suitable transverse derivatives. A single ray
therefore supplies a derivative value but does not, through differential Bianchi alone, restrict
which value it may take.

Every frozen linearly independent two-direction subset remains surjective. The first nonidentity
joint in the frozen census is a linearly independent three-direction neighborhood, not a longer
sample of one line. This is necessary algebraic first-jet compatibility; it is not a theorem that
the supplied tensor data are realized by a local metric 3-jet or by one smooth Levi-Civita metric.

## 5. Screen-covariant optical variation

Along one supplied affine null geodesic, let `k` and a parallel orthonormal quotient-screen frame
`S_A` obey

\[
\nabla_k k=0,
\qquad
\mathscr D_kS_A=0.
\]

For

\[
T_{AB}=R(S_A,k,S_B,k),
\]

with the G188 sign/index convention fixed so that the Jacobi generator has lower-left block `-T`.
Unlike G227's rank theorem, an overall curvature-sign change is load-bearing here.

the product rule gives exactly

\[
\frac{dT_{AB}}{d\lambda}
=(\nabla_kR)(S_A,k,S_B,k).
\]

There are no tangent or screen-derivative corrections in the parallel frame because affine and
parallel carry make them vanish.

Now use a moving orthonormal screen `E=S C`, with

\[
C^TC=I,
\qquad
\Omega=C^TC',
\qquad
\Omega^T=-\Omega.
\]

The moving-frame tide is

\[
T_E=C^TTC.
\]

Direct differentiation gives

\[
\boxed{
\mathcal D_\lambda T_E
=T_E'+[\Omega,T_E]
=C^TT'C.
}
\]

The commutator is therefore not another orchestra coefficient. It removes the apparent change
caused solely by rotating the measurement screen. A frozen rational noncommuting control gives a
nonzero omitted-commutator residual

\[
\begin{pmatrix}
14/5&-77/5\\
-77/5&-14/5
\end{pmatrix},
\]

while the covariant identity vanishes exactly.

## 6. Moving-screen Jacobi phase

In a parallel screen, the affine Jacobi first-order generator is

\[
A_S=
\begin{pmatrix}
0&I\\
-T&0
\end{pmatrix}.
\]

Let `y` be moving-screen position components and define the covariant velocity

\[
v=y'+\Omega y.
\]

The same physical phase obeys

\[
\boxed{
\frac d{d\lambda}
\begin{pmatrix}y\\v\end{pmatrix}
=
A_E
\begin{pmatrix}y\\v\end{pmatrix},
\qquad
A_E=
\begin{pmatrix}
-\Omega&I\\
-T_E&-\Omega
\end{pmatrix}.
}
\]

If `H=diag(C,C)`, then

\[
A_E=H^{-1}A_SH-H^{-1}H'.
\]

For symmetric `T_E` and skew `Omega`, exact algebra gives

\[
A_E^T\mathbb J+\mathbb J A_E=0.
\]

So the generator remains Hamiltonian, and its fundamental transfer remains symplectic. Deleting
either diagonal connection block, using the wrong commutator sign, using a nonsymmetric tide, or
using a nonskew connection is caught exactly.

## 7. Finite-phase boundary inside the Jacobi class

An isolated finite G226 matrix still cannot determine `D`. This can be shown without leaving the
G188 Jacobi class.

Begin with the scalar one-period equation

\[
u_{ff}+(2\pi)^2u=0.
\]

For the exact increasing reparameterization

\[
f(t)=t+\epsilon(1-\cos 2\pi t)^2,
\qquad \epsilon=\frac1{100},
\]

the Liouville transform `y=u(f)/sqrt(f')` obeys a Jacobi equation with tide

\[
T_\epsilon(t)=(2\pi)^2f'(t)^2+\frac12\{f,t\},
\]

where `{f,t}` is the Schwarzian derivative. The bound

\[
f'(t)\ge 1-8\pi\epsilon>0
\]

makes the reparameterization regular. At both endpoints,

\[
f(0)=0,\quad f(1)=1,\quad f'=1,\quad f''=0.
\]

Therefore both the constant tide `T_0=(2 pi)^2` and `T_epsilon` have exactly the identity full
phase over `[0,1]`, while

\[
T_0'(0)=0,
\qquad
T_\epsilon'(0)=48\epsilon\pi^4\ne0.
\]

Taking the same scalar tide in both screen directions supplies the 4-by-4 G188 witness. Thus the
finite full phase does not determine the initial curvature/tide derivative even within the actual
Jacobi family. G228 consumes a differentiable phase germ or supplied curvature first variation,
never one isolated endpoint matrix.

This section concerns the underlying affine G188 transfer. G226's endpoint clock normalization is
`M=R(omega_t)^(-1) F R(omega_s)`. G228 does not define a continuously clock-normalized generator;
if a clock normalization varied along the ray, its derivative would contribute an additional
`R^(-1)R'` basis term.

## 8. Ceiling

G228 derives exact necessary algebraic first-order compatibility and screen-gauge covariance for
supplied local data.
It rules out independently assigned three-direction curvature changes that violate the six
syzygies. It does not prove local metric 3-jet or smooth-metric realization and does not generate
the compatible values, select a global metric history, populate a null congruence, or supply dynamics,
action, source, matter, bootstrap, boundary, `X_max`, transfer, observation, mass, or signalling.
