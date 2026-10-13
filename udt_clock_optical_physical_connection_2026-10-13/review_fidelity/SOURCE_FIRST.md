# COC1 physical-fidelity source-first reconstruction

Saved before exposure to any COC1 researcher candidate, code, outputs, parent
notebook/conclusions, or sibling review. This is an initial independent argument,
not a final review verdict. Date: 2026-10-13, UTC save time in source receipt.

## Context, authority and exposure

Reviewer context: `/root/coc_review_fidelity`, a separately spawned fresh context.
Model: inherited parent model, exposed runtime identifies Codex/GPT-6 but supplies
no independently verifiable precise serving-model identifier. Same inherited model;
different-model, human-specialist and formal-proof independence are UNTESTED.
No nested agents. Argument: source-first reconstruction and concrete analytic
controls. Implementation: none yet; no numerical output consulted or generated.

Parent continuing-session startup is attributed at synchronized
`grok1fca5f6962169b680d7726564a3a62f95ee0277a`, with its full406 pass and preservation
inventory. I independently checked branch and HEAD at that exact revision. The
tracked-status check showed LIVE.md and HANDOFF.md modified; I did not read their
campaign changes. A normal porcelain line count was 74 (not a count of individual
files inside untracked directories); I do not substitute it for the parent's
76-name preservation inventory. No protected payload was inspected, hashed or used.
No synchronization, global premise-verifier replay, Git mutation or central edit.

Read method sources: AGENTS; CLAUDE How we work, DRIVER TRIGGERS, Reviews and
decisions, Runtime guardrails and Repo discipline; no-shortcuts, completeness-map,
verifier-before-record; CROSS_MODEL_VERIFY; goal-directed-research and the relevant
operating-plan discovery/review/stop sections. Read COC1 WORK_ORDER and
SOURCE_FIRST_REVIEW_PACKET. Retained scientific exposure: central D1/R6,
R7GRC/R8PSW/R8GRC/R8PCC/R8CMF/R13; original PCC1 initial argument, PSW1 controlling
repair, CMF1 repair/reviewed scope, GRC1 B candidate sections 2–3 and GRC1
clarifications. Exact file pins accompany this note. Prior reviewed-source proofs
are disclosed exposure; this is not blind reconstruction of those older theorems.

The working scientific scope is W4's one metric for ordinary clocks, rulers,
free fall and null rays. It supplies no light microphysics, field equation, chosen
reference or positional-attribution law. GR stays FILTER ONLY. CMF1 already
reconstructs total scalar curvature, so scalar reconstruction is not a first claim.

## Independent clock-duration cone calculation

Fix a smooth time-oriented Lorentz4 metric with signature -+++ and the retained
curvature convention. Fix an event p, future unit U, spatial unit n and
k=U+n, normalized by -g(k,U)=1. A is freely falling, p=A(0), q=A(2l), and
the relay event is the unique small regular intersection of the outgoing
generator with the past cone of q. The frame is fixed while l tends to zero.
The ideal relays have no delay. Units use the independently calibrated c_E=1.
These are supplied query/preparation choices, not selected physical populations.

Let e=A(n,U,U,n). Fermi coordinates along A give radial quadratic jets
g00=-(1+e r²), g0n=0, gnn=1. Curvature variation and transverse path changes
do not affect the cubic radial travel-time term. Integrating outgoing and incoming
null travel times gives t_cut=l+O(l^4), r_cut=l+e l³/6+O(l^4).
The source-normalized affine parameter obeys
lambda=r+e r³/6+O(l^4), hence

    lambda_cut = l + e l³/3 + O(l^4).

This Fermi calculation freezes e only for its displayed coefficient; it does not
postulate static geometry. In a full proof, rescaling by l and smooth transverse
incidence must justify the regular remainder, including angular dependence.

The vertex Jacobi determinant at fixed affine parameter is
lambda²[1-Ric(k,k)lambda²/6+O(lambda³)]. For an angularly dependent cut,
differentiation adds k times the cut's angular derivative. Since k is null and
orthogonal to the vertex angular Jacobi fields, these terms do not change the
induced two-metric. Therefore my source-first candidate coefficient is

    dA/dOmega = l²[1 + H(U,n) l² + O(l³)],
    H(U,n) = (2/3) A(n,U,U,n) - (1/6) Ric(U+n,U+n).

This area is the intrinsic area of the spacelike cone intersection, not a spatial
maximal surface, fixed affine cut, flux or brightness. Source angular coordinates
must use the source rest-frame sphere with its usual calibrated solid angle.

