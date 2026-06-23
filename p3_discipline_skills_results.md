# P3 — DISCIPLINE AS SKILLS (SOLVER_INTEGRITY_UPGRADES_SPEC P3)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** DONE.
Files: `.claude/skills/{solver-first,verifier-before-record,no-shortcuts,completeness-map}/SKILL.md`
+ a pointer section in `CLAUDE.md`.

## What it does
Factors the binding disciplines into four auto-loading, self-contained skills (each ≤1 screen),
so the full-form protocol unfolds on demand instead of living as long inline prose. Distilled
verbatim from the binding sources — no new claims introduced:
- **`solver-first`** — the mismatch -> SOLVER-not-MECHANISM four-question protocol (from CLAUDE.md
  + memory [[solver-first-not-mechanism]]).
- **`verifier-before-record`** — what a clean blind adversarial pass requires (from the repo-discipline
  section + the P1/P2 verifier practice this session).
- **`no-shortcuts`** — the anti-import/anti-freeze checklist + `python3 -m pytest tests/` (the P1+P2
  purity harness; from [[cleaner-is-not-clean-no-shortcuts]] + Principles 1-3 + ANTI-HANG).
- **`completeness-map`** — the ten completeness criteria + the six standing questions, quoted verbatim
  from SOLVER_COMPLETENESS_MAP.md (+ [[solver-architect-metacognition]]).

## Design decision (Charles-agreed): keep the tripwires INLINE
Skills lazy-load their BODY on invoke; only their DESCRIPTION is always in context. So moving the
binding rules ENTIRELY into skills would lose the always-loaded guarantee. Resolution: CLAUDE.md
keeps the short tripwires inline (binding, always-loaded) and adds a "Discipline skills" pointer
section naming the four skills as the expandable full-form. The skills UNFOLD the tripwires on
demand; they do NOT replace them. (Confirmed CLAUDE.md still carries all inline tripwires.)

## Acceptance (per spec)
- **Each ≤1 screen:** yes — 31-35 lines each.
- **Valid + discoverable:** yes — `.claude/skills/<name>/SKILL.md` is the correct project-scoped
  location (confirmed via claude-code-guide agent ad1e5935cf0c34cc8); frontmatter parses; `name`
  matches the directory. A FRESH session auto-discovers them — descriptions always loaded so the
  model knows when to invoke; the body lazy-loads only on invoke (negligible context cost).
- **CLAUDE.md points to them instead of inlining the full text:** yes — pointer section added; the
  long-form now lives in the skills, the binding tripwires stay inline.
- **Suite unaffected:** P1+P2 still 16 passed / 5 xfailed.

## Known caveat (expected, not a defect)
`.claude/` did not exist when THIS session started, so Claude Code cannot watch the new top-level
skills dir mid-session; the skills take effect in a FRESH session (the acceptance target) or after a
restart. Nothing to fix — this is the documented live-change-detection behavior.

## Next (per spec ORDER P1->P2->P3, then P4/P5 as bandwidth allows)
P4 — cross-model verify (ruling 2026-06-23: fresh zero-context Claude for load-bearing /
native-vs-import / must-quantize-class verdicts; documented command/flag; disagreement logged not
dropped). P5 — shrink the live state into a ruthlessly-pruned LIVE.md. Then the integrity arc is
complete and the physics frontier (time-live native S^2) resumes.
