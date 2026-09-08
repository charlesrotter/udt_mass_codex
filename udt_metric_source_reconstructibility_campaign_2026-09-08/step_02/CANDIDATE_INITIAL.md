# RT2 initial candidate — what a fixed product actually constrains

Explored then frozen2026-09-08 for fresh separate-context adversarial review.
CONDITIONAL CANDIDATE, NOT BANKED. Prior question/input/outcome record:
../RT2_PLANNED_QUESTION.md. Dependencies are ENTIRE reviewed RT1 with its
review caveats, banked G367--G369, and exact G351/G352 product/readout meanings.
No original source, recipe, physical premise or vacuum equation changes.

## 1. Domain, fixed geometry and distinct data questions

Retain RT1's smooth time-oriented4D Lorentz nonzero-S class, fixed nonzero
constant beta of matching sign, positive n, integrable null line and constant R.
Use a small connected submersion/flow box (r,phi,y1,y2) with q=dphi,
ell=q-sharp=partial_r, and compatible cross-phase labels y fixed along rays.
Regular rank-two cuts have positive intrinsic sheet density J at each event.
Restrict when needed to smaller coordinate rectangles whose compact closures
lie inside the smooth positive patch. Only local finite smooth AC measures
are considered; no singular/atomic, caustic or global flattening result.

Metric g and beta are FIXED. By reviewed RT1 all alternative normalized phases
in this same tensor representation satisfy

    q'=a(phi)q,  a>0,   n'=n/a^2,   j'=j/a.                     (RT2.1)

G367's aligned-conservation converse gives

    sigma(phi,y)=n J,       partial_r sigma=0.                    (RT2.2)

The fixed-product requirement is MORE than this converse. We distinguish
prescribed labels+prescribed s(y)|dy|, prescribed labels+free phase-independent
measure, and an explicitly changed cross-phase label identification. A phase
origin, a phase/spacing gauge and a varied normalized phase are not identical.
No physical instrument or uniquely selected initial data is presumed.

## 2. Exact density transformation at fixed labels

For phi'=F(phi), a=F'>0, the phase sheets and ray LINES are unchanged.
At the same event and same transverse labels the intrinsic screen metric and
its density J do not change: changing a cut tangent by a multiple of the null
ray does not change its screen inner product. An affine parameter for q' is
r'=r/a up to an allowed ray-origin choice, locally. Thus

    sigma'=n' J=sigma/a^2.                                      (RT2.3)

This is also a FULL-current/product calculation, not only a density name.
With consistent local orientation epsilon_g=J dr wedge dphi wedge dy1 wedge dy2,
eta=i_j epsilon_g=sigma dphi wedge dy1 wedge dy2. Since j'=j/a,

    eta'=eta/a=(sigma/a^2) dphi' wedge dy1 wedge dy2.              (RT2.4)

The G352 product in these original cross-phase labels exists precisely when
sigma/a^2 equals the relevant phase-independent measure density. Confusing
eta'=eta or transforming only dphi instead of the full current gives a wrong
power of a. Full S stays fixed, but j and its readouts generally do not.

## 3. Prescribed labels AND prescribed measure

Let dmu=s_fixed(y)|dy1dy2| be a supplied finite smooth POSITIVE measure.
There is a compatible phase/current at these fixed inputs iff

    sigma(phi,y)/s_fixed(y)=A(phi)>0, independent of y.            (RT2.5)

Necessity follows from sigma/a^2=s_fixed and a=a(phi). Sufficiency chooses
a=sqrt(A), integrates F'=a locally, and uses(RT2.1). Therefore the normalized
covector q', n' and j' are UNIQUE at this full fixed geometry/beta/label/measure
input, with only phase origin left free. They are not unique from the metric
alone. If the original phase too was prescribed, no such adjustment is allowed:
the direct necessary/sufficient test is sigma=s_fixed (a=1).

An equivalent coordinate-free-on-this-labelled-tube formulation is useful.
Let b be RT1's unique future-raised square root S=epsilon b^2, epsilon=sign(beta).
At the prescribed measure, factorization and product matching force

    n_match=s_fixed/J,
    q_match=sqrt[J/(|beta|s_fixed)] b,
    j_match=sqrt[s_fixed/(|beta|J)] b-sharp.                      (RT2.6)

The full source tensor already matches pointwise. The remaining test is FULL
ambient covector closure d q_match=0. On a sufficiently small contractible
chart this is equivalent to an exact phase. With RT1's dR=0, conservation then
follows from Bianchi. In the reference chart q_match=sqrt(sigma/s_fixed) q;
partial_r(sigma/s_fixed)=0, so closure is exactly the transverse independence
in(RT2.5). This is a real compatibility constraint on given data, not a new
physical law, a selected universe or a claim one cut supplies a4D extension.

For a FIXED supplied future unit observer U, after this match the mathematical
contraction equals the G352 continuous readout:

    Gamma_match=-g(U,j_match)
               =sqrt[s_fixed/(|beta|J)] [-b(U)].                 (RT2.7)

No detector, population, energy, physical normalization or response law is
derived by the equality. Metric+these data constrain a conditional query.

## 4. Prescribed labels, measure free but phase-independent

