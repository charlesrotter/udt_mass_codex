# KTI1 — where the twisting example's information survives

Initial mathematical candidate, 2026-09-10. CONDITIONAL; UNPROMOTED; fresh review pending.
Preserve these bytes. WORK_ORDER.md and DATA_FREEZE.md define the exact comparison.

## 1. Source-owned types

G176 and G179 control the completed evaluator, conditional on the working completed-pair
Dual Reciprocity clarification. For supplied E,J of the regular types,

    V=EJ,  h=V^T eta V,  T^2=-h00,
    beta=h01/h00,  m=sqrt(-det h),  beta_s=beta/m,  Phi=-log T.

The full h and its shift are retained before scalar readout. The older uncompressed
arbitrary-calibration expression (1/4)log((-det h)/h00^2) is a control after G176; it is not
the current completed scalar unless evaluated in the completed ruler coordinate.
G179 allows arbitrary supplied coframes and smooth query families; G180 proves regular
one-dimensional ruler integration, not cross-family synchronization or a neighborhood
data-acquisition theorem. G182 explicitly separates scalar, pair metric and full germ carry;
its tangent-jet statements require the common ambient/coframe setting they state.

The present result specializes these accepted conditional definitions to DCI1's comparison
family. It neither repairs the evaluator nor selects the family as a physical UDT history.

## 2. The underlying metric and the scalar silence

Let B=(b/2)(x dy-y dx) and theta=dt+B. Then

    g_b=-theta^2+dx^2+dy^2+dz^2,  U=partial_t,
    E_b=[[1,-by/2,bx/2,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]].

E_b is invertible with determinant one for every real b and event. U is unit, Killing and
geodesic. G220's scalar null-clock depth is zero on each supplied regular branch because
g(U,k) is conserved along that metric's affine null geodesic. This retains DCI1's warning:
zero scalar values do not establish equal branch incidence maps, travel times, or paths.

For any of the following pair germs the clock column is U, so h00=-1 and Phi=0. Thus the
scalar terminal chi is zero where it is the depth of the corresponding completed relation.
No complete null pair surface is inferred from G220's clock-leg compatibility.

## 3. Coordinate-marked pair records retain a shift field

Supply the coordinate germs J_i=(U,partial_i), i=x,y,z, jointly marked in one smooth
neighborhood. They are actual pair-immersion tangents: F_i(tau,s)=(t+tau,r+s e_i), with
the other spatial coordinates fixed. For these coordinate pairs,

    h_i=[[-1,-B_i],[-B_i,1-B_i^2]],
    det h_i=-1, T=1, L=1, m=1, beta_s=beta_i=B_i, Phi=0.       (1)

The metric on each pair is Lorentzian even when its coordinate ruler column is not
spacelike; the clock-orthogonal ruler has norm one. No artificial |B_i| cutoff is needed.

At p=(t,0,0,0), all h_i=diag(-1,1) for all b. All U-time derivatives of these stationary
records agree as well. The full pair matrices at this event, even with all their time
derivatives, therefore do not determine b or W. This is the D_point ambiguity.

For D_coord, the additional spatial first jets in the common marking yield

    C_ij=partial_i beta_j-partial_j beta_i,
    C_xy=b, C_xz=C_yz=0.                                    (2)

Thus b is read from a first spatial jet of the RETAINED SHIFT for this specified family
and orientation. W=b^2/2 is then determined. The whole field is more information than
needed for this one target: the two derivatives at the event suffice. No minimality
claim across arbitrary encodings or general metric class is made.

For clarity on the vorticity factor, U_flat=-theta, and the projected antisymmetric
covariant derivative is w=(1/2)dU_flat on the observer rest directions. With
X_i=partial_i-B_i U, one has g(X_i,X_j)=delta_ij and

    w(X_i,X_j)=-C_ij/2,
    W=w_ab w^ab=(1/4)sum_ij C_ij^2=b^2/2.                   (3)

