# G290 exact derivation — complete-pair screen holonomy and time-live transgression

Date: 2026-08-28
Grade: `EXTERNALLY_ACCEPTED_BOUNDED_G290__NO_DEFECTS`

## Landing

```text
EXACT_COMPLETE_PAIR_SCREEN_HOLONOMY_DESCENDS_CONDITIONALLY
__CONFORMAL_TWIN_HISTORY_SEPARATOR_DERIVED
__TIMELIVE_HOLONOMY_CHANGE_EQUALS_SCREEN_CURVATURE_FLUX
__ORIENTABLE_SCREEN_FULL_O2_ROTATION_DATA_IS_INVERSE_CONJUGACY_CLASS
__NO_PERSISTENCE_DYNAMICS_POPULATION_OR_HISTORY_SELECTION
```

Exact landing token:
`EXACT_COMPLETE_PAIR_SCREEN_HOLONOMY_DESCENDS_CONDITIONALLY__CONFORMAL_TWIN_HISTORY_SEPARATOR_DERIVED__TIMELIVE_HOLONOMY_CHANGE_EQUALS_SCREEN_CURVATURE_FLUX__ORIENTABLE_SCREEN_FULL_O2_ROTATION_DATA_IS_INVERSE_CONJUGACY_CLASS__NO_PERSISTENCE_DYNAMICS_POPULATION_OR_HISTORY_SELECTION`.

## Exact scope

Let `(M,g)` be a supplied smooth Lorentzian metric history. Let `W` be a supplied smooth regular
complete-pair network or congruence base with map `F:W->M`. The G225/G226/G274 layer supplies a
positive rank-two metric screen subbundle `S->W`, its orthogonal projection `P_S`, and path-labelled
screen carry.
The induced connection is

\[
D_Xs=P_S\!\left(\nabla^g_{F_*X}s\right).
\]

This is metric-native after those data are supplied. A bare null line at one event does not define
`D` on a base and is outside the theorem.

## Frame descent

Choose an oriented orthonormal screen frame `(e_1,e_2)` and the frozen convention

\[
a(X)=g(e_1,D_Xe_2),\qquad
U_\gamma=\exp\!\left(i\int_\gamma a\right).
\]

For

\[
e'_1=\cos\theta\,e_1+\sin\theta\,e_2,
\qquad
e'_2=-\sin\theta\,e_1+\cos\theta\,e_2,
\]

metric compatibility gives

\[
a'=a-d\theta.
\]

Therefore open carry is endpoint covariant,

\[
U'_{A\to B}=e^{-i\theta(B)}U_{A\to B}e^{i\theta(A)},
\]

while closed-loop holonomy is invariant. A large single-valued screen gauge can change the integral
by an integer multiple of `2 pi`, but not its exponential.

On an orientable screen bundle, an orientation-reversing `O(2)` gauge sends the signed
connection/phase to the opposite orientation. Thus the oriented `SO(2)` holonomy is not itself a
full-`O(2)` scalar. For rotation holonomy on that orientable stratum, the intrinsic unoriented data
are its inverse/conjugacy class

\[
\{U_\gamma,U_\gamma^{-1}\},
\]

or equivalently its real trace/cosine.

A genuinely nonorientable screen loop can itself carry a reflection holonomy. Such a loop is not
classified by `{U,U^{-1}}`; that global stratum remains open in this bounded derivation.

## Curvature and small loops

Because `SO(2)` is abelian, in every oriented local frame

\[
F_S=da.
\]

For a sufficiently small oriented loop bounding area `A` at `p`, the principal phase branch obeys

\[
\arg U_{\partial A}
=F_S(X,Y)\,\operatorname{Area}(A)+o(\operatorname{Area}(A)).
\]

One finite loop is not enough to recover curvature uniquely because phases are periodic. A shrinking
loop family removes that local alias. This is a curvature evaluator, not a new field equation.

## Exact conformal-twin separator

Take

\[
g_\alpha=e^{2\Omega}\eta,
\qquad
\Omega=\alpha(x^2+y^2+z^2),
\]

