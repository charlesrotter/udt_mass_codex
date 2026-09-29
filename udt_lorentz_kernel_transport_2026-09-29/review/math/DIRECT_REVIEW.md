# LKT1 direct mathematical review

**VERIFIED-WITH-CAVEATS for the frozen candidate's conditional mathematical
scope. No substantive mathematical defect or required scientific repair found.**
This is not empirical certification, scientific promotion, registry regrading,
native metric selection, or canon. Candidate:
`INITIAL_CANDIDATE.md`, SHA256
`600c261ec1662d8a8315034ef362f78563e7c8a193a2ca8fecad2d119ea46d52`.
All eight members of `CANDIDATE_FREEZE.json` matched their recorded hashes at this
review. This verifies correspondence only.

## Independence and exposure

Reviewer `/root/lkt_math` is a fresh separate context using the same inherited
model; exact runtime model identifier is unavailable. Different-model, human,
and formal-proof independence are UNTESTED. Parent startup/baseline attribution
and source versions are in `SOURCE_FIRST.md`, `SOURCE_PINS.json`, and its seal.
The source-first report was sealed before LKT1 candidate exposure. I then read
the candidate and freeze, wrote a direct check plan and my own coordinate-first
implementation, ran it, and sealed code/results before inspecting author code.
No other LKT1 review was read. No source or parent scientific file was edited.

During execution the parent disclosed a vacuous author assertion, `1-1`, and
emphasized the already-explicit SAME-presentation-potential scope. This is recorded
in `DIRECT_COMPUTATION_SEAL.json`; it was not hidden as blind independence. Only
after that seal did I read `checks/check_bridge.py` and `checks/CHECK_PLAN.md`.
The implementations share Python/SymPy and standard Christoffel/Riemann formulas;
this is separately authored implementation and argument checking, not independent
premises, libraries, or models. Source package suites and the full406 audit were
not rerun here. The parent baseline receipt hash was checked in the source-first
stage and matched LAUNCH, without claiming an independently repeated audit.

## Exact two-form correspondence and the scalar-character statement

Candidate (1) is correct with its chosen sign: S^T K S=eta,
S^T eta S=-K, and S^-1 D S=B(-delta), using the usual positive-off-diagonal
boost convention. Direct multiplication and the source-first exact rational
basis controls establish the conjugacy without conflating the two quadratic
forms. D preserves K and changes the original eta readout at nonzero real depth.
The abstract Lorentz representation can therefore be related to the reciprocal
character, while the actual physical readout still needs the typed metric/query
construction. The candidate retains that distinction.

The full-group obstruction is also correctly narrow. A smooth additive real
character on SO+(1,3) differentiates to a linear functional annihilating every
Lie bracket. All six standard Lie algebra generators are brackets; the character
therefore has zero derivative and vanishes on the connected group. My independent
matrices checked the three rotation-rotation, three rotation-boost and three
boost-boost bracket identities. Connectedness, smoothness, the additive target,
and arrow-only full-group scope are substantive hypotheses. This result does not
exclude FSL1's directional cocycle, a boost subgroup character, a groupoid depth,
a nonscalar relation, or a native UDT assignment. The candidate states those limits.

The directional join Phi_clock=log f is already source-owned conditional null
clock geometry. Its full-frame projective rapidity inequality and planar equality
are not generalized to the nonplanar case. The source-first fixed-ratio screen
control, with M_PT=4/9 instead of sech(Phi)=4/5, independently preserves that
boundary. No new fitted redshift response appears.

## General Lorentz2 bridge: independently recomputed, including shift

From the candidate's coordinate metric

    g_tt=-T^2, g_tx=-T^2 b, g_xx=L^2-T^2 b^2,

I computed its inverse and coordinate Christoffels by the metric formula, then
transformed covariant derivatives of the vector-frame columns

    e0=(1/T,0), e1=(-b/L,1/L)

to frame components. This independently yields the matrix connection J varpi
with

    varpi_t=[T_x-(Tb)_t]/L,
    varpi_x=b[T_x-(Tb)_t]/L+L_t/T.

This matches (5) for arbitrary smooth T,L,b in the T,L>0 patch, not just one
numeric or diagonal control. The frame is orthonormal and its time column is
the specified ordinary clock U. In this Lorentz2 sector the single generator J
commutes with itself, giving the exact solution exp(-J integral varpi); no
path-ordering approximation is being made. Endpoint frame/clock distinctions
and the totally geodesic requirement for importing this calculation into an
ambient four-metric are explicit and essential.

I also independently differentiated omega=T(k^t+b k^x) along the coordinate
affine-geodesic equation, substituting the two future-null vectors
k=omega(e0+epsilon e1). For both epsilon signs the exact residual is zero for

    d omega/dlambda = -epsilon omega varpi(k).

