# PIA1 independent source-first mathematical interface review

Status: source-first review completed before exposure to the PIA1 initial
candidate or parent control implementation. This is a scoped conditional
derivation and review record, not a maintained scientific account or physical
source admission. Parent final integration and candidate remain to be reviewed.

## Context, sources and exposure

Date: 2026-10-05. Actual separate subagent context `/root/pia_math`, Codex GPT-6
family inherited from parent; exact model variant was not exposed to this
reviewer. Shared model is allowed and no different-model claim is made.
Independent implementation and argument are distinguished from independent
physical evidence: the implementation below imports no parent code, but its
equations deliberately come from the same owned FRI1/TSI1 sources.

I independently read actual HEAD
`0c5386a6a6749de9dec6d4524b2fbdc1dbed5981`, branch `grok`, and status. No tracked
dirt was then present; the new PIA1 package and old untracked paths were visible.
I did not open protected payloads. Parent startup synchronization, prior full406
PASS and continuation guard PASS are attributed dispatch evidence, not checks
independently rerun by this reviewer. The scoped-subagent startup exception in
on-disk AGENTS.md applies.

Read sources: on-disk AGENTS.md; CLAUDE.md How we work, DRIVER TRIGGERS and repo
discipline; triggered no-shortcuts, completeness-map and verifier-before-record
protocols; PIA1 WORK_ORDER; UDT_DEVELOPMENT R16TSI/R16FRI and R8CPR;
FRI1 INITIAL_CANDIDATE; TSI1 INITIAL_CANDIDATE. Source hashes are in
CONTROL_RESULT.json. No external primary-source slot was used; the parent
owns that audit. No PIA1 implementation or candidate was read for this phase.

Scope: the stated finite FRI1 domain and clock/frame/record interface only.
No Hubble identification, mass mapping, physical radius-distance identification,
native geometry selection, instrument feasibility theorem or new physics.

## 1. The domain has large necessary redshift and geometry consequences

FRI1 supplies, conditionally,

    mu=mH in [.005,.01], A=aH in [.05,.1], E in [1,10],
    0<y=1/(HR)<=1/50000, principal B_*=0,
    h=1-3mu/A, w=sqrt(mu/A^3-1),
    Z=(1-wB)/(sqrt(h) alpha y).

These are free-and-explored physical restrictions, not inferred observations.
Its actual-incidence proof supplies `0<=B<=.0001`, `w<9` and
`alpha<=1.000000006`. Also `.4<=h<=.85`. Thus the safe lower bound is

    Z >= .9991 / [sqrt(.85) * 1.000000006 * .00002]
      = 54183.804776552... > 54180.

Using weak inequalities here is conservative even where FRI1 has strict ones.
All factors are positive, so squaring the last comparison is legitimate;
the saved control checks it using exact rational arithmetic. This is an
analytic uniform lower bound, not the exact minimum of Z over the domain.

Independently of any physical mass definition,

    R/a=1/(Ay)>=500000, R/m=1/(mu y)>=5000000,
    1/H between 10a and 20a,  m/a in [.05,.2].

These are necessary geometric restrictions. In this tail
`f(R)=1-2mu*y-y^-2<0`; R is the areal coordinate in the supplied continuation,
where it is timelike, not an automatically measured observer-source distance.
Consequently `R/c_E` below is a dimensional expression, not a measured light
travel time or baseline. A known absolute emitted frequency and identified
received frequency would permit the necessary test `nu_e/nu_o>54180`, after
admitting this clock readout. Passing that test does not certify the rest of D;
failing it would reject this particular protocol's admission, not UDT generally.
An unknown source normalization cannot itself establish absolute Z.

## 2. Observing coverage and the supplied shape are linked

Use receiver seconds t, `K=c_E H`, and a chosen dimensionless coverage
`C=K Delta t>0`. Direct unit conversion gives

    a=A*c_E*Delta t/C,
    R>=50000*c_E*Delta t/C.

FRI1's long base control has `H Delta ell=1`, so C=1. At this coverage,
`a/c_E` is `.05` to `.1` of the receiver duration and `R/c_E` is at least
50000 times that duration. A physical source radius supplied independently
would reciprocally constrain the required duration. The source radius was
not independently supplied by FRI1, and these equations do not identify a real
clock's size with a. a is its orbital areal coordinate, not the material clock
radius. C=1 is one frozen control's coverage, not a universal required observing
time or an optimized design theorem. Better independently admitted errors
could change useful coverage.

FRI1's purely numerical long-control choices have `q/H=.001`,
`sigma/T=.001`, `epsilon_z=.003`, `eta=.0005`. Preserving only a literature
precision number while changing coverage, drift or time calibration does not
preserve its approximately 1.9% total deterministic H-interval width.

## 3. Emitter time, source drift, cycles and receiver calibration

Let s be emitter proper seconds. R8CPR/TSI1 give exactly `ds/dt=1/Z` along
the actual incidence map. If a source supplies an independent bound
`|d log nu_e/ds|<=q_e` over the entire relevant emitter interval, then

    |d log nu_e(s(t))/dt| <= q_e/Z(t) <= q_e/54180.

The corresponding FRI1 receiver-length q is `q_e/(c_E*54180)`. Conversely,
a drift stated in receiver seconds divides only by c_E to become q. Neither
the source's bound nor its domain of validity is established by this chain rule.
An arbitrary source drift can imitate a finite timing drift.

