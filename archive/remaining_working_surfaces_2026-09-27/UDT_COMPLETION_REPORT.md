# Guardrails and Central Science Completion Record

**Date:** 2026-09-05

**Work order:** `UDT_Complete_Guardrails_and_Central_Science_Tracking.md`

**Starting synchronized commit:** `0c71b413bf37553e03a8ea5b1824e3f34a917085` on `grok`

**Fixed scientific snapshot:** `f23199e4a47aaf83acb9ea7d1ad382cd814159c2`

## Outcome

| Goal | Status | Reason |
|---|---|---|
| A. Guardrail and discovery-workflow implementation | **COMPLETE for the active Codex/ChatGPT deployment** | The initial audited implementation passes static, unit, regression, two-sided behavior, and zero-context Codex instruction-chain checks. Claude hooks are retained inactive compatibility infrastructure; live Claude-hook testing is `NOT_APPLICABLE` to this deployment, not passed. |
| B. Central accepted-science account and tracking | **COMPLETE for the declared accepted scope and fixed snapshot** | All 335 registry rows are dispositioned, every main-argument row has a reviewed manuscript anchor, the source-indexed sidecar is generated from the existing registry, navigation and invalidation checks pass, and the completed manuscript has passed chapter and cross-chapter fidelity review. |

Historically named `CLAUDE.md` and `.claude/skills/` remain shared instructions in the explicit
Codex startup chain. Their names do not make Claude active. Open physical questions are not counted
as missing documentation.

## Baseline and preservation

The root checkout was synchronized with `origin/grok` before work began. Unrelated dirty and
untracked paths were preserved and excluded from inspection, mutation, staging, and citation.
The scientific records below remain byte-identical to the starting commit:

| Record | SHA-256 |
|---|---|
| `CURRENT_SCIENTIFIC_PREMISES.tsv` | `3743533cfe1cc6a047e11cf182d90561c100727fc506aca3c5ff7a33779b2c3f` |
| `CURRENT_SCIENTIFIC_PREMISES.md` | `044a7067b2e678ddce77b34a328a179338db7e873ec4d73c8e64375e85cbc008` |
| `CANON.md` | `047b7fbbc1acacf01d2716e3c98cdefd0b9b20136ac4a3306f55dd6775465250` |

No scientific premise, source grade, evidence payload, or canon entry was changed. The new
coverage file copies stable IDs and controlling-source metadata but deliberately does not copy or
own scientific grades.

## Goal A — rule inventory

| Rule | Final disposition | Implemented location and check |
|---|---|---|
| R1 coherent authority/no hidden science | `VERIFIED` | `AGENTS.md` is primary; its specified `CLAUDE.md` sections and triggered `.claude/skills/` remain shared instructions despite historical names. Static tests and a read-only zero-context Codex rehearsal verify the effective chain. |
| R2 bounded discovery | `VERIFIED` | `AGENTS.md` permits authorized algebra, limits, examples, counterexamples, and conditional lemmas while keeping counterfactual physics unadopted. Behavioral cases `NUMERIC_METHOD` and `HELD_ALREADY_AUTHORIZED` pass. |
| R3 exploration/candidate/promotion | `VERIFIED` | Recoverable checkpoints and conditional unproved dependencies are explicitly typed. `FAILED_CHECKPOINT` passes without promoting the draft. |
| R4 controlled approximations/linear work | `VERIFIED` | Domain, error, and inherited downstream bounds replace the former absolute ban. `CONTROLLED_APPROXIMATION` and `FIRST_VARIATION` pass. |
| R5 quantifiers/bounded questions | `VERIFIED` | Witness, counterexample, finite-search, and completeness quantifiers are separated. Three corresponding behavior cases pass. |
| R6 validity, not aesthetics | `VERIFIED` | Original residual, object type, boundary, error, and convergence remain certification gates; appearance is not. Positive and negative behavior cases pass. |
| R7 finite solver-first diagnostic | `VERIFIED` | The diagnostic has a finite stop and permits a bounded incompatibility. `solver-first` tests retain equation, omission, convergence, and premise checks without demanding an unlimited search. |
| R8 evidence-matched preregistration | `VERIFIED` | Observation, numerical certification, and mathematical discovery now have distinct freezes; post-outcome tuning cannot become derivation. `DATA_TUNED_PROMOTION` passes. |
| R9 proportional review | `VERIFIED` | Packaging-only and scientific review are distinguished; existing sound utilities are reused; targeted and closure regressions are required. Static policy tests cover both clauses. |
| R10 concrete independence/objections | `VERIFIED` | Context, model exposure, implementation, source versions, and prior-verdict exposure are separate fields. `REVIEW_INDEPENDENCE` passes. |
| R11 evidence/dependency/impact tracking | `VERIFIED` | Stable IDs/source versions and review of both positive and negative descendants are required. `UPSTREAM_CHANGE` passes; the manuscript sidecar implements source/dependency tracking without becoming a second registry. |
| R12 honest automation | `VERIFIED_FOR_ACTIVE_DEPLOYMENT_SCOPE` | The AST scanner is active repository automation and tested. The Claude reminder hook is retained and unit-tested only as inactive compatibility code; no live-hook or Codex-enforcement claim is made. |
| R13 sync/offline/resources | `VERIFIED` | Non-destructive sync, commit-pinned offline audits, explicit budgets, timeouts, and single-GPU safety are retained. `HELD_OFFLINE_AUDIT` now permits the scoped audit without claiming freshness. |
| R14 assessable decisions | `VERIFIED` | New physical decisions require a lay account of change, provenance, alternatives, falsifiers, cost, and requested authority; already-authorized bounded work proceeds autonomously. |

