# Step03 candidate — a finite joint curvature protocol

CANDIDATE, UNPROMOTED; direct separate-context review pending.
IDs SC3-COMPATIBILITY, SC3-RECONSTRUCTION, SC3-BLINDNESS.
This is an eventwise algebraic result, NOT an Einstein PDE realization theorem.

## 1. Objects and exact measurement type

Use the G348 curvature convention
R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y] Z.
At one regular event choose an oriented orthonormal frame e0=u,e1,e2,e3,
with g(u,u)=-1 and u future. Define the covariant four-tensor

    Q_abcd = g(R(e_a,e_b)e_c,e_d).

This explicit slot convention avoids identifying differently ordered lower
Riemann components by name. It has skew first/last pairs, pair exchange,
and first Bianchi Q_abcd+Q_bcad+Q_cabd=0. Ric_bc=sum_a eta_aa Q_abca.
The adopted bounded G312 arena supplies Ric=Lambda g. It is a conditional
owner-provisional equation, not a new premise or selected scalar value.

The timelike tidal query is the symmetric matrix

    E_ij=Q_i00j=g(R(e_i,u)u,e_j).                         (1)

For each cyclic (i,j,k)=(1,2,3),(2,3,1),(3,1,2), supply null tangents
k_i^+=u+e_i and k_i^-=u-e_i. Both are future and normalized by -g(u,k)=1
AT THIS EVENT. Supply affine geodesic extensions and parallel screen bases
(e_j,e_k). Their quotient tide matrices are

    T_i^s(A,B)=g(R(e_A,k_i^s)k_i^s,e_B), s=+1,-1,
    (A,B) in (j,k).                                    (2)

These are exactly ideal infinitesimal Jacobi evaluations. For a Jacobi field
with initial value e_A, parallel frame and prescribed initial derivative,
the equation D^2J/dlambda^2+R(J,k)k=0 says that the corresponding negative
relative-acceleration component is (2); proper time gives (1) for timelike u.
W4/G261 supplies the working one-metric freefall interpretation; G348 supplies
the geometric null-screen operator. This does not build a detector or identify
raw apparatus records with these ideal components. Proper-time/ruler units
and affine normalization are supplied calibration/query data, not new laws.

Record six upper-triangular components of E and three of each of the six
T matrices:24 numbers. Arrange each into a symmetric matrix using these
queried components. If a protocol also independently measures the reversed
off-diagonal component, symmetry must be tested separately; it is not a
hidden equality between two independently recorded entries here.

## 2. Algebraic Einstein curvature decomposition

Let tau=tr E, Lambda=-tau, K=Lambda/3=-tau/3, and C=E-(tau/3)I.
Thus C is trace-free. Every algebraic Einstein Q is specified by E symmetric
and one symmetric trace-free three-by-three matrix B, with epsilon_123=+1:

    Q_i00j = E_ij,
    Q_i0jk = sum_l epsilon_jkl B_li,
    Q_ijkl = sum_mn epsilon_ijm epsilon_kln C_mn
               + K(delta_jk delta_il-delta_ik delta_jl). (3)

Other components follow by skew pairs and pair exchange. B is a convenient
dual representation of MIXED CURVATURE, not an independent field or carried
content. Its common familiar name supplies no physics in this argument.

Here is the algebraic converse, not just a proposed parameterization. Dualize
the spatial skew pair of Q_i0jk to define the unique3x3 B. First Bianchi for
the temporal/spatial triples gives tr B=0. Ric_0i=0 eliminates its antisymmetric
part, so B is symmetric. The purely spatial algebraic curvature can likewise
be represented as epsilon_ijm epsilon_kln L_mn with L symmetric (the three
spatial bivectors give a symmetric3x3 representation). Its Ricci contraction
is L_ij-(tr L)delta_ij. The full spatial Einstein equation requires this
contraction to be E_ij+Lambda delta_ij. Taking the trace and substituting
Lambda=-tr E fixes L=C-K I, exactly (3). No remaining spatial curvature
component is free. Conversely direct substitution, epsilon identities and
symmetry/trace-free B give all Riemann symmetries, first Bianchi and
Ric=Lambda diag(-1,1,1,1). Thus (3) has exactly6+5=11 real parameters.

## 3. Opposite-direction parity

Define even and odd recorded matrices

    H_i=(T_i^+ + T_i^-)/2,
    O_i=(T_i^+ - T_i^-)/2.

Expansion of (2) with (3), for each cyclic screen (j,k), gives

    H_i = [[E_jj-E_kk, 2E_jk],
           [2E_jk, E_kk-E_jj]],                         (4)

    O_i = [[2B_jk, B_kk-B_jj],
           [B_kk-B_jj, -2B_jk]].                        (5)

For clarity the linear-in-sign contraction before choosing a screen is

    Q_Ai0B+Q_A0iB
      =sum_l (epsilon_iAl B_lB+epsilon_iBl B_lA).

