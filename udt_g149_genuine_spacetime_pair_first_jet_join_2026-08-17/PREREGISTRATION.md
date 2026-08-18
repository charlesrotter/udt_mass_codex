# G149 preregistration — genuine spacetime complete-pair first-jet join

Date: 2026-08-17

## Question

Does the G148 relation-first identity remain exact when every quantity is computed from one
explicit smooth four-coordinate Lorentzian metric and one smooth calibrated pair immersion, rather
than from an arbitrary one-parameter matrix family?

The calculation will construct the Levi-Civita connection of the same complete coframe that supplies
the pair pullback, derive `dot(phi_pair)`, `a_n`, and `Omega` from that geometry, and compare a direct
covariant derivative of

\[
\xi=X_{\max}\tanh(\phi_{\rm pair})n
\]

with the G148 decomposition. This is a local kinematic join on a supplied history. It does not select
that history as physical.

## Exact bounded regime

- one smooth complete coframe `E(x)` assembled from coordinate-affine `B(x),Q(x),S(x)` on a local
  four-coordinate patch, evaluated at one marked point;
- one quadratic calibrated pair immersion `F(tau,sigma)` through that point;
- regular time-oriented pair data: `h00<0`, `det(h)<0`, finite real `phi_pair`;
- all complete-coframe blocks `B,Q,S` and pair first-jet blocks `Y,Z` retained;
- exact local first derivatives only; no field equation, action, source, boundary, global completion,
  observational fit, or time-evolution solve;
- null, degenerate, cut, focal, singular, and global strata are outside scope.

## Premise and choice ledger

| Item | Status | Ownership |
|---|---|---|
| complete coframe `E=[[B,0],[QS,Q]]` and `g=E^T eta E` | `DERIVED` evaluator on supplied blocks | frozen sources |
| calibrated pair pullback `h=F^*g` | `DERIVED` from supplied `g,F` | frozen sources |
| terminal `phi_pair=(1/4)log((-det h)/h00^2)` | `DERIVED` on regular pair | frozen sources |
| `xi=X_max tanh(phi_pair)n` | `CHOSE / WORKING_RELATION_FIRST_REPRESENTATION` | G148; not spacetime displacement |
| Levi-Civita connection | `DERIVED` uniquely from supplied metric | no GR field equations |
| affine `B,Q,S`, quadratic immersion, rational entries | `CHOSE_NUMERICAL_WITNESS` | frozen before outcome; not fitted |
| `X_max` | `WORKING_FOUNDATIONAL_FRAME`, symbolic | value and realization `OPEN` |
| physical history, dynamics, bootstrap, observations | omitted / `OPEN` | not inferred |

All coordinate slopes and pair second jets are free-and-explored witness data. No parameter is
pinned by habit or by a desired outcome.

## Exact objects and identities

At the marked point let

\[
J_0=F_*\partial_\tau,\qquad J_1=F_*\partial_\sigma,\qquad
h_{ij}=g(J_i,J_j).
\]

Define

\[
T=\sqrt{-h_{00}},\quad u=J_0/T,\quad
\beta=h_{01}/h_{00},\quad r=J_1-\beta J_0,\quad
L=\sqrt{g(r,r)},\quad n=r/L,
\]

and `P_H=I+u tensor u_flat-n tensor n_flat`. With

\[
a_n=g(\nabla_u u,n),\qquad \Omega=P_H\nabla_u n,
\]

the direct Levi-Civita calculation must satisfy

\[
\nabla_u\xi
=X_{\max}\operatorname{sech}^2\phi\,\dot\phi\,n
+X_{\max}\tanh\phi\,\Omega
+X_{\max}\tanh\phi\,a_n u.
\]

It must also verify

\[
\dot\phi
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}},
\]

with every derivative taken along the actual normalized pair clock `u`, not along an unrelated
matrix-family parameter.

## Preregistered certification and falsification gates

The bounded landing requires:

1. exact pair regularity and exact orthonormality of `u,n`;
2. torsion symmetry and metric compatibility for the computed Levi-Civita connection;
3. exact agreement of direct and trace-formula `dot(phi_pair)`;
4. exact vanishing of the four-vector residual in the G148 decomposition;
5. exact screen orthogonality `g(Omega,u)=g(Omega,n)=0`;
6. exact agreement of direct and independently reconstructed `a_n` and `Omega`;
7. each registered spacetime-gradient family `B,Q,S` and pair-clock-direction first-jet family
   `Y,Z`, when removed alone, changes at least one of `dot(phi_pair)`, `a_n`, or `Omega` relative to
   the all-live witness; no `sigma`-direction liveness claim is made;
8. an independent implementation that does not import the production module;
9. catch proofs that reject a wrong `a_n` sign, omission of `Omega`, and substitution of the G148
   algebraic `lambda` derivative for the spacetime clock derivative.

The experiment is not invalid merely because an individual amplitude happens to vanish. A failed
liveness gate narrows only this registered witness and cannot prove a sector physically absent.

## Maximum conclusion

At most:

```text
EXPLICIT_SMOOTH_COMPLETE_SPACETIME_QUERY_WITNESS__
PAIR_CLOCK_DERIVED_DOTPHI__LEVI_CIVITA_DERIVED_AN_OMEGA__
G148_COVARIANT_IDENTITY_EXACTLY_REALIZED__
ALL_BQS_SPACETIME_GRADIENT_FAMILIES_AND_PAIR_CLOCK_DIRECTION_YZ_FIRST_JETS_LIVE_IN_THE_REGISTERED_WITNESS__
PHYSICAL_HISTORY_DYNAMICS_REGIME_AMPLITUDES_AND_GLOBAL_COMPLETION_OPEN
```
