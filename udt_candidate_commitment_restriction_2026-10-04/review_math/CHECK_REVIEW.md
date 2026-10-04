# CPR1 parent numerical checks and preserved repair — mathematical review

Verdict: **VERIFIED-WITH-CAVEATS** for the repaired check and its retained finite
coverage. No blocking defect found. This supplement is candidate/code/output
exposed; it is not another blind pass. Earlier source-first and exposed seals
remain unchanged. Final integration is separately pending.

## Repair, actual receipts and scope

Read INITIAL_CHECK.py, current check_restriction.py, both numerical freezes,
CANDIDATE_FREEZE.json, CHECK_REPAIR.md, both diagnostic scripts/freezes,
all four actual capture receipts/stdout/stderr, CONSTRUCTION_RESULT.json and
CLARIFICATIONS.md. The initial code matches the original candidate freeze;
the repaired code matches its separate freeze. Eighteen pin/receipt checks pass
in PARENT_PIN_AUDIT.json. Hashes establish byte correspondence, not chronology
or scientific truth.

The exact code diff is limited to the internal root stopping threshold,
the disclosed reduced case list and updated counts. The initial internal stop
10^(-dps+10) was looser than original-incidence acceptance 10^(-dps+9).
The preserved central diagnostic reproduces the E=1,R=10^6,70-digit residual
4.0998519464711163e-61: smaller than the old 1e-60 stopping threshold but larger
than the required 1e-61 acceptance. Tightening the stop to 10^(-dps+7) repairs
this defect without relaxing acceptance or altering equations. The actual repaired
capture exits zero; its stderr is empty and saved result says PASS.

The documented 95 parent attempts equal 56 original + 5 first diagnostic +
4 center diagnostic + 30 repaired. The original count is reconstructed from
deterministic code order and the diagnostic identification of the failed center;
it is not a recovered raw per-case output. This distinction is correctly stated
in CHECK_REPAIR.md. The first run has no final numerical-result artifact, and its
partial pass messages are not treated as saved numerical evidence.

The repaired set has E=1 at R=10^3 and 10^6, E=10 at R=100, with two centered
step sizes and 40/70-digit solves. It retains one finite static example and an
escaping tail at two radii; it does not numerically track the same receiver
through the horizon. The regular-chart algebra, not those sparse samples, owns
the horizon continuation. Case narrowing is adequate for the declared illustrative
checks and does not turn finite arithmetic into proof of the asymptote.

## Independently recomputed saved quantities

New saved_artifact_check.py imports no parent code. It uses direct-radius
quadrature with geometric integration subdivisions, contracts the outgoing-chart
metric for receiver frequency, and uses an independently coded secant root solve.
This differs from the parent reciprocal-radius quadrature and bracketed Newton
iteration. Shared equations and mpmath arithmetic remain disclosed common inputs.

Before execution SAVED_ARTIFACT_FREEZE.json fixed the six saved central endpoint
checks at both precisions and twelve new 70-digit neighboring incidence solves.
These bring this reviewer's finite evaluated/solved case count to 43 including
the original failed attempt, within its 100-case budget. Same CPU/2 GiB/one-thread
limits, no wall or CPU timeout. The command was:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_candidate_commitment_restriction_2026-10-04/review_math/saved_artifact_check.py > udt_candidate_commitment_restriction_2026-10-04/review_math/saved_artifact_stdout.txt 2> udt_candidate_commitment_restriction_2026-10-04/review_math/saved_artifact_stderr.txt
```

Actual exit zero, all frozen assertions PASS. Saved endpoints satisfy independently
evaluated incidence; endpoint Z and H Z delta_tau_e agree. The three saved two-step
arrival derivative errors reproduce with maximum absolute disagreement 6.43e-68.
At the previously failing E=1,R=10^6 point the independently evaluated saved
70-digit incidence residual is 1.83e-70. The two derivative errors there are
6.667836479e-9 and 1.666959117e-9, consistent with centered-step convergence and
well below the unchanged 1e-6 acceptance. The saved terminal product is
0.9999415526, versus 0.9210476975 at R=10^3 for the same receiver history.
This is a finite trend, not an asymptotic error certificate.

## False-pass audit and omissions

The parent time equation is used to define t_e, so its near-zero residual alone
would be circular. The separate angular equation, metric endpoint frequency,
actual proper-arrival finite differences, step refinement, original-equation
symbolic check and the independent recomputation make the retained validation
substantive. The source-first reviewer already showed that freezing b incorrectly
changes actual arrival derivatives by 6.68%–46.9%; the derivative check is capable
of detecting that relevant mistake. The parent exact equations are reduced on
the declared norm relations, with denominators nonzero in the stated domain.
Those reductions are valid but are not numerical stability or formal proof checking.

I did not rerun the parent 80-case original program, repeat its complete symbolic
code, recreate every discarded intermediate sample, or add more production cases.
The earlier independent original four-dimensional curvature calculation owns its
separate exact cross-check. Parent output retains six central rows and derivative
error summaries; it does not retain every neighbor's numerical tuple. Twelve
neighbors were independently recomputed for this review instead. I do not claim
the saved central rows alone prove the parent's maximum residual over all thirty
repaired solves. Nor do these checks certify interval bounds, arbitrary phases,
all-observer separation, X_max, disk/stability recovery, or native response choice.

CLARIFICATIONS.md closes the two mathematical wording recommendations: monotone
f/r² supplies the uniform ray-domain margin for the tail implicit-function proof;
the squared proper-frequency test does not certify orbital or disk stability.
The distinct constant-along-each-ray b versus varying-across-rays b(R), and finite
emission endpoint versus infinite receiver proper time, are now explicit. These
are same-premise clarifications, preserving the initial candidate and all failures.
