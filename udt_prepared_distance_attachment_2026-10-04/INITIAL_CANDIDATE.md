# PDA1 initial candidate — a prepared fixed-emission distance limit

Unreviewed conditional analytic candidate. Parent construction precedes reading
either fresh reviewer's source-first argument. RG is UNADOPTED; no native UDT
geometry, field equation, scale or physical positional attribution is claimed.
The work order authorizes explicit attachment hypotheses and adverse controls.
All proper times/lengths use c_E=1; the examples choose a supplied unit scale.

## 1. Precisely prepared objects and the attachment hypotheses

Supply C3 Lorentz4 RG near a future spacelike boundary: g=x^-2 b, x>0,
nonzero timelike dx, and a normal collar b=-N^2 dx^2+h_ij dy^i dy^j.
Supply one emitter event e in the physical interior, its ordinary unit tangent,
and a chosen regular conformal-null ray from e approaching p=(0,y_p).
Write that ray q(x)=(x,z(x)), with z C1 at0, z(0)=y_p. Its nonzero affine
tangent has a regular limit; normalize the WHOLE ray to physical omega_e=1.
Since dx is timelike, x is a legitimate parameter near p. Nullness gives
|z'(0)|_h=N_*>0. Local clock variations required by R6 are supplied on this
regular branch at each finite reception. No global first-arrival/echo theorem
is hidden in the word regular.

Prepare free receiver worldlines on an interior spacelike hypersurface Sigma
using position labels a in a compact set with an open neighborhood of a_*.
Their initial timelike data are smooth and uniformly bounded. L(a) is metric
proper distance on Sigma from a specified origin, on a smooth domain away
from that origin and its cut locus. This specifies an experiment, not a
preferred universal observer population. A compact initial preparation does
NOT alone prove a common late domain, noncrossing or endpoint-map regularity.

State the following additional attachment conditions explicitly:

(H1) All receiver tails in the neighborhood are defined for a common
0<x<=x0 and remain in one compact normal collar with uniform N,h,inverse and
first-derivative bounds. Their spatial covectors w(x0,a) are uniformly bounded.
Any passage from the initial Sigma to this collar is part of the actual
geodesic preparation, not an assumed consequence of compactness.

(H2) For Y(x,a), the spatial receiver position, its label derivatives D_aY
converge uniformly near a_* to a continuous matrix J(a) as x->0. Interior
flow is C1. The endpoint map F(a)=lim Y(x,a) satisfies F(a_*)=y_p and
det J(a_*)!=0. The convergence/determinant are to be checked from the supplied
flow. They are not asserted to follow from FCL's pointwise estimate or bare
C3 regularity. Below H1 derives F and its continuity; H2 gives its C1 structure.

