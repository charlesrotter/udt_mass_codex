# G318 preregistration — nonconstant-conformal non-CMC branch classification

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_OUTCOME_SCRIPTS_OR_RESULTS`

## Whole bounded question

For the G316 conformal constraints

\[
-8\bar\Delta\psi+\bar R\psi
-|\bar A_{TT}+\bar L W|^2\psi^{-7}
+\left(\frac23\tau^2-2\Lambda\right)\psi^5=0,
\]

\[
\bar D_j(\bar L W)^{ij}=\frac23\psi^6\bar D^i\tau,
\]

free G317's constant `psi` inside one exact periodic one-coordinate family. Classify whether the
G317 interlock survives, is obstructed, or branches. Reconstruct the physical constraints and
initial Weyl data. Do not select a member or widen the claim beyond this family.

## Registered ansatz

On a marked flat `T^3` with dimensionless `2 pi` periodic coordinates, choose

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=\psi(x)>0,\qquad \psi'\not\equiv0,
\]

\[
\tau=\tau(x),\qquad \tau\ne0\ \hbox{throughout the registered sign-definite branch},
\]

\[
\bar A_{TT}^{ij}=\operatorname{diag}(\alpha,-\alpha/2+d,-\alpha/2-d),
\qquad W=w(x)\partial_x.
\]

Define `u=w'` and

\[
v=\frac32\alpha+2u.
\]

Then the total conformal trace-free tensor is preregistered as

\[
\bar A_{TT}+\bar L W
=\operatorname{diag}\left(\frac23v,-\frac13v+d,-\frac13v-d\right),
\]

and the vector equation is to reduce to

\[
\boxed{v'=\psi^6\tau'.}
\]

The constant-ratio separability class is

\[
v=k\psi^6\tau,
\]

where `k` is free and classified rather than chosen for physical merit. This separability class is
a diagnostic ansatz, not a UDT law.

## Preregistered vector branching

For nonconstant positive `psi` and sign-definite `tau`, test whether the vector equation gives

\[
(k-1)\tau'+6k\frac{\psi'}{\psi}\tau=0.
\]

For `k != 1`, preregister

\[
\tau=C\psi^n,\qquad k=\frac{n}{n+6},\qquad n\ne-6,
\]

with `C != 0`. Periodicity is to force

\[
\alpha=\frac23\langle v\rangle,
\qquad
w'=\frac12\left(v-\langle v\rangle\right),
\]

modulo the additive translation kernel in `w`.

The G317 direct physical form corresponds to `k=1`. Test the preregistered obstruction

\[
6\psi^5\psi'\tau=0.
\]

Thus, within the sign-definite registered family, nonconstant `psi` should reject the unchanged
G317 form rather than silently carrying it forward.

## Preregistered scalar classification

For the power branch, preregister the physical data

\[
\gamma_{ij}=\psi^4\delta_{ij},
\]

\[
K^i{}_j=\operatorname{diag}
\left(
\frac{n+2}{n+6}\tau,
\frac{2}{n+6}\tau+q,
\frac{2}{n+6}\tau-q
\right),
\qquad q=d\psi^{-6},
\qquad \tau=C\psi^n.
\]

Test whether both conformal and direct physical Hamiltonian constraints reduce exactly to

\[
\boxed{
-8\psi''
+\frac{8(n+3)}{(n+6)^2}C^2\psi^{2n+5}
-2d^2\psi^{-7}
-2\Lambda\psi^5=0.
}
\]

The direct momentum residual must reduce to

\[
(a-1)\tau'+(6a-2)\frac{\psi'}{\psi}\tau,
\qquad a=\frac{n+2}{n+6},
\]

and vanish from `tau=C psi^n`. This replay is required to prevent a conformal-only circular pass.

## Preregistered obstruction classes

Integrating the scalar equation over the periodic coordinate removes `psi''`. For `C != 0`, test:

- `n < -3`, `n != -6`, and `Lambda >= 0`: no positive nonconstant periodic solution in the
  registered power branch;
- `n = -3` and `Lambda >= 0`: no positive nonconstant periodic solution; if `d=Lambda=0`, periodicity
  reduces `psi` to a constant;
- `n = 0`: a CMC boundary, not part of the non-CMC landing;
- `n > -3`: the integral sign obstruction is absent, but existence is not automatic.

These are branch-scoped obstructions, never a general non-CMC no-go.

## Preregistered positive periodic witness class

For `n=-2`, preregister

\[
\tau=C\psi^{-2},\qquad
K^i{}_j=\operatorname{diag}
\left(0,\frac12\tau+q,\frac12\tau-q\right),
\qquad q=d\psi^{-6},
\]

and

