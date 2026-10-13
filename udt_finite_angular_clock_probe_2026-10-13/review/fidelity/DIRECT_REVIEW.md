# FAC1 direct fidelity review

Date: 2026-10-13. Reviewer `/root/fac_review_fidelity`, same fresh context as
SOURCE_FIRST.md; inherited same model, exact backend identifier unavailable.
**Verdict: VERIFIED-WITH-CAVEATS for the frozen conditional synthesis and its
source fidelity.** No blocking scientific defect was found in the inspected
argument. This verdict does not independently rederive every author series,
certify numerical error, adopt AMS, identify a positional cause, or promote UDT
physics. Final central integration has not yet been reviewed.

## Exposure and version binding

SOURCE_FIRST.md was frozen before new FAC1 proof/code/results or verdict
exposure, SHA-256
`b172b9b6ec516d568b8996ee3ac27a61064155238db8c2c7a390c63c44ddaf0a`.
The direct dispatch then disclosed the proposed vacuum coefficient and Kerr
lead. I read A's two-control and vacuum-quartic candidates, its plane-wave and
derivative-pairing scripts, B's initial and Kerr candidates/manifests, B's
analyze_saved and original Kerr-curvature scripts, the three coordinator proof
notes, then the frozen parent INITIAL_CANDIDATE. The latter arrived during this
review. No sibling mathematical review file or verdict was read.

The independently checked parent source bindings are:

| File | SHA-256 |
|---|---|
| INITIAL_CANDIDATE.md | 8107bffa757333daf5a04073e338147a0c0390b8ca65b081d4c0ca06fb290f1d |
| SCIENCE_FREEZE.json | 54173a2b42fb01f588016eb04a0277f28319acd5d935fb104900f04e03b1eeb9 |
| researcher_a/FREEZE_01.json | a8022d79102ad2233317ce858f798e23e76505c3e20eea229ea2a26d0d2efaa0 |
| researcher_b/MANIFEST.json | 1c7733408132d0eeb5c90b6c8340024f0670b74bae4cbd0a3f25f5e790d3fdbd |
| researcher_b/KERR_MANIFEST.json | 5ccbef24e0fc4b20b8bb4081e2c4d3a78d99dac06efc91ea776f12520463c0dc |
| researcher_b/KERR_CANDIDATE.md | f32a6675633cb51bae540843565ca48e52c61cd19a87db26311fafb35b40b7fe |
| RECOVERY_CANDIDATE.md | fede5c563151bbf75800892a0f9b3ebdcc61d3cbb28081249b248f576ec4f9f8 |
| RECOVERY_CONTINUATION.md | 1bba27b3539c944312a9752df6e70993766d12edfc33921f1012ae2190c1a336 |
| INVARIANT_ROUTE_CANDIDATE.md | c8c4638bde15c35d22400e4d16393145de9dba46ee49eb0429bb5a2799272ea1 |

The science freeze supplies exact bindings for the author source files. I have
not called this review an independent exhaustive audit of all 105 manifest
entries. Source-first parent-startup attribution remains unchanged. No git
mutation, central-file edit or protected-payload access was performed.

## Main adversarial checks

**Natural jets, rather than two-example fitting.** The claim needs the local
observable to be a smooth natural scalar with polynomial Taylor coefficients.
Rescaling by L makes the preparation distance and leading flight order one.
The flat flight/direction Jacobian maps a radial variation and tangent sky
variation onto their orthogonal sum, so its inverse is regular. It can be
expressed with n and the spatial projector; a direction chart singularity is
not a singularity of that physical map. Recursion thus introduces no inverse
curvature invariant. The log expands at p=1. This substantiates the finite-jet
argument rather than merely assuming dimensional homogeneity.

