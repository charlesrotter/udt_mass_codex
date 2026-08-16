# G123 exact derivation — declared common-event observer incidence relation

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS__EXACT_CHECKS_PASS`

## 1. Result first

For the **supplied common-event observer-exponential query**, the direct `A-B` relation has a
simple metric/query-natural construction. It is not a new spacetime path from A to B. It is the
incidence correspondence of the two complete observer charts:

\[
\boxed{
\mathcal C_{AB}=P_A\times_M P_B
=\{(p_A,p_B):F_A(p_A)=F_B(p_B)\}.
}
\tag{1}
\]

On the regular overlap where both observer-exponential maps are local diffeomorphisms, (1) is a
four-dimensional local graph

\[
f_{BA}=F_B^{-1}\circ F_A,
\tag{2}
\]

with exact tangent map

\[
D_{BA}=df_{BA}=(dF_B)^{-1}dF_A.
\tag{3}
\]

It composes and reverses exactly and can mix longitudinal pair and angular coordinates in the
supplied query split. Distinct regular preimages give distinct local graph branches. At a vertex
or nontransverse caustic the incidence set may instead be singular or positive-dimensional and is
retained as an unclassified stratified relation.

This closes the object type of the direct relation for this declared query class. It does **not**
derive same-event incidence as the universal physical meaning of co-presence, which remains
whole-solution membership. Moreover, (3) acts
on four-dimensional **observer-query tangent spaces**, not on four-dimensional transverse Jacobi
phase. Common-event incidence fixes endpoint incidence; it does not fix the derivative half of a
beam. Full phase matching remains G114's source-boundary compatibility condition.

The bounded landing is

```text
DECLARED_COMMON_EVENT_OBSERVER_EXPONENTIAL_INCIDENCE_RELATION_DERIVED_CONDITIONALLY
__REGULAR_STRATUM_IS_FOUR_DIMENSIONAL_LOCAL_QUERY_TANGENT_GRAPH
__REGULAR_MULTIPLE_PREIMAGES_GIVE_LOCAL_GRAPH_BRANCHES
__NONTRANSVERSE_VERTEX_OR_CAUSTIC_FIBERS_REMAIN_UNCLASSIFIED_STRATIFIED_RELATIONS
__DIRECT_TANGENT_MAP_IS_NOT_A_FULL_JACOBI_PHASE_ARROW
__PHASE_MATCHING_REMAINS_A_SOURCE_BOUNDARY_COMPATIBILITY_CONDITION
__NO_HISTORY_SELECTOR_FOUND_IN_DECLARED_COMMON_EVENT_TEST
```

## 2. The regular fiber-product theorem

Let `P_A,P_B,M` be smooth four-manifolds and let

\[
F_A:P_A\to M,
\qquad
F_B:P_B\to M
\]

be the observer-exponential maps derived conditionally from one supplied metric and two supplied
observer queries. Define

\[
G=F_A\times F_B:P_A\times P_B\to M\times M.
\]

Then `C_AB=G^-1(Delta_M)`, where `Delta_M` is the diagonal. If `G` is transverse to the diagonal,
the regular-value theorem gives

\[
\dim\mathcal C_{AB}=4+4-4=4.
\tag{4}
\]

Its tangent space is

\[
T_{(p_A,p_B)}\mathcal C_{AB}
=\{(v_A,v_B):dF_Av_A=dF_Bv_B\}.
\tag{5}
\]

If `dF_B` is invertible, (5) is locally the graph of (3). If both differentials are invertible,
both projections from `C_AB` are local diffeomorphisms and reversal is defined. This is the
observer-chart transition on their common-event overlap.

No curve from observer A to observer B is chosen. Each point of the relation says only that A's
and B's complete query coordinates describe the same event.

## 3. Exact composition and complete metric covariance

For three observer charts on one regular common overlap,

\[
f_{CA}=f_{CB}\circ f_{BA},
\qquad
D_{CA}=D_{CB}D_{BA},
\tag{6}
\]

and

\[
D_{AB}=D_{BA}^{-1}.
\tag{7}
\]

Let

\[
\mathcal H_i=F_i^*g=(dF_i)^Tg\,dF_i
\]

be the complete pullback metric in observer-query coordinates. Equation (3) gives

\[
\boxed{D_{BA}^T\mathcal H_BD_{BA}=\mathcal H_A.}
\tag{8}
\]

This is an exact identity of the full observer-chart transition. It does not say that the
longitudinal pair block, angular block, and mixed block are separately preserved. Indeed, the
transition can mix them before any terminal reciprocal readout.

Equation (8) also clarifies the earlier phrase “non-isometric observer map.” The complete direct
chart transition is an isometry between two pullbacks of the same ambient metric at the same
event. Nontrivial observer effects occur in the calibrated channel decomposition and its terminal
readouts, not as a failure of (8).

## 4. Exact flat three-observer witness

For the preregistered matrices `M_A,M_B,M_C`, exact reduction gives

\[
D_{BA}=
\begin{pmatrix}
1&1/5&12/5&0\\
0&4/5&-12/5&0\\
0&3/25&16/25&0\\
0&0&0&4/5
\end{pmatrix},
\qquad
\det D_{BA}=16/25.
\tag{9}
\]

The upper-right block, carrying A-angular input variations into B-longitudinal output coordinates,
has rank one in the preregistered query bases. Thus even this flat common-event chart transition can
mix the query's longitudinal and angular coordinates. The nonzero-rank statement is meaningful
relative to the supplied longitudinal/angular split and is preserved by block-preserving
reparameterizations; it is not a basis-free physical mixing magnitude. This is the complete
orchestra entering inside the direct relation, not an angular correction appended after a scalar
pair law.

The full pullbacks are

\[
\mathcal H_A=
\begin{pmatrix}
-1&-1&0&0\\-1&0&0&0\\0&0&16&0\\0&0&0&16
\end{pmatrix},
\quad
\mathcal H_B=
\begin{pmatrix}
-1&-1&0&0\\-1&0&0&0\\0&0&25&0\\0&0&0&25
\end{pmatrix},
\tag{10}
\]

and (8) holds exactly. Both terminal pair blocks have determinant `-1` and `phi_pair=0`; the full
transition is nevertheless nontrivial and mixed. This proves that terminal scalar equality does
not exhaust the direct relation.

## 5. Why the direct tangent map is not full Jacobi phase

For a point-observer sky query, a query-tangent variation has a source screen-phase image

\[
\ell_i(v)=
\left(\pi_{S_i}dF_i(v),\;\pi_{S_i}\nabla_vK_i\right)
\in E_i=S_i\oplus S_i.
\tag{11}
\]

This uses the metric/query two-jet and a supplied endpoint screen representative. In the exact
flat collinear control at affine radius `r_i`,

\[
\ell_i=
\begin{pmatrix}
0&0&r_i&0\\
0&0&0&r_i\\
0&0&1&0\\
0&0&0&1
\end{pmatrix},
\tag{12}
\]

which has rank two, not four. Its image is the point-observer Lagrangian plane

\[
\Lambda_i=\operatorname{col}\binom{r_iI_2}{I_2}.
\tag{13}
\]

For collinear source legs with radii four and five, the direct incidence tangent map is

\[
D_{BA}=\operatorname{diag}(1,1,4/5,4/5).
\]

It makes source position variations agree,

\[
(\ell_BD_{BA})_{J}=(\ell_A)_J,
\]

but not source momentum variations,

\[
(\ell_BD_{BA})_{\Pi}\ne(\ell_A)_\Pi.
\tag{14}
\]

Equivalently, the exact intersection dimension of the phase graphs at radii four and five is zero.
An aligned equal-graph control has intersection dimension two, so the matched phase stratum is
nonempty but not forced by common-event incidence.

Thus:

- `D_BA` is a complete direct map on query tangents;
- it is not a map on the full Jacobi phase fibers;
- equality of source phase requires the boundary/junction condition already isolated in G114.

The second or cotangent prolongation of a coordinate transition may be constructed, but it is not
automatically the physical transverse Jacobi phase comparison because the two source legs use
different ray directions and geodesic histories.

## 6. Regular branches versus singular incidence fibers

At cuts or other multiple-preimage events, several **regular** observer-exponential preimages may
label the same event. Each transverse preimage supplies its own four-dimensional local graph
branch.

At the point-observer vertex `lambda=0`, both angular columns collapse and `rank(dF)=2`. At ordinary
caustics the position projection may lose rank while full Jacobi phase remains regular. These
nontransverse fibers are outside the local graph theorem: their dimension may jump and they need
not be smooth manifolds.

Therefore the global object for this query is not one universal diffeomorphism. It is the incidence
relation (1): a family of regular graph branches where transversality holds, plus an unclassified
stratified set at nontransverse fibers. No singular member is discarded merely because a local
inverse fails, but G123 does not claim a complete singularity classification.

## 7. History-selection audit

The incidence construction, local graph theorem, composition, reversal, and pullback identity hold
for every supplied smooth metric/query wherever their stated rank hypotheses hold. They classify
the direct observer relation for the declared common-event query but do not exclude one regular
metric history in favor of another in this bounded test.

Requiring source phase alignment could be nonidentity data, but G114 already proves that it depends
on a supplied source-boundary or transfer rule. G123 does not promote it into a metric-only history
selector.

## 8. What is established and open

`DERIVED_CONDITIONALLY`:

- for the supplied common-event query, the direct relation is the incidence correspondence;
- its regular local stratum is a four-dimensional observer-chart transition;
- its tangent map composes, reverses, preserves the complete pullback metric, and may mix channels
  relative to the supplied query split;
- regular multiple preimages yield local graph branches;
- nontransverse vertex and caustic fibers remain unclassified stratified relations;
- the direct tangent map does not universally supply full Jacobi phase.

`OPEN`:

- whether this query is the universal physical direct relation implied by co-presence;
- physical ownership of one complete metric history and observer-query family;
- source-boundary phase matching and branch population;
- finite-radius time-live relations among terminal depth, frequency depth, shift, and screen phase;
- nonspherical/global completion, `X_max`, transfer, source, matter, action, and bootstrap closure.
