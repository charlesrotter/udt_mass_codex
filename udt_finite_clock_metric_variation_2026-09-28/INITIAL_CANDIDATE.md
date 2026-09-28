# FCV1 — first variation of the finite clock map

Initial candidate for adversarial review; CONDITIONAL, UNPROMOTED.
WORK_ORDER controls. This constructs an observable-response derivative and tests
its proposed direct identification with DDR's physical response. It assumes no
field equation and does not adopt an action, source or additional physics.

## 1. Domain and comparison protocol

Use a smooth one-parameter family of time-oriented Lorentz4 metrics g_epsilon,
signature (-+++), with h=partial_epsilon g_epsilon at zero. Proper time is in
length units, c_E=1. Smooth timelike worldlines z_e^epsilon(s),z_o^epsilon(t)
carry supplied increasing labels s,t. Their fixed-label displacements are
W_e,W_o. The fixed-worldline protocol is W_e=W_o=0; nonzero W makes the chosen
physical protocol explicit and permits a coordinate-covariance check.

Assume a convex-normal neighborhood for all relevant small epsilon, or a supplied
smooth nondegenerate geodesic branch admitting the same endpoint variational
formulas. All endpoint/metric/source-label derivatives below exist and commute.
The selected future-null incidence has a regular smooth arrival map t=A_epsilon(s),
with A'>0 and F_t!=0. No cuts, branch switches, multiple-image sum or caustic
continuation is asserted. No global completeness or physical population is chosen.

Define v_i=dz_i/d(label), N_i=sqrt(-g(v_i,v_i))>0, u_i=v_i/N_i. These quantities
are evaluated in the baseline metric unless epsilon is explicit. The proper-clock
ratio and logarithmic redshift are the existing G220/FSL1 observables

    Z_epsilon(s)=N_o^epsilon(A_epsilon(s)) A_epsilon'(s)/N_e^epsilon(s),
    D_epsilon(s)=log Z_epsilon(s).                            (1)

The geometric null-clock interface remains conditional. G176 supplies its
same-correspondence clock leg only when constructed as in G220; the full pair is
not assembled here. W4/W5 retain provisional status. Positional dilation remains
the founding interpretation of this geometry and c_E, not an extra term in (1).

## 2. Metric and endpoint variation of null incidence

Let F_epsilon(s,t)=sigma_g_epsilon(z_e^epsilon(s),z_o^epsilon(t)), with Synge
world function convention sigma=one half signed squared geodesic interval.
Parametrize each endpoint-to-endpoint geodesic affinely by lambda in [0,1].
The affine normalization is fixed by this interval, not by source frequency.
On the baseline null branch put k=dx/dlambda and omega_i=-g(k_i,u_i)>0.

The geodesic energy functional equals sigma:

    sigma = (1/2) integral_0^1 g(k,k) dlambda.

Vary it before imposing the null incidence. Integration by parts gives

    delta F = I[h] - g(k_e,W_e) + g(k_o,W_o) =: J,
    I[h]=(1/2) integral_0^1 h(k,k) dlambda.                   (2)

The interior displacement term is -integral g(nabla_k k,delta x)=0 by affine
geodesicity. Dropping that term is exact first-variation stationarity, not an
assumption that the physical ray stays fixed. Its changing shape is encoded by
the varied geodesic problem; source-label differentiation of I below includes
the dependence of the ENTIRE baseline ray family on s. All four components and
transverse motion are retained in (2); examples may use smaller symmetry classes.

Endpoint differentiation gives F_t=g(k_o,v_o)=-N_o omega_o, so null incidence
F_epsilon(s,A_epsilon(s))=0 implies

    V(s):=delta A_epsilon(s)=-J/F_t=J/(N_o omega_o).          (3)

F_s=-g(k_e,v_e)=N_e omega_e also recovers A'=N_e omega_e/(N_o omega_o), hence
Z=omega_e/omega_o. Equations(2)-(3) are standard variational geometry applied
to the existing comparison, not newly invented propagation physics.

## 3. Full clock-response derivative

At a fixed worldline label define b_i=delta log N_i. Covariant differentiation
of the squared clock tangent, including worldline displacement, gives

    b_i=-(1/2)h(u_i,u_i)-g(u_i,nabla_{u_i} W_i).

Differentiate (1) at FIXED emission label s. The exact result is

    Q(s):=delta D_epsilon(s)
       = b_o(A(s))-b_e(s) + [partial_t log N_o](A(s)) V(s)
         + V'(s)/A'(s).                                    (4)

