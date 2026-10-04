# FCL1 exposed fidelity and operational-clock review

Verdict: **ACCEPT_WITH_LIMITS**. No substantive defect or mandatory repair was
found in INITIAL_CANDIDATE at SHA256
`9563063c01c69ffef69654915e522d0019192d7470fb41d2c88fbf438a3c8371`.
Acceptance is a review verdict on the stated conditional mathematical argument,
not adoption of RG, native geometry, an observer population, or canon.

Reviewer: `/root/fcl_fidelity`, fresh separate context with inherited model;
independent argument and analytic recomputation, no different-model or human
claim. SOURCE_FIRST.md was sealed at2026-10-04T01:12:21.978897+00:00, before
the candidate's recorded freeze at2026-10-04T01:12:57.554660+00:00. Hashes
establish file correspondence; the separate agent/tool record owns exposure
chronology. No sibling review was read. Parent reports were not used to build
the source-first proof.

Exposed artifacts read: INITIAL_CANDIDATE.md, CANDIDATE_FREEZE.json,
CHECK_PLAN.md, check_controls.py, and checks/parent_controls.{stdout,stderr,json}.
All four frozen file hashes match the actual files. Both stream hashes match
their capture receipt. The source-first report and its seal remain unchanged.

## Mathematical seam and hidden-bound audit

1. The supplied endpoint permits a final curve segment in a relatively compact
   normal collar. Local bounds on N, h, h^-1 and first derivatives follow from
   C3 metric/defining-function data and the flow chart; no late-velocity bound
   is imported. The normal-flow chart removes the shift by coordinates without
   deleting spatial metric components or imposing a homogeneous metric ansatz.
   C3 inputs give a C2 flow chart and at least C1 metric coefficients, enough
   for the displayed momentum equation and estimates.
2. Direct differentiation of P_i=w_i/x using dx/dtau=-x gamma/N gives
   dP_i/dtau=-(gamma/N)(dw_i/dx-w_i/x). Contracting the exact lowered geodesic
   equation gives the candidate's RHS and therefore its force
   F_i=(partial_i N)gamma-N(partial_i h_jk)T^jT^k/(2gamma).
   The signs and x factors are correct. This derivation uses partial_i x=0
   as a coordinate identity, not a spatial-uniformity assumption.
3. h's uniform positive bounds give gamma comparable to sqrt(1+|w|^2) and
   |T_spatial|<=c|w|. Thus |F|<=C(1+|w|). No inference of bounded |w| occurs
   before this force estimate. With s=log(x0/x), the upper norm derivative
   obeys r'<=(-1+Cx0 exp(-s))r+Cx0 exp(-s), including r=0 by the norm's
   upper right derivative. Multiplication by
   exp(s-Cx0[1-exp(-s)]) gives a forcing at most Cx0; integrating proves
   the candidate's explicit bound. This is valid for arbitrarily large fixed
   finite r(x0). Its constant depends on that particular receiver.
4. The rate w=O(x(1+log(x0/x))) implies the claimed coordinate-displacement
   estimate by integration to the supplied endpoint. Bounded first derivatives
   then give N-N(p)=O(x); gamma-1=O(x^2(1+log(x0/x))^2). Subtracting
   -N(p)/x from d tau/dx leaves an integrable remainder. Thus the stronger
   logarithmic proper-time formula with bounded, indeed convergent, additive
   remainder is supported. It is stronger than, and consistent with, my
   source-first coordinate-free convergence proof.

The independent source-first proof controlled gamma with a tensor estimate,
then q=gamma^2-1. The candidate controls a spatial covector directly. These are
distinct analytic arrangements of the same admitted geodesic equation, not
different physical equations or a claim of different-model verification.

## Actual clock, affine normalization and gauge

My source-first review independently derived R6's clock relation, including
varying affine endpoint coordinates: additional endpoint derivatives are
multiples of k and disappear on contraction with null k. Therefore the
candidate can legitimately use Z=d tau_o/d tau_e=omega_e/omega_o on its
specified smooth branch. It does not require a fixed affine interval across
the family and cannot use separate emission/reception normalizations.

**Finite-regularity seam checked directly.** R6/FSL1's prose says smooth, which
is not automatically a claim that a C3 metric is C-infinity. The identity used
here requires only a C2 two-parameter ray map F(s,lambda), a C1 metric and its
Levi-Civita connection along the rays: k=partial_lambda F and
J=partial_s F are C1, their mixed partials commute, metricity gives the
derivative of g(k,J), and differentiating the null norm once in s gives
g(k,nabla_J k)=(1/2)J[g(k,k)]. All these operations are classical at that
regularity. The admitted gbar,Omega are C3, so g is C3 at every interior
event and its connection is C2; the stipulated regular smooth ray family
supplies at least the C2 variation required. The argument can be performed
in the original chart, without any need to assign extra smoothness to the
normal-flow chart. Endpoint limits only need continuity of the already
controlled factors. Thus the actual R6 identity extends directly to this
finite-regularity scope; no unproved C-infinity premise is being imported,
and no global family regularity or caustic theorem is inferred.

The interior emitter limit keeps x_e positive and its proper tangent regular.
The supplied regular nonzero future affine-data extension makes the emission
normalization factor tend to a finite positive value. Applying that one factor
along each whole ray preserves a nonzero future endpoint K. The geodesic
limit supplies T_o->n_p, so B_o=-gbar(kbar_o,T_o) tends to a finite positive
number. Thus x_o Z->1/B*>0 is justified. The branch regularity is a supplied
premise and has not been derived from receiver convergence.

