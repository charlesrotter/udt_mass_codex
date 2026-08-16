# Multiagent whiteboard synthesis

Date: 2026-08-15  
Frame: outcome-blind; BOSS and CMB outcomes sealed

Three independent roles examined the same bounded problem:

1. a complete-coframe representation geometer;
2. a global integrability and Jacobi theorist;
3. an inverse-problem skeptic.

Their common result is recorded below. This is a synthesis of banked equations and fresh algebraic
reasoning, not an external scientific review and not canonization.

## 1. Exact banked evaluator

On a supplied regular complete coframe and supplied calibrated pair realization,

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},\qquad
J=\begin{pmatrix}Y\\Z\end{pmatrix},\qquad
V=EJ,
\]

and

\[
h=V^{T}\eta_4V.
\]

On the regular A-calibrated Lorentzian stratum,

\[
\phi_{\rm pair}=\frac14\log\!\left(\frac{-\det h}{h_{00}^{,2}}\right),
\qquad
\frac{c_{\rm eff}^{({\rm pair})}}{c_E}
=\frac{-h_{00}}{\sqrt{-\det h}}
=e^{-2\phi_{\rm pair}}.
\]

These are `DERIVED_CONDITIONAL`: every angular and mixing channel enters before terminal readout,
but the physical histories of `E` and `J` remain `OPEN`.

## 2. The exact joint-flow identity

Define the complete coframe connection and the carried derivative of the pair realization by

\[
\Omega=E^{-1}dE,
\qquad
\mathcal D J=dJ+\Omega J.
\]

Then differentiation of `V=EJ` gives the exact identity

\[
\boxed{dV=E\,\mathcal D J.}
\]

Under an internal coframe change

\[
E\mapsto EH^{-1},\qquad J\mapsto HJ,
\]

one has

\[
\Omega\mapsto H\Omega H^{-1}-dH\,H^{-1},
\qquad
\mathcal D J\mapsto H\mathcal D J,
\]

so `dV` is unchanged. This is the smallest exact formula currently deserving the orchestra
metaphor: it assembles all moving instruments without confusing a passive frame change with a
physical response.

It is nevertheless a compatibility identity. Because `\mathcal D J` is not selected by the
current premises, it is not an equation of motion or a physical score.

## 3. Constructive nonselection

For fixed regular `E`, choose any regular realization `V_0` and a smooth perturbation

\[
V_\epsilon=V_0+\epsilon f(\zeta)W(\hat n),
\qquad f(\zeta_0)=f(\zeta_1)=0.
\]

For sufficiently small `epsilon`,

\[
J_\epsilon=E^{-1}V_\epsilon
\]

remains regular, retains both endpoint pair states, and changes the interior screen Jacobian and
sky/depth response. Thus endpoint composition, complete-coframe activity, and regularity do not by
themselves select the interior symphony.

This strengthens the G98 conclusion without claiming a global no-go: a future joint law can still
tie `E` and `J`.

## 4. The observable quotient is an output

For the ideal factorized reference of G106, avoid overloading the founding dual-pairing matrix `K`
and define

\[
\mathcal Q(\zeta,\hat n)
=\frac{p(\zeta,\hat n)}{p_\zeta(\zeta)s(\hat n)}
=1+m(\zeta,\hat n).
\]

Pure radial abundance cancels. Depth-dependent angular response survives. The exact centered-rate
identity is

\[
\partial_\zeta\log\mathcal Q
=\partial_\zeta\log p
-\left\langle\partial_\zeta\log p\right\rangle_{P_\zeta},
\qquad P_\zeta=p/p_\zeta=s\mathcal Q.
\]

For a regular one-to-one angular flow `F_zeta`, with

\[
X_\zeta=(\partial_\zeta F_\zeta)\circ F_\zeta^{-1},
\]

the corresponding measure continuity identity is

\[
\partial_\zeta[s(1+m)]
+\operatorname{div}_q\!\left(s(1+m)X_\zeta\right)=0,
\]

subject to additional source and branch terms when the underlying measure or branch inventory
changes. This constrains a supplied flow but does not select it. Density observes only the weighted
divergence; a weighted divergence-free rotational component remains invisible.

## 5. Coordinate-free chord variables

For an angular map `F_zeta`, let

\[
A_\zeta=dF_\zeta,\qquad C_\zeta=A_\zeta^\dagger A_\zeta.
\]

The polar/log decomposition separates a compact observable chord:

1. area expansion `one-half log det C_zeta`;
2. two trace-free shear components;
3. one screen-rotation/orientation channel;
4. terminal reciprocal depth `phi_pair` from the full pair metric.

These are more faithful variables than an arbitrary fitted polynomial. They still require one
complete history and measurement operator before comparison with data.

## 6. Candidate home A: extension of the reciprocal representation

The founded base generator is

\[
H_b=\operatorname{diag}(-1,+1),
\qquad D(\delta)=e^{\delta H_b}.
\]

A constant complete linear extension would have a generator

\[
H=\begin{pmatrix}H_b&A\\C&D_s\end{pmatrix},
\qquad G(\delta)=e^{\delta H}.
\]

