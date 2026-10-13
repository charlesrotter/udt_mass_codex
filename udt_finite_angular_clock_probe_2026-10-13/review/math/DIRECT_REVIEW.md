# FAC1 mathematical adversarial review — exposed source packet

Verdict: **VERIFIED-WITH-CAVEATS** for the conditional mathematical result and
the scoped supplied-GR discriminator described below. No substantive defect was
found in the inspected proof. This is a separate-context, same-model review with
an independently reconstructed plane-wave argument and implementation. It is
neither different-model/human review, formal proof certification, physical
adoption nor final central-edition fidelity attestation.

## Exact edition and exposure

SOURCE_FIRST.md, SOURCE_FIRST_RESULT.md and SOURCE_FIRST_PINS.json preserve the
pre-author-exposure stage. The exposed packet consists of the coordinator's
INVARIANT_ROUTE_CANDIDATE, RECOVERY_CANDIDATE and RECOVERY_CONTINUATION, A's
CANDIDATE and VACUUM_QUARTIC_CANDIDATE with exact-control scripts/results, and
B's CANDIDATE, saved vacuum data and subsequent KERR_CANDIDATE. No sibling-review
content was read. Source versions are pinned in direct_check01_result.json and
kerr_review_check01_result.json. A's FREEZE_01 SHA is
`a8022d79102ad2233317ce858f798e23e76505c3e20eea229ea2a26d0d2efaa0`;
all its named source bytes passed correspondence checks. The Kerr candidate SHA
is `f32a6675633cb51bae540843565ca48e52c61cd19a87db26311fafb35b40b7fe`.
The parent INITIAL_CANDIDATE was subsequently reviewed at SHA
`8107bffa757333daf5a04073e338147a0c0390b8ca65b081d4c0ca06fb290f1d`,
bound with the105 scientific files by SCIENCE_FREEZE SHA
`54173a2b42fb01f588016eb04a0277f28319acd5d935fb104900f04e03b1eeb9`.

## The load-bearing natural-jet argument survives

I challenged the step that two positive controls could be fitted to a falsely
universal formula. Two examples alone are insufficient. Here there is an actual
additional argument: in orthonormal normal coordinates, rescaling the proper
experiment by L leaves a unit-size flat boundary problem at L=0. At that limit
the flight-length and tangent-angle derivative is the isomorphism
`(dr,dv) -> dr*n+dv`, with dv orthogonal to n. Its inverse uses projection along
n and onto its tangent plane, so it is polynomial in n and independent of
curvature. The ratio's denominator is nonzero at the flat limit. Recursive ODE,
transport, incidence and logarithm expansions therefore contain no inverse
curvature, chosen eigenframe, extra length or nonpolynomial curvature scalar.
Varying emission on the same worldlines does not change that jet counting.

