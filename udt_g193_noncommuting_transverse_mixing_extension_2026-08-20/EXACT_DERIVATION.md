# G193 exact derivation — noncommuting transverse mixing

Date: 2026-08-20

## 1. Bounded landing

For the preregistered arbitrary positive `a(eta)` and real `mu(eta),nu(eta)` family, the added
transverse channel makes the screen history genuinely noncommuting when its relative strength
changes.  Nevertheless the full matrix Jacobi operator factorizes in its original parallel screen,
and the vertex-normalized screen has no nonvertex caustic on a connected regular interval.

This is a theorem for the displayed symmetric two-channel coframe family and supplied central pair.
It is not a theorem for arbitrary complete coframes, antisymmetric screen rotation, other pair
germs, or global completion.

## 2. Complete coframe, pair, and frequency

Let

\[
X=\binom{p}{w},\qquad
q=d\eta+dz,\qquad
M(\eta)=
\begin{pmatrix}
A(\eta)&\nu(\eta)\\
\nu(\eta)&0
\end{pmatrix},
\qquad A=\sqrt2\,\mu,
\]

and

\[
\theta^0=a\,d\eta,
\qquad
\theta^1=a\,dz,
\qquad
\binom{\theta^p}{\theta^w}=a[dX+MXq].
\]

Direct reconstruction gives

\[
\det E=a^4,
\qquad
\det g=-a^8.
\]

Thus the coframe is regular Lorentzian wherever `a>0`, independent of the values or rank of `M`.
On the supplied pair `p=w=0`,

\[
F^*g=a^2(-d\tau^2+d\sigma^2).
\]

The completed clock, ruler, selected normalized null germ, and affine tangent are

\[
U=a^{-1}\partial_\eta,
\qquad
N=a^{-1}\partial_z,
\qquad
\ell_+=U+N,
\qquad
k=a^{-2}(\partial_\eta+\partial_z).
\]

Full Christoffel reconstruction verifies `nabla_k k=0`.  Therefore

\[
\frac{d\lambda}{d\eta}=a^2,
\qquad
Z=-g(U,k)=\frac1a,
\qquad
\frac{dZ}{d\lambda}=-\frac{a'}{a^4}.
\]

The second mixing function does not alter the central frequency law.  Frequency turns remain the
sign-changing zeros of `a'`; `d_A(Z)` remains branch-local across such turns.

## 3. Parallel screen and exact tide

Because `M` is symmetric, the original coordinate screen vectors

\[
s_p=a^{-1}\partial_p,
\qquad
s_w=a^{-1}\partial_w
\]

are parallel and orthonormal along the central affine ray.  No time-dependent diagonalization is
used.

Let

\[
\mathcal H=\frac{a'}a,
\qquad
\tau_0=\frac{\mathcal H^2-\mathcal H'}{a^4}.
\]

Direct Riemann reconstruction gives the self-adjoint screen tide

\[
\boxed{
\mathcal T
=\tau_0 I_2+\frac{2M'-4M^2}{a^4}.}
\]

In components,

\[
\mathcal T=\tau_0 I_2+\frac1{a^4}
\begin{pmatrix}
2A'-4A^2-4\nu^2&2\nu'-4A\nu\\
2\nu'-4A\nu&-4\nu^2
\end{pmatrix}.
\]

The new channel enters through `nu'`, both diagonal `nu^2` terms, and the `A nu` cross term.  It
cannot be represented by appending one scalar angular correction after reciprocal readout.

## 4. Genuine noncommutativity

For two parameter values,

\[
[M_1,M_2]
=(A_1\nu_2-A_2\nu_1)
\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Hence histories with changing `A/nu` have no single constant screen rotation that diagonalizes the
family.  The frozen noncommuting control has commutator norm

\[
0.04228017920000001.
\]

Its forward endpoint Jacobi matrix is

\[
\mathcal D(0.65)=
\begin{pmatrix}
0.690331628271771&0.0145778127047724\\
0.0145147945716826&0.704238737873077
\end{pmatrix}.
\]

Thus the two cross responses need not be equal.  Its polar rotation angle is approximately
`-4.52e-5` radians.  The effect is a derived property of this chosen mathematical history, not a
universal sign or physical magnitude.

## 5. Matrix factorization

Write the physical screen map as

\[
\mathcal D(\eta)=a(\eta)Y(\eta).
\]

Using `d/dlambda=a^-2 d/deta`, the affine Jacobi equation

\[
\frac{d^2\mathcal D}{d\lambda^2}+\mathcal T\mathcal D=0
\]

reduces exactly to

\[
Y''+(2M'-4M^2)Y=0.
\]

Matrix order matters, but no commutativity assumption is required:

\[
\boxed{
\left(\frac d{d\eta}-2M\right)
\left(\frac d{d\eta}+2M\right)Y=0.}
\]

Let `L` be the fundamental matrix

\[
L'=-2ML,
\qquad L(0)=I,
\]

and define

\[
K(\eta)=\int_0^\eta L(s)^{-1}L(s)^{-T}\,ds.
\]

Because `M=M^T`,

\[
(L^{-T})'=2ML^{-T}.
\]

Consequently

\[
\boxed{Y=LK,\qquad \mathcal D=aLK}
\]

solves the matrix equation with

\[
\mathcal D(0)=0,
\qquad
\frac{d\mathcal D}{d\lambda}(0)=I_2.
\]

This is an ordered matrix quadrature.  It does not replace the noncommuting history by two scalar
modes.

## 6. Exact no-caustic proof

Liouville's formula gives

\[
\det L(\eta)
=\exp\left[-2\int_0^\eta\operatorname{tr}M(s)\,ds\right]>0.
\]

For every nonzero vector `v`,

\[
v^T L^{-1}L^{-T}v=\lVert L^{-T}v\rVert^2>0.
\]

Therefore `K(eta)` is positive definite for `eta>0` and negative definite for `eta<0`.  In two
screen dimensions, either case has positive determinant.  Since `a>0`,

\[
\boxed{
\det\mathcal D
=a^2\det L\det K>0
\quad\text{for every }\eta\ne0.}
\]

Thus the declared connected regular family has no nonvertex screen caustic.  This proof is exact;
the numerical census is only an independent consistency check.

## 7. Limits and verification

- `nu=0` returns G192's active/passive factorization.
- `mu=nu=0` returns the arbitrary conformal G190 screen.
- Constant `mu,nu` gives a full-rank commuting control.
- Varying `mu/nu` gives genuinely noncommuting controls without changing the proof.

The production derivation passes 16 exact symbolic assertions.  One independent leg uses Torch
automatic metric jets and a separately coded Riemann tensor at preregistered sample points.  A
second, formula-driven leg uses SciPy DOP853 matrix IVPs to compare the direct Jacobi equation with
the separately integrated ordered representation.  This is not a metric-derived tide evaluation
at every adaptive IVP call.  Across 264 frozen histories and 3,961 assertions the two-leg replay
finds

\[
\max\lVert\mathcal T_{\rm metric}-\mathcal T_{\rm formula}\rVert
=1.14\times10^{-13},
\]

\[
\max\lVert\mathcal D_{\rm direct}-aLK\rVert
=1.97\times10^{-11},
\]

below the preregistered `2e-8` ceiling.  Fifteen structural mutations are caught.

## 8. Epistemic boundary

The reason the result survives is now narrower and clearer: symmetry of the screen mixing matrix
creates a positive Gram integral.  G193 has not activated the omitted antisymmetric/rotational
channel or the third independent symmetric component, and it has not changed the supplied pair
germ.  No physical history, transfer, observations, global branch, or `X_max` enters.
