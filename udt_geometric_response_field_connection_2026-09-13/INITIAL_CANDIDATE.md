# GFC1 initial conditional connection candidate

UNREVIEWED, CONDITIONAL UNPROMOTED. Hand discovery and prior-source exposure
precede this freeze; no new GFC1 check or reviewer outcome has been seen.
WORK_ORDER and SOURCE_MAP control scope. This is a mathematical relation between
two existing supplied constructions, not a new physical law or field identity.

## 1. One existing full metric and two different constructions

On M=I times an open(v,x,y) patch, I a connected interval in(0,infinity), use
NR2's complete metric, with the same supplied dimensionless display units:

 g=-2du dv+dx²+dy²+Hdu², H=2(x²-y²)/u².

All coefficients evolve; no frozen slice, weak-field or optical approximation.
Let k=partial_v, l=partial_u+(H/2)partial_v, so g(k,l)=-1,
k and l null, and k is parallel. Set T=(k+l)/sqrt2, N=(l-k)/sqrt2,
e1=partial_x, e2=partial_y. Then (T,N,e1,e2) is orthonormal, T timelike.
These are declared auxiliary frame fields, not physical observers or a
preferred universal reference frame. Every equality below compares mathematical
two-forms with the supplied coordinate/generator normalization; no physical
units, charge, impedance or constitutive normalization is identified.

G95 assigns to each supplied oriented spacelike screen E with orthonormal
frame(E1,E2) the local connection A_E=g(E1,nabla E2), F_E=dA_E.
Its response J_E=d(*F_E) is defined geometry; J_E=0 is not generic.
NR1/NR2 separately give, for their transverse Killing family,

 K=q partial_x+r partial_y+(q'x+r'y)partial_v,
 q''=2q/u², r''=-2r/u²,
 F_K=d(K_flat)=2du wedge(q'dx+r'dy).

NR2 additionally establishes the source-free aligned family
F_a=du wedge[a_x(u)dx+a_y(u)dy] for arbitrary smooth real a_x,a_y.
This is the existing family, not a new field equation adopted here.

## 2. Entire screen class compatible with the parallel null line

For every smooth oriented spacelike rank-two E contained in k-perp on the
local patch, an orthonormal screen frame has
E_i=O_i^j e_j+b_i k, where O is SO(2) and b_i are arbitrary smooth functions.
This follows because k-perp/span(k) has its Euclidean metric dx²+dy².
Since k is parallel and nabla e_j is proportional to k, its connection is
A_E=O_1^j dO_2^j, locally an exact rotation one-form. Consequently

 F_E=0 for EVERY such screen E.                         (1)

Changing the lift b_i or rotating a frame within E cannot alter(1). Local
curvature zero does not assert global trivial holonomy. The full spacetime
curvature is nonzero: R_uxux=-2/u², R_uyuy=+2/u². Thus this screen projection
misses nonzero null tidal curvature; it does not declare the metric flat.
In particular the existing q=u²,r=0 gives F_K=4u du wedge dx, nonzero on I,
and cannot equal any k-compatible F_E, even up to a nonzero constant factor.
This is a class-specific mismatch, not a no-go for all screen reductions.

## 3. Smooth two-component changes of the screen plane

Keep g and N fixed. For ANY smooth real w1(u),w2(u), put

 c=sqrt(1+w1²+w2²), S_ij=delta_ij+w_i w_j/(c+1),
 T_w=cT+w1 e1+w2 e2,
 E_i=w_i T+S_ij e_j.

Direct Lorentz-boost algebra gives g(T_w,T_w)=-1, g(E_i,E_j)=delta_ij,
g(T_w,E_i)=0; N remains unit and orthogonal. Hence E(w)=span(E1,E2)
is a regular supplied oriented spacelike screen for all w, including w=0.
The denominator c+1>=2 removes the polar-chart zero issue. Unless w=0,
E(w) is not contained in k-perp: g(k,E_i)=-w_i/sqrt2. Changing w is a
change of reduction, not an SO(2) gauge rotation within a fixed screen.