There is no false positive physical-frequency limit in the candidate. Its
formula omega_o=x_o B_o entails omega_o->0; B_o is the positive finite
*rescaled* frequency factor. A useful final-report presentation is to state
that consequence explicitly. It is not a required mathematical repair.

The regular conformal-gauge transformation in the candidate is correct:
holding physical u,k fixed yields T'=T/a, kbar'=kbar/a^2, B'=B/a and
x' Z=a x Z. Z is invariant while the defining-function residue changes.
The logarithmic coefficient N(p)=1/sqrt(-gbar^-1(dx,dx)) is consistent under
regular gauge changes, but none of this selects its physical value.

The emitter parameter varies while one receiver approaches its boundary
endpoint. No fixed-emission distance interpretation, uniform population
bound, actual boundary reception, echo claim, X_max value, physical clock
anomaly or microscopic light law is asserted. The supplied boundary normal
is a mathematical limit, not a newly selected finite-time observer population.

## Independent recomputation of the saved controls

I inspected the actual code and saved stdout, rather than taking PASS as
evidence for the theorem. The receipt reports returncode0,0.4172915399540216s,
maxRSS49364KiB,2GiB virtual-address limit and no wall/CPU timeout. These are
capture-record observations, not an independently repeated performance run.
The saved result has Python3.10.12 and SymPy1.13.1, six nonuniform point/velocity
cases plus two exact worldline controls. No reviewer script was run.

For g=x^-2 eta with future x decreasing, independently let
gamma=sqrt(1+x^2). The saved free receiver is

    u=(-x gamma,x^2,0,0), y=2-gamma, x_e=y+x.

Its norm is-1 and d y/dx=-x/gamma=u^y/u^x. Direct conformal connection
evaluation gives zero acceleration: the x-component derivative is x+2x^3
and its connection term is-(x+2x^3), while the y terms are-2x^2 gamma and
+2x^2 gamma. A ray from (x_e,0) reaches (x,y) because y=x_e-x. The emitter
has d tau_e/dx=-x_e'/x_e; receiver d tau_o/dx=-1/(x gamma). Since
x_e'=(gamma-x)/gamma,

    Z = x_e/[x(gamma-x)],       x Z -> 1.

This independently matches the saved actual clock ratio and limit; it does
not merely reinsert the endpoint theorem into a test.

The saved accelerated receiver is

    u=(-(1+x^2)/2,(x^2-1)/2,0,0),
    y=1-x+2 arctan x,          x_e=1+2 arctan x.

Its norm is-1 and y'=(1-x^2)/(1+x^2)=u^y/u^x. Direct differentiation gives

    acceleration=((x^2-1)/(2x),-(x^2+1)/(2x),0,0),
    g(acceleration,acceleration)=x^-2.

The actual proper-time ratio is

    [-2/(1+x^2)] / [-2/((1+x^2)x_e)] = x_e -> 1,
    x Z -> 0.

These equal the saved values and show precisely why the free-geodesic
hypothesis matters. The physical acceleration is nonzero and unbounded near
the endpoint; this is not a counterexample within FCL1's admitted class.
Both controls have x_e in[1,3/2] on0<x<1/4, so their interior-emitter claims
are consistent with the displayed formulas.

For one nonuniform saved case, independently recomputing the omitted force
at (x,y,z,v)=(1/2,1/3,-1/4,1/5) with orthonormal spatial velocity(3/4,0,0)
gives gamma=5/4, N=13697/12012 and a1=107/90. Consequently

    F_y=5/28-3N/(50a1)=9259/76505,
    F_z=5/44,                 F_v=5/52.

This matches the first saved omitted-force row. The omitted-force assertion
would therefore fail for a force-free spatial momentum equation. I inspected
the remaining five rows and their code path but did not independently replay
each arithmetic case. Their shared-code regression status is not inflated
to an independently coded sweep. The general proof retains arbitrary h_ij;
the diagonal finite controls alone would not cover that generality.

## Scope, survivor and review omissions

The strongest supported survivor is the candidate's conditional local theorem
and its supplied regular-null-family clock corollary. No narrowing beyond the
authorized CPW1 successor premises is needed. FCW1's beta2 failure of the
nonzero-gradient premise and interior-bump nonuniqueness are retained.
No Einstein, action, source, scale-selection or native-light equation entered
the proof. RG remains UNADOPTED, and the theorem does not show that complete
UDT needs to acquire a new premise.

No substantive defect, numerical failure or same-premise repair request is
outstanding in this review. The optional direct omega_o->0 sentence above is
presentation advice. The unused reviewer-control budget need not be spent
to duplicate the same symbolic code: the load-bearing mathematical argument
and actual-clock controls have been independently recomputed analytically.

Not repeated: all six exact nonuniform cases, capture utility/runtime tests,
source-package suites, premise406 audit, maintenance suite, global ray/caustic
existence, uniform families, native physical admission or empirical matching.
Parent closure and later integration review own their respective gates. This
review made files only under review_fidelity and preserved unrelated/protected
work. A final integration review should check that central/public wording
retains these quantifiers, grades, source bindings and exclusions.
