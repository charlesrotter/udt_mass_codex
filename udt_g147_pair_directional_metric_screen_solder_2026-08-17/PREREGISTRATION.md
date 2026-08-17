# G147 preregistration — pair-directional / metric-screen solder

Date: 2026-08-17

## Whole question and exact bounded regime

On one supplied regular, time-oriented, calibrated observer-pair immersion

\[
F:\Sigma^2\longrightarrow (M^4,g),
\]

does the metric and the query-owned clock/ruler flag canonically identify the tangent screen of
nonzero bounded relational position with the pair-relative metric screen?

At a marked pair point let

\[
J_0=F_*\partial_0,\qquad J_1=F_*\partial_1,
\]

where `J_0` is the supplied future timelike clock tangent and the ordered transverse coordinate
supplies the ruler orientation. On the regular Lorentzian stratum define

\[
T^2=-g(J_0,J_0),\qquad
\beta={g(J_0,J_1)\over g(J_0,J_0)},
\]

\[
u={J_0\over T},\qquad
r=J_1-\beta J_0,\qquad
L^2=g(r,r),\qquad n={r\over L}.
\]

Let

\[
E_{\rm pair}=\operatorname{span}(J_0,J_1),\qquad
H_{\rm pair}=E_{\rm pair}^{\perp},\qquad
R_u=u^{\perp}.
\]

For the already adopted bounded scalar position `rho=tanh(phi_pair)`, with `rho != 0`, form the
query-relative vector `xi=rho n` in `R_u`. Test whether

\[
T_{\xi}S^2_{|\rho|}(R_u)=H_{\rm pair}
\]

as metric subspaces, so that the proposed solder is the identity inclusion on one already-common
rank-two carrier rather than new free data.

## Method classification

`METRIC_LED__CONDITIONAL_ON_SUPPLIED_QUERY_FLAG`.

No ball-composition control, Lorentz-rapidity identification, dynamics, action, source, fit,
bootstrap rule, observational profile, or global selector is used.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| Lorentz metric `g` | `SUPPLIED_CONDITIONAL` | Ambient bilinear form |
| Regular timelike immersion `F` | `SUPPLIED_QUERY` | Owns `E_pair` |
| Future clock tangent `J_0` and oriented transverse tangent `J_1` | `SUPPLIED_QUERY_CALIBRATION` | Own the pair flag |
| `H_pair=E_pair^perp` positive rank two | `DERIVED_CONDITIONAL` | Pair-first result to be replayed |
| `rho=tanh(phi_pair)` | `CHOSE / WORKING` then `DERIVED_CONDITIONAL` | Adopted bounded position coordinate on the supplied pair |
| `xi=rho n` | `CONDITIONAL_ASSEMBLY_TO_TEST` | Places scalar position along the query ruler in the observer rest space |
| `c_E` | `OBSERVED`, inactive algebraically | Clock/ruler unit calibration |
| Witness `B,Q,S,Y,Z,rho` below | `FREE_AND_EXPLORED_EXACT_CONTROL` | Nonphysical full-coframe liveness check |

No value is `pinned-by-HABIT`.

The exact registered full-coframe witness is

```text
B=[[2,1/2],[0,3]]
Q=[[1,1/3],[0,2]]
S=[[1/5,-1/7],[1/4,1/6]]
Y=I_2
Z=[[1/10,-1/8],[-1/12,1/9]]
rho=2/5
```

with

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},\qquad
g=E^T\operatorname{diag}(-1,1,1,1)E,\qquad
J=\binom{Y}{Z}.
\]

This witness is retained only if its induced pair metric is Lorentzian and `J_0` timelike. Failure
of those registered gates is a preregistered invalid-control result, not permission to tune it.

## Exact tests

1. Derive `g(u,u)=-1`, `g(n,n)=1`, and `g(u,n)=0` from the calibrated pair metric.
2. Derive `span(u,n)=E_pair`.
3. Prove by constraint equality that
   `T_xi S^2_|rho|(R_u)={w:g(w,u)=g(w,n)=0}=H_pair` for `rho != 0`.
4. Compare the two exact orthogonal projectors

   \[
   P_H=I-J(J^TgJ)^{-1}J^Tg
   \]

   and

   \[
   P_{u,n}=I+u(u^Tg)-n(n^Tg).
   \]

5. Verify rank two, idempotence, metric self-adjointness, and positive restriction.
6. Verify ambient basis covariance and calibrated pair-domain covariance. A reparameterization that
   changes the physical clock/ruler flag is classified as a different query, not gauge.
7. Replay the registered complete-coframe witness exactly with all `B,Q,S,Y,Z` blocks active.
8. Independently replay the load-bearing projector and subspace identities without importing the
   production implementation.

## Preregistered landings

- `CANONICAL_LOCAL_SOLDER_DERIVED__CROSS_QUERY_CARRY_OPEN` if the equality and covariance tests pass.
- `QUERY_RELATIVE_NONUNIQUE_SOLDER` if the same supplied calibrated flag permits inequivalent
  metric-natural isometric identifications not related by screen-frame gauge.
- `TYPE_FAILURE` if the directional sphere and pair screen do not share a well-typed carrier.
- `INVALID_REGISTERED_CONTROL` if the exact complete-coframe witness misses its regularity gate.

## Certification and falsification contract

The candidate theorem fails if any registered exact identity, covariance test, regularity gate, or
independent replay fails. A local equality of subspaces is not enough to claim an inter-query carry
or a positional-gyration / metric-transport equality.

Maximum conclusion if successful:

> On a supplied regular calibrated pair query at nonzero relational position, the query-relative
> directional sphere tangent and the metric pair screen are the same positive rank-two subspace.
> Their local solder is therefore canonical and contains no additional coefficient. This does not
> identify screens belonging to different pair queries, select a multidirectional ball law, derive
> complete observer-arrow reversal, or determine history, `X_max`, proper length, dynamics, or
> downstream physics.

## Omitted sectors and limits

- coincidence / `rho=0`, where position alone has no direction;
- null or degenerate pair surfaces;
- singular, cut, focal, branch-changing, and non-Hausdorff strata;
- cross-query and middle-observer screen carry;
- comparison of any positional angular defect with `U_gamma`;
- physical query-family selection, metric history, numerical `X_max`, proper/areal/signal distance;
- light, EM, observations, action, source, bootstrap, matter, mass, and global completion.