### Automation delivered

- Codex/ChatGPT loads `AGENTS.md`; that file explicitly requires the bounded shared reads from
  `CLAUDE.md` and task-triggered `.claude/skills/`. The zero-context rehearsal found this chain.
- `.claude/hooks/corral_trigger.py` and `.claude/settings.json` retain tested portable compatibility
  behavior but are inactive in the Codex deployment. No live Claude test is claimed.
- `.claude/guardrail_work_order_metadata.json` is the safe project-local default metadata source
  and authorizes no solver by default.
- `guardrail_import_scanner.py` is static-only. It handles exact main guards, nested/compound and
  alternate branches, definitions and handlers, package/relative imports, dynamic-import aliases,
  namespace packages, and execution-mode-aware transitive reachability without importing target
  code.
- The Codex rehearsal record is `tests/codex_instruction_chain_rehearsal_2026-09-05.md`.
- The behavior fixtures and full actual before/after responses are in
  `tests/guardrail_behavior_cases.json` and
  `tests/guardrail_behavior_evaluation_2026-09-05.json`.

### Two-sided behavior result

The prompts were frozen before revised-policy evaluation. A blinded separate-context subject saw
only the seven declared policy files and the cases. The collaboration runtime did not expose an
exact model identity, so this is recorded as a separate-context same-family evaluation, not a
human or different-model review.

| Policy | Required | Held back | Total | Substantive misses | Unnecessary blocks | Repeated permissions |
|---|---:|---:|---:|---:|---:|---:|
| Baseline `0c71b413` | 13/14 | 3/4 | 16/18 | 0 | 2 | 0 |
| Final revised bundle `0e3fef8e…` | 14/14 | 4/4 | 18/18 | 0 | 0 | 0 |

The two baseline defects were unnecessary refusal of a controlled approximation and of an
expressly authorized commit-pinned offline audit. Both are accepted, correctly scoped actions in
the final responses. Hidden imports, post-outcome promotion, invalid numerical certification,
protected-path access, and fabricated review independence remain rejected.

## Goal B — completed account and tracking

`UDT_METRIC_KERNEL_DEVELOPMENT.md` is the complete first central account for the declared accepted
metric/kernel scope at snapshot `f23199e4`. Its state marker is
`COMPLETE_FOR_DECLARED_ACCEPTED_SCOPE_AND_SNAPSHOT__FIDELITY_REVIEWED`; its final SHA-256 is
`3b625d8f43620a37c99d9f4f0fdc9390c3a12306b1da87281c143ce84d40a81e` and is bound by the verifier.

The generated `UDT_METRIC_KERNEL_COVERAGE.tsv` contains all 335 exact registry rows and has SHA-256
`b9a8d84d58b60dd6381af6512d89a63c8fa26750f0068e444dd039d329e74bc4`.
The fixed-snapshot disposition is:

| Role | Rows |
|---|---:|
| `MAIN_ARGUMENT` | 65 |
| `SUPPORTING_LEMMA` | 123 |
| `BOUNDARY_RESULT` | 76 |
| `CONTROL_ONLY` | 57 |
| `OUTSIDE_SCOPE` | 12 |
| `SUPERSEDED_HISTORICAL` | 2 |
| **Total** | **335** |