The constant-curvature K contribution cancels from every null tide because
the screen vectors are orthogonal to the null tangent. It remains in E.
These equations are algebraic consequences of one curvature tensor; they
do not assume two different rays have physically transported content.

## 4. SC3-COMPATIBILITY and SC3-RECONSTRUCTION

The24 declared numbers are compatible with one algebraic Einstein curvature
tensor IF AND ONLY IF the following thirteen scalar linear constraints hold:

1. Each of the six T_i^s has trace zero:6 constraints.
2. For each i, H_i11=E_jj-E_kk and H_i12=2E_jk:6 constraints.
   Its other diagonal then follows from the trace constraints.
3. O_1,12+O_2,12+O_3,12=0:1 constraint.                (6)

Necessity follows from (4)--(5). To prove sufficiency put
o_i=O_i12. Recover the mixed-curvature data by

    B23=O_1,11/2, B31=O_2,11/2, B12=O_3,11/2,
    B11=(o2-o3)/3, B22=(o3-o1)/3, B33=(o1-o2)/3.        (7)

The last condition in (6) makes the three diagonal differences agree with
all o_i. The recovered B is symmetric trace-free, and all O_i are trace-free
by the first condition. Build Q by (3). Equations (4)--(5) then reproduce
every recorded component. E also fixes Lambda=-tr E, so Q is UNIQUE in the
declared frame/metric at this point. This proves algebraic sufficiency and
reconstruction, not existence of a full lawful spacetime realizing arbitrary
record data. The thirteen constraints are independent: the linear map from
(E,B) to24 records is injective by (7), hence has dimension11, and (6) is a
complete13-equation description. Exact matrix ranks provide a further check.

For any ACTUAL supplied smooth metric in the admitted Einstein arena, these
are necessary identities of its ideal queries and the protocol reconstructs
its curvature value. If a fixed Lambda0 sector is separately supplied, add
tr E=-Lambda0; this is an existing sector restriction, not a new selection.
No claim is made that every reconstructed pointwise tensor occurs in the
particular compact G321/G332 data families or a physically occupied history.

The chosen protocol is not asserted minimal. Both signs make the parity and
cross-query restrictions explicit. No preferred physical triad is selected;
rotating or reversing the chosen oriented frame changes the query components
and the representation B consistently, not the underlying geometric claim.

## 5. Incompatible records and what simpler probes miss

An individually symmetric trace-free null tide need not agree with the
timelike tide or the other directions. For example take E=0 and all T=0
except T_1^+=T_1^-=diag(1,-1). Every null tide is symmetric/trace-free, but
H_1=diag(1,-1) violates (4). There is no joint algebraic Einstein Q.

A separate failure survives all trace and even tests. Take E=0, H_i=0,
O_1=[[0,1],[1,0]] and O_2=O_3=0, setting T_i^+=O_i,T_i^-=-O_i.
The three o values are(1,0,0), so their sum is nonzero. Each opposite pair
separately fits some mixed B; all three pairs cannot fit one trace-free
symmetric B. This detects shared-curvature consistency beyond checking each
individual null screen. These records are logical controls, not observations.

SC3-BLINDNESS: timelike E alone leaves all five B components undetermined
algebraically. Null tides alone are blind to the constant-curvature scalar:
adding delta K(g_bc g_ad-g_ac g_bd) changes E by-delta K I and Lambda by
3delta K, but leaves every null screen tide zero for that added part. The
combined protocol removes these particular algebraic blind directions.
It still leaves metric derivatives, separated-event geometry, finite-segment
Jacobi flow, full initial fields and physical occupancy undetermined. Equal
curvature at one point is not equality of spacetime or its later responses.

## 6. Scope and review history

This is a finite ideal-query constraint/reconstruction result, not just an
unlabelled curvature formula, a physically adopted law or a new content name.
A violation in actual data would bear on the joint measurement interface,
shared event/frame/scales and Einstein-arena assumptions; it would not isolate
UDT or a specific premise as false. No raw instrument interface is certified.

The author developed the parity/decomposition argument using admitted sources
before receiving reviewer findings. Standard tensor algebra is a mathematical
method. Exact basis calculations will check signs, all tensor constraints,
record-map and constraint ranks, reconstruction, blind directions and actual
changed-formula controls. They do not prove PDE existence or physical truth.
The actual author run passed15 guard groups on all11 exact tensor basis
elements (256 components each) and7 additional rational parameter controls.
Record/constraint/timelike/null ranks were11/13/6/10. All4 changed-formula
paths failed their intended first guards. No unexpected author failure or
same-premise repair occurred. Full matrices and streams are saved as evidence.
Step02 is not a dependency. No new physical premise, scientific grade,
curvature recipe, source, matter, history, scale, Xmax or canon is selected.
