# G123 preregistration — direct co-present observer incidence relation

Date: 2026-08-16
Status: preregistered before theorem reduction or witness evaluation

## Whole question and bounded regime

Let one supplied smooth time-oriented Lorentz metric `g` and one typed point-observer query give two
observer-exponential maps

\[
F_A:P_A\to M,
\qquad
F_B:P_B\to M,
\]

where each four-dimensional parameter space uses coordinates `(tau,lambda,n^1,n^2)`. Construct the
direct co-present `A-B` relation from these maps without introducing an independent spacetime path,
preferred branch, source state, action, or fitted rule.

The candidate direct relation is the common-event incidence set

\[
\mathcal C_{AB}=P_A\times_M P_B
=\{(p_A,p_B):F_A(p_A)=F_B(p_B)\}.
\]

Determine its regular dimension, branch/singular behavior, tangent map, complete-pullback metric
behavior, terminal-pair content, and relation to four-dimensional Jacobi phase.

## Frozen outcome classes

1. `DIRECT_TWO_DIMENSIONAL_PAIR_IMMERSION_ONLY`;
2. `DIRECT_FOUR_DIMENSIONAL_INCIDENCE_GRAPH_ON_QUERY_TANGENTS`;
3. `DIRECT_FOUR_DIMENSIONAL_FULL_JACOBI_PHASE_ARROW_DERIVED`;
4. `BRANCH_VALUED_OR_SINGULAR_INCIDENCE_RELATION_ONLY`;
5. `NO_METRIC_NATURAL_DIRECT_RELATION`;
6. `BOUNDED_INCONCLUSIVE`.

The conclusion may combine the regular and singular classifications. Equal dimension between a
query-tangent map and Jacobi phase does not identify their fibers.

## Frozen exact witnesses

Use flat spacetime only as an exact type/rank witness, not as a selected history. Three inertial
observers `A,B,C` view one common event. Their source-leg differentials in matched local query
coordinates are frozen as

\[
M_A=
\begin{pmatrix}
1&1&0&0\\0&1&0&0\\0&0&4&0\\0&0&0&4
\end{pmatrix},
\]

\[
M_B=
\begin{pmatrix}
1&1&0&0\\0&4/5&3&0\\0&-3/5&4&0\\0&0&0&5
\end{pmatrix},
\quad
M_C=
\begin{pmatrix}
1&1&0&0\\0&4/5&0&3\\0&0&5&0\\0&-3/5&0&4
\end{pmatrix}.
\]

These arise from observer A at spatial `(0,0,0)`, B at `(0,3,0)`, C at `(0,0,3)`, and common event
at `(t,x,y,z)=(5,4,0,0)`, with unit null directions and orthonormal sky tangents. The affine radii
are `4,5,5`.

Also freeze:

- the vertex stratum `lambda=0`, where angular columns collapse;
- source phase image planes represented in one matched component frame by
  `Lambda_A=col(4 I_2,I_2)` and `Lambda_B=col(5 I_2,I_2)`;
- an aligned control with equal phase graphs.

## Exact tests

1. Derive the regular-value/fiber-product dimension and local graph theorem.
2. On the frozen witness compute
   `D_BA=M_B^-1 M_A`, its inverse, and three-observer composition.
3. Verify complete pullback covariance
   `D_BA^T H_B D_BA=H_A`, where `H_i=M_i^T eta M_i`.
4. Check whether `D_BA` retains pair/angular off-block mixing.
5. Type the point-observer map from query tangents to endpoint Jacobi phase and determine its rank.
6. Test whether common-event incidence alone aligns the two source phase-image planes.
7. Retain all singular, caustic, cut, and multiple-preimage branches as relations rather than
   filtering them.

## Premise ledger

- metric history: `SUPPLIED_CONDITIONALLY`, not selected;
- observer germs, celestial carry, event/source incidence query: `SUPPLIED_QUERY`;
- observer exponential and its full differential: `DERIVED_CONDITIONALLY`;
- incidence relation and regular local inverse: target of this derivation;
- terminal pair metric/readout: `DERIVED` only after a regular pair block is supplied;
- full Jacobi phase propagator: `DERIVED_CONDITIONALLY` on each supplied causal branch;
- source phase matching/boundary rule: `OPEN`;
- preferred path, branch weight, source occupancy, transfer, observation, action, matter, bootstrap,
  `X_max`, and signalling: omitted.

## Certification and falsification contract

`DIRECT_FOUR_DIMENSIONAL_INCIDENCE_GRAPH_ON_QUERY_TANGENTS` requires an exact regular-value proof,
exact composition/reversal, and independent replay. It is falsified if the construction imports a
route or fails covariance.

`DIRECT_FOUR_DIMENSIONAL_FULL_JACOBI_PHASE_ARROW_DERIVED` requires a metric/query-natural,
information-preserving phase lift fixed before evaluation. A rank-two point-sky lift, equality only
after a source-boundary rule, or equal matrix dimensions is insufficient.

A history selector is found only if one preregistered covariant condition excludes a regular
history rather than merely classifying a query, incidence branch, or boundary match.

## Maximum conclusion

G123 may close the object type of the direct co-present relation in the declared point-observer
class. It cannot select a physical history or query, derive radiation/matter dynamics, determine
`X_max`, or make an observational claim.
