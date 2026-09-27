# Cognitive-Corral Triggers — implementation + catch-proof record

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-27. **Mode:** INFRASTRUCTURE (guardrail hardening).
**Spec:** `COGNITIVE_CORRAL_TRIGGERS_SETUP.md`. **Decision:** Charles chose Option A — implement the
guardrails NOW (independent of the local LLM), build the LLM hooks/export gate NOW, wire the actual
local LLM when installed.

Fixes headwind-defense gap (a): the cognitive corral was recall-class — this session it fired only when
Charles challenged (the driver drifted to a "cured" kap8 headline; the verifier caught it, not the driver).

## What was built
- **Part A — `CLAUDE.md ## DRIVER TRIGGERS`** (always-loaded): 6 imperative, output-bound triggers
  (#1 purist-logic / #2 solver-first / #3 whole-before-slice / #4 provisional-until-verified /
  #5 chose-or-derived / #6 derive-natively), each bound to observable self-output tokens; PLUS the
  **non-droppable allowed-lane clause** (CATEGORY-A technique / GR-as-reference always GREEN). Back-pointers
  added to the 7 source memories.
- **Part B — harness hooks** (`.claude/settings.json` + `.claude/hooks/corral_trigger.py`): PreToolUse on
  `Task|Agent|Bash` injects a NON-BLOCKING pause+honesty reminder at three structural moments — agent
  launch (observing-or-targeting), solver run (bound-grid + chose-or-derived), git commit
  (verifier-before-record). Merit-never: forces a procedure, never judges the answer. Hook field format
  confirmed against Claude Code v2.1.173 (claude-code-guide agent `aa108d9339303f7dc`).
- **Part C — freshness pass** (agent `ac9003e276baf2a51`): all 48 memories tagged
  DURABLE/CURRENT/SUPERSEDED/HISTORICAL vs `LIVE.md` (**26 DURABLE, 14 CURRENT, 7 SUPERSEDED, 1 HISTORICAL,
  0 conflicts; 40 included / 8 excluded** — ground-truth grep census, corrected 2026-06-27 after a blind
  verifier caught the agent's mid-pass self-count 28/9/6/1 was wrong). 3 judgment calls flagged for Charles (3 type:project files tagged DURABLE as
  method-discipline; `milestone-udt-makes-mass-natively`→SUPERSEDED as the imported-S³ object).
- **LLM export gate** (`export_for_local_llm.py`): builds the cross-check payload = DURABLE corral +
  CLAUDE.md + LIVE.md + only CURRENT memories + the allowed-lane clause verbatim; REFUSES untagged DATED
  and CONFLICT tags. The local LLM itself is not yet installed — this is the wiring point for when it is.

## CATCH-PROOF (per spec acceptance §)
1. **Agent trigger** — dispatcher on `{"tool_name":"Task"}`/`{"Agent"}` → observing-or-targeting reminder.
   PASS — and **live-confirmed in-session**: the PreToolUse:Agent harness hook fired on a real agent launch
   (the blind-verifier agent), injecting the reminder. So BOTH Bash and Agent hooks are live-confirmed.
2. **Solver trigger** — `{"tool_name":"Bash","command":"...continuation_solve_p1"}` → bound-grid/
   chose-or-derived reminder. PASS. Unrelated `ls` → SILENT (empty output). PASS.
3. **Commit trigger** — `{"command":"git commit ..."}` → verifier-before-record reminder. PASS — and
   **live-confirmed this session**: a real Bash call containing "git commit" fired the harness hook and
   injected the reminder (the settings.json was picked up in-session). Malformed stdin → silent, exit 0. PASS.
4. **Part A auto-load** — `## DRIVER TRIGGERS` is in `CLAUDE.md` (auto-loaded every session). Confirm the
   section appears in a FRESH session's context (pending: only fully verifiable next session).
5. **Merit-never audit** — re-read all reminder strings (3 hook + 6 CLAUDE triggers): NONE judges the
   answer's shape (no "is this a lump / the right mass / smooth enough"); every one demands honesty/
   provenance/procedure. PASS.
6. **Freshness / export gate** — every DATED memory carries a tag (48/48). Export gate PASSED (40 included,
   8 excluded as stale, allowed-lane present); NEGATIVE TEST: stripping a tag from a DATED memory →
   gate ABORTS (exit 1, names the untagged file); restored → PASS. The "refuse untagged DATED" teeth work.

## Scope (stated honestly)
- **Closes:** recognized forks (Part A higher baseline firing) + the three structural tool-call moments
  (Part B, recognition-independent).
- **Does NOT close:** a genuinely-silent fork with no trigger token and no tool-call signature — that
  residual is the **local-LLM / second-reader** job (not yet installed; export gate is its wiring point).
  This setup narrows the gap; it does not eliminate it.
- **Failure-detection (added 2026-06-27):** a `SessionStart` hook (matcher `startup|resume`, same
  `corral_trigger.py` dispatcher, format confirmed vs v2.1.173, agent `a8bad28918`) prints
  `✓ CORRAL GUARDRAILS ACTIVE` + the startup self-check at the top of every session. PRESENCE = hooks
  loaded; ABSENCE = hooks failed (the loud signal answering "how will I know if the triggers fail to
  fire"). Catch-proof: dispatcher emits the banner on `{"hook_event_name":"SessionStart"}` (+ `continue:true`),
  PreToolUse path unregressed. Live SessionStart firing confirms next session (it only loads at session start).
- **Empty-instance dry-run (2026-06-27, agent `ae0d35a4`):** SEAMLESS-WITH-NITS — orientation reads cleanly,
  no untagged contradictions, all hard pointers resolve, pytest matches. FINDING: a fresh SUBAGENT did not see
  the `## DRIVER TRIGGERS` section in its auto-loaded CLAUDE.md (yellow flag; subagent context may differ from
  a top-level session) — BUT the hooks fired regardless. Reinforces that the hooks (Part B) are the
  load-bearing mechanism. Nits fixed (prototype/ bare paths).
- **Pending:** only the Part-A auto-load of `## DRIVER TRIGGERS` in a FRESH top-level session remains unconfirmed
  (it is auto-loaded by design from CLAUDE.md; verifiable next session). The live hook firing is NO LONGER
  pending — both Bash and Agent hooks fired live in-session.

## Verifier pass (blind, adversarial — 2026-06-27, agent `a1c2571e0aa132210`)
Verdict: **CLEAN-WITH-GAPS** — Parts A/B/C, merit-never, the non-blocking hooks (live-fired for Bash AND
Agent), the export gate (lane-verbatim + refuse-untagged-DATED, negative-tested), and all 48 freshness
tags all PASS. Two gaps caught and FIXED here: (1) the Part-C tag counts in this doc were stale
(28/9/6/1 → corrected to 26/14/7/1); (2) trigger-#4's source memory lacked the back-pointer (added to
`session-handoff-pointer.md`). No functional defect.

## Verifier note
Catch-proof performed inline (above). The hook-field correctness was independently confirmed by the
claude-code-guide agent; the freshness classification by a blind agent reconciling only against LIVE.md
(merit-never). A full blind adversarial verifier pass on this infrastructure is deferred (low physics
risk; the catch-proof + negative test are the load-bearing checks).
