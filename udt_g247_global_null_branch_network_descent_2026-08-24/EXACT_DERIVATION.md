# G247 exact derivation — global null-branch network descent

Date: 2026-08-24

## Bounded landing

```text
REGULAR_DIRECTION_ROUTE_LABELLED_NULL_BRANCH_ATLAS_DESCENDS_GLOBALLY
__DIRECT_FUTURE_NULL_LINKS_FORM_A_QUIVER_NOT_A_CATEGORY_OR_GROUPOID
__FREE_MATCHED_NULL_CHAIN_CATEGORY_CARRIES_ADDITIVE_DEPTH_AND_PATH_LABELLED_PHASE
__CAUSTIC_BRANCH_AGGREGATION_GLOBAL_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN
```

Status after fresh external review:
`DERIVED_CONDITIONAL__EXTERNALLY_VERIFIED__NO_REPAIRS_REQUIRED`.

The metric history, proper-clock observer worldline germs, and future-null query type are supplied.
The result classifies the complete metric-generated branch family; it selects no route, observer
population, or history.

## 1. Global branch space from the null geodesic flow

Let `(M,g)` be a smooth time-oriented Lorentzian four-manifold and let

\[
z_i:I_i\longrightarrow M
\]

be a labelled family of future-timelike proper-clock observers. At the event
`e=(i,tau)` write `U_e=dot z_i(tau)` and define the observer sky

\[
\mathbb S_e^2=\{n\in U_e^\perp:g(n,n)=1\}.
\]

G245 gives the normalized future-null initial tangent

\[
k(e,n)=U_e+n,
\qquad -g(U_e,k)=1.
\]

Let `Phi_s` denote the maximal null geodesic flow. Its maximal domain

\[
\mathcal D\subset\{(e,n,s):e\in\mathcal E, n\in\mathbb S_e^2, s>0\}
\]

is open and the endpoint evaluation

\[
\operatorname{ev}(e,n,s)=\pi\Phi_s(k(e,n))
\]

is smooth. A direct future-null incidence is a tuple

\[
\boxed{q=(e_A,n,s,e_B)}
\]

such that `ev(e_A,n,s)=e_B`. The initial data `(e_A,n)` and maximal-flow parameter `s` are the route
label. Uniqueness of the geodesic initial-value problem makes this label global up to the declared
affine/chart equivalences; equal spacetime endpoints do not erase distinct initial directions or
windings.

For fixed observer labels `A,B`, form the fiber product of

\[
(a,n,s)\longmapsto\operatorname{ev}(z_A(a),n,s)
\]

with `b -> z_B(b)`. Wherever this fiber product is transverse, its components are the regular
incidence branches. In a convex normal neighborhood, eliminating `(n,s)` reduces exactly to the
G246 world-function chart

\[
\sigma(z_A(a),z_B(b))=0,
\qquad b=f_{AB}(a).
\]

Thus G246 charts are local charts on the regular part of one global direction- and route-labelled
incidence space; a global Synge world function is not required.

## 2. Exact overlap descent

Suppose two regular charts describe the same labelled geodesic-flow tuple. They have the same
initial event, normalized initial direction, and maximal-flow solution. Geodesic ODE uniqueness
therefore identifies their spacetime curve. Ordinary uniqueness in the implicit-function theorem
then identifies their target-clock correspondence on the connected chart overlap.

Consequently, the proper-clock derivative

\[
r_q=\frac{d\tau_B}{d\tau_A}
=\frac{-g(K_A,U_A)}{-g(K_B,U_B)}>0
\]

is chart-independent. On the associated null ribbon, G223's affine-null transformations give

