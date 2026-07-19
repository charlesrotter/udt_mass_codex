# Codex Zero-Context Startup Rehearsal — Preregistration

Date: 2026-07-19

Base: `ca2bf9eb042783cc028c5dd42fab84158c83a608`

Branch: `codex/startup-dress-rehearsal-fix-2026-07-19`

## Purpose

Test whether a genuinely fresh Codex instance can synchronize `grok`, follow the repository startup
instructions, recover the exact current scientific status and authority boundary, detect bad
pointers, and return a useful orientation without relying on conversation history.

## Baseline contract

Launch an ephemeral Codex instance from a new origin clone with user configuration ignored. It may
read repository evidence and run read-only Git/path checks, but it may not edit the repository or run
long scientific computations. Require it to report:

1. actual branch, HEAD, and status;
2. the read sequence followed;
3. the conditional current result and premise boundary;
4. the first and conditional second open gates;
5. the actual next-action authority;
6. missing, stale, contradictory, or ambiguous startup evidence; and
7. whether another fresh instance can safely continue.

## Failure criterion

The rehearsal fails if the instance cannot complete an orientation response, reads superseded
history as current, strengthens a conditional result, misses an open gate, invents authorization,
or encounters a broken required path.

## Registered correction scope

If the baseline fails, edit only the operational read boundaries and startup pointers in:

- `AGENTS.md`
- `LIVE.md`
- `HANDOFF.md`
- `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md`
- `INDEX.md`
- `MEMORY.md`
- `README.md`
- a concise rehearsal report created by this phase

Do not change equations, scientific verdicts, evidence packages, scripts, data, manifests,
registries, `CANON.md`, or research artifacts. Preserve all prior handoff history.

## Required correction behavior

- Mark the exact startup-current ranges in `LIVE.md` and `HANDOFF.md`.
- Require bounded section reads rather than whole-file dumps at startup.
- Use the current angular audit's lay decision tree and status ledger as the compact first evidence
  view; reserve full reports, scripts, JSON, and historical layers for task-specific follow-up.
- Preserve the same scientific status and authority boundary byte-for-meaning.
- A second fresh-clone, zero-context rehearsal must complete with no missing pointer, contradiction,
  claim-strength drift, or invented authorization.

## Verification

- verify all changed-document Markdown links and current frontier targets;
- replay the angular derivation/verifier and both latest package manifests;
- replay all six frozen native-action manifests;
- reproduce the documented test baseline;
- preserve the original 54-path dirty checkout by metadata only;
- commit and push the correction branch; and
- advance `origin/grok` only by a freshly verified normal non-force fast-forward.