This validates (7), including its sign, using the metric geodesic equation
rather than assuming the proposed frequency law. A connected regular future-null
segment retains its sign because omega>0. In a general shifted chart t need not
be monotone along every future ray; equations (5)–(7) use the path integral and
do not divide by dt. The later reciprocal zero-shift restriction restores the
positive dt needed in (8).

G176 normalization is used as a local supplied-record statement. Keeping m=TL
retains information that is absent from Phi_local=-log T alone. No spacetime
coordinate transformation with ds=m dx is asserted when m_t is nonzero. The
flat control g=-dt^2+(1+t)^2 dx^2 has connection dx and zero curvature by my
direct general curvature specialization. Its null incidence gives
1+t_o=2(1+t_e), hence Z=2 between x=0 and x=log 2; fixed-x proper time is t.
The discrepancy between Phi_local=0 and Phi_clock=-log 2 concerns different
queries. It does not challenge G176 or admit this control as native physics.

## Dynamic clock depth and the exact stationarity restriction

Substituting T=e^-phi, L=e^phi, b=0 into the independently derived connection
and null tangent gives

    d Phi_clock/dt = epsilon e^(-2phi) phi_x - phi_t
                  = d phi/dt - 2 phi_t.

Both orientations passed exact general-function checks. Integration yields (8).
If equality with the SAME phi endpoint difference holds for every sufficiently
short segment of either one fixed orientation through every point of an open
patch, then each such integral of phi_t vanishes. Divide by its positive short
t-coordinate length and take the endpoint limit; continuity gives phi_t=0 at
every point. Conversely phi_t=0 gives the equality. The argument requires all
short segments in the patch, not one finite cancellation. No approximation or
finite sampling is used in that implication.

The stationary consequence concerns these x-fixed clocks in this zero-shift
reciprocal chart. When phi_t=0, their common timelike Killing field supplies
SGE1's reciprocal actual two-way ratios, excluding net redshift on both legs
in that restricted sector. This does not impose stationarity on UDT or exclude
a different endpoint potential in an evolving geometry. For example the time-only
sector itself has Phi_clock=-Delta phi: it is endpoint-exact with potential -phi,
yet generally evolving. The candidate expressly includes this sign reversal.
Nor is a later future return identified with an inverse mathematical arrow.

## Curvature, integrability, and limitations

I formed the full coordinate Riemann tensor with exactly the candidate convention,
contracted Ricci, then contracted with g^-1. For arbitrary T,L,b the result is

    R=2(partial_t varpi_x-partial_x varpi_t)/(TL).

The computed Ricci tensor is symmetric and equals (R/2)g, giving additional
internal consistency checks. Independent sign anchors yield R=2a''/a for
-dt^2+a(t)^2 dx^2 and R=-f'' for -f(x)dt^2+dx^2/f(x). The reciprocal general
specialization matches (10) exactly. The sign and factor two are correct.

On a contractible Lorentz2 patch, dvarpi=0 is equivalent to path independence
for all curves in the stated oriented frame: closedness gives exactness, while
arbitrarily small oriented loops give necessity. SO+(1,1) has no nonzero rapidity
period that could conceal a loop integral. A spanning surface is understood with
boundary orientation fixed by the compared paths. Global periods and the
restriction to all curves are necessary qualifications. The candidate does not
infer full4D flatness from one scalar clock measurement, or enforce R=0/constant
as a native equation. Metric identities remain identities.

## Evidence quality, defects, and return

The independent direct computation passed 26 exact symbolic checks, after 20
source-first exact Fraction checks. Direct runtime was 1.534s, maximum RSS
51216KiB, Python3.10.12/SymPy1.13.1, under the existing 60s/512MiB capture utility
and one-thread environment. No failed run or overwritten artifact occurred.
The general arbitrary-function calculations check symbolic identities on their
nondegenerate domain; they are not formal proof certificates. The analytic
arguments above own the global/quantified conclusions. No numerical tolerance,
physical data, fit, GPU, or production grid entered.

The author's `local clock factor is unit` assertion is vacuous and carries no
evidence. Count the author log as 30 recorded items with that item excluded from
meaningful checks, rather than claiming 30 independent scientific validations.
The proper-clock property is established directly from g_tt=-1 in the supplied
flat control; no mathematical result depends on the assertion. Matrix zero
components and shared standard formulas also do not create extra independence.
The author sensitivity controls illustrate selected wrong forms, not exhaustive
mutation coverage; the check plan correctly says so. This is an evidence-reporting
correction, not a scientific repair or reason to change the frozen candidate.

No defective load-bearing mathematical step was found. The strongest survivor
is an exact conditional metric-to-boost-to-clock bridge, a recovered directional
cocycle, and a narrow necessary stationarity condition when the extra SAME-phi
identification is imposed on all short rays. Smallest required scientific repair:
none. Retain the candidate's Lorentz2, same-clock, same-presentation and query
qualifiers verbatim in integration; losing them would materially strengthen the
result. Final integrated wording and source bindings have not been reviewed by
this report and require their separately authorized correspondence check.
