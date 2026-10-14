# FKA1 clock-map realization — later-exposure mathematical cross-review

Reviewer `/root/fka_review_math`, 2026-10-14 UTC. Target:
`review/fidelity/CLOCK_MAP_REALIZATION.md`, SHA-256
`9cef9602e0f30512ed3fa4fbc7860f69c8366e3fdbfbaacd3152ed81cf90be2b`.
The sibling construction and its freeze were read only after my own DIRECT_REVIEW,
INDEPENDENT_ANALYTIC_CHECKS and direct pins froze. Those initial records remain
unchanged. The parent stated that its own curvature calculation agreed; that
statement is disclosed exposure and is not used as mathematical evidence.
This is actual separate-context review of a visible construction, not a blind
or different-model reconstruction and not independent discovery of its idea.

## Verdict and scope

**ACCEPT WITH LIMITS.** The construction exactly realizes both specified linear
clock maps in one smooth time-oriented geometry with unit geodesic clock curves
and an exchange isometry. It also supplies flat and nonflat realizations of those
same records, proving its stated bounded inverse nonuniqueness. The composition
law is correct. No mathematical or physical-premise repair is required at that
scope; one domain precision below would improve wording.

It does not derive the supplied maps, their positional interpretation, a physical
ruler calibration, a field equation or a full UDT realization. Null incidence is
an explicitly chosen geometric representation of the postulated relation, not
a separately imposed propagation cause. The source consistently retains this
distinction. No canon, source grade or adopted premise is changed by this review.

## Original metric, clock and causality checks

Let `C=Z exp(2 epsilon H)>0`, `H=P^2/ell^4`, and
`P=u^2-(Z+1/Z)uv+v^2`. From the displayed original metric, the radial matrix is

    [[0,-C/2],[-C/2,0]],

with inverse entries `g^uv=g^vu=-2/C` and determinant `-C^2/4`. Appending two
positive transverse entries gives one negative and three positive eigenvalues.
For `t=(u+v)/2`, direct contraction yields
`g^{-1}(dt,dt)=2(-2/C)(1/2)(1/2)=-1/C<0`.
Thus t is a temporal function on the stated domain; a time orientation chosen
by increasing t admits no closed future causal curve there. For causal radial
tangents, du and dv have the same weak sign; future orientation chooses the
nonnegative sign. The full metric has the same conclusion since transverse
positive norm strengthens the causal inequality.

On A(a)=(a,a/Z) and B(b)=(b/Z,b), P=0. Differentiating H explicitly gives
`H_i=2P P_i/ell^4=0`, so C=Z and both first coordinate derivatives C_i vanish
along each curve. Original contractions therefore give norms -1 for the constant
tangents `(1,1/Z)` and `(1/Z,1)`, respectively. Christoffel calculation from the
inverse metric gives only

    Gamma^u_uu=C_u/C,       Gamma^v_vv=C_v/C

in the radial product block; the remaining radial and all transverse connection
coefficients are zero. The two nonzero general coefficients vanish on both
curves. Their coordinate accelerations also vanish, so both displayed parameters
are affine unit proper times and both observers are geodesic for all epsilon.

Since P is symmetric under u↔v and the transverse product is unchanged, that
interchange is an isometry exchanging A(a) and B(a) while preserving the selected
time orientation. This is exactly a two-clock exchange statement; it does not
establish all-observer equivalence or a full native observer population.

## Both future correspondences, checked from the equations

Outgoing from A(a), u=a constant reaches B only when b/Z=a, i.e. b=Za. Its
v coordinate increases from a/Z to Za. Opposite outgoing from B(b), v=b constant
reaches A when a/Z=b, i.e. a=Zb. Its u coordinate increases from b/Z to Zb.
For Z>1 and positive proper times both are future null segments. A composed
return ends on A at Z^2 a>a, so composition is not inversion or a causal loop.

