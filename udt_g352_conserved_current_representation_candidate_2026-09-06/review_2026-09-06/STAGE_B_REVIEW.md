# Direct adversarial review of the conserved-current representation candidate

Verdict: VERIFIED-WITH-CAVEATS for the bounded local mathematical representation and converse.
No scientific defect requiring candidate repair was found. No source grade, physical premise,
population choice, accepted dependency, manuscript, or canon is promoted by this verdict.

Reviewed revision: `a4525d2176b0f6dbacf71830bab44f8c34e24627` on `grok`.
Candidate: `udt_g352_conserved_current_representation_candidate_2026-09-06/`.
Accepted-source snapshot: `3a31db478b094efc9bce5291349b552aed95059c`.
Review date: 2026-09-06 UTC. Reviewer: `/root/conserved_current_adversarial_review`.
Exact runtime model: UNKNOWN; different-model review UNTESTED.

## What survives adversarial examination

For the declared smooth local flowbox, supplied nonzero future exact null gradient k=grad(Theta),
smooth transported labels with fixed cross-phase identification, fixed DeltaTheta>0, and supplied
smooth finite nonnegative label density s, the candidate establishes

    C = s/(DeltaTheta J) k,
    div C=0,
    -g(u,C)=Gamma

for every finite future unit timelike observer u. The representation is unique for these fixed
data. It does not select those data from the metric. Within the declared class of smooth
nonnegative aligned currents, conservation is exactly

    J rho = F(Theta,lambda),

where F is arbitrary smooth nonnegative data on the three-dimensional local ray quotient.
The specified G352 product requires the stronger F=s(lambda)/DeltaTheta condition relative to
the fixed phase and identification. Conservation alone imposes no phase-independence condition.
The candidate's varying-total and nonseparable Minkowski witnesses both refute that stronger
implication while leaving the product representation intact.

This is the same conclusion as the independently frozen Stage A argument, whose full report is
unchanged: `STAGE_A_SOURCE_FIRST.md`, SHA-256
`dadddebe511aca3c4df1ba42f004fa6b4ddb8ea71287ddfb07d8eab9aa673376`.

## Authentication and exposure

Stage A was frozen and sent at 18:02:43 UTC before any candidate proof, code, output, or candidate
verdict was disclosed to this reviewer. Stage B disclosure named the committed revision above.
I then read WORK_ORDER.md, README.md, CANDIDATE_ARGUMENT.md, PREMISE_AND_COVERAGE.tsv,
REVIEW_RECORD.md, both hash manifests, all candidate Python/input/result files, and only status
metadata concerning unrelated work. No protected payload or prior unpromoted cone-extension
argument was read. The prior cone-review summary was checked by hash only as an explicitly
context-only manifest entry; it is not an accepted dependency.

`sha256sum --check .../ARTIFACT_SHA256SUMS` passed all 12 payload entries. Git lists exactly those
12 files plus ARTIFACT_SHA256SUMS at the reviewed revision. Empty, zero-exit `git diff --exit-code`
against that revision before and after replay established candidate working-tree byte stability.
The artifact-manifest hash is
`b8c85e257b87ebe24263c262ea74e9bf247ad83d589e9d29d79f6bad8b94230f`.
`sha256sum --check .../SOURCE_SHA256SUMS` passed all 20 entries. Stage A had already compared its
read source files directly to the accepted snapshot with an empty zero-exit git diff. The six
scientific-source hashes match the frozen Stage A SOURCE_SHA256.tsv. A bounded registry query of
G349/G351/G352 current status, epistemic label, and controlling source confirmed the source landing;
I did not dump the wide registry into context or independently rerun its verifier.

The candidate REVIEW_RECORD correctly discloses that the author saw the short Stage A summary
after writing the initial analytic argument but before freezing the candidate. That summary
prompted an explicit characteristic-phase-sheet versus transversal clarification. The author had
not read the full Stage A report at initial freeze. Therefore no author blind-discovery property
or wholly different proof route is claimed. My source-first reconstruction remained unexposed to
the candidate until after its freeze; the direct Stage B review was necessarily exposed.

## Load-bearing argument checks

1. Local chart existence survives. Since dTheta is nonzero and annihilates k, its restriction to
   any three-dimensional transversal cannot vanish identically at the point; otherwise it would
   annihilate all of TM. Completing Theta to coordinates there and transporting by the k flow
   gives the stated chart after shrinking. This requires the smooth open four-dimensional
   phase/label patch actually declared; merely measurable G352 product data or one null phase
   sheet would not suffice. Smooth compatibility of the supplied label identification is embodied
   in the transported-coordinate hypothesis, not deduced from G352's general measurable setting.

