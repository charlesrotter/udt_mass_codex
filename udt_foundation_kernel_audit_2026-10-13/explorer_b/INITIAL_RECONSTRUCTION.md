# Explorer B — initial foundation-to-kernel reconstruction

Status: unreviewed conditional analytic candidate, fixed before comparison with
old proofs or other researchers. No physics is adopted and no old result is
regraded. Source snapshot: grok
`67246b3528c8fbc363b98c1d06794517e8109f65`.

## Finding and scope

The supplied metric contains reciprocal positive temporal/radial scale factors.
Their normalized difference is exactly a hyperbolic tangent. That algebra does
not yet identify the factors with two received clock rates. For the explicit
stationary-clock preparation on this static metric, the two future signal
frequency ratios multiply to one; their travel delay does not by itself slow
ticks. Conversely, two receding inertial clocks can both receive slower ticks,
because opposite future signal maps are not mathematical inverses. These are
different scoped facts, not a whole-theory verdict.

The separately supplied June 18 owner wording warrants a useful conditional
reconstruction: a positive continuous scalar comparison that depends only on a
signed additive depth difference and composes multiplicatively on all such
differences is exponential. The same statement does not determine a radial
metric coefficient or make two opposite received rates both less than one.
One cannot obtain that last property by calling inverse factors mutual
slowdown. Weaker, ordered composition and actual causal-path composition remain
distinct alternatives requiring their domains and operational data.

## 1. Exposure, provenance and methodological choices

`INITIAL_APPROACH.md` was saved before the parent supplied the new
`OWNER_SOURCE_ADDENDUM.md`. I then read that addendum and
`ADDENDUM_SOURCE_PINS.json` before writing this reconstruction. It adds the
dated attributed owner requirement of difference-dependence and consistent
composition. The addendum's claim of unique metric derivation is assessed here,
not assumed. Its full underlying owner conversation remains unverified.

All initial exposures listed in INITIAL_APPROACH apply. No old derivation,
current scientific summary, founding.md, sibling argument or parent scientific
result was opened. The parent received my chosen approach and then my response
to the addendum; no researcher's result was sent back. Method instructions do
expose kernel notation/status, so this is staged exposure, not an absolutely
blind reconstruction. Same model, separate context; no different-model or
independent implementation claim. There is no numerical computation to replay.

The prompt screenshot was directly inspected and independently hashed. The
other quotations were read from the starting packet/addendum, with their full
source hashes supplied by the parent, not their old surrounding interpretations.
The conflicting illustrative units are not quantitative physics; Prompt 4
explicitly calls the number a metaphor.

Before derivation the following were fixed: investigate the benchmark's regular
static radial domain; use ordinary proper clocks and metric-null pulse paths
as the explicit operational realization; compare two future signal experiments;
test the mathematical distinction between delay and rate; and keep selected
observers/path preparations separate from owner-derived restrictions. The
stationary and moving test clocks below are free-and-explored preparations.
No field equation, action, profile selection, source, boundary, quantum model,
mass result, new independent physical field or cosmological fit is introduced.

## 2. Operational object before reciprocal algebra

Let A and B be future timelike worldlines with ordinary proper times tau_A and
tau_B. Choose a smooth family of future-directed null pulses linking an
emission interval on A to a reception interval on B, without branch changes or
caustic ambiguity in that interval. It defines a strictly increasing map

    tau_B,receive = F_AB(tau_A,emit).

If identical ideal clock sources emit nu_0 ticks per proper second, the
received tick rate in units of the receiver's proper seconds is

    R_AB = nu_B,receive / nu_0 = 1 / F_AB'.

This is the differential narrow-pulse-train limit. Finite pulse separations
instead use delta tau_A / delta tau_B; the distinction is explicit if F is
nonlinear. Mutual received slowdown means R_AB<1 and R_BA<1 in the two stated
experiments, with the emission/reception events and calibrations specified.

The inverse function F_AB^{-1} relates a B reception event back to its A
emission event. It is not a future signal traveling from B to A. The latter
experiment has its own map F_BA and generally different events. A future
round-trip composition advances the A clock, and is not required to be the
identity. It is therefore invalid to infer either that mutual slowing is
impossible in every Lorentzian geometry, or that two positive reciprocal
numbers already establish it.

This construction uses no propagation field equation beyond the stated
metric-null pulse assumption. If a different physical propagation or clock
law is intended, its replacement would need to be supplied and audited.

## 3. What difference-dependence and composition do establish

Consider the following precise formalization of the addendum, rather than
silently treating its words as an already specified equation. A positive scalar
comparison D depends on x=phi_B-phi_A alone; D(0)=1; and

    D(x+y)=D(x)D(y)