This includes receiver clock normalization, source normalization, movement of
the arrival event and the change of the whole arrival slope. It is linear in
h,W under the stated differentiability hypotheses. For baseline labels chosen
as proper time along both worldlines, N_e=N_o=1 along the baseline curves,

    Q=(1/2)[h_e(u_e,u_e)-h_o(u_o,u_o)]
       -g(u_o,nabla_{u_o}W_o)+g(u_e,nabla_{u_e}W_e)
       +(1/Z) d/ds [J/omega_o].                             (5)

In particular the general derivative is not just the local fixed-K derivative
of a clock coefficient examined in RMS1. The remaining path term is load-bearing.

Holding the source's numerical PROPER time fixed across metrics is a different
explicit comparison protocol. Choose a fixed label s0 as common clock origin,
tau_e^epsilon(s)=integral_s0^s N_e^epsilon(q)dq. Then

    delta s|tau = -[integral_s0^s N_e(q)b_e(q)dq]/N_e(s),
    Q|tau = Q(s)+D'(s) delta s|tau.                         (6)

Other origins or observer-control rules require their own terms. No hidden
preferred observer or synchronization rule is selected. First variation is exact
at epsilon=0; no finite-epsilon error estimate or nonlinear evolution follows.

## 4. Coordinate covariance check

For a diffeomorphism pullback g_epsilon=Phi_epsilon^*g, use the corresponding
same physical worldlines z_i^epsilon=Phi_epsilon^-1(z_i). Thus
h=Lie_xi g=2 nabla_(a xi_b), W_i=-xi along each line. Affine geodesicity gives

    I[h]=g(k_o,xi_o)-g(k_e,xi_e).

The endpoint terms in J cancel this exactly. Also b_i=0 because
(1/2)h(u,u)=g(u,nabla_u xi). Consequently J=V=Q=0. This is the proper gauge
check. Holding the coordinate curves fixed during the same metric pullback would
change the physical protocol and need not give zero. Covariance of this observable
with its worldlines is not a proof of a metric-only off-shell divergence identity
for the unidentified E[g]; endpoint/worldline variations participate in the balance.

## 5. Reciprocal inversion differentiates to an identity

Let B_epsilon=A_epsilon^-1 on the same regular correspondence. The reverse
proper-clock map obeys

    D_reverse,epsilon(A_epsilon(s))=-D_epsilon(s).

This reverses the SAME paired-event map; it is not a later causal return. At
paired varying events its variation is simply -Q. At fixed receiver label
t=A(s), the inverse-label displacement and response instead obey

    delta B(t)=-V(s)/A'(s),
    Q_reverse(t)=-Q(s)+D'(s)V(s)/A'(s).                     (7)

The moving-argument term cannot generally be dropped. Same-path composition
likewise differentiates the chain rule with compatible intermediate events.
These identities hold for every smooth regular metric family in this query
class. Differentiating them supplies no equation restricting g.

This does NOT identify or discharge the already owner-adopted DDR postulate.
Current G310/G312 instead require a specified physical symmetric response E to
annihilate all reciprocal metric-shape tangents on solutions, giving TF(E)=0.
The inverse-clock identity alone does not state that Q vanishes under those
metric changes. That extra identification is tested next, not assumed.

## 6. Interior reciprocal-shape witness

Use a supplied Minkowski baseline in coordinates (t,x,y,z), source x=0 and
receiver x=L>0, both y=z=0 and parametrized by coordinate t, which is proper time
on their lines. Take any smooth nonnegative b(x), nonzero and compactly supported
inside (0,L). On a tube of the selected finite ray family define the exact
reciprocal metric family

    g_epsilon=-exp[-2 epsilon t b(x)] dt^2
               +exp[2 epsilon t b(x)] dx^2+dy^2+dz^2.       (8)

Extend t b(x) with smooth time/transverse cutoffs equal to1 on the relevant
compact tube if compact support is needed. The central rays remain in y=z=0;
the transverse derivatives vanish there. This is an ambient free-null comparison,
not an induced-sheet geodesic assumed to be ambient. Small epsilon and a bounded
emission interval give a regular branch by smooth ODE dependence. Metric (8) is
a supplied geometric test family, not a newly admitted UDT solution or cosmology.

At zero, h=2t b(x)(dt^2+dx^2)=t b(x) H(u,n), where u=partial_t,n=partial_x and
H is exactly G310's factor-two reciprocal tangent. tr_g h=0. The time-space
block determinant is -1 for every epsilon. Both observer neighborhoods remain
exactly Minkowski for all epsilon; clock normalizations on the endpoint lines
are unchanged. All endpoint metric jets agree with the undeformed metric.