2. Volume equals screen Jacobian in precisely this normalization. k=partial_r and k-flat=dtheta
   force the displayed metric first row/column. Expanding its determinant proves det g=-det h
   for arbitrary H and W and arbitrary coordinate dependence. The screen block is positive
   because the two coordinate label vectors are in k-perp and independent modulo k. There is
   no omitted lapse, shift, frequency, or area factor. A different ray parametrization must
   transform the components and volume appropriately; it is not a counterexample to this chart.

3. Variable-cut gradients cancel without freezing the cut endpoint. Adding tau_A k to each
   label tangent leaves its Gram matrix unchanged, because both relevant contractions vanish.
   The candidate explicitly evaluates h and J at the changed endpoint. It derives this local
   identity directly and does not widen G349's full source-cone theorem to an arbitrary global
   congruence. General transversals r=tau(theta,lambda) pull back the horizontal three-form
   without tau derivatives, as claimed.

4. The represented object has the correct dimension and sign. i_C vol_g is a three-form pulled
   back from phase/label quotient data, not a spacetime four-density. Its absolute quotient
   density is G352's nonnegative product. Reversing the proof orientation changes both form
   representatives and leaves C unchanged. The zero-density set produces the zero vector,
   not a normalized null vector or a density-ratio witness. Local orientation is sufficient.

5. Observer contraction has the exact claimed type. Algebra gives -g(u,C)=rho omega at every
   admissible point. Writing k=omega(u+n) in a Lorentz orthonormal frame gives
   |(i_C vol_g)(u,E1,E2)|=rho omega for an orthonormal observer screen. The candidate's projection
   E_A=e_A+g(u,e_A)k/omega is orthogonal to u and retains the Gram matrix, with the correct sign.
   Thus the local proper-time-times-screen-area interpretation follows. The proof does not
   claim a detector worldtube law or a global worldline crossing theorem.

6. The converse is exact in the stated aligned class. The divergence equation reduces to
   partial_r(J rho)=0; connected r intervals give arbitrary F(theta,lambda). Connected phase
   intervals make partial_theta F=0 equivalent to phase independence when testing membership
   in some uniform-phase product, with finite label measure still required. Specified s requires
   equality to that s/DeltaTheta, not merely any factorization. Initial data on a single
   characteristic phase sheet do not determine neighboring phases; the candidate now states
   the correct three-dimensional transversal data explicitly.

7. Covariance does not smuggle in a population rule. s and J acquire the same absolute Jacobian
   under passive label changes. Under phase-dependent relabeling, the coordinate expression of
   F may vary with phase while the original identification and C are unchanged. Holding the
   new numerical labels fixed is a different cross-phase identification. A varying total mass
   on the full retained label set cannot be removed by a bijective passive relabeling. Under
   positive affine phase rescaling with spacing transformed together, rho changes inversely
   to k and C is fixed. Nonlinear rescaling at fixed spacing changes the realization and
   generally the current while retaining divergence conservation; it is correctly excluded
   from G352 gauge.

8. Free-data and ownership claims stay bounded. Fixed-data uniqueness from contraction with a
   nonzero volume form is elementary algebra. It is not uniqueness from the metric, selection
   of s or Theta, or classification of all conserved vector fields. The candidate makes no
   wave, Maxwell, stress, action, source, detector, carrier, energy, scale, or global extension
   premise. It does not claim that no other metric-native realization route is conceivable.

No defective step, surviving contradiction, or mandatory repair arose in these checks.

## Executable evidence and false-pass audit

The reviewer replayed the frozen baseline and all six mutation branches, one child at a time,
with separate stdout/stderr and actual child exits retained in STAGE_B_REPLAY.json. Baseline:
43 exact assertions, exit 0. Each mutant exited 1 at its intended AssertionError:

| Mutation | Observed failed guard |
|---|---|
| omit_area | expanding_density_value |
| coordinate_divergence | expanding_current_conserved |
| divergence_zero | nonconserved_control_detected |
| all_products | phase_dependence_not_product |
| omit_frequency | cut_1_clock_rate |
| omit_label_jacobian | label_density_jacobian |

