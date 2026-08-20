# G188 exact derivation — complete-coframe null-screen/Jacobi extension

Date: 2026-08-20

## 1. Supplied metric and null query

Let a smooth Lorentzian four-metric be represented on one regular neighborhood by an invertible
complete coframe

\[
g=E^T\eta_4E.
\]

Supply one future affinely parametrized null geodesic \(\gamma\), with tangent \(k\), one unit
source observer \(u_o\) normalized by \(-g(u_o,k_o)=1\), and one orientation of the source screen.
The metric history and query are supplied. Nothing below selects their physical population.

G179 used the pointwise pullback \(h=J^TgJ\). Finite propagation needs the next metric layers:

\[
g,\qquad \partial g,\qquad \partial^2g,
\]

equivalently \(E,\partial E,\partial^2E\) in a chosen coframe presentation. This is how the complete
orchestra enters propagation: through the metric connection and curvature before any readout, not
through an appended angular score.

## 2. The quotient screen is metric-derived

Along \(\gamma\), define

\[
\mathcal S_\lambda=k_\lambda^\perp/\langle k_\lambda\rangle.
\]

If \(X,Y\in k^\perp\), set

\[
\langle[X],[Y]\rangle_{\mathcal S}=g(X,Y).
\]

This is independent of representatives because replacing \(X\) by \(X+ak\) changes no inner
product with a vector in \(k^\perp\). In Lorentzian signature \((-+++ )\), the quotient has rank
two and is positive definite. At the source it is exactly the orthogonal screen of the Lorentzian
plane \(\operatorname{span}(u_o,k_o)=\operatorname{span}(u_o,k_o-u_o)\), hence the G186 projector
supplies its initial realization.

## 3. The metric carries the screen

Define

\[
\mathscr D_k[X]=[\nabla_kX].
\]

For \(X\in k^\perp\), affine geodesicity gives

\[
g(\nabla_kX,k)=\frac{d}{d\lambda}g(X,k)-g(X,\nabla_kk)=0.
\]

If \(X\mapsto X+ak\), then

\[
\nabla_k(X+ak)=\nabla_kX+\dot a\,k,
\]

so the quotient class is unchanged. Metricity of \(\nabla\) makes \(\mathscr D\) a metric
connection on \(\mathcal S\). No independent screen connection or transport coefficient survives.

## 4. Curvature fixes the full tidal operator

Define

\[
\mathcal T([X])=[R(X,k)k].
\]

It is well-defined because \(R(k,k)=0\), and \(R(X,k)k\in k^\perp\). Curvature symmetries give

\[
\langle[Y],\mathcal T[X]\rangle_{\mathcal S}
=\langle[X],\mathcal T[Y]\rangle_{\mathcal S},
\]

so \(\mathcal T\) is self-adjoint. In a parallel orthonormal screen basis \(s_A\),

\[
\mathcal T_{AB}=g(s_A,R(s_B,k)k)=\mathcal T_{BA}.
\]

The complete coframe enters through

\[
g_{\mu\nu}=\eta_{ab}E^a{}_\mu E^b{}_\nu,
\]

the Levi-Civita symbols built from \(\partial g\), and the Riemann tensor built from
\(\partial^2g\) and quadratic connection terms. A particular query may lie in the kernel of a
particular channel, but no \(B,Q,S\), shift, or time-live metric jet is deleted from the evaluator.

Local Lorentz coframe changes leave \(g\), \(\nabla\), \(R\), and \(\mathcal T\) unchanged.

## 5. The finite Jacobi map

For a regular branch with continuous \(\mathcal T(\lambda)\), the matrix initial-value problem

\[
\boxed{
\mathcal D''+\mathcal T\mathcal D=0,
\qquad
\mathcal D(0)=0,
\qquad
\mathcal D'(0)=I
}
\]

has one unique solution. This is the finite vertex-normalized screen map. Under independently
chosen passive endpoint screen bases,

