# FAC1 Kerr recovery application — fidelity supplement review

Date: 2026-10-13. Reviewer `/root/fac_review_fidelity`, continuing the same
separate review context and inherited model. Source-first and direct reports
remain sealed. No sibling review or verdict was read. This is a focused analytic
and physical-scope review, not a fresh independent context or numerical run.

**Verdict: VERIFIED-WITH-CAVEATS within the supplement's conditional scope.**
No defect or mandatory repair was found. The application is a direct consequence
of the already reviewed conformal construction, now using the actual adverse
Kerr coefficient rather than a hypothetical negative control. It does not derive
AMS, select a physical deformation, or establish tested-regime applicability.

## Exact versions

| File | SHA-256 |
|---|---|
| KERR_RECOVERY_APPLICATION.md | 4641cb612b5dedef520801b13de6152c445cd1c9481ff582b373fcae3cadbb13 |
| SCIENCE_SUPPLEMENT.json | 709fb835b5808ae5c25890d9b2631a5eacf28e2f73c1c83d88b829ab379dbb8a |
| SCIENCE_FREEZE.json | 54173a2b42fb01f588016eb04a0277f28319acd5d935fb104900f04e03b1eeb9 |
| Sealed DIRECT_REVIEW.md | f8d8b5abbfc264f461bcdd7e165bc187d83d779ed1226d475fc0fea3e7580d7f |

Actual HEAD remained `781bc355905f9d9c8ca5a7628784fdd4cf85a15d` at inspection.
The accompanying receipt records independent hash correspondence checks for
the initial science-freeze files and this supplement. Hash checks establish
preservation, not truth or scientific independence.

## Independent analytic check

The regular nonextremal Kerr exterior is analytic in its local chart. One can
choose an analytic coordinate tau with tau(q)=0 and the specified timelike
cotangent at q; no global time function or preferred observer is needed.
For `u=epsilon tau^2/2`, the metric `g_epsilon=exp(2u)g0` has u=du=0 at q.
Therefore its Ricci change there is exactly

    Delta Ric=-2 epsilon d tau tensor d tau+epsilon g0,
    Ric_epsilon(U,U)=-3 epsilon.

This is the same connection contraction independently reconstructed in the
source-first review. Preparing the free clocks separately for each metric is
essential and explicitly retained. The two actual means therefore have exact
quadratic coefficient epsilon/2 at q.

Joint analyticity of the rescaled preparation/incidence problem and compactness
of the preparation sphere imply that the cubic coefficient is O(epsilon),
since it vanishes in the vacuum limit. The quartic coefficient is
`-1/540+O(epsilon)`. No constant or linear-in-L term is present for this
parallel preparation. These facts give the stated two-parameter remainder;
there is no omitted epsilon-squared contribution to the quadratic coefficient
because the Ricci identity at q is exact.

Putting h=sqrt(epsilon), L=s h and dividing by h^4 gives the limiting function

    F(0,s)=s^2/2-s^4/540.

Its positive nonzero root has `s0^2=270`, hence `s0=3sqrt(30)`. Direct
differentiation gives `partial_s F(0,s0)=-s0`, which is nonzero. The analytic
implicit-function theorem therefore supplies a root s(h)=s0+O(h) separately
for each mean, and `L_±=3sqrt(30)sqrt(epsilon)+O(epsilon)`. For any fixed
`0<s_low<s0<s_high`, the two means have positive signs at
`s_low sqrt(epsilon)` and negative signs at `s_high sqrt(epsilon)` for all
sufficiently small epsilon>0. The roots are sign crossings locally; no global
uniqueness or common higher-order correction is implied.

The dimensional convention is appropriately stated. In units restored with
the control's Kerr mass-length M, the leading quartic is
`-L^4/(540 M^4)` and this imposed deformation would give the leading crossing
`3sqrt(30) M^2 sqrt(epsilon)`. Nothing sets epsilon or M physically. The
supplement's formula uses M=1 and explicitly labels that convention.

## Recovery quantifiers and physical meaning

The Kerr limiting means are negative at every sufficiently small fixed positive
L0. Smoothly matched preparation on a common regular tube consequently keeps
them negative at that L0 for small enough epsilon. At each fixed epsilon>0,
the positive quadratic term instead dominates sufficiently close to L=0.
These conclusions coexist. They prove that no epsilon-independent positive
initial interval survives, while positive intervals may exist for each metric.

Thus the supplement supplies a metric-level realization of the shrinking-domain
escape; it is stronger evidence for that logical possibility than a polynomial
surrogate. It remains a local one-laboratory construction. It does not establish
an all-event/all-observer AMS law, a distant positive branch, a solar threshold,
a physically admitted Kerr recovery family, a native vacuum sector, or a
physical cause decomposition. The conformal factor is a supplied metric family,
not a newly accepted field. The initial Carter tangent is followed by free
geodesic motion exactly as required by the theorem.

The statement about a common nonzero recovery interval is correct only when
the same actual queries are within the proposed positivity law throughout the
recovery family. The supplement retains that qualification. The owner's
distant-onset positional direction and finite-tolerance recovery are not ruled
out. The earlier warning that strong-field Kerr is not automatically an
empirically required recovery target remains load-bearing through the cited
candidate and direct review.

## Limits and disposition

This review uses hand algebra and the previously reviewed analytic incidence
and vacuum-coefficient arguments. No new Kerr clock simulation, numerical
threshold, numerical enclosure, different-model review or human review was
performed. No full406 audit was replayed for this same-premise consequence.
The strongest survivor is the actual smooth-metric shrinking-positive-domain
witness and its local crossing asymptotic. No repair is required on this pass;
the local scope and physical nonadoption must remain visible in final
integration. Central integration has not yet been reviewed.
