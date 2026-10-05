# OAA1 source-first fidelity review and numerical freeze

Reviewer: /root/oaa_fidelity, fresh separate context, inherited Codex/GPT-6 runtime;
no different-model or human-review claim. Date 2026-10-04. Independently verified
grok HEAD 11cca783c02f94fad287a95595928df36340ad06, tracked-clean status and visible
old untracked names; protected payloads were not opened or hashed. Parent reports
fresh fetch and normal guard PASS; prior CPR1 full406 PASS in408.622785s is
attributed, not independently replayed. Process visibility is sandbox-local;
no assertion about host-global process absence is made.

Read AGENTS, bounded startup documents, mandated CLAUDE parts, no-shortcuts,
completeness-map and verifier-before-record protocols, CROSS_MODEL_VERIFY, OAA
WORK_ORDER, central R8/SGE1/CGE1/CPR1/GRL1/R16/CCW1, CPR1 INITIAL_CANDIDATE and
CLARIFICATIONS, the positional/shared/local-clock owner statements, and roadmap
151–216. No new OAA parent candidate, code, numerical result or reviewer verdict
was opened before this source-first freeze. CPR1 is legitimate prior evidence,
so this is source-first independence for OAA, not blindness to its precursor.

## Independent argument before candidate exposure

For a chosen regular affine null geodesic from e to o let L=lambda_o-lambda_e>0
and omega_i=-g(k_i,u_i)>0. Define d_i=omega_i L. The replacement
k->c k, lambda->lambda/c leaves both d_i unchanged. At reception,
exp_o^{-1}(e)=-L k_o along the chosen geodesic, and its orthogonal projection on
u_o's rest space has norm omega_o L. Thus d_o is a precise endpoint-normalized
affine distance; d_e similarly uses the source endpoint normalization on this
same forward ray. Their ratio d_e/d_o=Z is exact. This does not make d_e a
distance measured using a later causal return, which is a different experiment.

This definition is standard method attribution: Bolos, gr-qc/0501085v4,
section4 Definition7, https://arxiv.org/pdf/gr-qc/0501085. The paper's global
discussion assumes a convex normal neighborhood. Here the construction is
restricted to the declared branch; no unique global inverse exponential map
or global absence of conjugate/winding branches is inferred. No external
field equation or physical interpretation is imported.

For CPR1 k^r=s, L=integral_a^R dr/s(r,b(R)), omega_e=(1-Omega b)/sqrt(h),
omega_o=A. With its strict regular limiting incidence b->b_*,
s->S_*=sqrt(1+H^2 b_*^2), L/R->1/S_* and RA->S_*/H. Therefore

    d_o ->1/H, d_e/R ->(1-Omega b_*)/[sqrt(h) S_*], d_e/d_o=Z ->infinity.

The first limit follows uniformly near b_*: choose a compact b interval inside
the strict source bound; s is bounded below there and 1/s differs uniformly
from1/sqrt(1+H^2b^2) by O(r^-2). Its integral remainder is O(1), so division
by R removes it. This is a useful finite affine endpoint limit, not a theorem
of monotonic approach, a universal maximum, or a unique distance-redshift law.
Both endpoint choices are coordinate invariant and yield different asymptotic
behaviors; coordinate invariance alone cannot select the intended separation.

The auxiliary SGE1 length integral omega(U)dlambda depends on the entire chosen
unit timelike tube extension. d_o can be represented by parallel-transporting
u_o along this ray, but that extension generally disagrees with u_e. Thus its
constant omega is not a replacement for SGE1's field agreeing with both clocks.
Spatial lengths need a spacelike curve/slice, radar needs two matched null legs,
and beam/area distances need a transverse map. None follows from L alone.
Calling every one of these an optical distance would hide different definitions.

In the expanding exterior f<0, grad r has norm f<0. Since the given future
receiver has dr/dtau>0, grad r is past timelike, and every future causal curve
has dr>=0 (strictly positive for nonzero causal tangent there). A receiver
already beyond the outer root cannot send a causal return to the source at
a<r_c. At the root itself future ingoing radial generators stay on the root;
the outward branch moves away. Thus the principal R->infinity experiment has
no late source-return radar range. This says nothing against one-way reception.

A separate ideal radial relay for a static source clock at a, on a< R <r_c,
gives radar D=sqrt(f(a))*integral_a^R dr/f. It diverges logarithmically as
R->r_c from below for a simple root, whereas constant-t proper radial length
integral dr/sqrt(f) has a finite horizon limit. This auxiliary source is
accelerated and differs from the orbiting source. Its equations cannot certify
an actual echo between the original fixed histories. Echo availability inside
the static region also needs its actual branch/incidence, not only f>0.

Observer law universality permits different readouts for different endpoint
velocities. In Minkowski spacetime with the same ray and endpoint events,
u_o=(cosh eta,sinh eta,0,0) gives d_o=L exp(-eta), Z=exp(eta), while emitter
normalization stays L. This is a mathematical control, not native UDT admission.
The absence of a preferred observer does not make d_o boost invariant.

The read owner sources specify ordinary local clocks, one geometry, additional
positional content beyond matched SR/GR, no preferred observer, recovery, and
an extreme-distance asymptote. They specify no distance definition, physical
population, unique comparison protocol, or numerical H. Their insufficiency
has not been proved: the exact unclosed step is deriving that assignment from
existing commitments. Identical metric and physically matched GR query still
give the same result. A conditional affine limit does not demonstrate an extra
UDT effect, select X_max, or force a new postulate.

## Freeze for independent bounded checks

Question/quantifier: check d_o, d_e, frequency contractions and differentiated
actual incidence for two supplied CPR1 fixed-history families, plus boost and
auxiliary radar controls. Metric-led conditional tests; neither a source law
nor a physical distance/population is adopted. m,a,H,E,b_* are free-and-explored
controls. Units c_E=1 and source/orientation/strict branch rules are pinned to
the conditional CPR1 definitions, not pinned by native theory.

Plan: m=1; (a,H,E,b_*)=(8,.02,1.2,0),(10,.01,1,2). Fix t_*=0,
u_infinity=U_infinity(b_*),phi_0=-P_infinity(b_*). Solve the actual two-equation
incidence reduced by eliminating t_e, using independently implemented quadrature
and a bracketed monotone scalar solve. R=60,600,6000,60000 and central perturbations
R(1+-1e-5), at45 and75 decimal digits:48 finite incidence cases including all
perturbations. Flat boosts eta=-1,0,.5,1 at both precisions add8. Three auxiliary
radar radii r_c-(r_c-a)*10^-j,j=1,2,3 at each precision add6, for62 planned
finite cases; keep failures and any repairs, total ceiling100.

Pass criteria: original angular/time incidence residual<1e-30; original
metric contractions/norms agree<1e-30; endpoint and differentiated arrival
ratio relative error<3e-8 at frozen step; precision difference<1e-25 on finite
records; at largest R, |H d_o-1|<.005 with decreasing final-three absolute
errors. The latter is only a finite asymptotic sanity check, not proof of a
general monotonic result. Boost identities<1e-30; radial radar increases while
slice length remains bounded over tested radii. No intended answer changes
these thresholds. Failure triggers a preserved diagnostic and bounded repair.

CPU only, one BLAS thread,2GiB address-space cap, no GPU, no grid, no wall/CPU
timeout. Package<100MiB. Raw stdout/stderr and machine-readable numbers saved
under review_fidelity. Stop on resource ceiling or unresolved numerical domain
failure; do not silently discard cases. No parent OAA implementation imported.
Full406, original Ricci package, beam map, real data and every possible branch
are not independently replayed by this fidelity review.
