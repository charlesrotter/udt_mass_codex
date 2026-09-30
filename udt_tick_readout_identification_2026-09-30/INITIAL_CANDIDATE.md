# TRI1 initial conditional derivation — which clock comparison needs a frame?

DRAFT for review; CONDITIONAL, UNPROMOTED. The regular null-clock interface
is inherited, not a new universal physical light/detector law. This rederives
and operationally separates existing FSL1/R6 kinematics from PRI1's optional
population-to-observer route. The basic redshift theorem is not a new discovery.

## 1. Supplied geometry and actual clocks

Supply a smooth time-oriented Lorentz4 metric of signature(-+++), actual future
unit proper clocks u_e,u_o and a smooth regular one-to-one branch of future
null geodesics between them. Set c_E=1 in length units for proper time. On
proper-time intervals let reception be t=A(s), A smooth, A'(s)>0. Caustics,
branch changes, loss, re-emission and relays are outside this simple matching.
Every assertion below keeps that domain, unless a purely counting statement
explicitly needs less. The metric and queries are supplied conditional data,
not a native selected UDT geometry or an empirically validated model.

Choose affine ray tangents k(s,lambda) with fixed parameter endpoints and a
smooth choice of normalization. Write omega_i=-g(k_i,u_i)>0. For J=partial_s x,
commuting family coordinates, the affine geodesic equation and nullness give

    d[g(k,J)]/dlambda = g(k,nabla_J k) = (1/2)J[g(k,k)] = 0.

Endpoint J_e=u_e and J_o=A' u_o therefore give

    Z=A'=omega_e/omega_o;   received/emitted rate = 1/Z.       (1)

The last phrase means matched infinitesimal proper-time intervals, or a
specified differentiable tick-phase/count density below. For a finite interval,
Delta t=int Z(s) ds. One cannot replace this by Z(s0) Delta s without constant
Z or a stated error bound. No population rest observer is used in (1).
Actual endpoint clocks are required inputs; geometry alone does not choose
worldlines, events, initial motion or a branch.

## 2. Normalization is not a physical population law

The final ratio is unchanged under k -> a(s)k with a(s)>0 constant along each
ray: both endpoint omegas multiply by the same a(s). This assertion follows
from the ratio after the regular-family proof; it does not require a separately
rescaled affine coordinate to keep the original fixed endpoint interval.
An arbitrary affine normalization does not specify an absolute tick frequency.
If a calibrated emission cadence nu_e(s)>0 is supplied, set

    a(s)=nu_e(s)/omega_e(s),   omega'_o=nu_e(s)/Z(s).           (2)

This is an operational normalization on that branch, not a new propagation
law, quantum energy identification or change of local proper-clock rates.
Selecting emission cadence means specifying how ticks are labelled/emitted;
ordinary proper time remains unchanged. Absolute cadence is extra data when
it has not already been prescribed by the clock/query protocol.

At an intermediate point of the same ray let v be any future unit observer.
Then (omega_e/omega_v)(omega_v/omega_o)=Z. The actual direction and same ray
must be retained in transport, as in FSL1. A population rest frame can serve
as such an auxiliary frame without changing the product. Changing an actual
endpoint worldline changes the experiment and need not preserve Z. No path
independence, later-return inversion or preferred observer follows.

## 3. Tick counting without a photon or energy law

On the emission proper-time interval give a locally finite nonnegative tick
counting measure mu_e. Its atoms can be the actual labelled emission ticks;
no continuum approximation is then needed. Under the stipulated one-to-one
labelled correspondence, reception is the mathematical pushforward

    mu_o(B)=mu_e(A^{-1}(B)).                                  (3)

For t0<t1, this gives exact matched finite counts on (t0,t1]. This is conditional
accounting of preserved labels, not a claim that all physical detectors receive
every emission, or that radiation amplitude/energy is conserved. Branches or
lost labels require their own accounting.

Only if mu_e has a density r_e(s) ds does change of variables give

    r_o(A(s))=r_e(s)/Z(s).                                   (4)

Equivalently a differentiable increasing phase C_e(s) pulls back to
C_o(t)=C_e(A^{-1}(t)), so C'_o=C'_e/Z. A real discrete step-count function
need not have an ordinary derivative; (3), rather than an invented smooth
rate, remains exact in that case. No Planck law, energy per tick, area flux,
intensity, luminosity or instrument transfer function is derived.