for all signed differences in its additive connected domain. Assume continuity
(or smoothness inherited from a chosen smooth geometric comparison). Taking
h=log D gives h(x+y)=h(x)+h(y). For rational q, h(q)=q h(1) after choosing a
depth unit; continuity extends this to real arguments. Locally the same result
follows by differentiating at y=0: h'(x)=h'(0). Thus

    D(x)=exp(k x),       D(-x)=1/D(x).

No numerical verification is needed for this exact conditional statement.
The sign and nonzero magnitude of k can be absorbed into the orientation and
scale of the depth label unless phi already has a fixed physical definition.
k=0 is the trivial comparison and cannot be discarded by composition alone.
Without a regularity condition, the functional equation itself allows
noncontinuous additive logarithms; the packet's smooth benchmark is regular,
but the semantic owner assertion alone does not state that hypothesis.

If D is a ratio of stationary proper-clock lapse factors, then

    N(phi_B)/N(phi_A)=exp(k(phi_B-phi_A))

implies N(phi)=N_0 exp(k phi). A calibration fixes N_0; an orientation/unit
convention k=-1 produces the supplied temporal coefficient N^2=exp(-2phi).
This step is conditional on identifying the abstract comparison with that
lapse ratio. Difference-dependence in phi is translation invariance of the
depth label, not yet a rule assigning phi to spacetime positions or a proof
that no physical observer is privileged.

Three limits on the inference matter:

* No radial proper-length coefficient appears in this functional equation.
  It supplies neither A(phi)=1/N(phi) nor staticity, spherical symmetry,
  areal radial gauge, or a profile phi(r).
* If both opposite received rates are identified with the same D at reversed
  arguments, full signed composition yields their product one. Both cannot
  be strictly below one. Likewise an even positive dilation magnitude obeying
  this same full group law is identically one: D(-x)=D(x)=1/D(x).
* There is a mathematically consistent weaker alternative: D_AB=exp(-k
  |phi_B-phi_A|), k>0, is symmetric and less than one for distinct depths.
  It composes through an intermediate B only when B lies between A and C in
  depth. For A=C and B distinct it fails the full position-group law. An
  accumulated nonnegative path depth can instead add on concatenated paths,
  but that is path-dependent data and a future return path need not have
  zero depth. Neither alternative is identical to unrestricted signed
  difference-composition, and neither alone constructs a metric realization.

The addendum therefore narrows the algebra only after its scalar, composition
law and domain are defined. Its mutual-clock claim needs a causal operational
realization; it cannot by itself serve as proof of a structural metric identity.

## 4. Supplied benchmark: exact local and signal calculations

On a regular interval r>0 with finite smooth real phi(r), write

    ds^2 = -N(r)^2 c_E^2 dt^2 + A(r)^2 dr^2 + r^2 dOmega^2,
    N=exp(-phi),   A=exp(phi),   N A=1.

Staticity, spherical symmetry, diagonal form, areal r and N A=1 are supplied
branch restrictions. Finite positive N,A give the Lorentzian local domain.
This is not a derived unique global model of the original postulates.

For a clock fixed at r,angles, d tau=N dt. On a static time slice the radial
proper-length increment is d ell=A dr. Radial null pulses satisfy

    dr/dt = +/- c_E N/A = +/- c_E exp(-2phi),
    |d ell/d tau| = c_E.

The latter is a local clock/ruler measurement by the static orthonormal frame.
The former is a chart speed. Their meanings cannot be exchanged. With ordinary
proper clocks and metric-null signals, finite local c_E is already built into
the calibrated Lorentzian metric. The claim that an unobservable underlying
infinite speed produces this geometry is not a further consequence of these
equations. If phi=0 is interpreted as removing all positional dilation, the
benchmark still has finite null slope c_E; that interpretation of phi is an
additional identification to test, not established by the packet.

Take A at radius a and B at b>a, same angular direction, with both stationary.
Their future radial travel time is

    T_ab = (1/c_E) integral_a^b A(r)/N(r) dr
         = (1/c_E) integral_a^b exp(2phi(r)) dr.

Finite smooth phi on the compact path makes this finite. Staticity and fixed
endpoints make T_ab independent of emission time. Thus t_receive=t_emit+T_ab,
and neighboring pulses satisfy delta t_receive=delta t_emit. It follows that

    F_AB' = N(b)/N(a),
    R_AB  = N(a)/N(b) = exp(phi(b)-phi(a)),
    R_BA  = N(b)/N(a) = exp(phi(a)-phi(b)),
    R_AB R_BA = 1.

