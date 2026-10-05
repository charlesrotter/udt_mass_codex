# OAA1 mathematical review — sealed source-first argument

Review state: independent source-first derivation and finite checks completed;
parent OAA1 candidate, implementation and results have not been read. This is
not yet a review verdict on that unexposed candidate. Reviewer `/root/oaa_math`
is an actual fresh separate context on the same inherited model, with independent
argument and implementation. Different-model and human independence are absent.

The assigned parent message supplied the intended questions, operational resource
limits and continuing-session startup attribution. After my first derivation I
sent the parent the endpoint-normalization result; the parent replied that its
own derivation had already reached the same limit and a radial-limit residue.
No parent residue formula, candidate or code was exposed. This communication is
disclosed rather than described as a completely blind comparison.

## Authority, sources and scope

I independently checked branch `grok`, HEAD
`11cca783c02f94fad287a95595928df36340ad06`, and no tracked changes at intake.
The status showed the disclosed old local names and the new OAA1 workspace.
Protected payloads were neither read nor hashed. Per AGENTS scoped-review rule,
top-level startup, remote synchronization, the normal guard and full 406-row
premise audit are attributed to the parent's recorded checks, not independently
claimed. The parent reported its prior full audit PASS in 408.622785 seconds.

Read from disk: AGENTS, CLAUDE How we work / DRIVER TRIGGERS / Repo discipline,
the no-shortcuts, completeness-map and verifier-before-record skills; OAA1 work
order; central R8 timing/SGE1, R8CGE, R8CPR and R16; exact CPR1 initial candidate,
clarifications and premise ledger. Source hashes are in SOURCE_FIRST_FREEZE.json.
No external literature or imported physical equation was needed for this argument.

The only physical geometry is the same **conditional** CPR1 family. Circular
test emitter, outgoing finite-energy radial receiver, outward null ray, regular
strict source bound, positive H and escaping/regular limiting incidence retain
their source meanings. The numerical choices are `free-and-explored` query data.
Definitions below are differential-geometric methods, not a new metric law,
observer population, physical response or admission of this completion as UDT.
The maximum conclusion is a conditional distance-clock relation and a causal
return obstruction. No native/additional effect, global distance ceiling or
X_max realization is established.

## 1. Endpoint affine normalization on the actual circular-source ray

Use c_E=1, so proper time is in length units. For CPR1's Killing-energy-one
affinely parametrized future ray, k^r=s>0 and

    L0(R,b) = lambda_o-lambda_e = integral_a^R dr/s(r,b).
    omega_e = (1-Omega*b)/sqrt(h), omega_o = A > 0.

Scaling k to k/omega_j makes its frequency one at endpoint j. Its affine
parameter consequently scales to omega_j*lambda. Define on this specified ray

    D_e = omega_e L0,    D_o = A L0.

These are positive, affine-gauge-invariant, endpoint-observer-normalized null
affine lengths. An arbitrary original affine rescaling cancels in each product.
Changing the endpoint observer generally changes the length; that is a changed
physical comparison, not affine gauge freedom or a forbidden preferred observer.
The chosen ray resolves any exponential-map/branch ambiguity. The construction
does not establish an echo measurement, a spatial-slice length, a luminosity or
angular distance, or SGE1's auxiliary-congruence integral int omega(lambda)dλ.

The exact relation is

    D_e / D_o = omega_e/A = Z.

This concerns two normalizations of one future ray. It does not substitute the
inverse correspondence for an actual future return. Nor does it establish that
the owner has already adopted one normalization as physical separation.

All rays here retain the actual incidence with fixed emitter/receiver histories.
In particular b=b(R) varies between rays. Differentiating the two source equations
gives, with q=1-Omega*b and I=int_a^R dr/(r²s³),

    dt_e/dR = A/(v*q),
    db/dR = -[Omega*A/(v*q)+b/(R²s)]/I.

No derivative is computed by freezing b for the orbiting source.

## 2. Positive-H limit and the approach-direction restriction

Let S(b)=sqrt(1+H²b²). On any compact neighborhood of a strict limiting b_*,
the source inequality makes s uniformly positive for r>=a. Define

    C(b) = -a/S(b) + integral_a^infinity [1/s(r,b)-1/S(b)] dr.