I directly inspected the normal-metric jet types in
[Brewin v3, equation 11.1](https://arxiv.org/pdf/0903.2087v3): the quadratic,
cubic and quartic terms have the stated R, derivative-R and
second-derivative-R/quadratic-R structure. The reference supplies a coordinate
method, not the FAC1 coefficient. No boundary-value coefficient from that paper
is substituted for this clock experiment.

**Derivative-contraction exhaustion.** I independently reconstructed the slot
count without executing A's enumerator. A trace-free Weyl tensor has four slots
in two antisymmetric pairs. Avoiding an internal trace allows at most two U
slots, one per pair. At second derivative order the two remaining Weyl slots
must therefore pair with the two derivative slots. In the actual derivative
ordering the inner derivative is a Weyl divergence and vanishes throughout the
vacuum neighborhood; the outer derivative is then a derivative of zero. If a
derivative slot instead carries U or contracts with the other derivative, the
remaining Weyl slots force a trace or an antisymmetric double-U zero. This
covers every pairing. No derivative of the external U is taken, and no
commutator is silently set to zero. At first derivative order, the available
external slots are insufficient without an antisymmetric zero or Weyl trace.
Pointwise Ricci-flatness alone would not suffice; the candidate explicitly
requires neighborhood Ricci-flatness.

**Quadratic invariant space.** Full-sphere averaging introduces only the spatial
metric and U. The four-dimensional algebraic Weyl tensor is determined by its
two symmetric trace-free spatial matrices E and B. Their O(3)-even quadratic
scalars are E² and B²; the mixed contraction is parity odd because B uses one
dual. The un-oriented preparation/measure cannot generate it. Thus control
coefficients determine two constants only after this classification, as the
candidate now says. I found no omitted contraction that defeats the statement.

**Actual future comparisons.** A's reverse Kasner incidence starts at B's
prepared event T with its transported velocity. Its numerator is the source
frequency there; its denominator is A's reception frequency. The plane-wave
implicit derivative similarly uses the independent future root at tau=0,
whereas forward uses the root at s=0. Neither calculation substitutes the echo
or the inverse at a previously matched event. Both means use the original
preparation angles. The plane-wave expressions divided by z and the Kasner
chart divisions have analytic geometric limits; the full shooting-map
argument, not their chart denominators, owns regularity on the axes.

**Remainder and signs.** The compact sky and finite-chart cover justify a common
small-L interval and an integrable Taylor remainder for each fixed laboratory.
No uniformity over unbounded U is inferred. Positive/negative nonzero quartic
coefficient gives the corresponding two local signs. The weak necessary
condition is `4E²>=3B²`; strict `>` is sufficient locally. Equality is
undecided. The candidate consistently avoids a finite-L iff or regional
classification from this leading term.

## Independent arithmetic and saved-artifact computation

CHECK_FREEZE.md preceded the reviewer execution. The independent standard-library
script `check_direct_01.py` imported no author code. It used exact Fraction
sphere moments for the printed polynomials and independently reconstructed
endpoint frequency contractions from saved q, receiver momenta, preparation
time and reception times, then recomputed the weighted means. B's analysis
implementation had been visible; this is independently written arithmetic and
artifact recomputation, not a wholly independent geodesic solver.

Exact results:

| Quantity | Recomputed result |
|---|---:|
| Kasner forward sphere quartic | 4/1215 |
| Kasner reverse sphere quartic | 4/1215 |
| Plane-wave forward/reverse sphere quartic | 1/720 each |
| Electric invariant coefficient | 1/90 |
| Magnetic invariant coefficient | -1/120 |
| Nonextremal E=0 Kerr quartic | -1/540 |
| Outside-ergosphere Kerr quartic | -19169269043200000/12061790310418024683 |

The five baseline Kasner lengths, five refined lengths, two flat controls and
four epsilon=-1e-5 records were recomputed from their angular endpoint data.
Maximum directional log discrepancy was below 4.45e-16; maximum reconstructed
weighted-mean discrepancy was 4.754e-17. Flat means recomputed as zero. At
epsilon=-1e-5,L=.04 the independent means were
`+4.207342272180858e-10` and `-2.056025279700695e-10`. Their combined mean is
positive while the reverse mean is negative. These are consistency checks on
saved floating-point results, not certified enclosures of true means. The
author's separate refinement study remains its own evidence.

TPS1 capture `checks/direct_01.json` records the exact command, Python3.10.12,
source/output hashes, zero exit code, 0.032189 seconds captured wall time,
16,764KiB max RSS, 2GiB address-space limit, one thread and no killing timeout.
Its stdout SHA-256 is
`73979aebfb2654f1424de481b2dca4f98a184c64897f56e0f13fd6d42514629d`;
stderr is empty. No failed check preceded it. No CPU slot remains occupied.

## Kerr and the recovery implication

I inspected [Wylleman–Costa–Natario section6.2](https://arxiv.org/html/2007.15384v2),
including the metric/coframe and zero-charge Kerr specialization, and
[Mashhoon Appendix C, C6–C8](https://arxiv.org/pdf/2007.12023v3) for the principal
electric/magnetic curvature matrices. Setting charge to zero in the stated
Einstein–Maxwell control yields regional GR vacuum; this is not inferred from
four sampled Ricci checks or adopted as UDT dynamics. The primary formulas and
B's metric calculation use consistent squared norms despite the magnetic
orientation sign.

Independent exact substitution gives r_plus=5/4<3/2, Sigma=3, Delta=3/16,
E²=0 and B²=2/9 at the simpler nonextremal point. At r=31/20,
Delta=6/25 and gtt=-21/1261, so magnetic dominance persists strictly outside
the ergosphere. Neither witness depends on a coordinate horizon or a degenerate
metric. The Carter vector specifies a possible initial unit tangent; the clock
then follows its own geodesic. No accelerated Carter orbit is substituted into
the freely prepared theorem.

This establishes an actual supplied Ricci-flat control for the adverse quartic
sign, conditional on the reviewed local clock theorem. It refutes automatic
AMS over all Ricci-flat metrics/preparations. It does **not** show the exact
Kerr laboratory is a mandatory empirically tested recovery target. The
candidate expressly preserves this distinction. A small absolute curvature
obtained by rescaling a black-hole metric also does not make its dimensionless
strong-field arrangement a solar-system regime.

My pre-exposure SOURCE_FIRST independently derived the conformal Ricci-jet
escape and fixed-query continuity reasoning. The exposed coordinator version
agrees, with its time origin shifted from0 to1. RECOVERY_CONTINUATION's negative
epsilon sign, joint expansion, and root `9sqrt(30)/4` are algebraically
consistent: writing L=s h, epsilon=-h² makes the normalized leading function
`-s²/2+(4/1215)s^4`. Its positive root is simple. Analytic incidence gives the
stated nearby roots, while not proving global uniqueness. The source family's
analyticity supports this argument; it is not asserted for arbitrary merely
smooth data without the corresponding regularity reasoning.

For any strictly negative limiting mean at a fixed L, smooth matching on a
common regular tube carries the finite endpoint records and sphere integral
continuously. Hence positivity at that *same* finite query cannot survive all
the way to the limit. It is essential that AMS apply there for all small
correction parameters. Local positivity with a shrinking radius, distant-onset
scope, or finite-tolerance recovery does not make this promise. The synthesis
preserves all three qualifications.

## Physical fidelity and the decision to return

The result can serve the geometry-selection goal as a conditional discriminator:
AMS in a stated vacuum comparison regime rules out some curvature data while
retaining nonzero anisotropic tidal data in other supplied examples. Its use
does not require pretending that the total mean already isolates a cause.
Conversely no native UDT restriction follows until the physical applicability
of that sign is established. The positive Kasner and negative Kerr controls
make both points concrete. GR remains a filter/control, not a native vacuum
law; the owner’s distant positional direction remains open.

The parent INITIAL_CANDIDATE accurately compresses these boundaries. Its
necessary/sufficient distinction is correct; its repeated equality of means is
explicitly only through the displayed order; its recovery warning retains a
common query. Its comparison to older restrictions should remain tied to the
specific all-direction Ricci-flat sign arguments of PSW/FPC, rather than be
shortened to a claim that every directional condition eliminates Weyl.
This is an integration wording caution, not a defect in the frozen candidate.

A return with this conditional tool and the unresolved physical decision is
justified by the approved decision-ready return point. Continuing an arbitrary
metric census would not identify the statistic with the intended additional
effect. This does not establish exhaustion of all useful direct-clock ideas or
require new physics; a next in-scope hypothesis could still be explored if it
offers a concrete attribution/applicability test. The present result merits
preservation without inventing that next hypothesis as an accepted input.

## Defects, survivors, repairs and omissions

No blocking defect or mandatory scientific repair was found. The strongest
survivor is the scoped vacuum clock coefficient, its conditional AMS inequality,
the actual Kerr adverse control, and the recovery-quantifier distinction. The
smallest repair needed before promotion is none on this fidelity pass; all
listed caveats must survive central integration and the final brief.

This review did not independently derive the complete Kasner arbitrary-angle
series, rerun A's symbolic scripts, integrate fresh Kerr rays, derive regional
Kerr vacuum from its general metric, prove numerical enclosures, replay the
old PSW/FPC suites, or perform a full406 premise audit. The scope is substantive
fidelity/argument review with targeted independent recomputation. The separately
assigned mathematical reviewer owns its actual additional work; no work or
verdict from that context is presumed here. Different-model and human review
remain unavailable. No registry grade, founding premise or CANON changes are
licensed by this review.