The fourth normal-metric jet contains nabla²R and R², and no higher jets; lower
orders contain R and nabla R. I independently inspected the corrected primary
normal-coordinate expansion and its recursion. Only this structural statement,
not any clock coefficient, is imported. [Brewin, arXiv:0903.2087v3,
equation11.1](https://arxiv.org/pdf/0903.2087v3).

The original construction introduces g,U,n and the unsigned preparation-sphere
measure. Integrating n tensors gives spatial-metric pairings. Expanding
`h=g+U U` consequently leaves complete contractions with g and U. There is no
spatial orientation datum; a pseudoscalar E:B cannot be introduced by choosing
an oriented frame merely to name B. In four dimensions Weyl is algebraically
equivalent to the two symmetric trace-free matrices E and B. Quadratic invariant
pairings leave E²,B²,E:B; parity removes the third. This establishes a
two-constant space before the controls determine its constants.

The crucial derivative elimination does **not** need an illicit commutation.
For an ordered nabla_e nabla_f C_abcd contraction, a metric pairing between
Weyl slots is a derivative of a zero trace; putting two U's in either
antisymmetric Weyl pair gives zero. Avoid both cases and four Weyl slots need
external partners: at most two U's can occupy them, while exactly two derivative
slots remain. Each derivative must then pair with one Weyl slot. In particular
the inner derivative is a Weyl divergence, identically zero in a Ricci-flat
neighborhood. The outer derivative of that zero tensor is zero. U is only an
external vector at the event, so no derivative of an unspecified U congruence
is being discarded. The same argument with one or no derivative leaves no
linear vacuum invariant. My independent slot enumeration classified all10,
26 and76 possible g/U contraction patterns at derivative orders0,1,2. That
finite enumeration checks the index bookkeeping; the preceding argument and
natural-jet hypotheses carry the geometric conclusion.

Consequently the candidate formula survives:

    M_plus(U,L) = [4E²-3B²]L⁴/360 + O(L⁵),
    M_minus(U,L)= [4E²-3B²]L⁴/360 + O(L⁵).

Ricci flatness throughout a neighborhood is essential. Ric=0 merely at the
event does not remove Ricci derivatives. Equality here concerns the displayed
coefficients, not complete finite clock functions. No observer congruence,
unbounded-boost uniformity or finite-sign equivalence has been proved.

## Controls, preparation and angular coverage

Before exposure I derived the plane-wave geodesics, parallel preparation,
exact null-incidence world function and both independent first derivatives.
The complete directional quartic coefficients agree exactly with A's different
coordinate implementation, including the odd longitudinal terms that distinguish
the two emissions. Both exact sphere means are L⁴/720+O(L⁶). The calculation
includes the removable z=0 and null-du=0 directions, rather than deleting them.
The relation p_minus=-F_b/F_s is used at the independent B0 emission root;
using the inverse at the original outgoing endpoints would be the wrong object.

I read and checked the Kasner recurrence against its original preparation,
transport, conserved-momentum, normalization and incidence equations. Its
axisymmetric reduction represents the full sphere because rotations in the
equal-exponent plane and coordinate reflections preserve the entire prepared
experiment. The actual average is integral_0^1 dmu with z=mu², not a triad.
The null direction is solved jointly with arrival time. The saved forward and
reverse quartic polynomials independently reintegrate to4/1215. The arbitrary
unneeded fourth ray-direction coefficient cancels from the fourth clock
coefficient, as it must; the retained preparation and arrival orders suffice.
I did not independently rebuild the complete Kasner symbolic recurrence.

As a distinct saved-artifact check, I reconstructed all480 outgoing/reverse
endpoint log ratios from B's saved ray momenta, receiver momenta and proper
endpoint times, without importing B's implementation. Their largest difference
from saved logs is4.443e-16. Recomputed means differ by at most5.327e-17 and
retain their positive signs. This checks endpoint arithmetic and angular
aggregation, not a new null solve or rigorous numerical enclosure. Its observed
convergence corroborates the exact series without proving its coefficient.

The exact control values and independently checked electric/magnetic
normalizations give a=1/90 and b=-1/120. FPC1's negative principal-axis average
cannot be substituted for the full sphere. The normal-coordinate theorem also
explains why first and reverse quartic means can agree even though their
directional records and higher finite terms differ.

Angular uniformity is justified by the complete physical shooting problem,
not by assuming the factored Kasner angle gauge stays invertible on an axis.
The flat inverse is uniform on compact S²; local angular charts have a finite
subcover and the metrics/branches remain smooth on a reduced common tube.
The source's polynomial identities extend from dense charts by continuity.
The resulting uniform Taylor remainder may be integrated. This proves local
sign for a nonzero leading coefficient, but supplies no numerical radius,
all-distance assertion, interval bound or all-boost compactness.

## Kerr negative witness and its boundary

I independently opened the primary coframe/principal-observer source and the
primary canonical Weyl formulas, checked their displayed domains, and compared
the quoted scalar against B's original-coordinate curvature implementation.
The zero-charge Kerr solution is Ricci-flat on the regular exterior neighborhood;
the regional premise is supplied by the sourced GR solution, not by four
pointwise Ricci checks. [Wylleman, Costa and Natario, section6.2](https://arxiv.org/html/2007.15384v2),
[Mashhoon, Appendix C, C6–C8](https://arxiv.org/pdf/2007.12023v3).

My independent exact coframe/scalar substitution confirms, at M=1,
a=sqrt(15)/4,r=3/2,y=2/sqrt(5), that U is unit future, the frame is invertible,
r>r_plus=5/4, Sigma=3, Delta=3/16, E²=0 and B²=2/9. The conditional clock
coefficient is therefore -1/540. At r=31/20 it remains strictly negative with
gtt<0; the adverse sign does not require the stationary-limit surface. I did
not rerun a separate original-metric Kerr curvature calculation or any Kerr
null shooting. B's direct curvature differentiation and the independent primary
scalar/frame route provide distinct checks of the load-bearing point values.

The Carter field specifies only the initial tangent. Replacing A by a held
Carter orbit would change its acceleration and invalidate this use of the
free-clock theorem. The candidate explicitly follows the geodesic from that
initial tangent, so this objection does not apply. A pointwise purely magnetic
measurement is not a purely magnetic vacuum region. The negative quartic and
the regular local theorem imply both means are negative for sufficiently small
positive L. This refutes automatic positive means for all supplied Ricci-flat
laboratories. It does not refute UDT, require this strong-field observer/query
to lie in tested recovery scope, or establish any native vacuum admission.

## Recovery and proposed return

The conformal family is an explicit supplied metric perturbation, with each
clock preparation recomputed. At f=df=0 and Hess f=epsilon dt², the conformal
Ricci change is -2 Hess f-g tr(Hess f), so Ric(U,U)=-3epsilon and each mean
starts at epsilon L²/2. The two sign branches therefore recover the same
Kasner geometry smoothly while having different infinitesimal signs.
Joint smooth/analytic dependence and the zero vacuum cubic mean justify the
stated remainder and L=s sqrt(delta) limit for epsilon=-delta. Its nonzero
limiting root s0=sqrt(1215/8) is simple, since the derivative of
`-s²/2+(4/1215)s⁴` there is s0. Thus the claimed nearby separate crossings
L_plus/minus=s0 sqrt(delta)+O(delta) follow. Neither global root uniqueness nor
a native scale follows.

For a negative limiting finite GR query, continuity is enough to obstruct
nonnegative means at that **same fixed L** in a smoothly matched recovery
family on a common regular tube. Compact directional regularity controls the
integral. The quantifier cannot be weakened to a parameter-dependent positive
radius and still yield that contradiction. Distant onset and finite-tolerance
recovery are also not excluded. No unproved physical assignment of a total
angular statistic to an additional positional effect enters this mathematical
continuity statement.

A return at this conditional discriminator is scientifically justified once
the integrated edition receives its required review. The inquiry has resolved
the full-sphere versus axis ambiguity, obtained a nonautomatic local curvature
inequality under the unadopted AMS trial, and supplied both positive and negative
vacuum witnesses. Another unmotivated metric survey would not settle the
remaining physical attribution or regime choice. This is a decision-ready
conditional result, not a native-selection breakthrough or a full-postulate
insufficiency result. Any central summary must retain the neighborhood vacuum,
fixed-frame local scope, independent-emission preparation, equality boundary,
and common-finite-query recovery qualification.

The parent synthesis preserves these boundaries and coefficients. One minor
compression improvement is requested for integration: its phrase “older
all-direction restrictions that remove it” should name the older
**all-event/all-observer/all-direction Ricci-flat** restriction. A single
observer's all-direction leading condition forces E=0 but does not alone
eliminate the magnetic Weyl tensor. This is a wording boundary, not a defect
in the FAC1 theorem or the original correctly quantified FPC1 argument. Preserve
the frozen initial candidate and make the clarification in the reviewed
integrated edition.

## Evidence limits and remaining review

Three reviewer captures completed without scientific failure: source-first
plane-wave0.847s, direct arithmetic0.236s, and Kerr scalar/frame0.242s; all used
one thread,2GiB virtual memory and no CPU/wall timeout. Maximum reported RSS
was54,832KiB. No GPU, installed dependencies, protected payload or author-code
execution was used. Same symbolic library and inherited model remain shared
independence limits. Normal/premise/maintenance closure and exact central-edition
attestation are the coordinator's separate gates; this review does not mark
them passed or supply their evidence.