\[
\psi''=\frac{C^2}{16}\psi-\frac{d^2}{4}\psi^{-7}-\frac{\Lambda}{4}\psi^5.
\]

The preregistered first integral is

\[
I=-4(\psi')^2+\frac{C^2}{4}\psi^2
+\frac{d^2}{3}\psi^{-6}-\frac{\Lambda}{3}\psi^6.
\]

At a positive equilibrium `p`, test

\[
C^2p^8-4d^2-4\Lambda p^{12}=0,
\]

and the strict center condition

\[
\omega^2=\frac{C^2}{4}-3d^2p^{-8}>0.
\]

If `C^2 p^8 > 12 d^2`, set

\[
\Lambda=\frac{C^2p^8-4d^2}{4p^{12}}>0.
\]

The standard autonomous-ODE phase portrait should then give a local family of positive nonconstant
periodic oscillations around `p`. For any natural period `P`, the exact rescaling

\[
\psi(x)=\Psi(\kappa x),\quad
C=\kappa C_0,\quad d=\kappa d_0,\quad
\Lambda=\kappa^2\Lambda_0,quad \kappa=P/(2\pi)
\]

must place a member on the marked `2 pi` torus. This is coordinate/parameter construction, not a
calibrated physical scale.

## Preregistered tide diagnostic

For the `n=-2` branch, compute the full spatial Ricci tensor and initial electric/magnetic Weyl
data directly. With `H=psi'/psi`, test

\[
E^i{}_j=\operatorname{diag}(E_x,-E_x/2,-E_x/2),
\]

\[
E_x=4\psi^{-6}(\psi')^2-\frac{C^2}{4}\psi^{-4}
+d^2\psi^{-12}+\frac{\Lambda}{3},
\]

and the only independent orthonormal magnetic component

\[
B_{\hat y\hat z}=B_{\hat z\hat y}=-4d\,H\,\psi^{-8}.
\]

Also test

\[
E_x=-I\psi^{-6}+\frac43d^2\psi^{-12}.
\]

For `d=0`, small periodic center orbits below the zero-energy barrier have `I>0`, so their electric
tide is nonzero. For `d!=0`, any nonconstant orbit has nonzero magnetic tide wherever `psi'!=0`.
The maximum claim is therefore only that the registered periodic witness family is tidal; it does
not exclude zero-tide data in omitted nonseparable sectors.

## Certification and falsification contract

Production must use exact standard-library arithmetic for all algebraic identities and may use the
standard phase portrait only as a declared mathematical method. An implementation-distinct verifier
must reconstruct Christoffel, spatial Ricci, both physical constraints, and Weyl components without
importing production functions or reading production output. Hostile checks must catch at least:

- wrong `4/3`, `2/3`, `psi^6`, or mean-subtraction factors;
- silently retaining G317's `k=1` form for nonconstant `psi`;
- wrong `k=n/(n+6)` or physical eigenvalue ratios;
- wrong power or sign in the scalar ODE;
- a conformal-only pass that violates a direct physical constraint;
- false existence in the integrated `n<=-3`, `Lambda>=0` obstruction class;
- wrong equilibrium or center condition in the `n=-2` class;
- treating period rescaling as a measured scale;
- omission of spatial-Ricci terms from electric Weyl;
- wrong magnetic-Weyl conformal factor or failure to symmetrize it;
- calling coordinate variation tide without a nonzero Weyl invariant;
- calling this one separable tile a full non-CMC theorem;
- selecting a profile, topology, scalar, scale, history, matter/mass law, or physical `X_max`;
- changing the metric, reciprocal kernel, angular cancellation, or observational interface.

Run the current premise verifier and full repository suite before banking. Fresh external
adversarial review is required before an externally accepted grade.

## Preregistered landing classes

Exactly one maximum landing may be used:

1. `NONCONSTANT_PSI_FORCES_A_POWER_LAW_NONCMC_INTERLOCK__G317_DIRECT_FORM_IS_OBSTRUCTED__POSITIVE_PERIODIC_TIDAL_BRANCH_EXISTS__NO_PHYSICAL_DATA_SELECTION`
2. `NONCONSTANT_PSI_POWER_INTERLOCK_EXISTS_BUT_REGISTERED_PERIODIC_BRANCH_IS_OBSTRUCTED__NO_PHYSICAL_DATA_SELECTION`
3. `REGISTERED_NONCONSTANT_PSI_NONCMC_SEPARABILITY_FAMILY_HAS_NO_LAWFUL_DATA`
4. `CLASSIFICATION_INCONCLUSIVE_WITHIN_REGISTERED_SCOPE`

No landing changes the metric, reciprocal kernel, angular cancellation, observational interface,
or premise grades.