The baseline ray is t=s+x, k=L(1,1,0,0), lambda=x/L, omega_o=L, A=s+L and Z=1.
Equations(2)-(5) yield, with B0=integral_0^L b(x)dx>0 and
B1=integral_0^L x b(x)dx,

    I=2L(s B0+B1),
    V=2(s B0+B1),
    Q=delta log Z=2B0>0.                                   (9)

Independently the exact outgoing null equation is dt/dx=exp[2 epsilon t b(x)].
Differentiating at epsilon=0 gives d(delta t)/dx=2(s+x)b(x), with initial
delta t=0. Differentiating its arrival with respect to s reproduces (9).
This is a nonzero original-equation response to an interior reciprocal metric
deformation, despite unchanged endpoint clock geometries.

For an exact algebra control only, L=1 and b=x^2(1-x)^2 give B0=1/30,B1=1/60,
V=s/15+1/30,Q=1/15. That globally polynomial control is smooth but NOT compactly
supported away from the endpoints: it checks the ray/clock calculation, not the
all-endpoint-jets assertion. The general smooth compact bump and positivity
argument above own that stronger assertion; a normalized artificial integral is
not being counted as its independent numerical verification.

Consequences are specific:

- Endpoint finite jets alone cannot determine this finite observable response.
- Directly requiring EVERY clock comparison to be stationary under EVERY
  compact reciprocal-shape metric change would reject this flat baseline query.
  Such stationarity is not an existing consequence of inverse-clock reciprocity.
- This does not refute UDT, prove flat finite cosmology is physically selected,
  or exclude a local equation governing g. Local equations can have observables
  depending on the whole path. The failed step is equating those distinct objects.

## 7. Why one measurement derivative is not a smooth local E

At fixed W=0 and a fixed regular query, Q[h] is a linear functional of metric
perturbations. If smooth compact h has support disjoint from the compact
baseline ray (including endpoints), it vanishes in a neighborhood of that ray;
nearby source-label rays miss that support too. Equations(2)-(4) then give Q[h]=0.
Its distributional support is contained in that ray, including endpoint terms.
It is not a query-independent smooth symmetric tensor at a spacetime point.

More sharply, suppose a smooth tensor coefficient C^{ab}(x) on a four-domain
represented this ONE measurement derivative as integral C^{ab}h_ab dV_g for
all smooth compact h. Tests supported off the ray force C=0 there; smoothness
then forces C=0 everywhere, since a finite regular ray has empty interior. This
would make Q identically zero, contradicting the compact-bump witness (9).
Even if testing is restricted to trace-free h, the same argument forces TF(C)=0
and contradicts the nonzero trace-free witness. Thus the direct smooth-volume
coefficient identification fails for this supplied query. Distributional
query-dependent sensitivity remains well-defined; calling it E would change
the response architecture rather than derive the current physical E.

This is not a theorem against deriving a local field law from some justified
local limit, collection of comparisons or physical variational principle. No
averaging measure, ray population, limit identification or stationarity principle
is supplied here. Adding one because it produces a desired field equation is
outside this work order. Local Metric Sufficiency applies to a local response;
it does not demand that every finite clock observable be local in endpoint jets.

## 8. Result of the attempted connection

We have an explicit full comparison-response formula (2)-(6), including true
metric change, receiver-event movement and gauge/clock-protocol terms. Same-map
inversion/composition remains an identity under that variation. The derivative
of one finite clock reading is query/path dependent and its direct identification
with a smooth local DDR response fails in the exhibited class. No native equation
selecting g has been derived by this attempt. A different justified physical
identification remains OPEN; no additional postulate is proved necessary.

Consequently there is no new dynamical candidate here on which to claim SR/GR
empirical correspondence or the FSL1 global asymptote. The explicit flat,
static-lapse and conformal controls are mathematical checks of the conditional
formula. They do not establish solar precision, cosmology, scale or X_max.
G310/G312, RMS1/CRV1 and the founding positional interpretation are unchanged.

## Method credit

G220 already uses the world function for null-clock incidence; FSL1 supplies its
finite frame/readout account. World-function/time-transfer methods also appear
in Le Poncin-Lafitte, Linet and Teyssandier, section2 of
https://arxiv.org/html/gr-qc/0403094v2 . We use the endpoint variational method,
not that paper's post-Minkowskian expansion, topology, gravitational constants or
physical light assumptions. Its signature is opposite ours. All first-variation
and clock formulas needed above are explicitly derived; no finite weak-field
approximation is substituted for the metric.