On u constant the original affine equation is

    v''+(C_v/C)(v')^2=0,

equivalent to `(C v')'=0` along the curve. Positive C bounded above and below
on each compact segment gives a regular increasing affine parameter. The other
direction has the same proof with u and v interchanged. Product transverse
geodesics satisfy x''=z''=0, so the direct branch with identical transverse
endpoints has zero transverse motion. This establishes the chosen branch rather
than silently assuming a generic four-dimensional path has no transverse data.

An additional direct contraction cross-check confirms the proper-clock slope.
For the outgoing affine tangent K=(0,k/C), k>0,

    omega_e=-g(K,A')=k/2,
    omega_o=-g(K,B')=k/(2Z),
    omega_e/omega_o=Z.

For the other direction use K=(k/C,0) and exchange A/B, giving the same ratio.
This is an exact metric contraction check of the stated conditional null
representation, not an independent physical propagation explanation. Because
the supplied maps are linear, finite interval ratios equal Z exactly; MR1's
varying-rate issue does not affect this control.

## Curvature and genuine inverse nonuniqueness

The connection above gives

    Ric_uv=-partial_v(C_u/C)=-partial_u partial_v log C,
    R=2g^uv Ric_uv=(4/C) partial_u partial_v log C.

The flat transverse factors add no scalar curvature. Substituting log C=log Z+
2epsilon H yields R=(8epsilon/C) H_uv. This derivation is directly from the
original connection, not an inference from the candidate kernel.

At Z=2 and u=v=ell, my explicit derivative values are

    P=-ell^2/2,
    P_u=P_v=-ell/2, P_uv=-5/2,
    H_uv=2[(ell^2/4)+(5ell^2/4)]/ell^4=3/ell^2,
    C=2exp(epsilon/2),
    R=12epsilon exp(-epsilon/2)/ell^2.

The result agrees exactly. At epsilon=0, constant C gives zero curvature
everywhere; for nonzero epsilon this event has nonzero R. Hence at least the
flat member and any such curved member cannot be related by an isometry on
patches containing the checked event. The construction only needs this pair to
disprove uniqueness from these records. It does not need, and does not assert,
that every two distinct nonzero epsilon values are mutually non-isometric.

The input clocks, their entire admissible bilateral map records and their
geodesic preparations stay fixed while curvature differs. This proves the
restricted inverse ambiguity claimed. It is not a countermodel satisfying every
founding physical postulate, nor a theorem that every conceivable clock/ruler
record fails to determine a metric.

## Where the missing metric information can appear

The completed scalar uses the fixed target tangent Z U and gives T=Z,
Phi=-log Z and chi=(1-Z^2)/(1+Z^2) in both directions. It is unchanged across
this family, as claimed. This does not imply that the full completed record is
unchanged.

For example, choose the outgoing affine parameter with endpoints lambda=0,1.
From C dv/dlambda=k its normalization gives

    k(a)=integral_(a/Z)^(Za) C(a,v)dv.

The receiver Gram density from the stated null family is
`m=Z omega_o=k(a)/2`. On this ray H is nonnegative, zero at the two endpoints,
and strictly positive inside. Thus increasing epsilon strictly increases k and
m for the same coordinate endpoint normalization, while Z and chi remain fixed.
At epsilon=0 specifically, `m=a(Z^2-1)/2`.

This exact check supports the candidate's distinction between clock scalar,
full density/shift record and additional geometry. It does not adopt this m as
a universal measured distance or independently prepared physical ruler; that
operational identification remains separate. Changing affine conventions must
also retain the usual density covariance.

## Actual-map composition check

For positive differentiable slopes alpha=f'(a) and beta=g'(f(a)), the chain rule
gives Z_composite=alpha beta. With Phi=-log Z, the stated logarithmic rule follows
at the correct intermediate argument. The matrices D=diag(Z,1/Z) multiply to
D_composite exactly. Their contrast is

    chi(alpha)=(1-alpha^2)/(1+alpha^2).

Direct addition of the two rational contrasts gives

    [chi(alpha)+chi(beta)]/[1+chi(alpha)chi(beta)]
        =(1-alpha^2 beta^2)/(1+alpha^2 beta^2).

The denominator is positive because both contrasts are strictly between -1 and
1. This proves the formula without assuming a physical reverse map is an
inverse. For the true inverse, its derivative at f(a) is 1/alpha and its contrast
is -chi(alpha). A supplied physical return need not satisfy that condition.
This strengthens the usable composition statement while retaining the metric/
G176/readout assignments; it does not derive the time/length slot identification
from the two observed clock rates alone.

## Domain precision and updated return assessment

The metric formula is smooth on the entire positive u,v quadrant for every fixed
finite epsilon and ell>0. If the working domain is instead a finite open patch,
the clock maps and echoes should be quantified only for the proper-time intervals
whose required curves and segments lie in that patch. Equivalently define the
metric on the full quadrant and keep every individual check on a compact segment.
The stated “containing the required clock/ray segments” already supports the
local reading; making it explicit prevents an unintended all-positive-time
claim on a bounded patch. This is a nonblocking scope clarification.

My initial direct review judged the observed local-germ/calibration routes
sufficient for the narrow audit return. This later probe is nevertheless an
informative additional reverse-direction construction: unlike an arbitrary local
germ, it realizes both full specified clock maps in one common causal geometry
and proves a precise inverse nonuniqueness. I did not independently originate it;
this cross-review checks it after exposure and updates the return assessment
accordingly. Incorporating its bounded result strengthens the return justification.

No further sampling of epsilon is needed: the exact family and scalar-curvature
comparison establish the claim. A genuinely new discriminatory equation or an
already admitted source fixing additional records could change the conclusion;
the present construction neither supplies one nor proves a new physical premise
necessary. The reviewed result remains conditional realization, bounded inverse
ambiguity and correctly typed composition, followed by the authorized discussion
return rather than automatic successor work.
