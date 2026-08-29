# G298 exact derivation — the causal family owns a richer relation than one pair plane

Date: 2026-08-29

## Landing

```text
MULTIPLE_INEQUIVALENT_NATURAL_PAIR_ONE_JET_PROJECTIONS_SURVIVE_FROM_THE_DERIVED_COMPLETE_RELATION_STATE
__NO_UNIQUE_TRANSFER_TO_G2_IS_OWNED
```

Status: `EXTERNALLY_REVIEWED_DERIVED_WITH_CAVEATS`; fresh review found no algebra error, the
projection/completeness regrade was applied, and its repair chain is externally closed.

G298 derives a positive construction and a sharper type obstruction. Every supplied regular
directed null leg naturally generates a complete path-labelled relation state. That state admits
at least two natural, gauge-inequivalent regular projections to calibrated rank-two pair one-jets,
and both projections return the same reciprocal clock depth under W1. The target-local projection
forgets transported-source/path carry and is not an equally complete relation state. Current
premises nevertheless do not select a unique projection of the richer state into `G_2(g)`.

## 1. The metric-owned directed-leg relation state

Let `gamma:X->Y` be one supplied regular future-directed affine null leg, with metric-unit future
clocks `U_X,U_Y` and tangent `k`. Define endpoint frequencies

\[
\omega_X=-g(k_X,U_X)>0,
\qquad
\omega_Y=-g(k_Y,U_Y)>0,
\]

and the exact G220 comparison rate

\[
\boxed{r=\frac{\omega_X}{\omega_Y}
=\frac{d\tau_Y}{d\tau_X}>0},
\qquad
\boxed{\delta=-\log r}.
\]

The source null direction has the unique unit spatial decomposition

\[
K_X=\frac{k_X}{\omega_X}=U_X+n_X,
\]

where

\[
\boxed{g(U_X,n_X)=0,
\qquad g(n_X,n_X)=1.}
\]

Levi-Civita transport on the supplied route gives

\[
\widetilde U_X=P_\gamma U_X,
\qquad
\widetilde n_X=P_\gamma n_X.
\]

These objects, together with the route label and its directional-delay/Jacobi carry, form a natural
branch-indexed directed-leg relation state. Nothing here uses reciprocal depth as an input; `delta`
is read only after the frequency ratio is independently derived.

## 2. First natural pair one-jet: transported-source ruler

Source-clock normalization makes the target comparison-clock tangent `r U_Y`. Carrying the source
ruler along the same route gives the candidate

\[
\boxed{J_T=(rU_Y,\widetilde n_X).}
\]

Write the G269 endpoint decomposition

\[
U_Y=\Gamma\widetilde U_X+a\widetilde n_X+W,
\qquad
W\perp\operatorname{span}(\widetilde U_X,\widetilde n_X).
\]

Then

\[
a=\Gamma-r^{-1},
\qquad
\Gamma=\frac12(r+r^{-1}+r\lVert W\rVert^2).
\]

The full columns retain the ambient screen component `W` before pullback. Their Gram matrix is

\[
\boxed{
h_T=J_T^TgJ_T=
\begin{pmatrix}
-r^2 & ra\\
ra & 1
\end{pmatrix},
\qquad
\det h_T=-r^2(1+a^2)<0.
}
\]

Thus `J_T` is always rank two on the stated regular stratum. Applying W1 only now gives

\[
T^2=-h_{00}=r^2,
\qquad
\boxed{\Phi=-\log T=-\log r=\delta}.
\]

This is a valid `DERIVED_CONDITIONAL` transfer to one calibrated pair one-jet.

## 3. Second natural pair one-jet: target-local null ruler

The same causal leg independently supplies the target-local unit spatial null direction

\[
\boxed{n_Y=\frac{k_Y}{\omega_Y}-U_Y},
\qquad
g(U_Y,n_Y)=0,
\qquad
g(n_Y,n_Y)=1.
\]

It therefore supplies a second regular candidate

\[
\boxed{J_L=(rU_Y,n_Y)},
\]

with

\[
\boxed{
h_L=J_L^TgJ_L=
\begin{pmatrix}
-r^2&0\\
0&1
\end{pmatrix},
\qquad
\det h_L=-r^2<0,
\qquad
\Phi_L=-\log r.
}
\]

This is not the forbidden shortcut `J=(U_Y,n_Y)`: its clock column carries the independently
derived comparison rate `r`. Its full ambient columns vary with the active screen state even though
their Gram matrix is diagonal.

Both projections are diffeomorphism-natural, independent of proper-clock origins, invariant under
positive affine rescaling of `k`, compatible with constant metric homothety, and regular inputs to
the same W1 pair evaluator. This algebraic fact does not make `J_L` an equally complete carrier of
the path-labelled relation state.

## 4. Active screen proves that the two planes are not gauge-equivalent

Use an orthonormal target basis

\[
\widetilde U_X=e_0,
\qquad
\widetilde n_X=e_1,
\qquad
W=w e_2,
\]

with `w` nonzero. Then

\[
U_Y=\Gamma e_0+a e_1+w e_2,
\]

and parallel transport of the normalized null tangent gives

