# G196 exact derivation — longitudinal screen-mixing descent

Date: 2026-08-20

## Declared family

Let `X=(p,w)^T` and

\[
M(\eta,z)=S+\Omega,
\quad
S=\begin{pmatrix}A&N\\N&B\end{pmatrix},
\quad
\Omega=R\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

The preregistered coframe is

\[
\theta^0=a(\eta)d\eta,
\qquad
\theta^1=a(\eta)dz,
\qquad
\theta_{\rm screen}
=a(\eta)\left[dX+M(\eta,z)X(d\eta+dz)\right],
\]

with arbitrary positive `C3` `a` and arbitrary real `C2` entries of `M`. The chosen pair is
`p=w=0`, and the chosen outgoing germ is `eta=z=s`.

The coframe and metric determinants are

\[
\det E=a^4,
\qquad
\det g=-a^8,
\]

so the displayed family remains regular wherever `a>0`.

## Pair and ray typing

On the central pair,

\[
h=-a^2d\eta^2+a^2dz^2.
\]

The outgoing affinely parametrized null tangent, unit clock, and screen are

\[
k=a^{-2}(\partial_\eta+\partial_z),
\qquad
u=a^{-1}\partial_\eta,
\qquad
e_A=a^{-1}\partial_A.
\]

Direct Christoffel reconstruction gives

\[
\nabla_k k=0,
\qquad
-g(u,k)=a^{-1}.
\]

Thus activating longitudinal dependence in `M` does not change the central pair metric, affine ray,
or frequency law in this family.

## The derivative selected by the pair

Define

\[
D_+=\partial_\eta+\partial_z.
\]

The screen connection along affine parameter `lambda` is

\[
C_\lambda=\frac{2\Omega}{a^2}.
\]

Since `d/dlambda=a^{-2}d/ds` on `eta=z=s`, the same connection in the coordinate `s` is

\[
C_s=2\Omega.
\]

The direct Riemann contraction in the coordinate screen gives

\[
T_c=\tau_0I+rac{1}{a^4}
\left(2D_+S-4S^2-4[S,\Omega]\right),
\]

where

\[
H=\frac{a'}a,
\qquad
\tau_0=\frac{H^2-H'}{a^4}.
\]

No separately weighted `partial_z`, `partial_eta-partial_z`, mixed second derivative, `D_+Omega`,
or `Omega^2` term survives in this self-adjoint curvature tide. Pure rotation remains connection
carry rather than an independent area-focusing tide.

This does **not** make off-ray structure globally absent. It says that this selected germ restricts
the field to its own ray and differentiates it along that ray.

## Exact ordered factorization

For coordinate screen amplitude `Y`, direct expansion gives

\[
(D_+-2M^T)(D_++2M)Y=0.
\]

Equivalently,

\[
D_+^2Y+2(M-M^T)D_+Y
+\left(2D_+M-4M^TM\right)Y=0.
\]

Restrict to any outgoing ray with constant `eta-z`, write `M_bar(s)` for the restricted matrix, and
solve

\[
L'=-2\bar M L,
\qquad
L(0)=I.
\]

Then the vertex-normalized coordinate Jacobi map is

\[
Y=LK,
\qquad
K(s)=\int_0^s L^{-1}(q)L^{-T}(q)\,dq,
\]

and the physical screen map is

\[
D=aLK.
\]

The order `L^{-1}L^{-T}` is load-bearing; no commuting exponential was assumed.

## Scoped caustic theorem

For every nonzero vector `v`,

\[
v^TL^{-1}L^{-T}v=\lVert L^{-T}v\rVert^2>0.
\]

Hence `K(s)` is positive definite for `s>0` and negative definite for `s<0`. In two screen
dimensions, both cases have positive determinant. Also

\[
\det L(s)=\exp\left[-2\int_0^s\operatorname{tr}\bar M(q)\,dq\right]>0.
\]

Therefore

\[
\det D=a^2\det L\det K>0
\]

at every nonvertex point of a connected regular outgoing-ray interval. This is an exact sign proof,
not an inference from the finite numerical census.

## Same-ray alias control

The independent replay compared two fields differing by

\[
\Delta A=0.7(\eta-z)^2.
\]

On `eta=z`, both `Delta A` and `D_+ Delta A` vanish, so that selected pair has identical response.
Off the ray, for example at `(eta,z)=(0.31,0.07)`, the fields differ by `0.04032`. This proves the
right bounded interpretation: one pair samples its own directional restriction; it does not
determine the full surrounding field.

## Maximum conclusion

The theorem holds for the displayed `a(eta), M(eta,z)` affine coframe family and supplied central
outgoing germ. It does not select the functions, cover transverse dependence or arbitrary complete
coframes, choose physical observers, prove global completion, derive transfer or observations, or
establish `X_max`.