This is the cheapest sharp candidate census because reversal and composition are automatic for a
one-parameter representation. The census must distinguish:

- a structureless constant extension;
- an extension built covariantly from supplied screen/mixing tensors;
- a passive coframe transformation;
- an active positional action on the physical pair relation.

For a structureless constant generator, covariance under the full screen `O(2)` action forces the
off-block intertwiners `A=C=0` and forces `D_s=aI`. If determinant one is imposed on the complete
four-dimensional representation, `tr H=0` gives `a=0`. Full `O(2)` therefore leaves only the
neutral lift `diag(-1,+1,0,0)`. Under oriented `SO(2)` covariance, a screen-rotation term
`b epsilon` also commutes with the screen action; it is gauge-like until an active physical carry
makes it observable.

This limited algebra does **not** exclude field-dependent covariant generators built from the
complete metric. It tells the next audit exactly where nontrivial weights must come from.

If paired weights `+w` and `-w` survive the full active carry, positive quadratic invariants can
contain

\[
A e^{2w\delta}+B e^{-2w\delta}
=2\sqrt{AB}\cosh\!\left(2w(\delta-\delta_*)\right),
\qquad
\delta_*=\frac{1}{4w}\log(B/A).
\]

That is a native algebraic route to a quiet interior and louder ends. It is a survivor shape, not
a selected history. The hostile test is decisive: if the weights cancel after `E` and `J` are
carried according to their exact tensor types, the apparent score was passive covariance dressed
as dynamics.

## 7. Candidate home B: metric-derived Jacobi/Riccati propagation

For a supplied metric history, geodesic or null screen query, affine parameter, initial screen, and
regular branch, the screen Jacobi map obeys

\[
\ddot{\mathsf D}+\mathsf R_{\rm screen}\mathsf D=0.
\]

Where `D` is invertible, its optical matrix

\[
\mathsf L=\dot{\mathsf D}\mathsf D^{-1}
\]

obeys

\[
\dot{\mathsf L}+\mathsf L^2+\mathsf R_{\rm screen}=0.
\]

For a monotone reciprocal parameter `zeta`,

\[
\mathsf D_{\zeta\zeta}
+\frac{\ddot\zeta}{\dot\zeta^2}\mathsf D_\zeta
+\frac{\mathsf R_{\rm screen}}{\dot\zeta^2}\mathsf D=0.
\]

This is the strongest currently known conditional way to tie the pair realization to a supplied
metric history. It is not a history selector: the metric, query, initial data, branch, and monotone
parameter remain supplied. It should be applied after the representation census, not substituted
for it.

## 8. Candidate home C: full sky/depth integrability

For `Omega=E^-1 dE`,

\[
d\Omega+\Omega\wedge\Omega=0,
\]

and the mixed sky/depth block obeys

\[
\partial_\zeta\Omega_A-\partial_A\Omega_\zeta
+[\Omega_\zeta,\Omega_A]=0.
\]

These equations, plus the immersion condition on `J=dF`, can reject independently fitted window
curves that cannot arise from one smooth global object. For a smoothly supplied `E`, however, they
are compatibility identities and do not select the history.

## 9. Why brute force must come later

An unrestricted inverse fit is non-identifiable because:

1. `E` and `J` compensate through `V=EJ`;
2. source density, angular Jacobian, and branch weights compensate;
3. the G106 reference quotient removes pure radial modulation;
4. finitely many survey windows leave an infinite-dimensional functional nullspace;
5. quadratic pair statistics discard sign and phase;
6. density/Jacobian data see determinant-like compression but not all shear and rotation.

A quiet middle in a compressed statistic could therefore mean a quiet physical response,
within-window cancellation, or phase rotation before squaring.

The lawful later inverse program is:

1. implement the finite reference/weight/mask operator;
2. retain signed one-point residual maps before pair compression;
3. include cross-window maps and cross-spectra;
4. require one latent history for every window and dataset;
5. choose the basis from the forward operator or its singular vectors, not from a desired shape;
6. cap dimensionality by independently resolved operator/covariance rank;
7. report the identified set, nullspace, and symmetries;
8. freeze a candidate on a discovery subset and test held-out windows, caps, and surveys without
   refitting.

Its maximum conclusion would be an `OBSERVED/CONDITIONAL` silhouette of the score, not a derived
metric law.

## 10. Joint verdict

```text
NO_CURRENT_COMPACT_SCORE_DERIVED
__COMPLETE_JOINT_FLOW_INTERFACE_IDENTIFIED
__RECIPROCAL_REPRESENTATION_EXTENSION_IS_THE_CHEAPEST_SHARP_NEXT_CENSUS
__JACOBI_RICCATI_IS_THE_STRONGEST_CONDITIONAL_E_TO_J_TIE
__BRUTE_FORCE_CAN_ONLY_RECOVER_AN_OBSERVABLE_SILHOUETTE
```

This ends the false choice between endless algebra and unconstrained fitting. The next calculation
is a finite outcome-blind classification with an explicit hostile falsifier.