\[
\frac{k_Y}{\omega_Y}=r(e_0+e_1).
\]

Hence

\[
n_Y=(r-\Gamma)e_0+(r-a)e_1-w e_2.
\]

The determinant of the three vectors `(rU_Y,e_1,n_Y)` in this `1+2` subspace is

\[
\boxed{\det(rU_Y,e_1,n_Y)=-r^2w.}
\]

For every `r>0` and `w` nonzero this has rank three. Therefore

\[
\boxed{
\operatorname{span}(rU_Y,\widetilde n_X)
\ne
\operatorname{span}(rU_Y,n_Y).
}
\]

No pair-domain basis change can relate the two one-jets because such a change preserves their
two-plane image. They coincide only on the transported-planar stratum `W=0`.

The target-local construction does not retain the transported source ruler or its path carry inside
its two-plane. It is therefore a natural regular projection, not an equally complete physical pair
germ in the W5 sense. The transported-source projection preserves that source-frame carry but does
not contain the target-local ruler inside its two-plane. The complete path-labelled causal state
contains both, as well as the route morphism and higher directional-delay carry. W5 privileges
retaining that richer state, but neither W5 nor G269 proves a unique projection from it to one
rank-two germ. Calling either projection *the* physical pair germ requires an additional
projection/ownership statement not supplied by W1, W5, G269, or G297.

## 5. Corrected factorization

G297 proposed a direct partial map

\[
C_g:\mathfrak D_g/\mathcal G_D
\dashrightarrow
\mathfrak G_2(g)/\mathcal G_F.
\]

G298 sharpens it to

\[
\boxed{
\mathfrak D_g/\mathcal G_D
\longrightarrow
\mathfrak R_g/\mathcal G_R
\mathrel{\substack{\displaystyle\dashrightarrow\\[-2pt]
\scriptstyle\pi_T,\,\pi_L}}
\mathfrak G_2(g)/\mathcal G_F,
}
\]

where `mathfrak R_g` retains the ordered route, endpoint clocks, null directions, clock ratio,
parallel-transported source plane, target-local null plane, and directional-delay/higher carry.
The first arrow is derived conditional on the supplied metric, observers, and routes. At least two
natural regular projections `pi_T` and `pi_L` survive. They are not equally complete: `pi_L`
forgets transported-source/path carry. Current premises still do not own a unique transfer to
`G_2(g)`.

The calibrated target quotient permits pair-domain changes that preserve the comparison-clock
line and pair-plane image. Such reparameterizations cannot identify the active-screen witness
because its two image planes are distinct.

## 6. Reflection, reversal, caustics, and multiple routes

- **Reflection:** incoming and outgoing legs produce separate relation states and separate one-jets.
  The causal corner supplies no unique smooth two-surface germ, so G298 does not add one.
- **Physical return:** the later future-null return is its own directed leg. It is not the
  mathematical inverse of the outgoing leg.
- **Mathematical reversal:** inverse transport and reciprocal rate are well-defined on the reversed
  path when that object is admitted, but do not populate a future return route.
- **Caustics:** the theorem is restricted to declared regular legs and regular endpoint one-jets.
  Multiple branches at a cut or caustic remain separate; no route is discarded.
- **Hard branch control:** on a flat cylinder, the two antipodal null routes have rulers `+e_1` and
  `-e_1`. The isometry `e_1 -> -e_1` exchanges them. The lawful output is the invariant two-member
  set, not either preferred route.

## 7. What is and is not closed

| Object | G298 status |
| --- | --- |
| branch-indexed directed causal relation state | `DERIVED_CONDITIONAL` on supplied metric/clocks/routes |
| transported-source pair one-jet `J_T` | `DERIVED_CONDITIONAL` natural projection |
| target-local pair one-jet `J_L` | `DERIVED_CONDITIONAL` natural regular projection that forgets transported-source/path carry |
| W1 depth on either projection | `DERIVED_CONDITIONAL`; exactly `-log r` |
| unique causal-family to pair-one-jet transfer | `NOT_DERIVED`; active-screen counterexample |
| reflection smoothing or unique higher pair surface | `OPEN` |
| route/observer/event population | `OPEN` |
| metric history, residual dynamics, scale, observations, `X_max` | `OPEN` |

This does not weaken the native kernel. It identifies that its complete input should not be reduced
to one arbitrary two-plane before the full directed relation state has been typed. A future owner
clarification could select a projection, but G298 does not adopt one.

## Evidence

- preregistered and pushed at `c7128f21` before production outcome;
- ten frozen source hashes;
- 1,260 exact rational production cases and 17,660 assertions;
- independent algebraic-witness implementation: 20,000 exact rational cases and 358,543 assertions;
- exact active-screen rank-three separator;
- flat-cylinder isometry-exchanged branch control;
- seven hostile semantic catches;
- no observation, fit, action, source, matter, scale, `X_max`, or protected input.

Fresh zero-context adversarial review found no core algebra defect and required the exact
projection/completeness repair recorded in `EXTERNAL_REVIEW_GPT54.md`. R2–R4 passed the first
repair-only follow-up; the exact R1 lay-language completion passed the final follow-up. The repaired
bounded landing is externally closed.
