# PSW1 geometry/dynamics source-first candidate

Status: CONDITIONAL WHITEBOARD CANDIDATE, UNPROMOTED; peer proposals not read.
Author context: `/root/psw_geometry`, inherited model, actual separate context.
Different-model independence is not claimed. Source-first fixed before cross-review.
This fixed evidence edition is not a second maintained scientific account.

## Scope, authority and source reconstruction

Independently checked `grok`, HEAD `4953c9ae806d42f0042d4fac14682db12c93143c`,
and worktree names. No tracked dirt at inspection. Parent startup/synchronization
and the passing TPS1 full406 audit are attributed through PSW1 `SNAPSHOT.json`
and TPS1 `diagnosis/checks/final_premises.json`, not claimed independently rerun.
No protected payload was read or hashed. Only this `geometry/` directory is owned.
Read on-disk AGENTS, CLAUDE work/triggers/repo rules and the five triggered local
protocols (no-shortcuts, solution-space, solver-first, completeness, verifier).

The maintained definitions and R1–R10, R16 and relevant R18 were read, together
with exact source owners listed in `SOURCE_HASHES.json`. Registry inspection was
limited to G176/G310/G312/G402/G403/G415 for normalization, response and prior
clock-curvature scope. Their grades are inherited, not changed. In particular:

* The positional meaning of observed `c_E`, ordinary local proper clocks, one
  shared geometry, and an additional positional contribution are admitted owner
  meaning. The tentative expectation of net redshift is not a universal sign law.
* R1's reciprocal character requires its actual F1–F4 hypotheses. R4 normalizes
  supplied complete pair data; `chi=tanh(Phi)` cannot choose a metric or event map.
* R6 gives actual received ratios once a metric and regular null-clock experiment
  are supplied. No population moment is needed to read already specified clocks.
* DDR is OWNER_ADOPTED_PROVISIONAL_POSTULATE and gives `TF(E)=0` for its specified
  symmetric response/all-pair domain. It does not identify `E`, set `E=0`, or
  equate reciprocity of inverse maps with two future signal legs.
* R10's curvature-class implication remains conditional. TPS1's `Ric=0,Lambda=0`
  is an intentionally supplied comparison equation, not the native physical
  admissibility criterion. Its initial/query freedoms are legitimate conditional
  data; their existence alone is not a proof of an absent law.

Question: find a geometric condition whose value can differ between candidates,
while exposing the physical identification that would make it a positional test.
Methods: differential geometry and finite polynomial jets only. The smooth metric,
local clock preparation and small laboratory size below are supplied controls,
`pinned-by-HABIT` in the mandated choice taxonomy (explicit operational choices,
not presumed universal physics). Curvature values and directions are symbolic,
`free-and-explored`. Ordinary proper-time/null-clock interface inherits R6's
conditional authority, not a new field equation. No action, matter/population,
physical scale, Hubble law, boundary or `X_max` completion is inserted.

## Route A: a prepared clock laboratory isolates a curvature coefficient

This is a conditional operational diagnostic. It makes no universal net-redshift
claim and does not identify its result as the additional positional contribution.
Its practical gain is a sharp test of one candidate interpretation that `Ric=0`
cannot satisfy: a strictly positive leading angular monopole in this preparation.

Choose an event p, future unit U and an orthonormal rest frame. Let the emitter
follow the geodesic with those data. At emitter proper time zero prepare, for
each unit rest direction n and small L>0, a receiver at `exp_p(L n)` with initial
unit velocity obtained by parallel transporting U along that spacelike geodesic.
The receiver thereafter freely falls. Set its proper clock to zero at preparation.
Use the direct regular future-null branch from emitter time s to that receiver,
with smooth arrival map A_L,n(s); evaluate `Z_L(n)=A'_L,n(0)`. This is a physical
preparation stated in geometric terms, not fixed coordinate receiver motion.
Regular small convex neighborhoods, smooth metric and bounded jets on a compact
subneighborhood supply the uniform small-L expansion. There is no distant claim.

Use the repository curvature convention and define the electric curvature
`E_ij=R(e_0,e_i,e_0,e_j)` at p. Here this E is **electric curvature**, not DDR's
response; to avoid ambiguity write `T_ij=R_0i0j` below. Then

    log Z_L(n) = -(1/2) T_ij n^i n^j L^2 + O(L^3).              (A1)
    <log Z_L>_S2 = -(1/6) Ric(U,U) L^2 + O(L^3).               (A2)