The reverse experiment uses a different future ray; here its reciprocal result
comes from the static endpoint lapse law, not from mistaking it for the inverse
of a causal map. Unless endpoint lapses are equal, one direction is redshifted
and the other blueshifted. Equal endpoint lapses yield no rate shift even with
a finite nonzero travel delay, including a nonconstant interior profile.

This directly refutes the implication “the supplied static metric necessarily
gives stationary separated clocks mutual received slowdown.” It does not prove
the founding requirement impossible for other worldlines or geometries.
Stationary clocks may be accelerated when N' is nonzero; their preparation is
declared, not smuggled in as an unaccelerated universal. The exact phi=0 control
below also uses unaccelerated clocks.

## 5. Metric restriction and calibration sensitivity

Repeat the stationary calculation for an arbitrary regular static spherical
areal metric with positive smooth N(r),B(r):

    ds^2=-N^2 c_E^2 dt^2+B^2 dr^2+r^2 dOmega^2.

It gives T_ab=(1/c_E)integral B/N dr, the same endpoint rate R_AB=N(a)/N(b),
and the same local proper clock/ruler null speed c_E. No B=1/N was used. Thus
proper clocks, metric-null signals and this clock-rate comparison do not fix
the reciprocal product. The B freedom changes geometry/travel time and is
not claimed to satisfy every founding requirement; it demonstrates only the
specific absence of B from these candidate selecting conditions.

Likewise local null directions constrain a conformal class rather than an
absolute clock scale: multiplying a Lorentzian metric by a positive smooth
Omega^2 preserves ds^2=0 while multiplying proper-time increments on a fixed
curve by Omega. This follows directly from the line element and does not
import a physical field equation. Null cones alone therefore cannot reconstruct
all clock comparisons or fix the metric normalization. A full conformal change
also changes areal radius, so it should not be described as preserving every
benchmark gauge restriction.

Even the displayed product N A=1 is tied to the chosen calibrated static
chart. Under t'=lambda t with fixed c_E units, N'=N/lambda while A is unchanged.
Endpoint ratios are unaffected, but the pointwise N A normalization changes.
A single time normalization can fix a constant N A; it cannot eliminate a
radially varying product while retaining areal r. A general radial coordinate
can remove such a product at the expense of the areal angular coefficient.
Thus the restriction has both a normalization aspect and substantive content
within the stipulated areal static branch.

## 6. The reciprocal scalar algebra that survives

For any positive pair p,q, independently of any metric, define a normalized
difference K and logarithmic contrast eta by

    K=(p-q)/(p+q),       eta=(1/2) log(p/q).

Then exactly K=tanh(eta), |K|<1, and exchanging p,q reverses its sign. Common
rescaling of p,q cancels. This is a useful identity, not a proof that p and q
are the needed physical objects or that normalized subtraction is a unique
readout selected by the owner statements.

In the supplied branch, choosing p=A=exp(phi) and q=N=exp(-phi) yields

    (A-N)/(A+N)=tanh(phi).

Choosing the squared metric magnitudes instead yields tanh(2phi); reversing
the order changes sign. Taking a physical positive rate R and using pair
(R,1/R) yields tanh(log R), whereas pair (sqrt(R),1/sqrt(R)) yields
tanh((1/2)log R). The pair choice and depth normalization are load-bearing.

Inversion symmetry alone does not uniquely select this scalar: log(p/q),
(2/pi) arctan(log(p/q)), and tanh(a log(p/q)) for a>0 also reverse sign under
exchange, with the latter two bounded. If normalized difference is adopted as
the definition, tanh follows uniquely from that definition and the positive
pair. If a specific rational composition law is also postulated, that is a
further condition to audit, not an automatic consequence of the word reciprocal.

Thus a complete defensible conditional chain is:

    supplied regular calibrated positive pair
        -> chosen logarithmic contrast / normalized difference
        -> exact hyperbolic-tangent identity.

The separate physical chain would need:

    metric + worldlines + future signal families + clock/ruler calibration
        -> actual received-rate maps
        -> justified identification of the kernel's pair/depth/readout.

The benchmark alone does not supply that last identification. The actual static
rates above are available as a test; they must not be replaced by coefficient
labels merely because those coefficients are reciprocal.

## 7. Positive control: two future signals really can both slow

To prevent a negative result wider than its hypotheses, take the regular
phi=0 benchmark on a radial annulus. Set c=c_E and use x=r-a on an interval
away from r=0. A sits at x=0; B follows x=L+v t with L>0 and 0<v<c, restricting
times to maintain positive separation. Both are inertial on this radial
Minkowski preparation. Let beta=v/c and gamma=(1-beta^2)^(-1/2). Their proper
times can be chosen tau_A=t and tau_B=t/gamma.