The saved-input stdlib recomputation also replayed with exit 0 and matched saved values. It remains
same-author implementation evidence, even when this reviewer reruns it. Replays are regression
evidence; the wrapper's exit is not substituted for its child outcomes.

False-pass examination found the guards nonvacuous for the six specified damaged branches. In
particular the nonconserved control prevents an always-zero divergence routine from passing; the
second observer prevents a missing frequency factor from hiding behind omega=1; and the explicit
transformed-density check prevents a missing Jacobian from cancelling in a density/area ratio.
The suite is not an exhaustive mutation test. Some identities use algebraically equivalent forms,
the two saved observers are axial, product_compatible only tests a derivative, and the arbitrary
metric determinant test does not numerically enumerate all positive screen matrices. Those are
limits of finite regression coverage, not defects in the separately checked analytic argument.

For a separate implementation of the saved load-bearing witness, I authored
independent_map_witness.py without candidate imports. It differentiates the full endpoint map

    X(v,w)=(tau(v,w)-theta, tau(v,w) n(v,w))

with the supplied stereographic n and the supplied local cut gradient. This reconstructs tangents
from the map instead of adopting the producer's hard-coded tangent matrix. It obtains the source
area by a three-dimensional cross product and computes current/observer/screen volume contraction
by the 24 explicit exterior-product terms rather than the producer's matrix determinant call.
An independent observer-rest coarea contraction agrees as well. All arithmetic is exact.

The resulting saved cut areas are 16 and 100; frequencies 1 and 1/2; rho values 7/30 and 14/375;
Gamma values 7/30 and 7/375; absolute time-screen form values 56/15 and 28/15; ratio 2/25.
All match the frozen saved result. A further off-origin label (1/3,2/5) with a transverse boost
u=(5/4,3/4,0,0) gives cut radius 944/315, screen area 22278400/1002001,
omega=245/286 and Gamma=11344725/127432448 by both contraction routes. This tests a case outside
the frozen axial-origin witness, but is still a finite mathematical regression, not a general proof.

Commands: `timeout 60s python3 /tmp/udt-current-review-MVXr11/replay_frozen.py` and
`timeout 60s python3 /tmp/udt-current-review-MVXr11/independent_map_witness.py`.
Both wrapper commands exited 0. Python 3.10.12, SymPy 1.13.1. Raw per-child commands, timestamps,
streams, exits and expected outcomes are in STAGE_B_REPLAY.json; independent command/output/exit
are in STAGE_B_INDEPENDENT_RESULT.json. No timeout, unexpected test failure, floating-point
tolerance, GPU, or numerical solve occurred. Peak memory was not measured; the work remained
small CPU symbolic/rational computation under the declared operational target.

## Caveats, omissions, and return

- Verification applies to the local smooth regular representation and aligned-current converse,
  with a smooth supplied phase/label identification. It does not extend the general G351/G352
  measurable theory to a smooth spacetime current without those extra regularity conditions.
- No ordinary current continuation across caustics, vertices, branch overlaps, atomic/singular
  content, global quotients, or global topology has been established. Finite total label measure
  alone does not prove finite integrated observer rate on an unrestricted patch; G352 frequency
  integrability remains a condition whenever that separate integrated measure is asserted.
- Context freshness is established by the separate source-first agent stage. Exact model identity
  and a different-model axis are UNKNOWN/UNTESTED. Stage B is exposed; the analytic route overlaps
  the candidate's natural flowbox route. The full-map witness is independently implemented, not
  an independent proof of the general theorem. No human specialist review or physical confirmation
  is claimed.
- I did not rerun accepted G349/G351/G352 full production suites, the full repository suite, or
  the 335-row premise verifier. The parent reports the premise audit passed and is capturing
  closure separately; that report is not an independent reviewer rerun. Authentication hashes
  certify correspondence only, not truth, external authorship, or trusted chronology.
- No repository file was edited by this reviewer. All authored material is in this fresh /tmp
  directory. Protected/unrelated payloads, disks, worktrees, accepted grades, LIVE, HANDOFF,
  manuscript, and CANON were untouched. Remote freshness was not independently claimed. Backup
  completeness and pre-reboot unsaved-state disposition remain UNVERIFIED; ScratchDisk was not
  used and remains only an archive-dependent-task issue.

Return: the candidate may be preserved as a reviewed, unpromoted conditional mathematical candidate
within the work order. No same-premise repair/re-review is required by this review. This conclusion
does not accept a new scientific dependency or confer physical/canonical status.
