# G194 exact derivation — arbitrary symmetric screen mixing

Date: 2026-08-20

## 1. Bounded landing

For the preregistered arbitrary positive `a(eta)` and arbitrary real symmetric `2 x 2 M(eta)`
family, the central frequency law, full matrix Jacobi operator, ordered factorization, and exact
positive-Gram no-caustic proof all close.

This removes G193's frozen lower-right screen component.  It is a theorem for the displayed
symmetric coframe family and one supplied central pair.  It is not a theorem for antisymmetric
screen rotation, arbitrary complete coframes, other pair germs, or global completion.

## 2. Complete coframe, pair, and frequency

Let

\[
X=\binom{p}{w},\qquad q=d\eta+dz,\qquad
M(\eta)=\begin{pmatrix}A(\eta)&N(\eta)\\N(\eta)&B(\eta)\end{pmatrix},
\]

and

\[
\theta^0=a\,d\eta,\qquad
\theta^1=a\,dz,\qquad
\binom{\theta^p}{\theta^w}=a[dX+MXq].
\]

Direct reconstruction gives

\[
\det E=a^4,\qquad \det g=-a^8.
\]

Thus the coframe is regular Lorentzian wherever `a>0`, with no condition on the sign, trace,
determinant, rank, or eigendirections of `M`.  On the supplied pair `p=w=0`,

\[
F^*g=a^2(-d\tau^2+d\sigma^2).
\]

The completed clock, ruler, normalized null germ, and affine tangent are

\[
U=a^{-1}\partial_\eta,\qquad
N_z=a^{-1}\partial_z,\qquad
\ell_+=U+N_z,\qquad
k=a^{-2}(\partial_\eta+\partial_z).
\]

The full Christoffel reconstruction gives `nabla_k k=0`, hence

\[
\frac{d\lambda}{d\eta}=a^2,\qquad
Z=-g(U,k)=\frac1a,\qquad
\frac{dZ}{d\lambda}=-\frac{a'}{a^4}.
\]

All three symmetric mixing functions remain absent from the central frequency law.  Frequency
turns are still controlled by zeros of `a'`, so `d_A(Z)` remains only branch-local across turns.

## 3. Parallel screen and full metric tide

Because `M=M^T`, the original coordinate screen

\[
s_p=a^{-1}\partial_p,\qquad s_w=a^{-1}\partial_w
\]

is orthonormal and parallel along the central affine ray.  No time-dependent diagonalization is
used.

With

\[
\mathcal H=\frac{a'}a,\qquad
\tau_0=\frac{\mathcal H^2-\mathcal H'}{a^4},
\]

direct four-dimensional Riemann reconstruction gives

\[
\boxed{\mathcal T=\tau_0 I_2+\frac{2M'-4M^2}{a^4}.}
\]

In components,

\[
\mathcal T=\tau_0 I_2+\frac1{a^4}
\begin{pmatrix}
2A'-4A^2-4N^2 & 2N'-4N(A+B)\\
2N'-4N(A+B) & 2B'-4B^2-4N^2
\end{pmatrix}.
\]

The formerly frozen function `B` enters through `B'`, `B^2`, and the `NB` part of the shared
off-diagonal term.  The complete screen contribution is upstream of terminal readout; it is not a
post-readout scalar correction.

## 4. Noncommutativity is generic

For two parameter values,

\[
[M_1,M_2]_{12}
=N_2(A_1-B_1)-N_1(A_2-B_2),
\]

with the opposite sign in the `21` component and zero diagonal.  Thus a changing anisotropy axis
generically prevents one constant rotation from diagonalizing the history.

The frozen noncommuting control has commutator norm

\[
0.034840754354551015.
\]

At `eta=0.65` its Jacobi cross asymmetry is approximately
`3.49e-5` and its polar rotation angle is approximately `-2.49e-5` radians.  These are properties
of that chosen mathematical control, not universal signs or physical magnitudes.

## 5. Ordered factorization

Write the physical screen map as

\[
\mathcal D(\eta)=a(\eta)Y(\eta).
\]

Using `d/dlambda=a^-2 d/deta`, the affine Jacobi equation becomes

\[
Y''+(2M'-4M^2)Y=0.
\]

Without assuming that matrices at different times commute,

\[
\boxed{
\left(\frac d{d\eta}-2M\right)
\left(\frac d{d\eta}+2M\right)Y=0.}
\]

Let

\[
L'=-2ML,\qquad L(0)=I,
\]

and define

\[
K(\eta)=\int_0^\eta L(s)^{-1}L(s)^{-T}\,ds.
\]

Since `M=M^T`,

\[
(L^{-T})'=2ML^{-T}.
\]

For `Y=LK`,

\[
(\partial_\eta+2M)Y=LK'=L^{-T},
\]

so the outer factor annihilates it.  Therefore

\[
\boxed{\mathcal D=aLK}
\]

obeys

\[
\mathcal D(0)=0,\qquad
\frac{d\mathcal D}{d\lambda}(0)=I_2.
\]

This is an ordered matrix quadrature, not a commuting exponential or two decoupled scalar modes.

## 6. Exact no-caustic classification

Liouville's formula gives

\[
\det L(\eta)=
\exp\left[-2\int_0^\eta\operatorname{tr}M(s)\,ds\right]>0.
\]

For every nonzero vector `v`,

\[
v^T L^{-1}L^{-T}v=\lVert L^{-T}v\rVert^2>0.
\]

Thus `K(eta)` is positive definite for `eta>0` and negative definite for `eta<0`.  In two screen
dimensions either case has positive determinant.  Since `a>0`,

\[
\boxed{
\det\mathcal D=a^2\det L\det K>0
\quad\text{for every }\eta\ne0.}
\]

Hence the entire declared connected regular symmetric family has no nonvertex screen caustic.
This is an exact function-space result; the finite census only checks the implementation.

## 7. Limits and independent replay

- `B=0` returns G193.
- `B=N=0` returns G192.
- `A=N=B=0` returns the conformal G190 screen.
- Scalar, diagonal unequal, rank-changing, and genuinely noncommuting histories all stay inside
  the theorem.

The production reconstruction passes 19 exact symbolic assertions.  The independent verifier uses
Torch metric jets and a separately coded Riemann tensor at registered points, plus a formula-driven
SciPy DOP853 matrix-IVP comparison.  It does not evaluate a metric-derived tide at every adaptive
IVP call.

Across 267 histories and 4,007 assertions,

\[
\max\lVert\mathcal T_{\rm metric}-\mathcal T_{\rm formula}\rVert
=5.33\times10^{-15},
\]

\[
\max\lVert\mathcal D_{\rm direct}-aLK\rVert
=1.46\times10^{-11},
\]

and the largest Wronskian residual is `7.87e-12`, all below the preregistered `2e-8` tensor
ceiling.  Twenty-two hostile mutations are caught.

## 8. Epistemic boundary

G194 closes the arbitrary smooth symmetric `2 x 2` matrix sector in the displayed coframe family.
The load-bearing structure is symmetry, not commutativity, diagonal form, trace, rank, sign, or a
fitted regime ratio.  Antisymmetric screen rotation is now the nearest distinct failure-boundary
test.  Physical history, pair population, transfer, observations, global branches, and `X_max`
remain outside this theorem.
