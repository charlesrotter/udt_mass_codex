# FKA1 constructive continuation — clock maps, geometry and ruler comparison

Candidate supplement to INITIAL_CANDIDATE and REPAIR, for actual cross-review.
This route originated in the fidelity review when challenging the initial
return decision. Original derivations are preserved in
review/fidelity/CLOCK_MAP_REALIZATION.md and RADAR_TAPE_PROBE.md with freezes.
Their author is not an independent reviewer of this added construction. The
mathematical reviewer and explorer A perform later separate-context checks;
their actual reports own those claims. The coordinator independently recomputed
the metric/curvature algebra. This is not another blinded proposal or independent
original discovery by the coordinator.

## Scope and choices

Question: can specified mutual clock maps have a single geometric realization,
and does their completed ruler automatically equal a specified timing ruler?
Use common length-time units and choose Z>1, ell>0 and finite real epsilon.
The given maps are b=Za and a=Zb for a,b>0. These are opposite future
comparisons, not inverses. Their return map is a -> Z²a.

The maps, clock preparation, common origins, smooth metric family, null encoding
and immediate-return radar convention below are free-and-explored mathematical
controls. No physical metric, field equation, ruler protocol or new premise is
adopted. This is not an all-UDT model, no-go or sufficient realization of c_E's
full physical meaning. It tests precisely the stated clock data and calibration.

## One geometry realizes both clock maps

Define on the positive u,v quadrant with two flat transverse coordinates

    P=(v-u/Z)(v-Zu), H=P²/ell⁴,
    C=Z exp(2 epsilon H),
    g=-C du dv+dx_perp²+dz_perp²,
    g_uv=g_vu=-C/2.

The full quadrant avoids inferring all positive-time maps from a fixed finite
patch. Each finite query uses its compact connecting segments; no geodesic
completeness, global completion or boundary condition is asserted.

C>0 gives a smooth Lorentz metric. For t=(u+v)/2,
g inverse(dt,dt)=-1/C<0, so t is a time function. Choose

    A(a)=(a,a/Z,0,0),  B(b)=(b/Z,b,0,0).

Along each, H and dH vanish. Thus C=Z, dC=0 and g(A',A')=g(B',B')=-1.
The only nonzero possible radial Christoffels are Gamma^u_uu=partial_u log C
and Gamma^v_vv=partial_v log C. They vanish on these constant-tangent curves,
so both clocks are freely falling with a,b their proper-time parameters.
P=u²-(Z+1/Z)uv+v² is symmetric under u↔v; that isometry exchanges the clocks.
This particular exchange symmetry is not an all-observer universality theorem.

The future null segment u=a joins A(a) to B(Za); v=b joins B(b) to A(Zb).
They admit increasing affine parameters since C v'=constant or C u'=constant
along the respective ray. Hence one geometry represents exactly both stipulated
maps, ordinary clocks and the return record, for every epsilon. This is a
conditional representation of the clock relation, not a separate propagation
cause placed upstream of the postulate.

The family contains genuinely different geometries. Direct contraction gives

    Ric_uv=-partial_u partial_v log C,
    R=(4/C) partial_u partial_v log C=(8 epsilon/C)H_uv.

At Z=2,u=v=ell, H=1/4 and H_uv=3/ell², so
R=12 epsilon exp(-epsilon/2)/ell². The epsilon=0 member is flat; every
nonzero finite epsilon has nonzero curvature there. The same displayed clocks,
free preparations, timing maps and exchange symmetry do not distinguish these
flat and curved members. This is only nonuniqueness from that record set in
this supplied class, not from all UDT commitments or all possible measurements.

## A specified timing ruler tests the completed tape

Choose the immediate-return radar convention D_rad(a)=(Z²-1)a/2. This is a
function of the same records and an explicitly chosen synchronization convention,
not an assertion of an independent travel mechanism or a native ruler law.

Construct the actual endpoint-normalized affine ribbon F(a,lambda)=(a,V,0,0),
lambda in[0,1], by

    S(a)=integral from a/Z to Za of C(a,v)dv,
    integral from a/Z to V(a,lambda) of C(a,v)dv=lambda S(a).

C>0 gives a smooth V. Its tangents are K=(0,S/C,0,0) and J=(1,V_a,0,0).
Original metric contraction gives

    h00=-C V_a, h01=-S/2, h11=0, det h=-S²/4.

At epsilon=0, -h00=1+lambda(Z²-1)≥1. On each compact emission window
0<a0≤a≤a1, continuity gives a positive epsilon_* such that h00<0 on the
whole ribbon for |epsilon|<epsilon_*. This is an existence bound, not a claimed
universal numeric threshold. No whole-ribbon timelike-J claim is made outside
that range.

G176 completion on that regular ribbon has m=S(a)/2, constant along lambda.
The one-family completed tape is L_completed(a)=S(a)/2. At epsilon=0 it equals
D_rad. For positive epsilon, H>0 in the open ray interior implies C>Z and
L_completed>D_rad. For negative epsilon the strict inequality reverses.
These exact inequalities hold in the stated regularity range without quadrature.
The same clock maps and their matched endpoint kernels remain unchanged.

The comparison proves that equality to this specified timing ruler is a
substantive condition, not the result of normalization alone. Requiring it
would exclude all nonzero sufficiently small epsilon in this family, but that
requirement is not adopted. The completed tape is neither the null proper
length (zero) nor automatically a spacelike proper ruler. At epsilon=0,
m'(a)=(Z²-1)/2>0, so m d lambda is not a globally exact spatial coordinate
with the original clock leg. The tape integral is along each fixed-a family.

## Composition stays meaningful without a propagation premise

For regular clock maps f and k with finite strictly positive derivatives,
the derivative chain rule gives, at matched intermediate arguments,

    Z_(k composed f)(a)=Z_k(f(a)) Z_f(a),
    Phi_(k composed f)(a)=Phi_k(f(a))+Phi_f(a),
    D_f(a)=diag(Z_f(a),1/Z_f(a)),
    D_(k composed f)(a)=D_k(f(a))D_f(a).

Here Phi_f=-log Z_f; the G176/normalized-contrast representation gives

    chi_(k composed f)(a)
      =[chi_k(f(a))+chi_f(a)]/[1+chi_k(f(a))chi_f(a)].

Strictly positive finite slopes give |chi|<1 and positive denominator. The
inverse map has reciprocal slope at the matched event; an opposite physical
comparison need not be that inverse. This is actual-map composition, not a
universal endpoint potential, additive spatial distance or proof that the
physical time/length dual pairing follows from mutual slowing alone.

## Consequence for the return

This closes two concrete probes left incomplete by the initial candidate:
reverse construction of a common geometric realization and agreement with
an explicitly chosen timing ruler. It strengthens the positive side without
claiming native selection. No further numerical sampling of these exact
families would change their conclusions. A new informative argument would
need an admitted relation that selects or restricts the physical comparison/
ruler assignment, or an actual derivation of the contested dual-slot implication.
The current audit does not prove that such an argument is impossible or that
new physics is necessary. Reviewers still judge the proposed return.