The integral converges because its integrand is O(r^-2). Equivalently, setting
x=1/r gives the nonsingular expression

    C(b) = -a/S + integral_0^(1/a)
           b²(1-2mx)/[S*s(x,b)*(S+s(x,b))] dx.

These parameter-dependent integrals are smooth near b_*. Expansion, with
uniform derivatives there, yields

    L0 = R/S(b)+C(b)+O(R^-1),
    A = S(b)/(H R)-E/(H² R²)+O(R^-3).

CPR1's implicit-function argument supplies a smooth actual branch in x=1/R,
with b=b_*+O(x). Therefore

    D_o = 1/H + B/R + O(R^-2),
    B = S_* C(b_*)/H - E/(H² S_*).
    D_e/Z = D_o -> 1/H,  D_e -> infinity,  Z/D_e -> H.

The b'(0) contribution cancels from the leading constant 1/H. This is why the
finite receiver-normalized limit survives actual angular incidence rather than
requiring b to stay fixed. It is independent of a,m,E,b_* within this particular
escaping class, but H remains supplied and observers outside this class are not
covered.

For derivative and side-of-limit claims the coefficient matters. Set

    omega_e,* = (1-Omega*b_*)/sqrt(h),
    T = S_*/(H² omega_e,*) > 0,
    z_c = H omega_e,*/S_* > 0.

The smooth x expansions give

    tau_e,*-tau_e = T/R+O(R^-2),
    Z/R -> z_c,  Z(tau_e,*-tau_e) -> 1/H,
    Z(D_o-1/H) -> z_c B,
    dD_o/dtau_e -> -B/T,
    dD_o/dtau_o -> 0.

The derivative statement follows from smoothness in x and nonzero T, not from
illegitimately differentiating an unspecified big-O remainder. If B<0, D_o
approaches from below and increases sufficiently near the endpoint. If B>0 it
approaches from above and decreases there. If B=0 this order decides neither
side nor strict monotonicity. Even when B<0, this establishes only eventual
behavior, not a maximum/monotonicity theorem over the whole history.

For CPR1's explicit b_*=0 preparation, C(0)=-a and

    B=-(aH+E)/H² < 0,
    Z(1/H-D_o) -> (aH+E)/(H sqrt(h)),
    dD_o/dtau_e -> (aH+E)/sqrt(h) > 0.

Here a local inverse-gap relation is legitimate. It must retain the preparation,
observer normalization, asymptotic domain and its conditional geometry.

The sign qualification is substantive. At fixed 0<H<1/(sqrt(27)m), take
a down to 3m through a>3m and |b_*| up toward its strict source bound. At the
limiting critical ray, s vanishes linearly in r-3m, so the positive near-source
part of C diverges logarithmically. The asymptotic subtraction remains bounded
there. Thus C and hence B can become positive while every finite member retains
strict regularity. One may choose negative b_* to keep q away from zero.
This supplies an analytic existence argument for both approach signs; the finite
counterexample below verifies a concrete admitted member. These near-photon
circular test clocks are not claimed linearly stable. Adding a stable-orbit
restriction would require its own coverage check.

## 3. Causal return and radar

The continued metric has g^(rr)=f. In the exterior cosmological region f<0,
grad r is timelike. Its pairing with the fixed future receiver is v>0, fixing
grad r to be past directed. Every nonzero future causal vector V consequently
has dr(V)>0. At the outer horizon the corresponding nonnegative inequality
holds; a generator cannot cross back into r<r_c. Thus no future causal signal
from a reception event R>=r_c in this outgoing extension can reach the circular
source at a<r_c. This is a cone argument, not a choice to send the wrong ray.

The source conditions H²<m/a³ and a>3m imply 27m²H²<1, so the outer horizon is
simple. A and L0 are finite there and CPR1's Z is finite at crossing. The later
R->infinity divergence and finite D_o limit are consequently one-way records,
not an available source-clock two-way radar limit on those late events.

If an actual future echo from an event R<r_c is assigned, the original circular
emitter's radar range is (tau_return-tau_emit)/2. In the static patch, causality
implies |dr/dt|<=f. Both outward and returning legs therefore satisfy the lower
bound

    D_radar >= sqrt(h) integral_a^R dr/f(r).

