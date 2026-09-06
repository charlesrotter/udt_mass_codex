# Step02 candidate — finite shared-content queries have testable compatibility

CANDIDATE, UNPROMOTED; fresh direct review pending.
IDs SC2-CONE, SC2-OVERLAP, SC2-INVISIBLE. Assumptions are in QUESTION.md.
No raw instrument output, physical count, content identity or recipe is adopted.

## 1. Exact finite query class

Use the G351/G352 sources at70034a6f and reviewed SC1-READOUT only at their
conditional scopes. Let (Lambda,F) be one supplied measurable label space and
E_1,...,E_n a finite partition into NONEMPTY measurable cells. Empty cells
are discarded. Let m be the number of declared ideal readout queries and

    K_a(lambda)=A_aj on E_j,       A_aj >= 0 finite.

Here K_a is a SUPPLIED kernel of the G352 form
1_[X_i(lambda) in B_a] omega_i(lambda)/Delta in the chosen finite class.
Constancy on cells is a query restriction, not a general metric theorem.
The algebra below works for any such finite nonnegative matrix; it does not
claim every matrix is realized by arbitrary fixed geometric data.

For any finite nonnegative countably additive mu define M_j=mu(E_j). Then

    y_a=integral K_a dmu=sum_j A_aj M_j,        M_j>=0.    (1)

Finiteness/integrability follows because every kernel is bounded on this
finite partition. Zero rows, zero columns and zero mu are allowed. No total
mass, normalized probability, smooth density or absence of singular content
is imposed. The measurable sets, weights and shared label identification
are ordinary fixed query inputs; M and finer content remain unknown data.

## 2. SC2-CONE: exact feasibility and a separating certificate

The ideal record y is realizable by such a mu if and only if

    y belongs to C_A={A M : M in R^n, M>=0}.              (2)

Necessity is (1). For sufficiency choose any lambda_j in each nonempty E_j
and set mu=sum_j M_j delta_(lambda_j). Evaluation at a point is a countably
additive measure on F, even if individual singletons are not measurable.
Its mass on E_j is exactly M_j and its total is sum_j M_j<infinity. These
are atoms in LABEL space, not the distinct atomic PHASE/time-count branch.
Neither atomicity nor this representing measure is physically selected.

The cone C_A is closed in R^m in this finite nonnegative class. Remove zero
columns only for this proof, since they do not change y. If all columns are
zero then C_A={0}. Otherwise let c be the smallest positive column1-norm.
For a convergent sequence y_l=A M_l with M_l>=0 and no zero-column mass,

    ||y_l||_1=sum_j ||A_:j||_1 M_lj >= c sum_j M_lj.

Thus M_l is bounded, has a convergent subsequence, and its nonnegative limit
represents the limit y. The nonnegative-column hypothesis avoids cancellation.
This argument is not a closure theorem for general nonconstant kernels.

There is an exact dual characterization:

    y in C_A  iff  h.y>=0 for every h with A^T h>=0.      (3)

One direction is h.y=(A^T h).M>=0. For the converse, if y is outside C_A,
choose a closest point p in the closed cone. It exists: a minimizing sequence
can be confined to a bounded ball by comparison with0, then compactness
and closedness apply. Put r=y-p, nonzero. Differentiating squared distance
along the segment p+t(x-p) for x in C_A gives r.(x-p)<=0. Taking x=0 and
x=2p yields r.p=0, so r.x<=0 for every x in C_A. Consequently h=-r obeys
A^T h>=0 but h.y=-||r||^2<0. This proves (3) by a finite-dimensional argument,
not by a numerical solver's success or a physical positivity postulate.

A negative certificate disproves the JOINT supplied geometry/kernel, common
nonnegative measure and ideal-readout assumptions for that record. It does
not identify which assumption failed, or by itself refute UDT observationally.

## 3. SC2-OVERLAP: three individually positive records can fail jointly

Take three nonempty retained cells P,Q,R. At three cuts choose the transported
preimage windows P union Q, Q union R, P union R. Let r_i>0 be the known
constant omega_i/Delta at each cut, and normalize z_i=y_i/r_i. Then

    z1=p+q, z2=q+r, z3=p+r,
    p=(z1+z3-z2)/2,
    q=(z1+z2-z3)/2,
    r=(z2+z3-z1)/2.                                    (4)

Here lowercase p,q,r are cell masses, not G350 weights or a curvature recipe.
Nonnegative p,q,r exist exactly when all three triangle inequalities

    z1+z2>=z3, z1+z3>=z2, z2+z3>=z1                    (5)

hold. These inequalities also imply each z_i>=0 by summing pairs. They
are additional restrictions beyond separate nonnegativity of each readout.

