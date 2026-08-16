# Exact derivation — constant complete reciprocal-representation census

Date: 2026-08-16  
Scope: regular local zero-order constant generators on a supplied pair-relative `2+2` split  
Status: `VERIFIED_WITH_CAVEATS`; reviewer-found proof-script defect repaired and corrected external follow-up verified

## 1. Question and epistemic boundary

The founded reciprocal character is

\[
D(\delta)=e^{\delta H_b},
\qquad H_b=\operatorname{diag}(-1,+1),
\]

on an already supplied ordered depth. This audit asks for every **constant** one-parameter
representation on the complete base-plus-screen vector space that genuinely extends that base
action.

The pair-relative split is conditional but legitimate: a supplied regular pair realization owns a
timelike pair plane and a positive screen. Without that supplied split, the bare Lorentz metric does
not contain the displayed `H_b` as a structureless invariant endomorphism.

No observational curve, desired loudness pattern, coefficient, regime location, action, source,
bootstrap condition, or `X_max` value enters.

## 2. A finite extension is more than a top-left block

Write a general constant generator as

\[
H=\begin{pmatrix}H_b&A\\C&D_s\end{pmatrix}.
\]

Merely fixing the top-left block makes this an infinitesimal block match, not yet a categorical
extension of the founded representation. There are three exact extension types:

### Embedded extension

For the inclusion `i(u)=(u,0)`, require

\[
Hi=iH_b.
\]

This is equivalent to `C=0`. The base is invariant and

\[
e^{\delta H}i=iD(\delta).
\]

### Quotient extension

For the projection `p(u,w)=u`, require

\[
pH=H_bp.
\]

This is equivalent to `A=0`. The screen is invariant and the induced base quotient action is
exactly `D(delta)`.

### Split extension

Requiring both gives

\[
A=C=0.
\]

These types are classified rather than silently identified. A generic `A,C != 0` generator with
top-left `H_b` is rejected only as a **finite extension type**; this is not a no-go on future
field-dependent coupled laws.

## 3. Residual screen covariance

Let the residual screen-frame action be

\[
L_R=\operatorname{diag}(I_2,R).
\]

A structureless constant generator must obey

\[
L_RHL_R^{-1}=H
\]

for every declared screen gauge transformation `R`.

Both `SO(2)` and `O(2)` contain rotations with no nonzero fixed vector. Therefore

\[
A=0,\qquad C=0.
\]

At generator level the exact off-block equations are

\[
A\epsilon=0,\qquad \epsilon C=0.
\]

These are infinitesimal covariance equations, not eigenvalue-one equations. The external review
found that the first production script had accidentally coded `(A epsilon-A)=0` and
`(epsilon C-C)=0`. In two screen dimensions both the incorrect and correct equations have only the
zero solution, so the classification was unchanged; the script and hostile regression have been
repaired.

The constant screen endomorphism must lie in the screen centralizer.

For a supplied screen orientation,

