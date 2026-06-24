# P5 — SHRINK THE LIVE STATE (SOLVER_INTEGRITY_UPGRADES_SPEC P5)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** DONE (acceptance-tested by a
fresh zero-context agent). Files: `LIVE.md` (new) + read-first pointers in `HANDOFF.md` / `STATE.md`
+ the resume memory.

## What it does
Creates `LIVE.md` — a short (~50-line), ruthlessly-current single file holding ONLY: the binding
method (pointer), the current activity (integrity arc P1-P5 done), the immediate next action, the
parked physics frontier (time-live native S²), and the must-not-lose durable canon. Nothing not true
RIGHT NOW. HANDOFF.md / STATE.md remain the detailed append-record; LIVE.md WINS if they disagree.

## Why
STATE.md needed "READER NOTE / inoculation" banners precisely because it had grown long and accreted
stale next-steps — the banners papered over the risk. `LIVE.md` removes the risk at the root: a fresh
agent reads ONE short current file first, so a stale next-step buried in the long history can't be
mistaken for the live instruction. (The banners in STATE.md are left as history; LIVE.md being the
entry point retires their function.)

## Wiring
- `HANDOFF.md` + `STATE.md`: a "READ LIVE.md FIRST" pointer added at the very top of each.
- Resume memory (`session-handoff-pointer` + MEMORY.md index): read-order now starts at LIVE.md.
- Read order is now: LIVE.md → CLAUDE.md "How we work" + discipline skills → HANDOFF TOP → INDEX.md.

## Acceptance (per spec) — MET
"A fresh agent can act correctly from LIVE.md alone, without stale-next-step risk." Tested by a fresh
zero-context agent (id ac34d012785859feb) given ONLY LIVE.md:
- Correctly stated the current state (integrity arc done; physics frontier parked), the next action
  (the two MAP-first decisions, gated on Charles), and the binding rules (MAP/gated-DERIVE, data-blind,
  anti-hang, the skills).
- Verdict: "strong cold-start entry point ... self-sufficient enough to keep an agent from acting
  wrongly"; it correctly would NOT auto-launch a solve (the gating language forces a pause).
- One flagged ambiguity (migration sequencing vs the physics frontier) → FIXED: the NEXT ACTION line
  now states the migration is a SEPARATE gated step, not the immediate next.

## The integrity-upgrades arc is now COMPLETE (P1-P5)
P1 purity harness · P2 operator-from-the-action · P3 disciplines-as-skills · P4 cross-model verify ·
P5 LIVE.md. All committed + blind-verified; `pytest tests/` = 16 passed / 5 documented-gap xfails.
The physics frontier (TIME-LIVE NATIVE S²) resumes next, starting with the two MAP-first decisions.