with the supplied static clock, `z` pair direction, oriented `x-y` screen, and circle
`gamma_rho`. The conformal Christoffel symbols are

\[
\Gamma^\lambda{}_{\mu\nu}
=\delta^\lambda_\mu\Omega_\nu
+\delta^\lambda_\nu\Omega_\mu
-\eta_{\mu\nu}\eta^{\lambda\sigma}\Omega_\sigma.
\]

Using `e_1=e^{-Omega} partial_x` and `e_2=e^{-Omega} partial_y` gives directly

\[
a=2\alpha(y\,dx-x\,dy),
\qquad
F_S=-4\alpha\,dx\wedge dy.
\]

For `x=rho cos psi`, `y=rho sin psi`,

\[
\int_{\gamma_\rho}a=-4\pi\alpha\rho^2,
\qquad
U_{\gamma_\rho}=\exp(-i4\pi\alpha\rho^2).
\]

Flat space (`alpha=0`) gives unit holonomy. Although an isolated loop may alias—for example
`alpha=1`, `rho^2=1/2` also gives unit holonomy—a sufficiently small oriented loop family recovers
`-4 alpha` and separates distinct local `alpha` values after orientation is supplied. Without an
orientation, `alpha` and `-alpha` give the same inverse/conjugacy data, while the registered flat
versus nonzero conformal twins are still separated by sufficiently small loops. The metrics retain
the same null cones while their center scalar curvature is `R(0)=-36 alpha`. Screen holonomy
therefore hears representative-metric history that pure null topology cannot.

## Time-live transgression

Let `C` be a supplied oriented loop worldtube with

\[
\partial C=\gamma_{t_2}-\gamma_{t_1}.
\]

Stokes descent gives the exact conditional identity

\[
\frac{U_{\gamma_{t_2}}}{U_{\gamma_{t_1}}}
=\exp\!\left(i\int_C F_S\right).
\]

For the independent control `Omega=alpha(t)(x^2+y^2+z^2)`,

\[
a=2\alpha(t)(y\,dx-x\,dy),
\]

and the fixed-radius cylinder has

\[
\frac{d}{dt}\int_{\gamma_\rho}a
=-4\pi\rho^2\dot\alpha(t)
=\int_{\gamma_\rho}\iota_{\partial_t}F_S.
\]

Hence the accumulated flux is exactly

\[
-4\pi\rho^2\bigl[\alpha(t_2)-\alpha(t_1)\bigr].
\]

This equation evaluates change on a supplied history. It does not set the flux.

## Nonselection theorem

Every smooth regular function `alpha(t)` satisfies the gauge-descent, curvature, and transgression
identities above. The identities therefore distinguish histories but reject none of this family.
No persistence, propagation, or admissibility residual has appeared.

The exact result is consequently:

- a native conditional metric evaluator: yes;
- a conformal-history discriminator: yes;
- a topological sector/persistence law: only kinematically and under supplied regular continuation;
- a physical-history selector or evolution equation: no.

## Evidence

- preregistration commit: `a1401ebe`;
- production: 19 exact symbolic checks and 9 separately typed conclusions;
- independent: 2,400 exact direct-Christoffel cases and 28,801 formula-level standard-library
  assertions; many assertions replay the same registered identities at different exact inputs;
- hostile controls: 7 of 7 hostile-claim witnesses passed, including phase alias, missing screen
  projection, full-`O(2)` overclaim, and selection promotion; these are not injected production
  mutants;
- no action, source, field equation, carrier, boundary, observation, mass, scale, Planck cutoff,
  physical history, or `X_max` entered.

A fresh zero-context internal adversary returned `VERIFIED_WITH_CAVEATS`: it retained the five-part
landing after the orientation, nonorientable-loop, and evidence-semantics repairs above. Fresh sealed
external `gpt-5.4` review then returned `ACCEPT_BOUNDED_G290`, with no scientific defects and no
remaining evidence or wording repairs.
