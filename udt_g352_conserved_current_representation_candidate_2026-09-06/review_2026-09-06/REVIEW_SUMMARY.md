# Reviewed conditional candidate — conserved-current representation

Current status: VERIFIED-WITH-CAVEATS; UNPROMOTED CONDITIONAL CANDIDATE.
Date: 2026-09-06. Reviewed target: a4525d2176b0f6dbacf71830bab44f8c34e24627.
Accepted-source snapshot: 3a31db478b094efc9bce5291349b552aed95059c.

Fresh separate-context adversarial review found no substantive mathematical
defect, unresolved objection, or required same-premise candidate repair. It
examined the general analytic argument, not just passing finite checks.
This verdict does not change accepted scientific grades or dependencies.

## Plain-language decision brief

The representation works locally: G352's chosen smooth product can be written
as a conserved spacetime current, and that current reproduces its prescribed
observer readout. But writing the data as a current does not determine the data.
Conservation along rays is strictly weaker than requiring the same supplied
population on every phase sheet.

For supplied g, Theta, DeltaTheta and smooth compatible transported labels on a
regular product flow box, let k=grad Theta be nonzero future null and let J>0 be
the metric sheet-area density in those labels. For the supplied smooth finite
nonnegative label measure dmu=s(lambda)d^2lambda, the reviewed statement is

    C = [s(lambda)/(DeltaTheta J)] k,
    div C=0,
    -g(u,C)=Gamma

at every supplied finite unit future timelike observer. This C is unique for the
FIXED product data. It is not a metric selection of s, Theta, spacing or labels.
The mathematical current is defined by i_C vol_g representing the supplied
three-dimensional phase/label quotient measure; no new physical continuity
equation is adopted.

The full converse within the declared smooth nonnegative ALIGNED class is

    C=rho k and div C=0  iff  J rho=F(Theta,lambda),

where F is arbitrary smooth nonnegative data on the three-dimensional ray
quotient. The chosen G352 product requires F=s(lambda)/DeltaTheta relative to
its fixed phase and cross-phase identification. An initial transversal meets
all those rays locally; one characteristic phase sheet does not determine the
data on neighboring phases. No numerical solve is required for this conclusion.

In Minkowski space, Theta=z-t and C=(2+Theta)(partial_t+partial_z) on a bounded
positive domain are conserved but have varying phase-slice totals. A separate
C=(1+Theta*x)(partial_t+partial_z) witness is genuinely phase-label nonseparable.
These refute conservation-implies-product, not the stated G351/G352 premises or
their chosen branch. They are mathematical comparison objects, not source laws.

## Who supplies what

| Layer | Contribution | Still not supplied |
|---|---|---|
| Supplied metric and phase geometry | Screen area, metric volume, gradient, divergence and observer contraction | Physically populated phase or conserved amount |
| Owner-provisional G351/G352 premises | Source-free conserved label content and the specified clock-rate reading | Actual population, physical carrier or source |
| Chosen product realization | Continuous phase weight, fixed spacing, same mu and cross-phase identification | Derivation of phase independence or phase calibration |
| This reviewed candidate | Local smooth current representation and exact aligned-class converse | Native physical-content selection or a new adopted law |

Geometric area/volume/solid-angle measures do exist; the result does not deny
them. Identifying one with physically carried mu remains a separate issue.
Arbitrary supplied s, including zero and different normalizations/profiles,
survives. Therefore this route alone does not close the physical-realization
frontier, and it does not force a choice between a new premise and a native
derivation. No claim excludes other routes or supplies the missing data.

## Review and checks

Reviewer: /root/conserved_current_adversarial_review, fresh context with no
inherited conversation and no model override. Exact model UNKNOWN; different-
model review UNTESTED. Stage A reconstructed from accepted sources before
candidate exposure and froze at SHA256
dadddebe511aca3c4df1ba42f004fa6b4ddb8ea71287ddfb07d8eab9aa673376.
The direct Stage B report has SHA256
75a6f69795cff56696ff5e01a3fc0ec81d5fe82ff82c221e63a48d1b4e165ad9.

The source-first argument independently reached the same natural flowbox route;
this is not claimed to be a wholly different general proof. Parent exposure to
the Stage A summary before candidate freeze is disclosed in REVIEW_RECORD.md.
Stage B then reviewed the frozen candidate and authenticated all13 initial
candidate files and all20 source-manifest entries.

- Baseline43 exact assertions and all6 specified code-mutant failures replayed
  at their intended AssertionError. The always-zero divergence and cancelled
  relabel-Jacobian false-pass risks were specifically tested. Counts are finite
  regression evidence, not proof or exhaustive implementation coverage.
- Independent reviewer implementation differentiated the full endpoint map,
  formed source area by a cross product and expanded the24 exterior-product
  terms. It reproduced areas16/100, frequencies1 and1/2, Gamma7/30 and7/375,
  and ratio2/25, plus an off-origin transverse-observer control.
- The parent replayed that reviewer implementation successfully. This replay
  is not another independent review. The original stdlib saved-input check is
  implementation-distinct but same-author/context evidence.
- The parent's fresh closure premise audit passed all335 exact registry rows
  and its other named guards, exit0 with empty stderr, in398.54 seconds.
  Twelve focused existing repository policy/startup tests passed. These are
  controls, not scientific premises or evidence of physical realization.

No scientific repair was needed. A parent manifest invocation from the wrong
working directory failed to open relative filenames. The separate-stream
reproduction and correct-directory all9-file pass are retained. This was an
invocation defect, not a candidate or reviewer-artifact content mismatch.

## Limits, preservation, and authorized return

The extra smooth phase/label compatibility is a declared restriction, not a
consequence of G352's merely measurable product domain. The result is local and
regular, includes zero without ratios, and establishes no ordinary current
across caustics, vertices, branch overlaps, singular/atomic content or global
topology. A finite integrated observer-rate measure still needs G352's separate
frequency-integrability condition; pointwise identities do not remove it.

No accepted-source full production suite, full repository suite, human specialist
review, physical confirmation, different-model review or peak-memory certification
is claimed. The reviewer did not independently rerun the premise verifier.

All10 reviewer artifacts were archived byte-identically; correspondence and hash
manifests are retained. Initial argument, work order, premise ledger, check code,
inputs and outputs stay frozen. Only current README/review-status metadata and
their live artifact hashes are updated. The full13-file initial snapshot remains
pinned and recoverable at a4525d21. The original46 unrelated status entries stay
unchanged; protected payload contents were not inspected.

This completes the authorized cycle and stops before a new scientific question,
premise adoption, physical content/source/population selection, scientific grade
or accepted-dependency change, manuscript revision, production solve or canon.
The completed infrastructure audit and fixed-snapshot manuscript remain distinct
from the still-open physical-realization frontier. No repository-only blocker
remains for this completed test. Backup completeness and pre-reboot unsaved-state
disposition remain UNVERIFIED; ScratchDisk blocks archive-dependent tasks only.

Details: [source-first review](STAGE_A_SOURCE_FIRST.md),
[direct adversarial review](STAGE_B_REVIEW.md), [dispatch](REVIEW_DISPATCH.md),
[premise audit](PREMISE_AUDIT.json), [repository checks](REPOSITORY_CHECKS.json).