Using mean(n_i)=0 and mean(n_i n_j)=delta_ij/3,
mean(e)=Ric(U,U)/3 and mean(Ric(k,k))=(4 Ric(U,U)+R)/3. The timelike contractions
cancel:

    A_edge/(4 pi l²) = 1 - R l²/18 + O(l³).

The integrated leading coefficient is total scalar curvature and is frame
independent. Requiring its nonpositive matched contrast in every frame adds only
Delta R>=0; it does not require Einstein Ricci or full curvature isotropy.

Analytic sign/normalization controls:

1. de Sitter curvature K: center-clock diamond edge radius is
   tanh(sqrt(K)l)/sqrt(K), giving normalized area 1-2K l²/3+O(l^4).
   Here e=-K, Ric(k,k)=0 and R=12K, agreeing with both formulas. An affine-cut
   area has no such leading scalar term: the clock cut has moved.
2. Ultrastatic -dt²+h_K: its edge is the spatial radius-l sphere, with area
   4pi sin²(sqrt(K)l)/K. Thus coefficient -K/3=-R/18 even though this central
   frame has zero electric tides and stationary clocks have unit received ratios.
3. Schwarzschild at a regular point: Ric=0 and electric eigenvalues
   (-2w,w,w), w=mu/r³. Directional coefficients are (-4w/3,2w/3,2w/3), while
   the integrated leading coefficient vanishes. Neither zero scalar nor zero
   integrated coefficient means flat geometry or absence of clock/lensing effects.

## The all-direction, all-prepared-frame sign is much stronger

For a matched pair with time-oriented tangent isometry I, matched clock units,
source frame and protocol, put D=A_g-I*A_g0 and deltaH=H_g-H_0. Suppose the
explicitly UNADOPTED trial is deltaH(U,n)<=0 for every U,n. The sign condition is

    4D(n,U,U,n) <= Delta Ric(k,k).

Boost within the U,n plane. Then k_eta=exp(eta)k while the plane curvature
D(n_eta,U_eta,U_eta,n_eta)=e_D is unchanged. For all finite eta the trial reads

    4e_D <= exp(2eta) Delta Ric(k,k).

Taking eta->-infinity gives e_D<=0: the retained directional clock condition S.
Taking eta->+infinity gives Delta Ric(k,k)>=0: the retained optical condition F.
Conversely S and F give the cone-area sign immediately. Thus the directional
trial is equivalent to S+F, whose retained null-screen rigidity argument yields

    D=kappa B_g, kappa>=0;  deltaH=-2kappa/3.

This is a single geometric protocol encoding two prior conditions, not an argument
that W4 or positional interpretation adopts either one. Both boost limits occur
after extraction of the fixed-frame local coefficient. Smoothness on its own
gives no common finite l across unbounded boosts. Finite angular/boost sampling
does not establish the universal statement. The integrated sign alone lacks this
rigidity and must never be substituted for the directional premise.

## Attribution, reference subtraction and regional compatibility

Clock records and area records depend on the same total metric. They can identify
contractions or, with sufficiently rich preparation, metric curvature. They do not
label which part is positional, ordinary gravitation or matter. Covariance of a
contraction does not select its cause. A locally measured R is already within
CMF1; the new protocol could change required ideal measurements, not this logical
limitation. A decomposition needs a supplied reference/physical separation rule.

Concrete ambiguity: for one supplied space form of curvature K, using a matched
space-form reference K0 gives kappa=K-K0. The sign and magnitude of the
additional coefficient can change while all actual total records are unchanged.
This is a pair of real local geometric controls, not an assertion that every
arbitrary regional subtraction is realizable by a reference metric. Calibration
of c_E supplies units and does not remove this ambiguity.

Pointwise null-screen data Q_k(x,y)=D(x,k,k,y) have a one-dimensional algebraic
curvature kernel D=kappa B_g when all null directions/screens are supplied.
They miss kappa including its sign. Adding clock-cut information accesses that
component. However pointwise blindness does not imply complete finite lensing
equivalence: propagation paths, cut locations and endpoint normalizations can
differ in the two metrics.

Across a region smooth event/frame matching is additional data. If D=kappa B_g,
write S=I*Ric[g0]; then Ric[g]=S+3kappa g. Physical contracted Bianchi gives

    3 d kappa = div_g S - (1/2)d tr_g S.

