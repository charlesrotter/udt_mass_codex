# FCW1 operational proposal — what an exterior clock network can miss

Status: **INITIAL PROPOSAL / UNREVIEWED CONDITIONAL ARGUMENT**, one target.
This is the simulated operational/Feynman-inspired role, not a claim about any
physicist's views or endorsement. Context `/root/erc_fidelity` is explicitly
**REUSED**, with earlier ERC1 source-first/direct/final review exposure. It is
separate from the other FCW1 proposer contexts but is not fresh. Exact inherited
model/runtime identifier unavailable; no different-model independence claimed.
I have not read or received the other FCW1 proposals before sealing this file.

Parent attributes synchronized grok b90ede0302bcb9c841df3f594ca25b84b4fea107,
clean tracked tree,76 preserved old untracked names, no host scientific workers
and the prior full406 pass. I independently checked branch/HEAD and absence of
tracked dirt and read AGENTS, current LIVE/HANDOFF blocks, this WORK_ORDER,
CLAUDE sections and relevant method protocols. I did not replay top-level startup
or full406, inspect protected payloads, or read unrelated historical datasets.
The work order's initially intended fresh third proposer was unavailable;
the explicit parent dispatch authorizes this disclosed reused context instead.

## One precise proposed connection to test

**Trial N: exterior null-comparison sufficiency.** Fix a regular open laboratory
region U in one Lorentz4 geometry. Supply every ordinary proper-clock worldline
segment whose preparation and motion remain in U, together with all regular
null branches connecting its events, possibly passing through an interior region
V outside U. Include complete first-arrival maps, both independently emitted
directions, future echo maps, finite tick intervals, endpoint directions and
any finite cascade of specified relays whose clocks remain in U. Do not replace
the actual future return by the inverse of a previous map.

The trial physical identification would say: this full exterior record determines
the completed physical metric comparison throughout the region probed by those
signals, up to diffeomorphisms fixing U. Equivalently, no two nonisometric metrics
with the same exterior calibration and these records are physically distinct
for that claimed complete assignment.

This sufficiency statement is **NEW, UNADOPTED and not implied** by the current
kernel, W4/W5/W6, DDR, no preferred observer, or universal law. It is not required
for every native UDT route. It is a concrete version of a tempting finite-network
closure assumption, offered for attempted refutation rather than adoption.
Current W4 does supply ordinary clocks, null propagation and free fall on a
shared metric. R6/R7 supply conditional arrival/frequency and direction-aware
composition; they do not establish this inverse/completeness claim.

Physical reason to examine N: if the native finite-pair state is reconstructed
from signal comparisons alone, one must know which interior metric information
those records actually contain. More exterior observers or more directions do
not automatically supply all metric components. This question does not assume
E=Ric, the quadratic response, an action, a matter source, an asymptote or a
particular clock technology.

## A concrete counterexample candidate, not a selected geometry

Take any smooth Lorentz metric g and smooth positive Omega with Omega=1 on an
open neighborhood of every clock/preparation/relay event in U. Let

    g_tilde=Omega^2 g.

Treat these as two supplied control geometries, not two physical spacetimes or
two admitted UDT solutions. Same endpoint calibration means the metrics and all
their derivatives agree in U. Thus all allowed exterior observer histories,
local orthonormal directions, proper labels, preparation operations and free
geodesic segments confined to U can be matched identically.

Write w=log Omega. Direct substitution into the metric connection gives

    Gamma_tilde^a_bc-Gamma^a_bc
      =delta^a_b partial_c w+delta^a_c partial_b w-g_bc partial^a w.

For an affinely parametrized g-null tangent k this implies
nabla_tilde_k k=2k(w)k. Hence k_tilde=Omega^-2 k is affine for g_tilde,
and the same oriented null curve joins exactly the same events. This is a
calculation, not an extra null-propagation postulate. Timelike causal cones
also agree, so regular selected arrival events and earliest causal incidence
are unchanged; no new shortcut is inserted by the conformal factor. Global
branch assumptions remain those of the declared experiment.

An endpoint unit clock transforms as u_tilde=Omega^-1 u. Therefore

    omega_tilde=-g_tilde(k_tilde,u_tilde)=Omega^-1 omega,
    Z_tilde=(Omega_o/Omega_e)Z=Z  when both endpoints lie in U.

