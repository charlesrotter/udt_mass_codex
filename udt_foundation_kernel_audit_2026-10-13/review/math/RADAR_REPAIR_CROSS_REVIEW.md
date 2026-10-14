# FKA1 ruler continuation and controlling repair — mathematical addendum

Reviewer `/root/fka_review_math`, 2026-10-14 UTC. Later exposure follows the
frozen SOURCE_FIRST, OWNER_CLARIFICATION_RESPONSE, DIRECT_REVIEW/checks and
CLOCK_MAP_CROSS_REVIEW. Read `review/fidelity/RADAR_TAPE_PROBE.md`, its freeze,
shared REPAIR.md and CONSTRUCTIVE_SUPPLEMENT.md. No explorer cross-check or
sibling direct review was read. Exact versions are in this addendum's pins.

**Verdict: ACCEPT WITH LIMITS.** MR1 is repaired correctly by the controlling
finite-interval statement. The ruler probe and shared constructive supplement
are mathematically sound at their stated local/conditional scope. No additional
scientific repair is needed before integration. This does not attest to an
unseen final integrated freeze or adopt the radar convention as native physics.

## Exposure and independent content

Before receiving the parent's radar-proposal message, my frozen
CLOCK_MAP_CROSS_REVIEW independently obtained
`S(a)=integral_(a/Z)^(Za) C(a,v)dv`, normalized affine `K^v=S/C`, `m=S/2`,
strict epsilon ordering and the flat value `a(Z^2-1)/2`. The proposal to compare
that value with an explicit immediate-return radar convention was subsequently
supplied by the parent, with the sibling source following afterward. The
regular-strip argument was independently worked out and messaged to the parent
before reading that source. This chronology is disclosed; I do not claim
independent discovery of the radar idea or blinded review of its proof.

These checks use exact analytic differentiation, metric contraction and the
implicit function theorem/compactness with their hypotheses verified below.
No numerical worker, quadrature, old checker or scientific code was run.

## Direct ribbon check

For fixed Z>1, ell>0, define the smooth positive integrand C as in the frozen
clock-map construction. The endpoint-normalized equation is

    integral_(a/Z)^V C(a,v)dv = lambda S(a),
    S(a)=integral_(a/Z)^(Za) C(a,v)dv > 0.

For every fixed finite a>0 the integral is strictly increasing in V, from zero
to S(a), so there is exactly one V for 0<=lambda<=1. Its derivative with respect
to V is C>0. The implicit function theorem gives smooth dependence on a, lambda
and epsilon, locally also across the endpoints. At fixed lambda these points
stay in the positive quadrant on a neighborhood of every compact admissible
parameter window.

Differentiate the actual immersion F=(a,V,0,0). Its columns are
`J=(1,V_a,0,0)` and `K=(0,S/C,0,0)`. The original metric has g_uv=-C/2, giving

    g(J,J)=-C V_a,
    g(J,K)=-(C/2)(S/C)=-S/2,
    g(K,K)=0,
    det h=-S^2/4.

K is affine by C K^v=S, constant along each ray. No desired completion was
used to produce these entries. At the endpoints V(a,0)=a/Z and V(a,1)=Za,
so V_a is respectively 1/Z and Z. Since C=Z there, the original clock norms
are exactly -1 and -Z^2, retaining the actual source/target proper-clock labels.

At epsilon=0 the implicit solution is
`V=a[(1-lambda)/Z+lambda Z]`. Then

    V_a=(1-lambda)/Z+lambda Z >= 1/Z > 0,
    -h00=Z V_a=1+lambda(Z^2-1) >= 1.

Fix a compact positive emission interval a in [a0,a1] and lambda in [0,1].
Smooth parameter dependence on a slightly larger neighborhood and compactness
give uniform convergence of h00 to its epsilon=0 value as epsilon->0. There
therefore exists epsilon_*>0 with h00<0 on the whole rectangle whenever
|epsilon|<epsilon_*. Rank two already follows from S/C>0. These are exactly
the hypotheses needed to apply G176 throughout the ribbon. No universal value
of epsilon_* or whole-ribbon claim for arbitrary finite epsilon is proved.