\[
a_j=\frac{a_i}{f'\alpha},
\qquad
\vartheta_j=(f')^{-1}\vartheta_i,
\]

and the transition factors obey their exact triple-overlap cocycle. Therefore the regular branch
atlas, G246 completed ribbon, invariant mixed clock-ruler pairing, and scalar clock arrow all
descend on overlaps.

This is descent of each labelled branch. It is not a quotient identifying different branches with
the same endpoints.

## 3. Direct future-null links are not closed under composition

Let the objects be observer-event germs and the direct arrows be the regular future-null incidence
germs just defined. In flat `(1+1)` Minkowski space take

\[
A=(0,0),\qquad B=(1,1),\qquad C=(2,0).
\]

Then

\[
(B-A)^2=0,
\qquad
(C-B)^2=0,
\]

and both legs are future-directed, while

\[
(C-A)^2=-4<0.
\]

Thus `A->B` and `B->C` are direct future-null arrows but there is no direct future-null `A->C`
arrow to serve as their composite. Direct links are not closed under composition. They form a
directed multigraph, or **quiver**, with route-labelled parallel edges.

This exact counterexample rejects both preregistered alternatives A and B. In particular, the
direct-link space is neither an ordinary action groupoid nor an open subgroupoid of one.

## 4. The generated future-null chain category

Let `Q_g` be the direct-incidence quiver. Its free category `Path(Q_g)` has:

- objects: supplied observer-event germs;
- generating arrows: direct regular future-null incidence germs;
- general arrows: finite matched strings `(q_1,...,q_N)`;
- source and target: the first and last event germs;
- composition: concatenation of matched strings;
- identity: the empty string at an object.

Associativity is literal associativity of concatenation. The empty string is not a zero-affine-span
null ribbon; coincidence remains separately typed.

For a fixed chain length, the regular smooth stratum is an iterated fiber product of regular edge
spaces over their shared event germs. The union over all lengths is generally a stratified or
diffeological category, not one finite-dimensional Lie groupoid. Cuts, branch births, caustics,
and variable chain length prevent a universal ordinary Lie-groupoid description.

## 5. Reversal and future return

Reversing one geometric null generator changes a future-directed edge into a past-directed edge.
It is not an arrow of the future-null quiver. A physical future return is a separately generated
edge from the opposite observer's future cone, with generally different endpoints and clock map,
as G246 proves exactly.

One may algebraically form the free groupoid completion by adjoining formal inverses, or enlarge
the geometry to both time orientations and quotient immediate retracings. Neither construction
turns the formal inverse into the physical future return. Therefore G247 derives a physical
future-chain **category**, not a physical causal groupoid.

## 6. Scalar cocycle on matched chains

For one edge germ `q:A->B`, G216/G246 give

\[
r_q=\frac{d\tau_B}{d\tau_A}>0,
\qquad
\delta_q=-\log r_q,
\qquad
q_q=r_q^{-1}.
\]

For a matched chain `A->B->C`, the shared middle proper clock gives

\[
r_{ABC}=r_{BC}r_{AB},
\]

so

\[
\boxed{\delta_{ABC}=\delta_{AB}+\delta_{BC}},
\qquad
\boxed{q_{ABC}=q_{BC}q_{AB}}.
\]

Thus `r` is a functor to the one-object multiplicative positive-real group and `delta` is its
additive real cocycle. The statement applies to the chain arrow. It does not assert the existence
of an independent direct null `A->C` edge, and it does not force any such edge to equal the chain.

## 7. Path-labelled phase is the complete composable channel

On one supplied edge, G226 gives the clock-normalized screen phase

\[
M_q^T\Omega M_q=r_q\Omega,
\qquad M_q\in\operatorname{CSp}^+(4,\mathbb R).
\]

At a shared event, incoming and outgoing ray directions generally have different screens. Off the
antipodal stratum, the frozen G225 standard evaluator supplies the least-turning lift

\[
L_B=\operatorname{diag}(C_B,C_B),
\qquad L_B^T\Omega L_B=\Omega.
\]

The two-edge chain phase is therefore

\[
\boxed{M_{ABC}=M_{BC}L_BM_{AB}},
\]

with

\[
M_{ABC}^T\Omega M_{ABC}=r_{BC}r_{AB}\Omega.
\]

Middle screen gauges cancel, but the matrices generally do not commute. G225's finite `O(2)`
direction holonomy and the curvature-dependent Jacobi phase survive in their lawful order. The
complete phase is consequently path-labelled; it cannot be replaced by the scalar multiplier or
an endpoint-only flat screen identification.

At antipodal direction changes, the least-turning lift has no unique continuous extension. The
phase functor is then defined only after retaining a path/axis branch label, or it is returned as a
multivalued set. G247 does not insert a choice.

## 8. Global and degenerate strata

- **No incidence:** no generating edge occurs on the declared observer pieces.
- **Coincidence:** the categorical identity is the empty chain; no nontrivial null ribbon is
  inferred.
- **Several regular incidences:** every direction- and route-labelled edge is retained.
- **Cut or self-intersection:** endpoint projection is noninjective, but initial-direction/route
  labels keep the branches distinct.
- **Conjugate point or caustic:** the position Jacobi block can lose rank and the regular endpoint
  branch chart can ramify or fail. The full G226 phase along the labelled geodesic remains
  invertible. G247 retains a labelled singular stratum and does not claim a unique G246 endpoint
  graph there.
- **Antipodal vertex directions:** the G225 screen lift is branch-valued until a path/axis is
  supplied.
- **Incomplete null generator:** the edge ends at the maximal geodesic-flow domain.
- **Closed future chain:** possible only on metric histories with the requisite causal structure;
  it is a future cycle, not automatically an invertible arrow.

The regular branch atlas therefore descends globally, while its natural completion is stratified
and branch-valued rather than a smooth thin endpoint groupoid.

## 9. Exact verification

The production implementation passes:

- 2,048 exact rational chain cases;
- 20,499 assertions;
- 2,047 noncommuting phase-order controls;
- the exact null-null-timelike closure counterexample;
- 21 labelled cylinder windings;
- a singular position-block/invertible-full-phase caustic control;
- exact affine-null overlap cocycles.

The independent standard-library `Fraction` implementation imports no production code or output
and passes 5,000 cases and 55,010 assertions. Sixteen hostile mutations are caught, including
forced direct closure, future-return/inverse conflation, branch erasure, phase scalarization,
vertex omission/reordering, and caustic-block inversion.

## 10. Maximum conclusion

G247 closes the global **mathematical home** of the regular null relations already derived in
G245/G246: a route-labelled quiver and its generated chain category, with an exact scalar cocycle
and path-labelled phase evaluator. It does not select which edges Nature populates, one image or
winding, the physical metric history, a transfer/aggregation law, or any observation. It derives
no `X_max`, action, source, matter, bootstrap, mass, or signalling law.