This is necessary, not sufficient for full curvature realization. The reference
Bianchi identity cannot annihilate the right side because its connection differs.
The retained FLRW comparison H0=t, H=t+c has kappa=2ct+c², an explicit regional
counterexample to general constancy. By contrast an Einstein reference
Ric[g0]=Lambda0 g0 with constant Lambda0 makes S=Lambda0 g and forces constant
kappa on a connected regular physical region. Ric[g]=(Lambda0+3kappa)g then
follows; equal matched Weyl remains extra. Einstein Ricci is not constant
sectional curvature; nonzero Weyl is still possible.

GR-recovery controls make the reference choice substantive. Comparing total
Schwarzschild to flat space cannot pass the all-direction sign since w!=0 has
both tidal signs. Comparing Kottler f=1-2mu/r-kappa r² to Schwarzschild with
the same mu and matching areal frames gives D=kappa B while retaining ordinary
nonzero Weyl. Thus this rule may constrain an added difference without erasing
the retained weak-field Weyl sector, but only after the matching/reference choice.
Choosing a flat reference universally would instead make the full curvature a
space form and conflict with the nonzero Schwarzschild comparison sector.

As a separately imported GR comparison, if one supplies
G_ab+Lambda g_ab=8pi G T_ab, its trace is R=4Lambda-8pi G T.
For perfect-fluid comparison data T=-rho+3p, R=4Lambda+8pi G(rho-3p).
Thus dust trace and Lambda can both contribute positive measured R; radiation can
have R=0 with nonzero Ricci. This is a transparent algebraic ambiguity, not an
adopted UDT matter model, source or equation. Geometric scalar reconstruction
alone cannot distinguish those imported interpretations.

## Physical preparation and explicit error controls to demand

An intrinsic area assigned by a supplied metric is not yet an actual area
measurement. The clock supplies l and its source tetrad supplies angles, but
relay positions need a realizable geometry/preparation/readout procedure that
measures transverse lengths or an independently justified equivalent. Brightness
does not supply that area without emission, propagation and detector laws, all
absent here. A continuum of appropriately placed immediate relays is an ideal
event-locus protocol. Its geometric well-definition is useful and does not certify
an instrument, a realizable observer population, negligible backreaction or
finite experimental angular coverage. One could investigate those missing
interfaces, but cannot announce them delivered by the area theorem.

Central free fall is load-bearing. In flat space, a constant-proper-acceleration
clock A(tau)=(sinh(a tau)/a,(cosh(a tau)-1)/a,0,0) has endpoint interval
s=2sinh(a l)/a for the same clock duration 2l. The null-cone intersection has
exact total area pi s², hence

    A_edge/(4pi l²)=sinh²(a l)/(a²l²)=1+a²l²/3+O(l^4).

A scalar estimator that assumed free fall would report R_est=-6a² although R=0.
In source angles its directional radius is
lambda/l=1+a l cos(theta)+a²l²[cos²(theta)-1/3]+O(l³), producing an O(l)
directional contamination as well. This is a concrete query mismatch, not new
physics; accelerometer/preparation control or a derived correction is necessary.

For relative-area error epsilon_rel, coefficient error contains
epsilon_rel/l²; if using absolute area error epsilon_A it contains
epsilon_A/l^4. A fixed readout noise cannot be removed by taking l->0.
Independent duration error delta l perturbs area/l² by approximately
2 delta l/l, so its curvature estimate error scales as delta l/l³.
Sufficient ideal requirements include epsilon_rel=o(l²), delta l=o(l³),
bounded fixed-frame geometric remainder and controlled angular/preparation
errors. Nonzero relay delays must be independently bounded/corrected at the
corresponding duration order. These are conditions, not measured finite constants.
Smoothness supports local remainder existence but gives no experimental bound.

## Direct-review priorities and present uncertainty

Check the candidate's exact source event, cut definition, affine normalization,
area measure, and coefficients against this independent route. Look specifically
for swapping integrated and directional signs; unrecorded clock acceleration;
uniform-boost claims; total/additional conflation; automatic regional constancy;
brightness as area; and a claim that clocks alone already prepare/read the relay
surface. The strongest conditional theorem may survive all of these without
selecting physical reference, attribution or geometry.

No COC1 verdict, candidate review or attestation has yet occurred. My general
coefficient derivation is analytic and still needs direct proof scrutiny;
the exact controls above are independent checks of its signs and special cases.
No empirical, production, global, protected-branch or whole-corpus check occurred.
Await parent direct-review dispatch after notifying it of this saved note.