The completed density is m=sqrt(-det h)=S/2 and is independent of lambda.
Integrating it on a fixed-a family over [0,1] gives L_completed=S/2. This is a
family integral, not an assertion that m(a)d lambda is an exact two-variable
spacetime differential preserving the original clock leg. In fact at epsilon=0,
`partial_a m=(Z^2-1)/2>0`; the proposed shared supplement explicitly retains
that integrability warning.

## Radar convention and strict mismatch

The prescribed return map is a_ret=Z^2 a, so the chosen radar convention gives

    D_rad=(a_ret-a)/2=(Z^2-1)a/2,
    t_rad=(a_ret+a)/2=(Z^2+1)a/2.

In ordinary time units the range expression is multiplied by calibrated c_E.
This is an independently **specified convention** on the same clock records,
not a second independent measurement record or evidence for another transport
mechanism. Neither radar range nor m is thereby identified with an independently
prepared spacelike proper ruler or with the owner's uniquely intended length.

For a>0 and a/Z<v<Za, both polynomial factors of P are nonzero, so H=P^2/ell^4
is strictly positive. Hence C>Z throughout that interior when epsilon>0,
and C<Z when epsilon<0. Integrating a strict continuous inequality over the
nonzero interval gives exactly

    epsilon>0: L_completed>D_rad,
    epsilon=0: L_completed=D_rad,
    epsilon<0: L_completed<D_rad,

with whole-ribbon completion interpreted in the established small-|epsilon|
range. The derivative check is also correct:

    partial_epsilon L_completed|_0
        = Z integral_(a/Z)^(Za) H(a,v)dv > 0.

The finite inequalities are already exact; no Taylor approximation or numerical
integral is being substituted for them. Equality with this particular timing
ruler would indeed rule out nonzero sufficiently small epsilon within this
family. Such equality is an additional test condition, not an adopted UDT law
and not an implication of reciprocal normalization.

This completes the bounded operational-ruler compatibility probe. It demonstrates
why fixing a normalization and identifying a physical ranging protocol are
distinct operations, even with the same complete clock maps and geodesic clocks.
It does not reopen arbitrary normalization freedom inside an unchanged G176
query; the underlying supplied metrics/ribbons differ.

## Repair and shared supplement fidelity

REPAIR.md correctly replaces the potentially finite reading of candidate §2 by
the exact integral/average formula, with pointwise Z retained only as the local
interval factor and local cadence inverse. It also correctly preserves the
constant-Z controls and subsequent differential constructions. This satisfies
MR1; no changed physical premise or new analytical run is needed.

CONSTRUCTIVE_SUPPLEMENT.md preserves the reviewed original metric, geodesic
clocks, exchange symmetry, both future maps and curvature coefficient. Its full
positive-quadrant definition resolves the finite-patch/global-map ambiguity
identified in CLOCK_MAP_CROSS_REVIEW, while each finite query remains on compact
segments. It makes no unsupported completeness or boundary assertion.

The supplement also preserves the compact-window small-|epsilon| condition,
specified radar convention, family-only tape integral, finite positive map
slopes, matched intermediate arguments in composition, and no-native-selection
limits. Its nonuniqueness concerns precisely this record set and supplied class.
Neither the construction nor its checked compression asserts that all founding
premises are insufficient, that the full postulate fails, or that a new physical
premise is proved necessary.

With these constructive continuations included, I support the proposed bounded
return: reviewed conditional kernel/clock mathematics, successful common-geometry
realization controls, a substantive ruler-identification test, and explicit open
physical-assignment/dual-slot joins. More parameter sampling cannot change these
exact statements. Final integrated wording and preservation checks remain a
separate required review stage.