\[
\operatorname{Cent}_{M_2(\mathbb R)}SO(2)
=\{aI_2+b\epsilon:a,b\in\mathbb R\},
\qquad
\epsilon=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

For the full unoriented screen group,

\[
\operatorname{Cent}_{M_2(\mathbb R)}O(2)
=\{aI_2:a\in\mathbb R\}.
\]

Hence the complete structureless constant classes are

\[
H_{a,b}=H_b\oplus(aI_2+b\epsilon)\quad[SO(2)],
\]

and

\[
H_a=H_b\oplus aI_2\quad[O(2)].
\]

This classification is complete inside the declared constant screen-covariant class. In
particular, constant off-block mixing and constant screen shear require an undeclared preferred
screen tensor and do not survive this gate.

## 4. Exact finite family

Exponentiation gives

\[
\boxed{
G_{a,b}(\delta)
=\operatorname{diag}\!\left(
e^{-\delta},e^{+\delta},e^{a\delta}R(b\delta)
\right),
}
\]

where `R` is the ordinary `2x2` rotation. Therefore

\[
G_{a,b}(\delta_2)G_{a,b}(\delta_1)
=G_{a,b}(\delta_1+\delta_2),
\]

and

\[
G_{a,b}(\delta)^{-1}=G_{a,b}(-\delta).
\]

The founded base restriction is exact for every `a,b`.

## 5. Determinant and pairing gates are not the same premise

The founded base action already has determinant one and preserves

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Those base facts place no restriction on `a` or `b`. Promoting either to the complete
four-dimensional action is an additional condition and is therefore explored as a fork.

The complete determinant is

\[
\det G_{a,b}(\delta)=e^{2a\delta}.
\]

Thus complete determinant one is equivalent to

\[
a=0.
\]

For the natural direct-sum test pairing

\[
\widetilde K=K\oplus I_2,
\]

the generator condition is

\[
H^T\widetilde K+\widetilde K H=0.
\]

Its exact residual is

\[
0_2\oplus2aI_2,
\]

so it also requires `a=0` and permits `b`. The same scale conclusion holds for a nondegenerate
`SO(2)`-invariant screen bilinear form. No complete pairing has been promoted to a UDT premise here.

## 6. Extending abstract clock–ruler exchange

The founded exchange obeys

\[
K H_b K=-H_b.
\]

How exchange acts on the screen is not founded, so two exact extensions are classified.

If it fixes the screen,

\[
X_I=K\oplus I_2,
\qquad X_IH_{a,b}X_I^{-1}=-H_{a,b}
\]

requires

\[
a=b=0.
\]

If it also reflects the screen orientation,

\[
X_F=K\oplus F,
\qquad F\epsilon F^{-1}=-\epsilon,
\]

then exchange oddness requires only

\[
a=0
\]

and permits `b`.

Thus every examined complete exchange lift removes the common screen dilation. The rotation
survives only when exchange reverses screen orientation. These are conditional extension choices,
not consequences silently read back into the two-channel foundation.

## 7. Passive and active actions

This is the decisive ownership distinction.

### Passive coordinate carry

For any invertible ambient basis change `P`,

\[
E\mapsto EP^{-1},\qquad J\mapsto PJ,
\]

so

\[
V=EJ\mapsto EP^{-1}PJ=V.
\]

Every terminal pair observable is unchanged. Any proposed score implemented only this way is frame
bookkeeping.

### Passive orthonormal screen rotation

For `O in O(2)`,

\[
E\mapsto\operatorname{diag}(I_2,O)E
\]

rotates the screen part of `V` and leaves

\[
h=V^T\eta_4V
\]

unchanged. The `b` channel is therefore zero-order screen-frame gauge. It may label a future
connection/holonomy transport channel, but the constant local rotation is not a terminal score.

### Conditional active coframe action

If one **chooses** the active placement

\[
E(\delta)=G_{a,b}(\delta)E(0),
\qquad J(\delta)=J(0),
\]

then

\[
V(\delta)=G_{a,b}(\delta)V(0).
\]

Writing `V=(U;A_s)`, the pair metric becomes

\[
\boxed{
h(\delta)
=U^TD(\delta)^T\eta_2D(\delta)U
+e^{2a\delta}A_s^TA_s.
}
\]

The rotation `b` cancels exactly. The common screen dilation `a` generally changes `h`, terminal
`phi_pair`, and `c_eff/c_E`.

For the exact rational witness

\[
V=\begin{pmatrix}5&0\\0&1\\1&0\\0&1\end{pmatrix}
\]

and `e^delta=2`, the original, neutral-lift, and `a=1` active metrics are

\[
h_0=\operatorname{diag}(-24,2),
\]

\[
h_{a=0}=\operatorname{diag}(-21/4,5),
\]

\[
h_{a=1}=\operatorname{diag}(-9/4,8).
\]

Their squared terminal ratios are respectively

\[
12,\qquad 21/20,\qquad 9/32.
\]

So `a` is a real active direction under this explicit placement.

### Compensated pair carry

The same metric deformation can be paired with

\[
J(\delta)=E(0)^{-1}G_{a,b}(\delta)^{-1}E(0)J(0),
\]

which leaves `V` and `h` unchanged. More generally, G98's exact reachability means coordinated
`E/J` histories can preserve or alter the same terminal chord.

The representation itself therefore does not own the active carry of `J`. It classifies a possible
metric action after that choice; it does not derive the physical history.

## 8. What the constant family can and cannot play

Under only the founded base gates and residual full `O(2)`, the structureless constant extension
contains one free screen-dilation weight:

\[
H_a=\operatorname{diag}(-1,+1,a,a).
\]

Under oriented `SO(2)`, a second rotation weight `b` appears but is zero-order gauge. No constant
screen shear, anisotropic angular generator, or base-screen mixing survives.

Consequently a constant extension supplies at most the weight set

\[
\{-1,+1,a\}
\]

on the coframe and

\[
\{-2,+2,2a\}
\]

on quadratic terms. Positive combinations of opposite weights can have an interior minimum, but
the Lorentzian terminal ratio is not universally flat, monotone, or loud-quiet-loud. The census
does not select a shape.

The constant action also does not determine the physical angular map or its Jacobian. Connecting
the screen metric to the G105/G106 observer-sky response requires a supplied query plus a Jacobi or
other metric-derived propagation rule. It cannot be inferred from `a` alone.

## 9. Exact landing

Within the preregistered constant zero-order class:

```text
CONSTANT_EXTENSION_CENSUS_COMPLETE
__BASE_ONLY_GATES_LEAVE_ONE_ACTIVE_SCREEN_DILATION_PARAMETER
__FULL_DETERMINANT_PAIRING_OR_EXTENDED_EXCHANGE_REMOVES_IT
__ORIENTED_SCREEN_ROTATION_IS_ZERO_ORDER_GAUGE
__NO_PHYSICAL_SCORE_SELECTED_BECAUSE_ACTIVE_EJ_CARRY_IS_UNOWNED
```

Premise stamps:

- `DERIVED`: the constant `O(2)`/`SO(2)` centralizers and absence of constant off-block
  intertwiners;
- `DERIVED`: exact group composition, reversal, determinant, conditional pairing, exchange, and
  active/passive algebra;
- `CONDITIONAL`: the pair-relative split and each complete determinant/pairing/exchange lift;
- `CHOSE` for the witness only: active left action with fixed `J`, used to prove possibility rather
  than physical ownership;
- `OPEN`: the physical active action/carry, field-dependent generators, pair propagation, history,
  regime dependence, and global completion.

The most important negative is scoped: the constant structureless census does not contain the
complete orchestra score. It leaves one common screen-scale ansatz under the weakest gates, and
that ansatz is killed by several lawful but not-yet-owned stronger extensions.

## 10. Next justified calculation

Do not fit `a`. First determine whether a supplied metric history and observer query naturally tie
the pair realization to the coframe through the exact screen Jacobi/Riccati propagation. Run this
for the complete constant survivor classes as a **conditional propagation atlas**, keeping the
metric history, initial screen data, branch, and affine parameter explicit.

If the Jacobi carry cancels the apparent `a` freedom, the constant candidate dies. If it converts
`a` into a gauge-invariant screen response, the result is still a conditional finite family until
a physical history owner is supplied.