An A pulse emitted at t_e reaches B when c(t_r-t_e)=L+v t_r, so

    F_AB(tau_A)=(tau_A+L/c)/[gamma(1-beta)],
    F_AB'=1/[gamma(1-beta)].

A B pulse emitted at coordinate time t_e=gamma tau_B reaches A at
t_r=t_e+(L+v t_e)/c, so

    F_BA(tau_B)=gamma(1+beta)tau_B+L/c,
    F_BA'=gamma(1+beta).

Since 1/[gamma(1-beta)]=gamma(1+beta), both received rates are

    R_AB=R_BA=sqrt((1-beta)/(1+beta)) < 1.

Both maps run into the future. Their derivatives are equal rather than
reciprocal; the round-trip derivative is (1+beta)/(1-beta)>1. This directly
shows why inverse-map reasoning cannot prohibit mutual received slowing.
It supplies ordinary relative-motion slowing, not an additional positional
effect, and is neither a full model of the original cosmology nor its empirical
validation. It is an exact control of the logic and comparison objects.

## 8. Diagnostic closure, survivors and next discriminators

The stationary mismatch was checked at equation level: no omitted term within
the declared diagonal static radial metric; no numerical approximation or
convergence issue; the restrictions are fixed observer radii and staticity;
the claim is only that preparation. Their force was checked by explicitly
changing to receding clocks, which changes the result. No compensating physical
mechanism is introduced.

Survivors before old-source comparison are: (i) exponential scalar comparisons
under explicit regular signed composition; (ii) the supplied metric's local
and stationary-signal consequences; (iii) exact positive-pair tanh algebra;
and (iv) compatibility of mutual received slowing with two actual future signal
experiments in at least one ordinary moving-clock preparation. What remains
unestablished is the postulates-to-unique-metric implication and the identification
of this kernel with the intended additional positional received-clock effect.

The next informative step is source comparison, not a larger numerical survey:
locate the exact old structural-identity argument, its definition of reciprocal
comparison, calibration and composition domain. It could supply a missing
hypothesis, reveal that a conditional lemma already owns the result, or exhibit
an invalid replacement of future received-rate maps by inverse coefficients.
A time-dependent reciprocal radial extension is an available further analytic
control if the comparison hinges on staticity rather than the pair algebra;
it has not been adopted or used as evidence here. The campaign should return
only after that comparison and authorized fresh adversarial review, with any
remaining meaning question explicit. No whole-theory no-go, empirical claim,
premise revocation, unique profile or physical-selection theorem is asserted.

## 9. Additional source hashes and verification limits

Initial packet and authority hashes are in INITIAL_APPROACH. Additional
independently computed SHA-256 values follow. Hashing is correspondence, not
scientific verification or recovered conversation provenance.

| File | SHA-256 |
|---|---|
| OWNER_SOURCE_ADDENDUM.md | 859303072648d7f8011e0753acfc5274ac28dfd6a34cbc8143e99227a0a87fcb |
| ADDENDUM_SOURCE_PINS.json | 749102d46bf918d7740a4b95dd7ac2c9f4c3e629a96c630a1195bea041151aca |
| UDT_RESEARCH_OPERATING_PLAN.md | c85c2da3d62e1b6fe0fae43847764e222857b8a9705c1b6d86f7f60e24f0c77c |
| no-shortcuts/SKILL.md | fd3a1f3218481134f2af829d3ae4175ac53518f75bf9673287efbfb7d7708fc1 |
| completeness-map/SKILL.md | a8cf9e5f4a6d35a0d0ebfe4bc48dbf328ca74e318f020a6a22cb683666a611c0 |
| solver-first/SKILL.md | b80b1ca9fe5ebccb7170c39b97ca26f32c950650328d9a2f380c3793cb9cd61b |
| verifier-before-record/SKILL.md | 9b3a4aacd4b4006b2b7f01edada73b7c87b99bea6e754583558713bfc145e5ac |

I independently reran `git branch --show-current`, `git rev-parse HEAD`,
`git status --short --branch`, `git status --porcelain=v1 --untracked-files=no`,
and the listed SHA-256 reads. Tracked status was empty. A process listing from
the available tool namespace showed only its own sandbox/tool processes; this
is not proof of host-wide process absence. No GPU, solver, CPU scientific
worker, external source search, numerical test or independent implementation
was used. Parent's full406/startup evidence is attributed, not independently
replayed or claimed as proof of these arguments. All findings await fresh review.