There exists SOME finite smooth positive phase-independent measure locally
iff sigma is multiplicatively separable:

    sigma(phi,y)=A(phi)B(y),       A,B>0.                         (RT2.8)

Equivalently on the retained product chart,

    partial_phi partial_yA log(sigma)=0, A=1,2.                  (RT2.9)

Necessity is(RT2.3). For equivalence of the differential criterion, connected
label slices make partial_phi log(sigma) depend only on phi. Integrating on
the phase interval gives log(sigma)=f(phi)+h(y), hence separability. Converse
is direct. Positivity/smoothness and shrinking to a compactly contained label
rectangle ensure finite candidate measures; no global claim is involved.

For any fixed factorization sigma=A B, ALL allowed matches are

    a=c sqrt(A), c>0 constant;       s_new=B/c^2.                 (RT2.10)

Thus the arbitrary phase function is removed by product compatibility at
fixed labels, but a joint constant phase/measure freedom remains when the
measure is not prescribed. If sigma=s(y) already matched a product, a must
be constant. If that SAME measure is fixed too, a=1. The additive phase origin
is free in each case unless fixed separately. These are compatibility results,
not a demand to uniquely select every valid measure amplitude.

The tests are invariant under the admitted passive relabel y'=Y(y), independent
of phase: sigma,s and J acquire the same label Jacobian factor. A different
reference phase multiplies sigma by a phase-only factor and cannot manufacture
or remove separability. In(RT2.5) it correspondingly compensates the reconstructed
a, leaving q_match and j_match unchanged. Auxiliary reference choices are not
metric-selected physical content. G352's simultaneous affine Theta/Delta gauge
leaves q unchanged and is distinct from c!=1 at fixed beta with changed measure.

## 5. If cross-phase label identification is ALSO freely supplied

For ANY reference RT1 representation and ANY smooth a(phi)>0, a product can
be realized LOCALLY by explicitly choosing different cross-phase labels. Set

    Y2=y2,
    Y1(phi,y)=integral[y1_0 to y1] sigma(phi,xi,y2)/a(phi)^2 dxi.  (RT2.11)

Then det(D_y Y)=sigma/a^2>0. The inverse function theorem makes (phi',Y1,Y2)
a local quotient chart after shrinking; all these labels remain constant
along rays. On a same-phase screen, J_Y=J/[det(D_y Y)], so n'J_Y=1 and

    eta'=dphi' wedge dY1 wedge dY2.                             (RT2.12)

Terms in dY containing dphi' vanish in this wedge, which verifies the FULL
three-form/current. Choose a small common product range of phase and labels
inside the chart; unit label density has finite measure on its bounded label
rectangle. The local inverse construction selects a different cross-phase
identification based on supplied data. It is not a global product theorem.

This construction preserves the full fixed S while retaining arbitrary a(phi)
and generally changed j'=j/a. It does NOT preserve any originally prescribed
label system or physical measure correspondence. A phase-dependent Y is NOT
G352's phase-independent passive product gauge. At a=1 it can be a different
product description of the same full current; different labels alone need not
mean a different physical object. At nonconstant a, the current itself changes.
Data-dependent label choice proving existence supplies NO metric-only selector
and NO physical identification. It also does not prove a new physical premise
must be adopted; ordinary compatible label/query data may legitimately be given.

## 6. Actual metric diagnostic separating the data cases

Let

    g=2du dr+dx^2+dy^2-x^2(1+u y)du^2,

on a small regular patch with 1+u y>0, with partial_r future, beta=1.
Full-metric Ricci calculation gives R=0, S=(1+u y)du^2, and q=du,
n=1+u y, J=1 give a conserved representation. This is an OPTIONAL nonvacuum
comparison metric, not a new admitted UDT solve. At fixed labels(x,y),

    partial_u partial_y log(sigma)=1/(1+u y)^2 !=0.

No choice of F(u) and phase-independent measure in those fixed labels can
meet the product. Failure of this particular labelled construction is not
failure of g as an optional metric, much less failure of the UDT equations.

Nevertheless for ANY positive a(u), choosing
Y1=x(1+u y)/a(u)^2, Y2=y, phi'=integral a(u)du gives n'J_Y=1 and the
full product in the NEW labels, with the SAME S and j'=j/a. The example
distinguishes fixed-label obstruction from free-label existence, not typicality.
A separable positive counterpart tests the fixed-measure reconstruction and
its unique full covector. Finite tests support the general density argument;
the theorem is not inferred by accumulating metric examples.

## 7. Ceiling and decision meaning

This is a conditional source/phase/product COMPATIBILITY and data-freedom
classification, not a source-law adoption or content selection. At fully fixed
compatible label/measure data there is a definite extra exact-covector test
and a unique normalized phase gradient/current. With less specified data,
constant or functional freedom may remain; neither is automatically a missing
physical law. Conversely, mere existence of SOME product after freely adjusting
labels does not establish the metric alone selected the given carried content.

All G312 vacuum, G351/G352 owner-provisional, chosen-product, optional-beta,
RT1 locality/minimality and review limitations remain. No measurement transfer,
empirical fit, physical source relation, genericity, stability, global theorem,
coupled solve, canon or accepted-grade change is claimed. Fresh direct review
must assess this argument before the campaign uses it. This is the last
authorized substantive step; no new question follows automatically.