This diverges logarithmically as R approaches r_c from below. The assertion is
conditional on the specified echo's existence; I have not proved a unique free
null return branch for every circular phase or all R. Any branch/protocol loss
earlier only reduces radar availability. No inference of a finite radar ceiling
from the endpoint-affine limit is valid.

A useful exactly radial control uses a DIFFERENT static clock at a_s with
f(a_s)>0 and an ideal immediate geometrical relay at R. Its two radial null legs
give

    D_radar,static = sqrt(f(a_s)) integral_(a_s)^R dr/f(r), R<r_c.

The same logarithmic divergence occurs. This clock is accelerated in general;
it is not the geodesic circular source and is not substituted for its incidence.
An ideal relay is a declared geometrical protocol, not derived light/matter
interaction dynamics.

## 4. Finite independent checks and their limits

The equations, code, exact inputs, root/identity tolerances, iteration bound,
resources and output command were frozen before execution. All 18 finite cases
passed, with no retries or failures. They are three supplied parameter sets,
R=10^4,10^6,10^8, at 60 and 100 decimal digits. CPU only; 2GiB address-space
limit; one BLAS thread; no wall/CPU timeout or GPU. Recorded elapsed time was
20.83104658126831 seconds. Maximum scaled 60/100-digit discrepancy among b,Z,D_o,
D_e was 1.1209383736691915e-49, below the frozen 1e-40 bound.

The implementation solves the actual two-equation incidence through its scalar
elimination, preserving all Newton iterates/residuals. It independently compares
direct logarithmic-coordinate affine quadrature to the convergent-tail formula,
and explicit metric endpoint contraction to the regular A formula. It also
checks original incidence residuals, domain, emission side and normalization
ratio. Same-code assertions are regression/consistency checks, not independent
certification; the separate derivation and independent implementation are the
independence axes relative to the parent. No formal interval proof or empirical
confirmation is claimed, and no asymptotic limit is inferred from three radii.

For the counterexample m=1,a=3.001,H=.18,E=1,
b_*=-.999*a/sqrt(f(a)), choose t_*=0, u_infinity=U_infinity(b_*),
phi_0=-P_infinity(b_*). These fix one actual source/receiver preparation.

| R | receiver affine D_o | R(D_o-1/H) |
| --- | --- | --- |
| 10^4 | 5.55882503557947679 | 32.69480023921238 |
| 10^6 | 5.55558825454616205 | 32.69899060649002 |
| 10^8 | 5.55555588254588126 | 32.69903257019199 |

Here 1/H=5.55555555555555556 and the independently integrated coefficient is
B=32.69903299407383616>0. By contrast the b_*=0 preparation with m=1,a=10,
H=.01,E=1 has B=-11000 and approaches its limit 100 from below. The moderate
nonzero b_* control also passes. Full values, not these rounded displays, own
the finite checks in source_first_raw.jsonl and SOURCE_FIRST_RESULT.json.

## 5. Physical attachment and eventual candidate review criteria

The geometry supplies an invariant, explicitly normalized one-way finite affine
asymptote coupled to divergent received redshift. It does not identify the
additional UDT positional effect: a physically matched GR comparison with the
same metric, worldlines, units, ray and protocol has exactly the same Z, D_e,
D_o and causal/radar records, hence SGE1's additional contrast is zero.

Calling one record invariant does not select the metric or physical population.
Different ordinary observers/protocols may legitimately have different readouts
under one law. No claim that universality requires equal numbers is justified.
The supplied positive H sets 1/H; c_E and G_obs alone do not select H. The result
does not determine a global X_max, its realization/modulation, or prove that
all current postulates are insufficient or need an added premise.

On exposure I will reject any unqualified equivalence of affine/radar/spatial
distance, any frozen-b arrival derivative, any all-observer/global-ceiling claim,
any two-way echo beyond r_c, and any identification of same-metric GR horizon
behavior with an additional UDT effect. The strongest source-preserving survivor
is the explicitly conditional endpoint-affine relation plus causal/protocol
restrictions and the still-open physical identification.

Not repeated: full 406-row audit, general CPR1 curvature/geodesic reconstruction,
parent finite cases, native-response or empirical checks. No CANON, registry,
central maintained science or protected work was edited. All reviewer writes
remain in the assigned review_math directory. The manifest seal records bytes,
not truth, independent chronology or scientific acceptance.
