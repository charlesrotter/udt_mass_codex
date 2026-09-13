# CSS routes: source-first adversarial reconstruction

This note was written before opening CSS step_04/INITIAL_CANDIDATE.md, its
scientific code, or results. Source exposure: parent dispatch and WORK_ORDER;
G405 original INITIAL_CANDIDATE, exact current registry row, REPAIR_LOG and
review/REVIEW; OB1 REVIEWED_RESULT and INITIAL_CANDIDATE; current source pins,
premise summary and G312 authority; AGENTS/CLAUDE and triggered no-shortcuts,
completeness-map and verifier-before-record protocols. Mathematical discovery
precedes this note; finite numerical outcomes have not been generated.

Context /root/css_routes_review is a fresh allocated context. Actual first tool
action: 2026-09-13 00:03:33 UTC. Conservative allocation 00:02:25 UTC, deadline
00:42:25 UTC. Runtime model/version UNATTESTED; configured parent
gpt-6-astra/xhigh is attribution only. Different-model independence is UNTESTED.
Top-level startup and full398 execution are attributed to the parent; its new
audit was pending at allocation. I independently observed branch grok,
HEAD=origin/grok=b69e03913caf42e7b6d502e4f3449921c500b4dd and empty tracked diff.
Original untracked-status preservation is parent-attributed, not a payload audit.

## Question, source ceiling and choices

For the entire supplied smooth four-metric

    g=L²[-(dt+b(t)(x dy-y dx)/2)²+dx²+dy²+dz²], L>0,

what are the opposite-direction arrival maps along a supplied R-circle at
z=0, and their derivatives between the same stationary emission/reception
worldline? Coordinates t,x,y,z and R,b are dimensionless in this displayed
L convention; physical proper seconds on stationary clocks are L dt/c_E.
Local proper-clock normalization must be distinguished from bare coordinate K.

G405 supplies the general threading geometry and actual common marked
record reconstruction, conditionally at its banked scope. It supplies no
physical response, selected history, guide material or radiation law. OB1
is a reviewed conditional UNPROMOTED dependency, whose stationary ideal
reciprocal-loop result is a comparison limit. G176 remains WORKING;
G166 native assembly OPEN; G312 remains GR FILTER ONLY. No new premise,
accepted dependency, physical identification or canon is authorized.

Pinned-by-HABIT: the circle, stationary worldline, linear b(t), matching epoch,
and ideal guide enforcing future metric-null tangents. Free-and-explored:
finite rates and circulation values within a strict positive-slice window.
The exact geometry and induced null condition are pinned-by-THEORY only at
their supplied-source scope. No free-geodesic claim is made for a guide.

## Independent analytical route

Use polar labels x=R cos(theta), y=R sin(theta). Put

    A(t)=R² b(t)/2=A_e+q(t-e), q=R² bdot/2,
    theta=s alpha, s in {+1,-1}, 0<=alpha<=2pi.

The full pullback to the route is

    g_route=L²[-(dt+A(t)dtheta)²+R²dtheta²].

Future orientation relative to U=L^-1 partial_t requires
dt+A dtheta=R |dtheta|. Hence the actual-traversal equation is

    dt/dalpha=R-s A(t), t(0)=e.                                  (SF1)

For q!=0, the integrating factor exp(s q alpha) gives

    t_s(alpha)-e=(R-s A_e)[1-exp(-s q alpha)]/(s q),
    F_s(e)=e+(R-s A_e)[1-exp(-s Q)]/(s q), Q=2pi q.               (SF2)

For q=0, F_s(e)=e+2pi(R-s A_e). The limit is removable; evaluate with
expm1 or an explicit zero-rate branch. The interval map is affine in e:

    dF_s/de=exp(-s Q)>0.                                        (SF3)

The same constant L/c_E multiplies both stationary proper clocks, so SF3
is also their proper-clock pulse slope. For any finite positive emission
interval staying in the guard, its whole duration transforms by this same
factor exactly. This is an arrival-clock correspondence. No frequency-energy,
phase, photon, intensity or guide transport law is implied.

The metric coordinate slice is positive iff |A(t)|<R on the route; the
full neighborhood uses |b(t)| sqrt(x²+y²)/2<1. Linear A is monotone, and
positive slice on the entire time interval from earliest emission to latest
arrival follows from its endpoint bounds. Checking only A_e is insufficient.
The analytic formula outside this window is not an admitted positive-slice
benchmark. For q>0 one branch approaches A=R while the other can cross it;
the latter requires (R+A_e)exp(Q)<2R. A slightly wider spatial neighborhood
also requires a strict margin. No global-in-time linear profile is admitted.

With orientation Delta_-plus=F_-(e)-F_+(e),

    Delta_-plus=2[R(cosh Q-1)+A_e sinh Q]/q.                      (SF4)

Its frozen value is 4pi A_e, with the opposite sign if one reports F_+-F_-.
For q!=0 the sign is the sign of A_e+R tanh(Q/2). Thus a nonzero changing
history can create an asymmetry when initial circulation vanishes, and can
reverse the frozen ordering for appropriately signed nonzero A_e. All such
witnesses must independently pass the complete traversal guard.

If b is frozen ONCE at an epoch e0 and the fixed frozen geometry is reused
for neighboring emissions, both frozen pulse slopes are 1. If a different
frozen metric b=b(e) is chosen separately for each emission, differentiating
that family gives 1-s2pi q instead. These are different controls. The latter
is not the repeated-signal slope in one fixed frozen geometry.

## Calibration and adverse checks to perform

All b profiles share the same comoving lapse at fixed L. In g/L² the lapse
is 1; in bare g with K=partial_t it is L. An absolute dimensionless depth
therefore requires the declared comparison-clock calibration; equal lapse
or equal completed clock-leg depths across b must not erase the retained
shift and densities. c_E alone selects neither L, R nor b(t).

Holding dimensionless parameters fixed and changing L scales all proper
transit and event durations by L/c_E while leaving pulse slopes unchanged.
An initial full marked metric/first-derivative record can supply b and bdot
at its common marking; it does not derive the linear continuation law or
physically acquire those records. Pulse slopes fix only q=R² bdot/2 in this
family. Independent radius/clock calibration is needed to disentangle its
dimensionful components. Equal local lapse alone cannot supply these data.

The guide restriction is substantive: at b=0 the ambient metric is flat,
and a circular future null route has nonzero radial acceleration, which is
not proportional to its tangent. It is therefore not a free null geodesic.
G220's free-geodesic energy/clock formula cannot be used without a separate
guide transfer argument. For time-dependent threading, the two route
integrals sample different spacetime histories; the stationary single-time
circulation cancellation cannot be imposed on them.

Planned independent numerical route: integrate the actual-time angular ODE
dalpha/dt=1/[R-s A(t)] with an event at alpha=2pi, using an implementation
that imports no parent scientific function. Compare these arrivals and
finite-difference emission derivatives to SF2/SF3; inspect original full
metric-null and future-root residuals; test positive/negative/zero/tiny rates,
nonunit R and L, frozen controls, sign reversal, inadmissible full traversal,
and the flat-guide/free-geodesic distinction. Numerical checks are finite
FLOAT64 diagnostics, not proof of the formula's quantifiers.

Resources: CPU, single library thread, one scientific subprocess in this
context at a time; existing capture_existing.py <=180 seconds/2048 MiB;
PYTHONDONTWRITEBYTECODE=1. Write only review_routes/. No GPU, production
grids, subagents, git mutation, protected/runtime/disk/archive inspection.
Finite controls/tolerances will be saved before confirmation. At deadline
return reviewed conditional/narrowed/refuted/unresolved finding and omissions.
