# G226 exact derivation — conformal-symplectic assembly on a supplied null chain

Date: 2026-08-22

## Bounded landing

```text
SUPPLIED_COMPOSABLE_NULL_CHAIN_HAS_A_CAUSTIC_SAFE_CONFORMAL_SYMPLECTIC_SCREEN_PHASE_FUNCTOR
__PROPER_CLOCK_RATIO_IS_THE_EXACT_CONFORMAL_MULTIPLIER
__G224_VERTICAL_RULER_CARRY_IS_ITS_INVERSE
__G225_DIRECTION_HOLONOMY_SURVIVES_AS_A_MATRIX_CHANNEL
```

Status after fresh review and repair-only closure:
`DERIVED_CONDITIONAL__EXTERNALLY_VERIFIED__REPAIRS_VERIFIED`.

The metric, two regular affine null edges, their marked endpoint observer germs, and one actual
shared calibrated event are supplied. G225's pointwise least-turning map is used as the frozen
standard geometric evaluator, not promoted to selected physical transport.

## 1. The full screen phase is the correct object

Let `V` be the oriented one-dimensional null tangent line at an incidence and let `S` be its
positive G188 quotient screen. The intrinsic first transverse jet is

\[
\mathcal P(V,S)=S\oplus\operatorname{Hom}(V,S).
\]

An element is `(x,p)`, where `x` is a transverse displacement and `p` gives its transverse
derivative for any chosen null generator. A generator `k in V` evaluates the phase as

\[
z_k=\binom{x}{p(k)}.
\]

The associated Wronskian form is

\[
\Omega_k((x,p),(y,q))
=\langle x,q(k)\rangle-\langle p(k),y\rangle.
\]

It scales with the generator:

\[
\Omega_{\gamma k}=\gamma\Omega_k,
\qquad \gamma>0.
\]

This generator weight is the joint where the G224 scalar carry and the G188 phase meet.

## 2. Affine G188 evolution is symplectic

In a parallel orthonormal screen frame along one affine null edge, the Jacobi equation is

\[
D_k^2x+\mathcal T x=0,
\]

where the G188 tidal operator `T` is self-adjoint. With `v=D_kx`, this becomes

\[
\frac{d}{d\lambda}
\binom{x}{v}
=
\begin{pmatrix}0&I\\-\mathcal T&0\end{pmatrix}
\binom{x}{v}.
\]

For

\[
\Omega=\begin{pmatrix}0&I\\-I&0\end{pmatrix},
\]

self-adjointness gives

\[
A^T\Omega+\Omega A=0.
\]

Therefore the full affine fundamental transfer `F_e` obeys

\[
\boxed{F_e^T\Omega F_e=\Omega.}
\]

The G188 vertex-normalized Jacobi map is only the upper-right position block of this full
four-dimensional transfer. It is not the composable phase by itself.

## 3. Clock normalization turns the phase symplectic law into the reciprocal law

Let the parallel affine generator on an edge `e:A->B` be `K`, and define endpoint frequencies

\[
\omega_A=-g(U_A,K_A)>0,
\qquad
\omega_B=-g(U_B,K_B)>0.
\]

The G224 clock-normalized null generators are

\[
N_A=K_A/\omega_A,
\qquad
N_B=K_B/\omega_B.
\]

If `z_N=(x,D_Nx)`, then

\[
z_K=R(\omega)z_N,
\qquad
R(\omega)=\operatorname{diag}(I_2,\omega I_2).
\]

Hence the full edge matrix in clock-normalized endpoint phases is

\[
\boxed{
M_e=R(\omega_B)^{-1}F_eR(\omega_A).
}
\]

Since

\[
R(\omega)^T\Omega R(\omega)=\omega\Omega,
\]

the exact edge law is

\[
\boxed{
M_e^T\Omega M_e=r_e\Omega,
\qquad
r_e=\frac{\omega_A}{\omega_B}
=\frac{d\tau_B}{d\tau_A}.
}
\]

Thus `M_e` lies in the positive conformal symplectic group
`CSp^+(4,R)`, with multiplier equal to the G216 proper-clock ratio. G224's vertical ruler
coefficient is

\[
\boxed{q_e=\frac{\omega_B}{\omega_A}=r_e^{-1}.}
\]

There is no second scalar coefficient. In four phase dimensions,

\[
\det M_e=r_e^2.
\]

A constant affine rescaling `K -> gamma K` conjugates `F_e` by `R(gamma)` while multiplying both
endpoint frequencies by `gamma`; these changes cancel exactly in `M_e`.

## 4. The shared-event vertex lift

At the actual shared event, let G224 give the vertical-line isomorphism

\[
s:V_-\longrightarrow V_+
\]

and let the frozen G225 evaluator give

\[
C:S_-\longrightarrow S_+.
\]

The unique natural first-jet lift is

\[
\boxed{
L(C,s)(x,p)=(Cx,C\circ p\circ s^{-1}).
}
\]

