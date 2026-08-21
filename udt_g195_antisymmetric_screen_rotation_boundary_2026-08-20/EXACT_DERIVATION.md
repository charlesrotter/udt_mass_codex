# G195 exact derivation — antisymmetric screen rotation

Date: 2026-08-20

## Bounded family and status

This is a `DERIVED_CONDITIONAL` theorem for the preregistered coframe family

\[
\theta^0=a\,d\eta,\qquad \theta^1=a\,dz,\qquad
\theta_{\rm screen}=a[dX+M(\eta)X(d\eta+dz)],
\]

with

\[
M=S+\Omega,\qquad
S=\begin{pmatrix}A&N\\N&B\end{pmatrix},\qquad
\Omega=R J,\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Here `a>0` is arbitrary `C3`, `A,N,B,R` are arbitrary real `C2`, and the supplied
completed observer-pair germ is `p=w=0` in the outgoing `+z` direction.  This is not a theorem for
arbitrary complete coframes, spatially dependent mixing, other pair germs, global completion, or a
physically selected profile.

## Direct metric reconstruction

Writing `g=E^T diag(-1,1,1,1) E`, exact reconstruction gives

\[
\det E=a^4,\qquad \det g=-a^8.
\]

The central pair pullback is

\[
h=a^2(-d\eta^2+dz^2).
\]

The normalized outgoing null germ and its affine representative are

\[
k=a^{-1}(\partial_\eta+\partial_z),\qquad
\ell=a^{-2}(\partial_\eta+\partial_z),
\]

and the central frequency measured by the normalized clock is

\[
\mathcal Z=-g(a^{-1}\partial_\eta,\ell)=a^{-1}.
\]

All of these identities are independent of the entries of `M`, but the screen connection and
curvature are not.

## Coordinate-screen connection and tide

Let `e=(e_2,e_3)` be the coordinate-aligned orthonormal screen.  Along affine parameter `lambda`,
the exact screen connection is

\[
C_\lambda=\frac{2\Omega}{a^2},
\]

or, using `d/dlambda=a^{-2}d/deta`,

\[
C_\eta=2\Omega=2RJ.
\]

Thus the coordinate screen is parallel exactly when `R=0`; it may not be called parallel in the
G195 family.

Put

\[
H=\frac{a'}a,\qquad
\tau_0=\frac{H^2-H'}{a^4}.
\]

Direct contraction of the four-dimensional Riemann tensor gives the self-adjoint coordinate-screen
tide

\[
\boxed{
T_c=\tau_0 I+
\frac{2S'-4S^2-4[S,\Omega]}{a^4}.
}
\]

The apparent rotation dependence is a commutator with the symmetric strain.  No independent
`R'` or `R^2` focusing term survives.  In particular, when `S=0`,

\[
T_c=\tau_0 I
\]

even for arbitrary variable `R`.

## The actual parallel screen

Let `O(eta)` solve

\[
O'=-2\Omega O,\qquad O(0)=I.
\]

Because `Omega` is skew-symmetric, `O` is orientation-preserving orthogonal.  The carried screen
`f=eO` is parallel.  Define the symmetric strain in that screen by

\[
\widetilde S=O^T S O.
\]

Differentiation gives

\[
\widetilde S'
=O^T\bigl(S'-2[S,\Omega]\bigr)O.
\]

Conjugating the direct metric tide therefore yields

\[
\boxed{
T_p=O^T T_c O
=\tau_0 I+\frac{2\widetilde S'-4\widetilde S^2}{a^4}.
}
\]

This is exactly the G194 tide form, but with the symmetric strain expressed in the Levi-Civita
parallel screen rather than in the rotating coordinate screen.

## Ordered factorization for arbitrary real `M`

Let `Y_c` be the conformally rescaled Jacobi matrix in coordinate-screen components.  The affine
Jacobi equation is equivalent to

\[
\boxed{
(\partial_\eta-2M^T)(\partial_\eta+2M)Y_c=0.
}
\]

Expansion gives either of the exactly equivalent forms

\[
Y_c''+2(M-M^T)Y_c'
+(2M'-4M^TM)Y_c=0,
\]

or

\[
\left[(\partial_\eta+2\Omega)^2
+2S'-4S^2-4[S,\Omega]\right]Y_c=0.
\]

The ordering is load-bearing.  Replacing `M` by its symmetric part before metric reconstruction,
reversing the factors, or treating the matrices as commuting changes the equation.

Let

\[
L'=-2ML,\qquad L(0)=I,
\]

and

\[
K(\eta)=\int_0^\eta L(s)^{-1}L(s)^{-T}\,ds.
\]

Then

\[
(\partial_\eta+2M)(LK)=L^{-T},
\]

while

\[
(L^{-T})'=2M^TL^{-T}.
\]

Therefore the vertex-normalized physical Jacobi map in coordinate-screen components is

\[
\boxed{D_c(\eta)=a(\eta)L(\eta)K(\eta).}
\]

No symmetry assumption on `M` was used.  The G194 Gram representation was therefore not limited to
symmetric mixing: its ordered form extends to every smooth real `2x2` matrix in this displayed
family.

## Exact no-nonvertex-caustic theorem

For every nonzero vector `v`,

\[
v^T L^{-1}L^{-T}v=\lVert L^{-T}v\rVert^2>0.
\]

Hence `K(eta)` is positive definite for `eta>0` and negative definite for `eta<0`.  In two screen
dimensions, `det K(eta)>0` whenever `eta` is nonzero.  Also

\[
\det L(\eta)
=\exp\left[-2\int_0^\eta \operatorname{tr}M(s)\,ds\right]>0,
\]

and `a>0`.  Consequently

\[
\boxed{\det D_c(\eta)>0\quad\text{for every }\eta\ne0}
\]

on every connected regular interval in the bounded family.  The parallel-screen map differs only
by the orientation-preserving matrix `O`, so it has the same determinant.  The source vertex is the
only zero of the Jacobi determinant.

For pure rotation (`S=0`), `L=O`, `K=eta I`, so

\[
D_c=a\eta O,\qquad D_p=a\eta I.
\]

Rotation changes orientation carry but produces no independent area focusing.

## Exact conclusion

The direct symbolic run passed 22 identities.  The bounded landing is

```text
ROTATION_CARRIES_COVARIANTLY__GENERAL_REAL_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE
```

This is stronger than the preregistered first outcome because the proof removes the symmetry
restriction from the ordered Gram representation.  It does **not** determine the physical
profiles `a,A,N,B,R`, select another observer pair, or establish the result for arbitrary complete
metric families.  Independent finite-history reconstruction and hostile mutation catches remain
required before banking.