For a finite collection of such streams received by the same proper clock,
with their emission measures/correspondences separately supplied and counted
once each, mu_tot=sum_j (A_j)_*mu_e,j. In the density case,

    r_tot(t)=sum_j r_e,j(A_j^{-1}(t))/Z_j(A_j^{-1}(t)).         (5)

This is additive labelled counting, not a stress tensor or definition of a
new effective redshift. Any different recording weights/protocol need separate
specification. Where R=sum_j r_e,j(A_j^{-1}(t))>0, the formal normalized ratio
r_tot/R is the source-rate-weighted mean of 1/Z_j at those matched events.
R compares distinct source proper times by this supplied correspondence; it
is not a new universal clock. Neither the source rates nor recording weights
are selected by the individual Z_j values.

A finite exact control takes A1(s)=2s, A2(s)=4s on positive intervals. With
constant source densities(1,1), r_tot=3/4 and r_tot/R=3/8; with(3,1), they
are7/4 and7/16. The individual Z values stay(2,4). These are counting controls
for supplied maps, not an admitted UDT cosmology or a rule choosing the rates.
For a nonlinear control A(s)=s+s^2 on0<=s<=1, total reception duration2 differs
from A'(0) times source duration1, while a unit continuous source density has
exact total count1 after pushforward. Atoms at s=1/4,3/4 arrive at5/16,21/16.

## 4. Why the ratio does not select PRI1's population moments

PRI1 defines J=int k dnu when finite/timelike and M=int k_flat k_flat dnu
for a supplied finite second moment. Those are full population data, whereas
(1) is invariant under the per-ray normalization above. This is an information
and scope distinction, not a new symmetry of a physically specified population.

At a point use k+=(1,1,0,0), k-=(1,-1,0,0), with atomic weights4,1. PRI1 gives
v_J=3/5 and v_M=1/3. Replace k+ by (1/2)k+ while keeping the atomic weights.
The new moments are J=(3,1,0,0), hence v_J=1/3, and
M(r)=exp(-2r)+exp(2r), hence v_M=0. Each beam's same-ray endpoint ratio stays
unchanged if its affine tangent is scaled consistently at both endpoints.
All measures are finite positive and non-single-ray; no degeneracy creates the
change. They demonstrate that those ratios do not fix these moments without
normalization/population information.

If k denotes physically normalized frequency/momentum, this replacement
changes the spectral state; it is NOT a gauge transformation of the same
physical population. If only unparametrized rays are specified, their affine
scales are a convention and cannot secretly become physical moment weights.
A supplied cadence/physical spectrum can remove that ambiguity via(2), but
population measure, sampling and clock coupling must still have provenance.
This example does not say that rich frequency/direction/count measurements
cannot reconstruct a physical state, or that PRI1's fixed-state theorem fails.

## 5. Consequences for the research dependency

The received-tick definition supplies the per-channel derivative/inverse-rate
relation, on the conditional regular clock interface. It does not prescribe a
population moment to minimize or identify actual observers with its minimizer.
For prescribed actual clocks no such population choice is a prerequisite.
PRI1's comparison-frame question is conditional on choosing its population-based
route; it is not a new gate on all positional-clock calculations.

This corrects the scope of the preceding lay framing that UDT must justify
which population comparison rule is physically appropriate: that is needed
when proposing to define clocks from a population, not for every comparison
of already specified clocks. It changes no FSL1 or PRI1 equation or original
grade. The finite count transport above adds explicit bookkeeping and controls
under stated matching/data assumptions; no detector physics is being imported.

Positive descendants: R6/R7 clock comparisons and kernel clock-leg readout
remain usable given g, actual clocks and branch. PRI1 R18O still constructs a
unique conditional moment observer from its full supplied state. Negative
survivors: its R18F criterion distinction and R18B raw-moment obstruction retain
their exact domains. CCR1's response obstruction is neither evaded nor imposed
on these fixed-geometry readouts. A state/measure continuation is still needed
when claiming a metric derivative, not just for applying(1)-(5).

The unresolved native question remains quantitative geometry/pair assignment
for physically justified comparisons. No metric history, response, matter,
physical X_max, positional distance curve or empirical SR/GR recovery is selected.
This is not a full-underdetermination theorem or proof a new postulate is needed.
The concrete recommendation is to keep actual-clock readout separate from any
optional population-defined congruence, and carry cadence/weight choices only
where that observational or response problem actually calls for them.
