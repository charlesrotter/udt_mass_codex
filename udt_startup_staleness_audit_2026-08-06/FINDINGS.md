# Startup / Orientation Staleness Audit — 2026-08-06 (READ-ONLY; findings for Charles's ruling)

Yardstick: phi+orchestra (milestone 08-05) -> c_eff reframe (verified 08-06) -> mu (deferred);
ACTIVE LANE = x_max pair question (`udt_xmax_pair_question_MAP_2026-08-06.md`, O1 pending); assembly
lane ARCHIVED-LEGACY; build FORWARD. Agent: read-only sweep, nothing edited/committed.

Counts: ARCHIVE-BODY 3 (F2,F5,F8) | RE-POINT 3 (F1,F3,F7) | KEEP-AS-HISTORY 4 (F4,F6,F9,F10) |
TRIM 0 | UPDATE 0. CLEAN: AGENTS.md, INDEX.md (both carry step 5a with the 08-06 frontier docs).

| # | Doc + location | Stale content | Why stale | Class |
|---|---|---|---|---|
| F1 | INFLIGHT_STATE.md PURPOSE block (~L14-17) | "read ... P4_ARC_SUMMARY, ROADMAP_LINEAR_TIME, ... A3 audit" | sends a fresh session to July docs for a banked P4 arc; CONTRADICTS the 08-06 banner 4 lines above | RE-POINT |
| F2 | INFLIGHT_STATE.md body (~L14-157) | the full 2026-08-01 A3 launch runbook + increment list | A3 is COMPLETE/BANKED (e379098); a launch runbook for a done task in the live in-flight file | ARCHIVE-BODY |
| F3 | HANDOFF.md Fresh-entry path (~L88-101) | numbered path leads with 08-05 spine, never lists the 08-06 frontier docs | the RESTART ANCHOR names them but the numbered path a reader follows does not | RE-POINT |
| F4 | HANDOFF.md (~L127-133) next-investigation = cocycle test | superseded by x_max O1 | but under "PRIOR (2026-08-05)" header; anchor overrides | KEEP-AS-HISTORY |
| F5 | LIVE.md PRIOR-STATE 08-05 block (~L67-249, INSIDE STARTUP markers) | ~183 lines of 08-05 narration loaded as "current" by the BEGIN->END rule | superseded on c_eff/x_max; but it is the MILESTONE (largely still-valid banked structure) -- JUDGMENT CALL: move below STARTUP_CURRENT_END with a compact pointer, or keep | ARCHIVE-BODY (candidate) |
| F6 | LIVE.md (~L204-211) next-investigation | superseded by x_max O1 | under PRIOR header; topmost overrides | KEEP-AS-HISTORY |
| F7 | CURRENT_RESEARCH_PROGRAM.md startup route (~L173-186) + next-investigation (~L151-168) | route + next-step terminate at 08-05 material; omit the frontier docs | FRONTIER UPDATE prepended at top sets O1, but the route below still ends at 08-05 | RE-POINT |
| F8 | ROADMAP_LINEAR_TIME_2026-07-31.md (whole) | linear-time program: Step 2 T4-linear next | superseded by the phi+orchestra->c_eff->x_max frontier; zero awareness of the 08-05/06 line; reached only via F1 | ARCHIVE-BODY |
| F9 | P4_ARC_SUMMARY_2026-07-31.md (whole) | historical P4 arc index | correct history; only MIS-PRESENTED as current via F1's pointer -- fix F1, leave the doc | KEEP-AS-HISTORY |
| F10 | UDT_SCIENTIFIC_FRONTIER_2026-07-19.md | historical frontier checkpoint | already flagged historical in AGENTS/INDEX; over-cited nowhere | KEEP-AS-HISTORY |

Trip-hazard (the one intra-file contradiction): INFLIGHT_STATE.md 08-06 banner says "read the x_max
MAP"; its PURPOSE block 4 lines below says "read ROADMAP_LINEAR_TIME / A3 audit" -> a reader
following the second lands on the superseded T4-linear program. Sole live entry point for both July
docs (P4_ARC_SUMMARY, ROADMAP_LINEAR_TIME) is INFLIGHT F1/F2; fixing them removes it.