The original Levi-Civita formula gives

 A_w=[(w2*w1'-w1*w2')/(c+1)
       -(w2*H_x-w1*H_y)/(2sqrt2)]du
    =[B_w(u)-sqrt2*(w2*x+w1*y)/u²]du,                  (2)
 B_w=(w2*w1'-w1*w2')/(c+1).

Proof: g(e_j,nabla T)=-H_j du/(2sqrt2), with the same transverse
components for nabla N; nabla e_j=-H_j k du/2. Differentiating E_i
separates the moving-boost term B_w du from the ambient connection term.
In the latter, w2*S_1j-w1*S_2j=w2*delta_1j-w1*delta_2j. Differentiating
c²=1+w1²+w2² reduces the former to the displayed B_w. This contribution
must not be omitted from the CONNECTION even though its exterior derivative
vanishes for u-only profiles. Exact exterior differentiation yields

 F_E(w)=sqrt2/u² du wedge(w2 dx+w1 dy).                 (3)

Every full connection one-form in this u-dependent boosted frame is a
multiple of du, so its wedge-square is zero. With convention
[nabla_a,nabla_b]V^c=R^c_dab V^d, Cartan therefore also gives

 F_E(w)(X,Y)=g(E1,R(X,Y)E2).                            (4)

This equality uses this metric/frame dependence; general G95 reductions can
have nonzero off-diagonal/extrinsic wedge terms. It is not a universal rule
that arbitrary screen curvature equals one ambient-curvature component.

## 4. Exact relationship and its price in supplied data

Equations(2)--(3) give a bijection between smooth profile pairs w(u) in THIS
specified boost family and the existing aligned coefficient pairs:

 a_x=sqrt2*w2/u², a_y=sqrt2*w1/u²,
 w1=u²*a_y/sqrt2, w2=u²*a_x/sqrt2.                    (5)

It holds through all profile zeros and nodal events, with no polar phase
extension problem. It is not a bijection between all screens and all fields:
SO(2) frame gauge, other reductions and other field families are outside it.
For the existing Killing family, choose

 w1=sqrt2*u²*r', w2=sqrt2*u²*q',

and then F_E(w)=F_K exactly. In the simple q=u²,r=0 example,
w1=0,w2=2sqrt2*u³, A_w=-4uxdu and
A_w-K_flat=-d(u²x). Thus the local potentials also differ by an exact form.
This follows only after the explicit screen choice; it does not assert that
UDT selects it, that K is the screen connection, or that physical light uses
that screen. Matching an additional constant scale is absorbed into the
supplied target normalization and corresponding w, not selected by g.

Every(3) is closed, null where nonzero and divergence-free on the full metric:
raising gives F^{vx}=-a_x, F^{vy}=-a_y and antisymmetric partners,
sqrt(-det g)=1, so partial_a F^{ab}=0 by v/transverse independence.
Therefore these ACTUAL G95 screen connections have J_E=0 in the stated family.
Source-freeness is a derived consequence of this conditional geometric family,
not imposed as a new UDT law. G95's general nonzero-response counterexample
remains valid outside this restricted family.

## 5. Maximum conclusion and exclusions

There is an explicit positive connection: every existing aligned field on
this one metric has a representative as actual G95 screen curvature in the
declared smooth boost family. There is also a geometric restriction: screens
compatible with its parallel null line all give zero curvature. The extra
screen-profile functions encode the target field's freely supplied functions;
the metric/kernel does not select those choices by this calculation.

This removes this specified representation question from the list of merely
uncomputed joins, conditionally and pending review. It does not identify the
physical/native response, fix a reduction from metric alone, choose a unique
history, prove a new postulate necessary, or classify all metrics/screens/fields.
G179/G213's metric/complete-record bridge remains intact; G312 membership and
G351/G352 physical interpretation remain separate. No source/stress, photon,
Maxwell action, carrier, observation, scale, global completion or canon claim.