The remainder constants depend on the fixed metric neighborhood and preparation;
no universal finite-size tolerance is asserted. The average is an ideal angular
average of repeated experiments, not a physical matter/radiation population.

### Derivation, including the receiver and proper-time derivative

Fermi coordinates around the central emitter have, on the radial direction n,
to the order that contributes to (A1),

    g_00=-(1+q r^2)+O(|(t,x)|^3), q=T(n,n),
    g_0n=O(|(t,x)|^3), g_nn=1+O(|(t,x)|^3).

The quadratic cross and spatial radial contractions vanish by curvature
antisymmetry. In the first equation curvature at time t differs from its value
at p by O(t); along the L-scaled laboratory this enters the cubic remainder.
Parallel initial velocity has zero radial coordinate component through order
L^2: its difference from the Fermi time vector is transverse at that order,
again because the radial Riemann contraction is zero. Such transverse terms
change neither the order-L^2 frequency contraction nor the cubic radial arrival
calculation. General transverse motion and curvature remain in the remainder;
no totally geodesic 2-surface is claimed.

For `|s|=O(L)`, keeping the total-degree-three arrival terms gives

    r_B(t)=L-(q/2)L t^2+O(L^4),
    t_o=s+r_B(t_o)-(q/6)r_B(t_o)^3+O(L^4),
    tau_B(t)=t+(q/2)L^2 t+O(L^4).

The first is actual geodesic displacement; the second integrates the null
equation `dt/dr=1-q r^2/2+...`; the third is actual receiver proper time.
Consequently

    A(s)=s+L+q[L^2(s+L)/2-L(s+L)^2/2-L^3/6]+O(L^4).

Smooth rescaled geodesic/arrival dependence and transverse arrival give a C1
remainder, whose s derivative is O(L^3). Therefore
`A'(0)=1-qL^2/2+O(L^3)`, proving (A1). The single flight time
`A(0)=L-qL^3/6+O(L^4)` is different information and cannot replace the derivative.
Finally `<n^i n^j>=delta^ij/3` and `sum_i T_ii=Ric(U,U)` prove (A2).

These are standard local geometric methods, reconstructed here at the declared
protocol, not a novel theory of redshift. They need substantive peer checking,
especially the general 4D preparation/expansion, beyond the finite control below.

### What it distinguishes, and the strongest objection

For a supplied Ricci-flat geometry (A2)'s leading coefficient is zero. Its Weyl
electric part can still produce direction-dependent redshift and blueshift. A
trace-free illustration `T=diag(-2,1,1)` gives leading coefficients `(1,-1/2,-1/2)`;
this algebraic example illustrates the angular trace, not a chosen TPS1 point.
If T is nonzero trace-free, its quadratic form takes both signs. If T=0, (A1)
says nothing about the sign of higher-order finite shifts.

In the *conditional* Einstein family `Ric=Lambda g`, (A2)'s coefficient is
`Lambda/6`. Thus imposing **the extra UNADOPTED physical identification**
"the positional effect must give a positive leading monopole in this preparation"
would require `Ric(U,U)<0`, and would rule out Ricci-flat candidates for that
identification at that event. If the extra requirement applied to every unit U,
the same strict inequality would be required for each; no such universal
quantifier is inferred here. All-direction positive leading coefficients are
stronger: they require negative-definite T, not just negative Ric(U,U).

Strongest objection: the founding additional-effect interpretation does **not**
specify this preparation or a nonzero L^2 monopole. An effect may first enter at
higher order, require finite separation, be combined with ordinary shifts, or
restrict other physical comparisons. No adopted premise identifies this net
coefficient as a positional component. Therefore a zero TPS1 monopole cannot
refute UDT, and selecting Lambda>0 from the desired sign would reverse the
argument. The surviving claim is the conditional diagnostic and exact additional
condition, not a native admissibility rule or a reason to discard TPS1 solutions.

### Executed finite check and nearest prior attempt

`check_fermi_jet.py` directly computes curvature in the supplied exact local
product control `g=-(1+q x^2)dt^2+dx^2+dy^2+dz^2`, restricted to its invariant
radial plane with `1+q x^2>0`. It checks the geodesic/null/proper-clock jets and
independently contracts endpoint frequency. All14 finite checks pass; symbolic
q remains free. Holding the receiver fixed instead would give `+qL^2/2`; the
check explicitly detects this wrong-sign preparation substitution. A six-axis
quadratic average equals the spherical quadratic average exactly, but is not a
finite-angle theorem about the higher-order remainder. Python3.10.12/SymPy1.13.1,
one CPU process,2GiB limit,50,520KiB maximum RSS,0.604s, no time cutoff. Exact
command and stdout/stderr/hashes are in the reused TPS1 capture receipt.