More strongly, the proper-time arrival map itself is identical, because the
null-event correspondence and the endpoint proper labels are identical. Finite
intervals, derivatives of all orders supported in the regular branch, immediate
echoes and finite relay compositions in U agree. Frequency-affine normalization
is not an observable added by this argument. Endpoint directions agree because
the endpoint metric/tetrads and null direction agree. No beam amplitude,
polarization or matter-interaction transport law has been assumed or tested.

This proposed ambiguity holds for **all allowed exterior observers and null
directions**, even where their rays traverse the modified interior. It is not
an all-observer statement about worldlines that enter V, or a claim about
all full pair ribbons, timelike transport, local volume records or interior
rulers. Those data have deliberately not been supplied by trial N.

For an explicit regular nonisometric witness, choose a Minkowski comparison
and a smooth nonzero bump f(x) supported strictly inside0<x<L, with

    g_tilde=exp(2epsilon f(x))[-dt^2+dx^2+dy^2+dz^2],
    U={x near0 or nearL, plus the exterior sides}.

Every boundary-to-boundary ray direction and all clock histories confined to U
have the unchanged record above. The scalar curvature is

    R_tilde=-6 exp(-2epsilon f)[epsilon f''+epsilon^2(f')^2].

A nonzero smooth compact bump cannot make this identically zero: that would
give (exp(epsilon f))''=0 with unit exterior value, forcing Omega=1. Thus for
epsilon!=0 this metric is not flat and cannot be diffeomorphic to Minkowski.
Both metrics are smooth, Lorentzian and causal on the supplied finite region.
There is no claim that either solves any adopted UDT equation. The slab chart
and bump are counterexample choices, not a preferred universal center or a
physical wall. Omega positivity is exact; small epsilon is needed only for
the optional perturbative illustrations below, not for null-record identity.

**Proposed outcome:** N is refuted as a kinematic inverse claim if the above
argument survives review. A relation imposed solely on these exterior null
records cannot distinguish this conformal family without further hypotheses.
That is a protocol/domain result, not a proof that native UDT is underdetermined,
that finite comparison laws are impossible, or that a physical Weyl gauge exists.
The complete-pair density warning in central R4/R5 remains fully intact.

## What would actually discriminate: send the clock through the interior

The smallest repair uses an existing W4 observer type, not an invented coupling.
Let an ordinary freely falling test clock cross the strip along x, with initial
local speed0<v<1 measured in the common exterior laboratory; put E=gamma(v).
For the static control choose E>max Omega so it crosses without a turning point.
This finite high-enough-speed choice is a declared diagnostic, not an assumption
that arbitrary physical probes or apparatus are already available.

The conserved metric energy and unit normalization give

    E=Omega^2 dt/dtau,
    dx/dtau=sqrt(E^2-Omega^2)/Omega^2,
    T(E)=integral_0^L E/sqrt(E^2-Omega^2) dx,
    tau(E)=integral_0^L Omega^2/sqrt(E^2-Omega^2) dx.

For epsilon near0 with E bounded away from1 and no turn, their first changes are

    delta T=epsilon E/(E^2-1)^(3/2) integral f dx+O(epsilon^2),
    delta tau=epsilon(2E^2-1)/(E^2-1)^(3/2) integral f dx+O(epsilon^2).

A nonnegative nonzero f therefore gives a timelike distinction despite exactly
unchanged exterior null-clock records. The transmitted probe clock can report
its accumulated proper time on arrival without a receiver synchronization choice.
One can also use a declared instantaneous turnaround in the shared exterior
region and compare launch/reunion on the same laboratory clock; both legs are
then actual future timelike segments, not inverse transport. That optional
turnaround is an ideal kinematic protocol, not a derived material apparatus.

Calibration is explicit: initial v uses ordinary local clock/ruler comparisons
under W4; the two metrics agree there. The symbol L names the supplied coordinate
extent in this control. To formulate a data-only comparison, normalize elapsed
times by the same measured exterior null echo duration2L; do not infer L from
a tested redshift curve or fit a curvature-response equation to define it.

Endpoint transit data alone have another limitation. The two integrals depend
on the distribution of Omega^2 along x, not its ordering. For example the
reversed bump Omega(L-x) has the same T(E) and tau(E) for every admitted E.
With individually fixed endpoint laboratory labels this is not an identification
of the same interior profile. A large transit spectrum is therefore not silently
promoted to pointwise reconstruction or a general rigidity theorem.

If a moving probe supplies proper labels at its radar reflections, one exterior
clock obtains s,r for outgoing/return signals and defines

    T_radar=(s+r)/2, X_radar=(r-s)/2.

In this particular conformal strip these equal t,x, since null curves have
dx/dt=±1 and the laboratory clock has Omega=1. Along the tracked timelike probe,

    Omega^2|probe=(d tau/dT_radar)^2/[1-(dX_radar/dT_radar)^2].

This is a direct proper-time identity. It needs smooth timelike data and regular
echoes; at v approaching1 the inverse is poorly conditioned. It is exactly the
sort of along-curve radar conformal-factor reconstruction already available in
R8, so **it is not claimed as a new second proposal or new theorem**. Its role is
to identify the specific missing finite comparison in N. One monotone probe
samples the static profile it traverses; nothing here establishes generic4D
metric tomography or physical law selection.

## Closest prior work and the limited new content

- ECS1 already gives complete restricted-sheet clock records with arbitrary
  transverse metric information. It explicitly stops short of every observer
  and direction. This proposal instead tests a full exterior network with rays
  crossing the unknown interior; the missing data are a conformal factor away
  from the clocks. The quantitative distinction is the observer domain, not the
  number of samples. Standard conformal-null geometry is not claimed novel in
  mathematics; its application to this exact finite-record sufficiency claim
  is the proposed increment relative to the inspected UDT sources.
- R4/R5 already show that normalized scalar/pair records can lose metric density
  and that complete rank-ten metric query records can recover the metric.
  Nothing here declares their common scale to be gauge. Exterior null records
  are not those full valued metric germs; the counterexample explains why the
  replacement is invalid.
- FPC/FNA/FST/ECS give prepared finite rates, full path-labelled pair assembly in
  supplied space forms, family discriminators and restricted inverse limits.
  Finite native representation does not establish N. The proposed counterexample
  preserves an exterior record, not FNA's full interior pullback/transport data.
- FCV1 already shows an interior nonconformal perturbation can alter a fixed
  finite clock record while leaving clock neighborhoods unchanged. Merely saying
  "finite paths contain information beyond endpoint curvature" would repeat
  that source. Here the opposite conformal null kernel is the distinguishing test.
- RCD1's echo relation q(L)=p(2L)/p(L) in the comoving sector is kinematic. Adding
  formula-generated echoes cannot independently select a response. PSC1/CMF1/CBR1
  already explore response discrimination with independently supplied curvature,
  ruler and preparation data. Trial N chooses no response; crossing-probe data
  reuse W4/R8 rather than assuming that the quadratic candidate was selected.

## Bounded next derivation and stop

Recommend one short analytic review target, not a new field solver: prove or
break the exact null-record invariance with the full clock/branch/relay-domain
quantifiers; check the conformal scalar and timelike transit formulas directly;
then state precisely which part of the proposed native complete-pair assignment
is not measured by N. A single original-connection symbolic check on the static
one-dimensional conformal family and its crossing probe would be enough as a
finite diagnostic if the parent chooses this target. A second control may use
the reversed bump to expose the endpoint-transit limitation. Do not add hundreds
of equivalent curves or label a finite symbolic check a general proof.

No numerical run was executed for this initial proposal. Analytic exploration
preceded this seal as the work order permits. Before any later computation,
freeze the exact families, domains, sample counts and tolerances; use the existing
2GiB/one-BLAS-thread/no-timeout capture and the parent four-script budget. Stop at
a reviewed conditional ambiguity/discriminator or an unresolved objection.
No source, matter, action, physical scale, preferred observer, photon transport,
hardware target, quadratic-law selection or global X_max claim enters.

If the user wanted a *new geometry-selecting physical law*, this operational
context has not found one. Its useful survivor is a precise boundary on a finite
comparison closure claim and a known-principle way to interrogate the missing
geometry. That result can constrain the form and data requirements of a future
physical assignment, while neither requiring a unique local response first nor
declaring that existing UDT premises cannot supply the assignment.

Await one cross-examination round. This initial proposal remains fixed.