If arbitrary generators satisfy `s(k_-)=a k_+`, its coordinate matrix is

\[
\operatorname{diag}(C,a^{-1}C).
\]

For the G224 frequency-one generators,

\[
s(N_-)=N_+,
\]

so

\[
\boxed{L_B=\operatorname{diag}(C_B,C_B),}
\]

and

\[
L_B^T\Omega L_B=\Omega.
\]

The vertex changes screen direction without inserting a scalar multiplier.

## 5. Exact two-edge composition

For supplied edges `A->B` and `B->C`, the path-labelled phase is

\[
\boxed{
M_{ABC}=M_{BC}L_BM_{AB}.
}
\]

Therefore

\[
\boxed{
M_{ABC}^T\Omega M_{ABC}
=r_{BC}r_{AB}\Omega.
}
\]

On the actual composed clock correspondence,

\[
r_{AC}=r_{BC}r_{AB},
\]

so the full matrix multiplier is the scalar reciprocal-kernel clock arrow, while

\[
q_{AC}=q_{BC}q_{AB}=r_{AC}^{-1}
\]

is the vertical ruler representation.

This makes the combined evaluator a path-labelled functor into `CSp^+(4,R)`. It does not make the
path thin or select which supplied null chain is physical.

## 6. Middle-screen gauge covariance

Let independently chosen passive screen bases act at `A`, the incoming and outgoing screens at
`B`, and `C` by `Q_A,Q_{B-},Q_{B+},Q_C in O(2)`. Write

\[
\widehat Q=\operatorname{diag}(Q,Q).
\]

Then

\[
M_{AB}\mapsto\widehat Q_{B-}^TM_{AB}\widehat Q_A,
\]

\[
L_B\mapsto\widehat Q_{B+}^TL_B\widehat Q_{B-},
\]

\[
M_{BC}\mapsto\widehat Q_C^TM_{BC}\widehat Q_{B+}.
\]

The two independent middle gauges cancel:

\[
M_{ABC}\mapsto\widehat Q_C^TM_{ABC}\widehat Q_A.
\]

Thus no middle screen frame is physical or left unowned by the assembly.

## 7. Caustics do not break the full phase

Write a full phase transfer in blocks,

\[
M=\begin{pmatrix}A&B\\C&D\end{pmatrix}.
\]

The G188 vertex Jacobi position map is `B`. At a caustic, `det B=0`; no inverse of `B` exists.
But every positive conformal-symplectic `M` is invertible, with

\[
\det M=r^2>0.
\]

Therefore composition continues through a position caustic using `(x,D_Nx)`. G226 does not assign
multiple-image weights or perform branch aggregation; it only proves that the local first-order
phase is not destroyed.

## 8. Residual holonomy remains matrix-valued

For positive `r`, define the algebraic normalized representative

\[
\widetilde M=r^{-1/2}M\in\operatorname{Sp}(4,\mathbb R).
\]

This separates the exact scalar grading from the residual focusing, shear, and rotation phase. It
is a classification device, not a new physical normalization law.

When the edge phases are identity controls, the G225 octant direction triangle contributes

\[
\operatorname{diag}(H,H),
\qquad
H=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\]

so the quarter-turn survives exactly in the phase functor. An ordered same-great-circle control
has `H=I`. With nontrivial edge tides, the vertex and edge matrices generically do not commute;
direction-space and curvature memory remain in their lawful order rather than becoming a fitted
scalar.

An independently supplied direct `A->C` relation is a different arrow. If both a direct and a
composite arrow are supplied, their full-matrix defect can be evaluated. No present identity
forces that defect to vanish.

## 9. Degenerate and global strata

- At a Jacobi caustic, the position block is singular but the full phase remains invertible.
- At a G225 antipode, the least-turning vertex map is nonunique; G226 returns no unique vertex
  phase without a supplied path/axis choice.
- A singular metric, nonregular null edge, or missing shared event lies outside the theorem.
- Cut loci, multiple branches, multiple-image weights, and topology-changing continuation remain
  branch-labelled and open.
- A closed chain with total clock multiplier one has a symplectic phase holonomy; it need not be
  the identity.

## 10. Verification

The production derivation passes 28 exact symbolic/rational checks. An independent
standard-library implementation uses exact `Fraction` arithmetic on 20,000 seeded two-edge
chains and passes 200,007 assertions; all 20,000 sampled ordered edge/vertex products are
noncommuting. Eight hostile mutations are caught, including `q` substituted for `r`, omission of
the derivative-screen rotation, inversion of a caustic position block, uncancelled middle gauge,
scalarized holonomy, and forced direct-equals-composite.

## 11. Maximum conclusion

G226 derives the caustic-safe conformal-symplectic assembly of the already owned scalar,
pointwise-screen, and along-edge Jacobi channels on one supplied composable non-antipodal null
chain. It does not select a null protocol, promote G225 to physical transport, populate observers
or branches, choose a metric history, or derive `X_max`, transfer, observations, action, source,
matter, bootstrap, mass, or signalling.