For example z=(1,1,3) is individually positive but has q=-1/2, and
h=(1/r1,1/r2,-1/r3) gives A^T h=(0,2,0)>=0 and h.y=-1.
It therefore has NO common finite nonnegative mu, not merely no mu in a
sampled family. A positive control p,q,r=(1,2,3) gives z=(3,5,4).

In contrast, disjoint preimage windows P,Q,R with the same positive r_i give
diagonal A. Every nonnegative y is then possible. Overlap/shared identity,
not another evaluation of T=R/A or selection of a source profile, supplies
the extra distinguishing power of this chosen protocol.

## 4. Actual geometric support for the overlap protocol

Supply Minkowski geometry g=-dt^2+dx^2+dy^2+dz^2, with coordinates expressed
in supplied length units. Choose alpha>0 and dimensionless phase
Theta=alpha(z-t), so k=dTheta=alpha(dz-dt), k#=alpha(partial_t+partial_z)
is nonzero future null and affinely geodesic. alpha has the corresponding
inverse-length units; neither alpha nor a physical scale is metric-selected.
Choose fixed Delta>0 and a neighborhood of parallel phase sheets with the
same transverse labels (x,y) and CHOSEN phase-independent mu.

For the reference sheet Theta=0 use three distinct graph cuts

    X_i(x,y)=(t_i,x,y,t_i).

The same labelled rays meet all three cuts; their screen area is dxdy, J=1.
Use retained rectangle Lambda=[0,3]x[0,1], partitioned by x in [0,1),[1,2),
[2,3] into P,Q,R. Boundaries are assigned once and the sets are Borel. At
cut i supply the constant future unit observer

    U_i^t=(d_i+d_i^-1)/2,
    U_i^z=(d_i^-1-d_i)/2, U_i^x=U_i^y=0, d_i>0.

Direct contraction gives g(U_i,U_i)=-1 and omega_i=-k(U_i)=alpha d_i>0.
Thus r_i=alpha d_i/Delta is known and constant across the window. Image
windows X_1(P union Q), X_2(Q union R), X_3(P union R) have exactly the
required preimages. Local worldline extensions with these tangents exist
(constant inertial lines); no finite-time crossing count is used.

For the exact numerical control alpha=2, Delta=3, d=(1,2,3), the compatible
record is y=(2,20/3,8); the incompatible one is y=(2/3,4/3,6). These values
are supplied rational protocol controls in the chosen units, not fits or
physical constants. The incompatible record is a proposed ideal record
tested against the geometry, not a claim that this geometry produces it.

This geometry is also Ricci-flat, but the proof does not need a curvature
content recipe or a chosen Einstein sector. Under common positive affine
phase/spacing scaling alpha->b alpha, Delta->b Delta, all r_i and constraints
stay unchanged. Under supplied observer changes r_i changes; the constraints
apply to the correspondingly normalized records, not unchanged raw rates.

## 5. SC2-INVISIBLE: what the finite protocol does not determine

Every query depends only on M=(mu(E_j)). Two measures are indistinguishable
exactly when their cell-mass vectors differ by an element of ker A. In
particular, all within-cell redistributions preserving cell masses are
invisible. Conversely equal record vectors imply A(M-M')=0 directly.
Nonnegativity still constrains which kernel displacements are admissible.

In the three-overlap protocol A is invertible after division by r_i, so the
three cell masses are unique whenever compatible. The full measure is not.
For example moving a positive point mass between two different measurable
points inside P leaves every query unchanged while changing the measure.
On the rectangular geometry these are ordinary Borel points; alternatively
distinct nonnegative integrable density profiles of equal cell integrals
give the same records. This statement does not assert such redistributions
on a cell whose measurable structure cannot distinguish its points.

A zero column is completely unseen: any finite additional mass on that cell
leaves y unchanged. In general total mass is not known unless the protocol
determines it. There is no hidden probability normalization in (2)--(5).

## 6. Evidence ceiling and discovery history

The analytic arguments establish the arbitrary finite-class quantifiers.
Exact arithmetic controls check (4), certificates, actual phase/observer/
window data, covariance and residual freedom. Deliberate formula mutations
are regression sensitivity checks; they are not independent proof or physics.
Actual author run:22 guard groups passed over216 signed record controls,
27 nonnegative mass controls and3 phase-scale controls. All4 changed formula
paths failed at their intended first guards; raw commands/streams are saved.
No unexpected author failure or same-premise repair occurred.
The author explored the finite-cone and overlap arguments before freezing
this candidate, using no observed record or reviewer conclusion. The reviewer
is independently reconstructing from sources and was asked to withhold findings.

No theorem about arbitrary continuous kernels, noise, finite-time integration,
cross-family addition, detected signal, physical counting, source population,
history, matter, scale, Xmax or canon follows. An actual instrument-to-y rule
remains a separate supported-interface question. The result constrains ideal
queries while retaining legitimate free content data, not a new physical law.