This uses torsion-free metric geometry, not a gravity equation. It agrees with DCI1's
previously reviewed direct geometric W. Signed b depends on the supplied orientation;
W is the scalar target independent of that sign. c_E=1 expresses calibration, not size
selection. General lapse, quotient metric, time dependence, unaligned observers, or
unrelated pair families require their own formulas and are outside this result.

## 4. A point shift is not invariant twist

Under the smooth coordinate change t'=t+f(x,y,z), theta=dt'+B', B'=B-df.
Two operations must be distinguished.

First transform the SAME geometric germs: E'=E K^-1, J'=KJ, with K the coordinate
Jacobian. Then V and h do not change. This is G179's matched coordinate covariance.
The transformed old coordinate ruler has a clock component partial_i f; it is not
the newly selected constant-t' coordinate ruler.

If one instead selects the constant-t' coordinate-germ family, the query has changed.
Its retained shift is beta'_i=B_i-partial_i f. These new queries are related by the
supplied common synchronization, not identical to the original marked queries. Yet

    partial_i beta'_j-partial_j beta'_i=C_ij,               (4)

because the mixed derivatives of smooth f commute. Hence the extraction in (2)-(3)
survives this common re-synchronization in the stated family. It does not permit
independent undocumented changes of clock origin/calibration across comparisons.

For b=0 and nonconstant f, some beta'_i are nonzero while C and W vanish. This exact
flat control refutes pointwise shift-as-vorticity. Even for b!=0, one can set selected
shift components to zero by a query change without deleting the nonzero antisymmetric
spatial variation. The original query's shift is never silently discarded.

## 5. A different supplied germ recipe hides twist even from full pair matrices

Choose instead J_i^perp=(U,X_i), X_i=partial_i-B_i U. These germs are regular, and
they too have actual local pair immersions. In the present linear family B_i is
constant along the i coordinate line, so one may take

    F_i^perp(tau,s)=(t+tau-s B_i(r), r+s e_i).

The two tangent columns are exactly U and X_i along that surface, and

    h_i^perp=diag(-1,1), m=1, beta_s=0, Phi=0,
    V_i=E_b J_i^perp=(e_0,e_i).                            (5)

These numerical h_i and V_i fields and all their ordinary coordinate derivatives
are identical for b=0 and b!=0. This proves ambiguity for D_perp as actually defined.
The equality does not include the ambient coordinate J_i^perp or the coframe E_b.
Metric-dependent adapted frames are being used; there is no claim that full physical
directions or frame transport have been identified across the two geometries.

The hidden information is visible if the INPUT tangent fields are also retained:

    [X_x,X_y]=-b U.                                       (6)

Alternatively dtheta=b dx wedge dy exposes it from the INPUT coframe field. Either
calculation uses neighborhood information absent from h/Phi/V-only records. Numerical
V coefficients alone cannot supply a changing ambient coframe or its structure.
This does not contradict G182's common-coframe germ-jet theorem: different E_b are
precisely what the stronger record map has omitted. Individual pair immersions exist;
no jointly orthogonal three-dimensional coordinate slice is assumed.

## 6. What is learned and what remains open

For DCI1's exact example, some currently retained pair data can expose twist while
scalar clock data remain silent. Specifically, D_coord's jointly calibrated spatial
first jets recover b and W through (2)-(3). Other regular supplied query families
yield identical full pair matrices and adapted V coefficients while W differs.
These statements concern distinct explicitly declared data maps, not competing answers
for one identical complete kernel input.

The kernel does not generate the common neighborhood event labels, clock synchronization,
ruler calibration, physical pair population or the derivative sampling. This argument
does not establish operational access to those records, or the generic sufficiency of
full h alone. Full E/J input distinctions are not advertised as inverse reconstruction
from scalar outputs. G220 path, screen and connection/transport records are neither
constructed nor asserted equal here; no new transport law has been introduced.

The missing join is therefore explicit: a supplied matched family makes one geometric
extraction possible, while its physical or founding realization remains OPEN. That
does not prove a new physical law is necessary. This case study applies existing source
distinctions; it is not a new theorem of differential geometry or a repository-wide
novelty claim. Source grades and the fixed manuscript remain unchanged.