Nearest inspected work: DCI1/G403 reconstructs `Ric(U,U)` from a congruence's
directional clock slope, mean drift and extra acceleration/twist information;
SGE1 gives a generic `O(L^2)` local bound; ICN1 reconstructs radar-plane metric
values/gradients and gives a restricted Taylor bound. The increment here is a
**specified geodesic preparation** that fixes the leading finite received-shift
coefficient and its angular trace, without inserting a population or auxiliary
congruence as a physical selector. This is novelty relative to inspected sources
only, not a corpus-wide or mathematical novelty claim.

Smallest executable next calculation: after review, compute the six `T_ii`
contractions in one analytically supplied nonflat Ricci-flat metric at a fixed
event/frame and verify the coefficient with an independently implemented local
geodesic/null arrival Taylor expansion. Also use one non-Ricci-flat control and
the wrong fixed-receiver preparation. No broad evolved-field or ray campaign is
needed. A later saved-TPS1 diagnostic would require its own reviewed request and
derivative/error budget; no such campaign is launched here. Interpretation still
requires Charles's decision on the explicitly stated UNADOPTED identification.

## Route B: sharp directional sign condition on specified comparison clocks

Let a smooth physical comparison congruence U be supplied in a regular tube.
DCI1/SGE1 give `K(n)=B(n,n)+a.n`, with `B=Hh+sigma`. The pointwise exact condition

    K(n)>0 and K(-n)>0 iff B(n,n)>|a.n|.                       (B1)

For all n, this is a real restriction on the metric/congruence first jet; for
geodesic clocks it is exactly positive definiteness of B. It is not simply
positive mean H: `B=diag(-1,1,1),a=0` has H>0 but a blue direction. It is not
isotropy: `B=diag(1,2,3),a=0` passes with shear. Positive strict margins persist
on sufficiently short regular comparisons by continuity. Opposite directions
at one point are two local comparisons, **not** the two finite legs of an echo;
actual finite legs still require their actual ray integrals and events.

Under the extra **UNADOPTED** identification that a stated set of physical
comparison clocks must have net positive infinitesimal shifts in every direction,
(B1) is a discriminating necessary/sufficient pointwise test. No preferred
observer does not provide this U or imply that stronger net sign. An arbitrary
auxiliary extension of just two endpoint clocks cannot be tested as physical:
SGE1 explicitly shows that its K changes by an endpoint-canceling exact term.

Ricci-flatness does not impose (B1). Flat spacetime with inertial parallel clocks
has B=0. Inside the future Minkowski cone the supplied Milne congruence has
`B=h/tau,a=0` and positive K in every direction, although curvature is still zero.
This is ordinary relative-motion preparation, not a native positional cosmology.
It demonstrates that even a passed net-redshift test would not separate a new
positional effect from supplied clock motion. No Hubble law is adopted.

Nearest inspected prior attempt: SGE1's `K=H+sigma(n,n)+a.n`, all-direction
isotropy condition and auxiliary-field control. The increment is the exact
inequality distinguishing positive directions without imposing isotropy, not
new geometry. The smallest calculation is evaluating the actual symmetric
deformation and acceleration of a *separately specified* physical congruence;
checking arbitrary TPS1 coordinate clocks does not supply that identification.
Route A is the more useful next comparison because its preparation eliminates
the leading relative-motion freedom instead of leaving a congruence unexplained.

## Return and open join

Neither route supplies a response law. The exact open joins differ:
Route A needs physical ownership of a particular prepared-clock curvature
coefficient; Route B needs physical ownership of a congruence and a net-sign
requirement. Neither is a mere demand for more initial data, and neither follows
by normalizing a reciprocal pair or setting `TF(E)=0` without specifying response.

Lay conclusion: one can now ask a sharper question than whether a vacuum example
has redshifts. Start free clocks with no initial relative motion, and compare
their received ticks in every direction. The first curvature contribution's
average is zero in Ricci-flat geometry, even when some directions redshift.
If UDT intends its additional positional effect to appear in that specific
coefficient, it requires an extra condition the TPS1 comparison did not impose.
Whether that is the intended physical condition remains open; the founding words
alone do not establish it.
