# G254 exact derivation — complete time-live solver closure audit

Date: 2026-08-24

## 1. Landing

```text
NO_OWNED_TIMELIVE_RESIDUAL
__CURRENT_NATIVE_RELATIONS_EVALUATE_SUPPLIED_TIME_LIVE_METRICS
__THEY_DO_NOT_DEFINE_AN_AMBIENT_METRIC_ODE_OR_PDE
__REDUCED_AND_GPU_HISTORY_SOLVES_ARE_NOT_YET_MATHEMATICALLY_DEFINED
```

This is a frozen-source equation-ownership result. It is not a no-go for UDT, a demand for a GR
equation, or a proof that a future global relation law cannot close the history.

## 2. Complete metric arena versus an evolution system

A local Lorentz metric has ten independent component functions. Equivalently, an invertible
coframe has sixteen functions and local Lorentz frame gauge removes six. Coordinate covariance
accounts for four further function-valued equivalences, leaving six local metric-configuration
functions after coordinate gauge. This is not a count of propagating modes: such a count requires
equations, constraints, and a principal symbol that the present corpus does not own.

The conditional complete coframe is therefore a lawful configuration arena. For a supplied metric
coframe `E` and supplied rank-two germ `J`,

\[
h=J^T E^T\eta E J
\]

is exact. Along a supplied parameter,

\[
\dot h=\dot J^TgJ+J^T\dot gJ+J^Tg\dot J
\]

is also exact. These equations retain every active sector, but they compute the pair response from
the supplied functions `E` and `J`; they do not compute `dot E` or `dot g`.

## 3. Why completed reciprocity does not become an ambient equation

For one regular pair pullback,

\[
h_\sigma=-T^2(dy^0+\beta d\sigma)^2+L_\sigma^2d\sigma^2.
\]

The G176 working clarification uniquely solves for the positive physical ruler calibration,

\[
m=T L_\sigma=\sqrt{-\det h_\sigma},
\qquad
\Phi=-\frac12\log(-h_{00}).
\]

The unknown solved here is the auxiliary-to-physical ruler density `m` on the supplied pair. For
every regular `h`, exactly one positive `m` exists. The equation therefore normalizes the query; it
does not reject a regular ambient metric or supply a time derivative for one.

Endpoint reversal and composition similarly reduce compatible edge depths to differences of a
supplied vertex potential. Every smooth potential satisfies those relations. They constrain the
typing of values, not the function that Nature realizes.

## 4. Connection, curvature, and propagation are evaluators

The remaining candidate equations separate cleanly:

| Relation | Exact role | Ambient-history restriction? |
|---|---|---:|
| Levi-Civita metricity and zero torsion | determine the connection from a supplied metric | no |
| Cartan structure equations | define connection and curvature in a coframe | no |
| Bianchi identities and Ricci commutators | identities/compatibility of metric curvature jets | no |
| null geodesic equation | propagates a supplied null germ in a supplied metric | no |
| Jacobi equation | propagates screen separation in supplied curvature | no |
| full phase/holonomy composition | composes supplied path-labelled transport | no |
| rank-complete pair network | reconstructs supplied metric values | no |

G231 makes the key distinction exact: Cartan data can integrate compatible supplied curvature
values, but the compatibility identities do not generate those values. G235 proves the analogous
network statement: a rank-complete completed relation network can reconstruct the metric while
accepting invariantly distinct metric histories.

## 5. Exact arbitrary-history counterfamily

Take the smooth time-live Lorentz family

\[
g_b=-dt^2+e^{2bt^2}(dx^2+dy^2+dz^2),
\qquad b\in\mathbb R.
\]

It lies inside the registered G211 common/relative scalar arena with `Omega=0`, `q=bt^2`, zero
shift, and a flat determinant-normalized spatial reference. It is a diagnostic family, not a
physical ansatz.

For the supplied clock--ruler germ `J=(partial_t,partial_x)`,

\[
h_b=\operatorname{diag}(-1,e^{2bt^2}),
\qquad
m_b=e^{bt^2}.
\]

After completed-pair normalization,

\[
(h_b)_s=\operatorname{diag}(-1,1),
\qquad
\Phi_b=0
\]

for every value of `b`. Thus every member satisfies the same completed-pair algebra on this germ.
The tape density and the other metric/Jacobi channels remain free to hear `b`; the result does not
claim that the complete network is blind to the history.

A direct four-dimensional Christoffel--Ricci contraction gives

\[
\mathcal R_b(t)=12b(1+4bt^2),
\qquad
\mathcal R_b(0)=12b.
\]

Therefore `b=0` and `b=7` have anchor curvatures `0` and `84`. They are invariantly distinct smooth
time-live histories, not coordinate copies, while both admit all the registered geometric
evaluators and completed-pair normalization. The standard-library independent implementation
recomputes the Ricci contraction at the anchor using exact fractions for 65 values of `b` and
obtains `R(0)=12b` in every case.

This counterfamily is sufficient to show that the current identities do not determine the
relative scalar history even inside a two-function subarena. Activating more screen, mixing,
shift, and determinant-one spatial functions enlarges the arena; it does not create a missing
equation.

## 6. Equation census

The preregistered contract contains thirteen candidate rows:

- eleven current relations or forbidden imports that do not count as ambient history equations;
- two legitimate future equation *types*: an independently owned invariant condition
  `C[g]=0`, or a genuinely global relation condition `G[g,R]=0`.

The frozen sixteen-source corpus owns neither type. Consequently,

```text
owned active ambient evolution equations = 0
```

This zero does not mean “zero physics.” It means none of the exact pair, transport, curvature, or
network equations has the mathematical type needed to determine an ambient metric history.

## 7. Why stages 2 and 3 stop

An ODE/PDE solve requires a residual whose zero set defines candidate histories, plus its unknowns,
constraints, gauge, and freely specifiable data. The present corpus supplies no such ambient
residual. Choosing a spherical ansatz would leave arbitrary functions; integrating geodesic or
Jacobi equations would evaluate that chosen history rather than solve for it.

A GPU implementation would therefore accelerate an evaluator or an imported residual. It could
not be certified as a native UDT history solver. Under the preregistered three-stage gate:

```text
stage 1: completed — no owned residual
stage 2: gated, not started
stage 3: gated, not started
```

## 8. What would reopen the solve

Either of the following would define a new, testable gate:

1. an independently motivated diffeomorphism-natural nonidentity condition `C[g]=0` that rejects
   at least one regular counterhistory; or
2. a genuinely global completed-relation law `G[g,R]=0` that constrains metric values rather than
   merely reconstructing or composing them.

Observational anchors can calibrate constants after such a law reduces the history to a finite
family. Using observations to specify an unrestricted function would instead be an empirical
reconstruction, which is legitimate only if labelled as such and is not the native solve audited
here.

## 9. Maximum conclusion

G254 establishes, in the exact frozen sixteen-source universe, that the existing native UDT corpus
does not yet define a complete metric-history ODE or PDE. It does not establish that an equation is
ontologically required, exclude an anchor-closed finite family after a future derivation, or choose
between a local invariant condition and a global relation law.