Every `MAIN_ARGUMENT` row has a body-level manuscript anchor. The other rows have an explicit
role, controlling source and hash, dependencies where applicable, scope/open-boundary note, and
Appendix coverage disposition. The sidecar now separates the currently observed source hash from
the last fidelity-reviewed source hash and its review ID. An ordinary
`update_metric_kernel_account.py --write` flags both positive and negative descendants of a changed
source and preserves that invalidation. Only `--record-review` with an exact new-source hash,
manuscript hash, affected-ID closure, snapshot, and review ID can restore reviewed status.
`verify_metric_kernel_account.py` checks exact bytes, source hashes, dependencies, counts,
anchors, placeholders, and the final manuscript hash. `README.md` and `INDEX.md` route readers to
the account, sidecar, updater, and verifier.

### Fidelity review

Separate-context source-first reviews examined the response-law/solution-space chapters and the
causal/area/transport chapters. Their identified scope, typing, quotient, parameterization,
frequency, area-rank, and adopted-versus-conditional defects were repaired without changing the
fixed scientific sources. A fresh cross-chapter seam review then caught two tracking defects:
overbroad generated body anchors and failure to bind the manuscript bytes. Curated anchors and an
exact manuscript hash fixed both. The repair follow-up accepted the complete first edition.

Reviewer exposure is recorded honestly: fresh/separate context and source-first where stated;
same model family; not human specialist review and not claimed as a different-model proof.

## Closure checks

Environment: Python 3.10.12, pytest 9.1.1, Codex CLI 0.144.5. Claude Code 2.1.201 is installed but
inactive and not part of the completion gate.

| Command/check | Outcome |
|---|---|
| `python3 verify_current_scientific_premises.py` | `PASS` — exact 335-row registry/startup/premise guards and 754 historical dispositions |
| `python3 verify_metric_kernel_account.py` | `PASS` — 335 rows, exact role counts, source/dependency/anchor/hash checks |
| `python3 -m pytest tests/test_metric_kernel_account.py -q` | `4 passed`, including the isolated end-to-end invalidation/review replay |
| Zero-context Codex instruction-chain rehearsal | `PASS_FOR_CURRENT_CODEX_INSTRUCTION_CHAIN_SCOPE` |
| `python3 -m pytest tests/test_import_scanner.py tests/test_solution_space_gate.py tests/test_corral_trigger.py tests/test_guardrail_policy.py tests/test_hygiene_header.py tests/test_metric_kernel_account.py tests/test_startup_surface.py -q` | `120 passed, 1 xfailed` in 404.92 s |
| `python3 -m py_compile` on the changed Python implementation and tests | `PASS` |
| `git diff --check` | `PASS` |

The expected legacy `test_no_habit_pins` xfail concerns a historical silent G/P fork; it is not a
waiver for any new failure. No new required-test failure will be exempted.

## What the workflow now permits

Charles can authorize one bounded question and let the agents explore calculations,
counterexamples, controlled approximations, and recoverable failures through its stated stop
condition without repeated permission requests. The workflow preserves adverse or unfamiliar
answers instead of selecting by appearance, distinguishes a documentation join from an open
scientific bridge, and rechecks both positive and negative dependents when an upstream source
changes. At the same time, it still blocks hidden physical imports, outcome-tuned derivations,
premise changes, protected-path access, and inflated review or certification claims.

## Scientific questions intentionally left open

The completed account does not select a physical history, observer/path population, source,
matter or mass law, native light/detector interpretation, absolute scale, or physical
`X_max`; it does not canonize the provisional premises. Those are genuine scientific choices or
research problems, not missing chapters in this fixed-snapshot edition.

## Follow-up repairs and remaining deployment limits

The source-invalidation defect was reproduced before repair: changing a controlling source in an
isolated copy and running the ordinary updater restored `FIDELITY_REVIEWED`. The new end-to-end
regression now requires the ordinary updater to retain `SOURCE_CHANGED__FIDELITY_REVIEW_REQUIRED`
or descendant dependency-review status across repeated runs. Its simulated explicit review succeeds
only when the record is tied to the exact new source, unchanged manuscript, snapshot, and complete
affected-ID closure.

The actual Codex rehearsal passed. Live Claude hooks remain untested because they are inactive and
not applicable to this deployment; that is neither a pass nor a remaining Codex-workflow blocker.
