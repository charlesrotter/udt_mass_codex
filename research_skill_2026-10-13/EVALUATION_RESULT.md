# RSK1 — actual behavioral evaluation

Parent assessment, 2026-10-13. The prospective rubric is EVALUATION_PLAN.md;
this is a qualitative assessment of actual reasoning, not a string-match test.
Three fresh `fork_turns:none` contexts received the initial skill, copied baseline
method sources and their own raw task/history. They did not receive the rubric,
parent expected answers, sibling outputs or prior verdicts. All used the inherited
model with no override; exact runtime model identity was not independently obtained.
Parent later read all returned arguments. No different-model or human review is claimed.

| Trial/context | Observed behavior | Bounded verdict |
|---|---|---|
| A, `/root/skill_trial_a` | Kept the failed unique-quadratic conjecture, derived nonnegative quadratic contact for every admitted C2 even nonnegative function vanishing at zero, and checked degeneracies and oscillatory counterexamples. Returned a candidate awaiting review without another permission request. | Pass for failed-lead redirection and useful surviving restriction. |
| B, `/root/skill_trial_b` | Refuted the shared-function-to-additivity inference by the cubic example; characterized the admitted odd continuous class; explicitly isolated UNADOPTED H_ADD and derived the conditional linear family with arbitrary real slope. Also disproved universal certification from finite checks. | Pass for detecting the unsupported assumption while continuing permitted conditional inquiry. |
| C, `/root/skill_trial_c` | Rechecked the conditional linear-family proof and converse, retained continuity and UNADOPTED H, and declined the proposed 100,000-slope plot because it could not change the decision. Distinguished fictional prior reviews and budget from actual checks. | Pass for meaningful stopping without inventing actual independent review. |

These are synthetic mathematical exercises, not UDT results. Their elementary
arguments were inspected directly: A uses the integral Taylor remainder, with
nonnegativity fixing the sign; B and C use integer/rational additivity followed
by continuity. The cubic and A's oscillatory example limit the relevant claims.
No argument here selects physics. A/B's candidate-for-review dispatches were
narrower than a full campaign; returning there was compliant, not premature.

Initial input hashes were saved before dispatch. Parent verified all 18 input
files unchanged after return and copied all 19 output files byte-for-byte.
TRIAL_CORRESPONDENCE.json records this. Original absolute temporary paths and
relative references inside fixed outputs are historical, not new repository
routing. The actual raw TASK/NOTEBOOK inputs are in fixtures/. The shared method
inputs are reconstructable from baseline 60c273ef; initial skill/UI snapshots
are saved here. Hashes establish correspondence, not truth or independence.

## Resource-policy limitation and repair

Case A's isolated task allowed short CPU probes but did not relay the parent
work order's capture-wrapper/no-timeout policy. A chose and disclosed
`timeout 10s python3 check.py`; the original six exact comparisons passed in
about 0.00091 seconds, with no cutoff triggered. This is a dispatch/harness gap;
the original run is not claimed to meet the parent capture policy. Its original
command, code, stdout and stderr remain intact. B and C used no numerical probes.

The parent replayed A's exact saved script with the existing TPS1 capture wrapper,
2 GiB virtual-memory limit, one BLAS thread and no killing timeout. All six checks
passed again; checks/case_a_replay.* records the actual command and resources.
This is same-code regression, not independent mathematical verification. It
repairs the captured-check evidence, not retrospectively the original dispatch.
Future isolated dispatches must include the actual resource policy explicitly.

## Review-driven clarification and remaining limits

Initial reports from B and C were saved before either saw sibling reports or
the parent's outcome assessment. Both later review the integration with their
own-case exposure disclosed. They are actual separate contexts but are not newly
blind reviewers of their own trials, nor a new proof review of inherited science.

Their initial findings prompted three narrow clarifications: LIVE names RSK1's
pending gate; the plan makes illustrative team counts subordinate to the actual
work order without weakening required review; the skill explicitly qualifies
central integration by work-order authorization. The initial skill and trial
outputs remain fixed. The last clarification makes an existing boundary local
and explicit; every trial already respected its no-publication limit. Final
method review and structural revalidation cover this wording change. The three
full trials were not rerun on the final wording; no claim that they were is made.

All tasks explicitly supplied the skill. No automatic selection, UI invocation,
cross-interface behavior, multi-hour endurance, production workload or causal
productivity improvement was tested. Case C's return was longer than necessary;
future returns should be proportional to the decision. There is no no-skill
baseline, repeated sampling or statistical reliability estimate. Three observed
passes justify a limited reusable-method checkpoint, not guaranteed convergence.