For every receiver interval fully within the admitted support hull,

    Delta s = integral dt/Z(t) <= Delta t/54180.

If distinct emitter pulses have proper spacing at least p_min>0, at most
`floor[Delta t/(54180*p_min)]+1` pulses can lie in the receiver interval.
If only an upper source frequency is known, the corresponding accumulated
cycle count is at most `nu_e,max*Delta t/54180`. These necessary sampling
bounds do not describe flux, detectability, pulse identification or detector
bandwidth. There is no claim that they alone exclude an optical or astronomical
source.

If the same supplied conditional branch and FRI1 rate bound are retained for
all later times, integrating `K(1-eta)<=d log Z/dt<=K(1+eta)` gives

    1/[K(1+eta) Z(t)] <= s_*-s(t) <= 1/[K(1-eta) Z(t)].

This strengthens the finite-emitter-endpoint bookkeeping conditionally; it
does not assert a physical source exists up to that endpoint or supplies
infinitely many individually detectable ticks. Future branch persistence is
explicit in this statement, rather than inferred from finite data.

Receiver calibration is separate. If `t_hat=(1+kappa)t`, a measured drift
per reported second is `K_hat=K/(1+kappa)`. Knowing c_E as a calibration scale
does not eliminate uncertainty in this clock map. A bound on kappa must be
propagated or represented by justified time-error bounds on the whole support.
Reference-frequency drift in the receiving instrument can likewise enter
the observed log-frequency difference; a constant reference normalization
cancels, but arbitrary drift does not. A deterministic error claim cannot be
borrowed merely from an Allan deviation, standard uncertainty or finite-sample
scatter without an explicit statistical-to-bound assumption or a revised
probabilistic inference theorem.

## 4. Finite-window operators and angular reference must match

For the actual FRI1 rectangular translated means with one fixed width delta,

    Ybar(t) = integral_(-1/2)^(1/2) Y(t+delta*u) du,
    dYbar/dt = integral_(-1/2)^(1/2) Y'(t+delta*u) du.

The derivative interval is inherited because this is a normalized positive
average and the whole support hull is admitted. There is no separate width
bias for this specific operator. Unknown center shifts are already handled
by FRI1's sign-safe time denominator; unknown width or response changes are
not silently covered by that argument.

A bounded repair, if physical timing responses are independently known:
for Lipschitz Y with `|Y'|<=L`, centered widths delta_i and delta obey

    |mean_delta_i Y(t)-mean_delta Y(t)|
       <= L*|delta_i-delta|*integral_(-1/2)^(1/2)|u|du
       = L*|delta_i-delta|/4.

Here `L=K(1+eta)+q_seconds` under the admitted source bound. This inequality
is an optional same-premise mathematical error term, not a measured instrument
bound. Its dependence on unknown K must be respected when solving an inverse
interval; substituting an estimated K without justification is circular.

The instrument's estimator also matters. `mean[-log nu_o]` generally differs
from `-log(mean nu_o)`. Jensen's inequality fixes their ordering but does not
make the difference constant in time. For the synthetic smooth function
`Y(t)=t^2` and width .4, the saved numerical example has the differences
0.0000709298 at center0 and 0.02631766 at center1. Thus taking differences
between windows need not remove the operator mismatch. That control diagnoses
an operator error; its values are not a UDT signal or physical noise model.

TSI1/FRI1 use signed position in the specified parallel radial frame, not
angular diameter or an arbitrary telescope frame. In an equatorial small
signed-angle description, residual frame rotation psi(t) and source-centroid
motion beta(t) add their own time dependence. A bound on their rates controls
differences of equal translated means, but absolute per-window angular error
also needs a reference-epoch offset bound. A constant unknown offset cancels
in differences; arbitrary rotation does not. The broad FRI1 envelope is
`|dtheta/dt|<K/20000`; this is an upper bound on the modeled source angular
change, not a minimum signal or a justified observing requirement. The
special witness has the narrower K/290000 bound. Neither a pointlike circular
emitter nor its parallel radial frame is obtained merely by observing a
resolved maser disk or recording angular positions.

## Checks, survivor and return point

Twelve independent standard-library controls ran once and passed. The exact
command was:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_physical_clock_interface_audit_2026-10-05/review_math/check_interfaces.py > udt_physical_clock_interface_audit_2026-10-05/review_math/control.stdout 2> udt_physical_clock_interface_audit_2026-10-05/review_math/control.stderr
```

The script sets a 2GiB address-space cap, uses one BLAS thread (no BLAS actually
imported), no GPU and no wall/CPU timeout. It records Python/platform and source
hashes. Exact Fraction comparisons check algebraic recombinations; other
controls are floating-point sanity checks and illustrative estimator witnesses,
not formal certification. Output logs and JSON are retained. No failed run,
parameter sweep or discarded repair occurred. Parent FRI/TSI implementations,
ray quadratures, continuum derivations and full406 were not replayed; no
independent physical source experiment was reconstructed.

The strongest source-first survivor is conditional: FRI1's physical admission
requires a particularly restricted geometry, a redshift exceeding 54,180,
correct clock-map calibration and a deterministic record/error operator of
the specified form. Good local frequency metrology alone does not establish
those joints. No defect in FRI1's finite-window proof was found in this review;
the potential defects are semantic transfers to actual devices without the
missing interface. Final candidate and integrated text require an exposed
review before a final PIA1 verdict is issued.