\[
\boxed{\mathcal D\mapsto Q_s^T\mathcal DQ_o,\qquad Q_o,Q_s\in O(2).}
\]

Thus the singular values and \(|\det\mathcal D|\) are invariant readouts. A zero determinant is a
caustic of the position block; the carried phase \((\mathcal D,\mathcal D')\) remains the lawful
object, and no inverse is asserted there.

In a generic complete metric, \(\mathcal T\) need not remain diagonal in any one parallel basis.
The full matrix equation, not two independently fitted scalar modes, is the native evaluator.

## 6. G187 is the reflection-diagonal specialization

In the primary static-spherical metric, reflection through the orbital plane makes the propagated
in-plane and out-of-plane screen directions invariant subspaces. Therefore

\[
\mathcal T_{\perp\parallel}=0
\]

and G187's two diagonal equations follow. Spherical symmetry was used to diagonalize the general
screen operator; it was not used to create the screen connection or Jacobi law.

## 7. Exact genuine-mixing witness

Use coordinates \((u,v,x,y)\) and the orthonormal complete coframe

\[
\theta^0=dv+\tfrac12du,
\qquad
\theta^1=dv-\tfrac12du,
\]

\[
\theta^2=dx+(x+y)du,
\qquad
\theta^3=dy+(x+y)du.
\]

This has a live lower base-to-screen mixing block

\[
S=\begin{pmatrix}x+y&0\\x+y&0\end{pmatrix}
\]

and gives

\[
g=-2du\,dv+dx^2+dy^2
+2(x+y)du(dx+dy)+2(x+y)^2du^2,
\qquad \det g=-1.
\]

On the central branch \(x=y=0\), take

\[
k=\partial_u,
\qquad
u_o=\tfrac12\partial_u+\partial_v,
\qquad
s_1=\partial_x,
\qquad
s_2=\partial_y.
\]

Then \(k\) is affine and null, \(u_o\) is unit with \(-g(u_o,k)=1\), and \(s_1,s_2\) are parallel
orthonormal screen vectors. Full Christoffel/Riemann reconstruction gives

\[
\boxed{
\mathcal T=
\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}.}
\]

The off-diagonal entry is nonzero and fixed. With unit vertex data,

\[
\boxed{
\mathcal D(\lambda)=
\begin{pmatrix}
\lambda/2+\sinh(2\lambda)/4&-\lambda/2+\sinh(2\lambda)/4\\
-\lambda/2+\sinh(2\lambda)/4&\lambda/2+\sinh(2\lambda)/4
\end{pmatrix}.}
\]

Hence

\[
\mathcal D_{12}=\frac{\sinh(2\lambda)}4-\frac\lambda2
=\frac{\lambda^3}{3}+O(\lambda^5)
\]

is a finite cross-screen response produced entirely by the coframe mixing. Deleting \(S\) makes
the witness flat, \(\mathcal T=0\), and \(\mathcal D=\lambda I\).

The witness is a chosen exact mathematical control, not a proposed physical spacetime.

The separate exact-Fraction verifier independently reconstructs metric jets, connection, and
curvature for the symmetric family `theta^A=dz^A+(Mz)^A du`. It certifies this genuine-mixing
witness family; it is not an independent generic arbitrary-coframe parser. The generality of the
abstract theorem comes from Sections 2--5, not from extrapolating the witness census.

## 8. Bounded landing

```text
GENERAL_COMPLETE_COFRAME_NULL_JACOBI_FUNCTOR_DERIVED_CONDITIONALLY
__G187_IS_THE_REFLECTION_DIAGONAL_SPECIALIZATION
__GENUINE_COFRAME_MIXING_GENERATES_OFFDIAGONAL_FINITE_RESPONSE
```

The complete metric therefore owns the finite screen evaluator once a smooth regular affine null
query is supplied. G188 does not select the complete metric or ray population and does not derive
emission, frequency transfer, flux, luminosity, an observed sky pattern, `R(Z)`, global completion,
or `X_max`.
