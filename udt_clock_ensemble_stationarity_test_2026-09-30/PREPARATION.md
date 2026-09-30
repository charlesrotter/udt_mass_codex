# CES1 fixed operational preparation and falsification probe

This is an explicitly supplied ensemble of repeated ideal test-clock experiments.
It is operationally defined, not a UDT-derived population or a mass distribution.
The law identifying its contrast response with DDR remains UNADOPTED. Physical
initial data and the label measure below are fixed before the calculation; no
weights will be changed to make a result vanish. Existing FCV1 and PCW1 examples
are exposed. An interior perturbation is deliberately chosen as an adverse test;
this is mathematical discovery, not an outcome-blind confirmation.

## Metric-covariant preparation

Use signature −+++ and proper-time length units c_E=1. Select a laboratory event
p with a unit future timelike U and an orthonormal spatial frame. These are query
data that are carried by a diffeomorphism with the metric. Choose a unit spatial
direction n at p, a proper separation L and positive rapidity η.

At p, the emitting clock begins its timelike geodesic with tangent U and zero
proper-time label. Prepare the receiver at exp_p(L n), using the spacelike
geodesic orthogonal to U at p. Parallel transport U and n along that preparation
geodesic and give the receiver initial tangent cosh(η) U_parallel+sinh(η) n_parallel.
It subsequently follows its timelike geodesic with ordinary proper time and
zero label at preparation. For emitter proper time s>0, use the smooth future
outgoing metric-null branch arriving at that receiver. Its received tick ratio
is Z=dτ_receiver/ds. No physical phase, photon energy or detector law is asserted
beyond the declared conditional metric-null clock interface.

The preparation is meaningful on a neighborhood of the baseline for which the
spacelike preparation and null-arrival branches are regular. An arbitrary
coordinate transformation moves the selected event/frame, both geodesics and
their labels together. Fixing these physical data is distinct from fixing a
coordinate velocity while changing its proper meaning.

Labels q=(s,L,η,n) range over a compact product with
0<s_-<s_+, 0<L_-<L_+, and 0<η_-<η_+<infinity. Use any fixed smooth nonnegative
normalized densities w_s,w_L,w_η supported in these intervals and uniform
dΩ_n/(4π) on the laboratory's unit direction sphere:

    dμ(q)=w_s(s)w_L(L)w_η(η) ds dL dη dΩ_n/(4π).

All endpoints, densities and the preparation are free-and-explored input data;
no numerical value or weight is tuned to an outcome. This is isotropy in the
laboratory frame, not a finite invariant distribution over all Lorentz boosts.
For general metric variations the abstract label measure stays fixed; any
metric dependence of its pushforward to physical event/query space is carried
by Q_g and cannot be dropped by silently switching integration variables.

## Baseline and compact metric probe

At Minkowski baseline choose inertial coordinates adapted to (p,U), with p at
t=0 and the emitter at x=0. Write r=|x| and v=tanh η. The receivers have
x(t)=(L+v t)n; this coordinate description follows from the physical preparation.
Their entire relevant histories lie outside r=L_-, whereas the emitter is at0.
Direction averaging is a laboratory choice, not a cosmological center.

Choose 0<a<b<L_-. Let b_0(r) be a nonnegative nonzero C-infinity bump supported
in (a,b), with dimensions inverse length. Let χ(t) be a smooth compact time
cutoff, identically1 on a neighborhood of every baseline ray's shell-crossing
times [s_-+a,s_++b], and identically0 near t=0. This is possible since s_-+a>0.
Set f(t,r)=χ(t)t b_0(r), extended by0 near r=0 and outside the shell, and use

    g_ε=−exp(−2εf) dt²+exp(2εf) dr²+r² dΩ².

The expression is smooth in Cartesian coordinates because f vanishes near r=0;
no geometric center singularity or material boundary is inserted. The difference
from Minkowski has compact spacetime support. For sufficiently small |ε| the
selected future radial arrival branch remains regular uniformly on the compact
label set, with the perturbed shell crossing still in χ=1. The metric remains
Lorentzian, and t is temporal. The geometry equals Minkowski on a neighborhood
of the preparation slice and of every relevant clock history.

At ε=0, the infinitesimal strain is

    h=2 f(dt⊗dt+dr⊗dr)=f H(U_radial,n_radial),
    tr_g h=0,

with the existing reciprocal strain normalization H=2(u_flat⊗u_flat+n_flat⊗n_flat).
The radial vector is only needed on the shell. The t-r determinant is exactly−1
for the full family. This is an admitted compact reciprocal test variation,
not a proposed physical field equation, cosmology, X_max input or cutoff law.

## Checks, quantifier and stop

Compute the actual arrival map by the radial null equation, including moving
receiver intersection, and multiply by ordinary clock normalization. Independently
cross-check the first variation using FCV1's affine-ray/endpoint formula. Show
from the metric support and geodesic uniqueness whether preparation, worldline
motion and proper-rate variations vanish; do not set them to0 by convenience.
Justify differentiation under the finite measure by uniform branch regularity.

Test C[g]=1/2 integral (log Z)² dμ against this compact strain. Nonzero first
variation disproves exact Minkowski stationarity for this specified preparation
class. One zero answer proves only this test. No minimum, stability, locality,
GR-precision or all-ensemble theorem is inferred. In particular, local SR is a
pointwise metric statement and does not itself require exact global Minkowski
stationarity under this unadopted comparison law. If the benchmark fails, stop
the proposed law at that benchmark and explain the remaining physical question;
do not infer that all UDT or every clock-ensemble response is excluded.