(H3) Define the geometrically computed number

    d = D_a L(a_*) [J(a_*)^-1 z'(0)].

For a below-endpoint initial-distance limit assume d<0 and put c=-d>0.
If d>0 the corresponding statement uses approach from above; d=0 is a genuine
attachment degeneracy. It is not legitimate to set x=L_*-L by definition.

These are sufficient local conditions, not claimed necessary for every possible
distance asymptote, nor a complete geometry-selection criterion. In the examples
H1-H2 are checked by explicit free-geodesic flows, while H3 can pass or fail.

## 2. Uniform receiver control and the endpoint map

FCL's exact equation and norm estimate have constants depending only on the
common compact collar and initial bound. With W0=sup_a|w(x0,a)|,

    |w(x,a)|<=exp(Cx0)(x/x0)[W0+Cx0 log(x0/x)]             (1)

uniformly in a. This follows from dw/ds=-w-xF_geom, |F_geom|<=C(1+|w|),
s=log(x0/x), by the same integrating-factor inequality on finite intervals.
No additional population rest law is used. Consequently gamma->1 and
dy/dx=-Nh^-1w/gamma=O(x[1+log(x0/x)]) uniformly. Integrating gives

    Y(x,a)=F(a)+O(x^2[1+log(x0/x)]),
    partial_x Y(x,a)->0                                (2)

uniformly. Uniform limits of the continuous finite-x flow give continuous F.
H2 then gives D_aF=J: integrate D_aY along each short label line segment and
pass to the uniform limit. Equations(2) and H2 give a joint one-sided C1
extension Y(0,a)=F(a), partial_xY(0,a)=0. No C2 boundary extension is needed.

The null-incidence equation is

    Y(x,a(x))=z(x).                                     (3)

The local implicit-function theorem at (0,a_*) gives a unique C1 label curve
a(x) for small positive x. A one-sided C1 extension, e.g. Y(x,a)=F(a) for
x<0, suffices as a mathematical IFT device. It adds no physical exterior.
Differentiate (3) at0:

    a'(0)=J(a_*)^-1 z'(0),
    L(x)=L_*+d x+o(x), L_*=L(a_*).                       (4)

When d<0, L is strictly decreasing with x close to0 and can be inverted there.
Thus the actual incidence derives

    x_o(L)=(L_*-L)/c+o(L_*-L).                          (5)

H2 ensures a local noncrossing label map near this endpoint. It is not a
statement about every earlier receiver crossing or the full null cone.

## 3. The actual received-frequency and distance limit

The physical affine ray tangent is k=x^2 kbar. From the uniform receiver
estimate, T=u/x tends to the future b-unit normal n_p along the actual
intersection a(x). Thus B(x)=-b(kbar,T)->B_*=-b_p(K,n_p)>0, and R6 gives

    Z(x)=1/[x B(x)],
    (L_*-L) Z -> c/B_* >0.                              (6)

This is a fixed-emission comparison among differently located free receivers.
It does not reuse the varying-emission one-receiver quantifier silently.
Emission normalization is common along the one fixed ray; local variations
for the actual received-tick derivative are taken separately on each receiver.
No independent redshift function is attached after the metric readout.

The coefficient is physical for this specified distance/preparation: under
x'=a0 x+o(x), c'=c/a0 and B_*'=B_*/a0, so c/B_* is unchanged. For the
same-correspondence scalar clock leg,

    (1+chi_clock)/(L_*-L)^2 -> 2 B_*^2/c^2.              (7)

This is scalar evaluation on the actual correspondence, not a full pair-plane
construction, selected scale or X_max. Equations(5)-(7) are endpoint limits,
not full-history monotonicity or a native physical distance law. A global
first-arrival domain and later future return require their own causal data.

## 4. Exact positive preparations and one-way/echo domains

Use the supplied g=x^-2(-dx^2+dy^2+dz^2+dw^2), future x decreasing. Sigma is
x=1 with induced Euclidean metric. Source is the ordinary free clock y=z=w=0,
emitting at e=(1,0,0,0). Initial radial distance is L=|a|. Fix the outgoing
ray q(x)=(x,1-x,0,0), kbar=(-1,1,0,0), omega_e=1.

For constant spatial momentum vector P, every prepared receiver is exactly

    gamma_x=sqrt(1+|P|^2 x^2),
    u=(-x gamma_x,x^2 P),
    Y(x,a)=a+(1-x^2)P/(gamma_1+gamma_x),
    F(a)=a+P/(gamma_1+1).                               (8)

The spatial Killing momentum is constant and unit normalization supplies u;
direct geodesic equations independently check (8). P may also be a smooth
function of the INITIAL label a, held constant along each chosen receiver.
All label/position derivatives below respect that distinction.

For P=0, the receivers are normal to Sigma and remain coordinate-comoving.
Then a(x)=(1-x,0,0), L=1-x and

    Z=1/x=1/(1-L), 0<L<1.                               (9)

This familiar supplied homogeneous control has an exact distance pole. It is
not silently called PSW parallel preparation: ambient parallel transport of
the source tangent along the coordinate straight path in Sigma gives
U=(-cosh L,-sinh L,0,0), not the constant normal U=(-1,0,0,0). PSW in turn
uses an ambient spacelike geodesic for its position preparation, not necessarily
this Sigma path. These are explicitly different queries in the same metric.

For any fixed finite P=p e_y (p may be nonzero), define

    D_x=p(1-x^2)/(sqrt(1+p^2)+sqrt(1+p^2 x^2)),
    L(x)=1-x-D_x,
    L_*=1-p/(sqrt(1+p^2)+1),
    Z=1/[x(sqrt(1+p^2 x^2)-p x)].                       (10)

L'(x)=-1+p x/sqrt(1+p^2 x^2)<0, L(1)=0, L(0)=L_*>0.
Thus the exact one-way range is 0<L<L_* and (L_*-L)Z->1. Each example has
finite uniformly bounded motion and J=I. The initial source/receiver velocities
differ if p!=0, so a near-zero-distance Doppler contrast is allowed; it is not
a violation of ordinary local physics or a universal positional coefficient.

For ideal immediate return to this source, the return null leg from q(x)
reaches y=0 at x_A=2x-1. Hence an echo exists exactly for x>1/2 in these
collinear controls: L<1/2 for p=0 and L<L(1/2) for fixed p. Its loss near the
one-way endpoint is causal domain loss, not a material wall or failed clock
law. Conformal Minkowski causal structure makes these actual first arrivals;
no global domain claim is transferred to the arbitrary RG theorem.

## 5. Smooth bounded preparation with a different distance exponent

The same supplied metric admits an exact preparation showing H3 is not implied
by smooth bounded data and noncrossing. Work in a sufficiently small compact
ball of initial labels near a_*=(1,0,0), writing a=(1+r,v,w). Prescribe the
endpoint map and constant-per-receiver momentum by

    F(a)=(1-v,r+v^2,w), d(a)=F(a)-a,
    P(a)=2d(a)/(1-|d(a)|^2).                            (11)

Choose the ball so |d|<1. Equation(8) then yields exactly this endpoint map,
since P/(sqrt(1+|P|^2)+1)=d. All initial velocities and their derivatives are
smooth and bounded on this fixed compact ball. There is no field equation or
metric fitted to this example: only the freely supplied receiver preparation
is chosen to test transversality. Its emitter/initial-distance definition is
the same as section4; initial receiver directions need not stay radial.

At a_*, P=0 and J=D_aF is the90-degree rotation in the first two coordinates,
with the third direction fixed. Along the whole x in[0,1] base receiver,

    D_aY=x^2 I+(1-x^2)J,
    det D_aY=x^4+(1-x^2)^2 >=1/2.                       (12)

Its smallest singular value is at least1/sqrt(2). On a sufficiently small
common label ball, uniform continuity bounds the derivative's difference from
this base matrix by less than1/(2sqrt(2)). The integral along label segments
then gives a uniform lower Lipschitz bound, proving local injectivity/noncrossing
for all x in[0,1], not merely a nonzero determinant at one point. The full
flow is analytic here and H1-H2 hold. But D L(a_*)=(1,0,0) and
J^-1 z'(0)=(0,1,0), hence d=0.

Exact flow can be written Y=F-P x^2/(gamma_x+1). Along the actual incidence,
a(x)-a_*=O(x), P(a(x))=O(x), so F(a(x))=z(x)+O(x^3). Equation(11) gives

    a_2(x)=x+O(x^3), a_1(x)=1-x^2+O(x^3), a_3(x)=0,
    L(x)=1-x^2/2+O(x^3), 1-L=x^2/2+O(x^3),
    B(x)->1, Z~1/x,
    (1-L)Z->0, sqrt(1-L)Z->1/sqrt(2).                  (13)

Analytic implicit dependence controls the remainders and their derivatives;
L increases toward1 on the late branch as x decreases. Thus redshift still
diverges, but has a square-root distance pole for this specified family.
This is a bounded-motion attachment degeneracy, distinct from CCW's unbounded-
boost cancellation Z=1. It does not refute a radial parallel-prepared law or
the intended positional asymptote. The initial direction/motion varies along
the sampled label curve. It demonstrates why distance alone cannot hide that
preparation information. The late local branch has no immediate echo since
its ray receptions have x<1/2.

## 6. Return and unresolved boundaries

The conditional question now has a precise positive answer: uniform free-clock
control plus a regular invertible endpoint map and nonzero initial-distance
transversality yields an actual simple distance pole, with coefficient derived
from the supplied metric/ray/preparation. Smooth bounded preparation alone is
insufficient for that sufficient-condition chain; section5 specifically shows
transversality can fail even with the other attachment conditions satisfied.

Automatic H2/common-collar admission for arbitrary C3 data, global branch
availability and a universal physical preparation have not been proved.
CCW's unbounded-boost family remains outside H1; FCL's pointwise theorem is
unchanged. Native RG admission, event/path assignment, additional-effect
attribution, scale and X_max remain open. A supplied positive example is not
a physically selected UDT model, and no complete-postulate insufficiency or
need for an added physical premise is established. Review, exact controls and
central descendant checks precede any reviewed return. No successor is started.
