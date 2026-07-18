# Phase R0 dependency summary

This summarizes the complete static edge table in `DEPENDENCY_MAP.tsv` at base `bfa0b9a`.
Dynamic and unresolved paths are deliberately retained; this is not a runtime trace.

## Coverage by category

| Category | Edges |
|---|---:|
| `FILE_PATH` | 1450 |
| `MANIFEST` | 1135 |
| `MARKDOWN_LINK` | 341 |
| `PYTHON_IMPORT` | 6667 |
| `STARTUP` | 399 |
| `TEST` | 161 |
| `TEXT_REFERENCE` | 7710 |

## Resolution matrix

| Category | Status | Edges |
|---|---|---:|
| `FILE_PATH` | `ABSOLUTE_EXTERNAL` | 248 |
| `FILE_PATH` | `DYNAMIC` | 1028 |
| `FILE_PATH` | `DYNAMIC_OR_GLOB` | 9 |
| `FILE_PATH` | `MISSING_OR_GENERATED` | 76 |
| `FILE_PATH` | `RESOLVED_BY_BASENAME` | 2 |
| `FILE_PATH` | `RESOLVED_DIRECTORY` | 1 |
| `FILE_PATH` | `RESOLVED_TRACKED` | 86 |
| `MANIFEST` | `AMBIGUOUS_BASENAME` | 82 |
| `MANIFEST` | `MISSING_OR_GENERATED` | 35 |
| `MANIFEST` | `RESOLVED_BY_BASENAME` | 480 |
| `MANIFEST` | `RESOLVED_TRACKED` | 538 |
| `MARKDOWN_LINK` | `ABSOLUTE_EXTERNAL` | 157 |
| `MARKDOWN_LINK` | `AMBIGUOUS_BASENAME` | 1 |
| `MARKDOWN_LINK` | `EXTERNAL` | 1 |
| `MARKDOWN_LINK` | `MISSING_OR_GENERATED` | 157 |
| `MARKDOWN_LINK` | `RESOLVED_TRACKED` | 25 |
| `PYTHON_IMPORT` | `EXTERNAL_OR_STDLIB` | 6071 |
| `PYTHON_IMPORT` | `RESOLVED_INTERNAL` | 596 |
| `STARTUP` | `ABSOLUTE_EXTERNAL` | 2 |
| `STARTUP` | `DYNAMIC_OR_GLOB` | 16 |
| `STARTUP` | `MISSING_OR_GENERATED` | 7 |
| `STARTUP` | `RESOLVED_BY_BASENAME` | 16 |
| `STARTUP` | `RESOLVED_DIRECTORY` | 33 |
| `STARTUP` | `RESOLVED_TRACKED` | 325 |
| `TEST` | `ABSOLUTE_EXTERNAL` | 2 |
| `TEST` | `DYNAMIC` | 13 |
| `TEST` | `DYNAMIC_OR_GLOB` | 15 |
| `TEST` | `EXTERNAL_OR_STDLIB` | 42 |
| `TEST` | `MISSING_OR_GENERATED` | 46 |
| `TEST` | `RESOLVED_ANCHOR` | 1 |
| `TEST` | `RESOLVED_INTERNAL` | 22 |
| `TEST` | `RESOLVED_TRACKED` | 20 |
| `TEXT_REFERENCE` | `RESOLVED_TRACKED` | 7710 |

## Unresolved/dynamic audit queue

Static edges total: 17863. Dynamic or unresolved edges: 1485.
The following are representative rows only; the TSV retains every row.

| Source | Line | Category | Raw target | Status |
|---|---:|---|---|---|
| `.claude/hooks/corral_trigger.py` | 32 | `FILE_PATH` | `out` | `DYNAMIC` |
| `.claude/hooks/corral_trigger.py` | 38 | `FILE_PATH` | `sys.stdin` | `DYNAMIC` |
| `.claude/skills/solution-space-not-imposition/SKILL.md` | 71 | `MARKDOWN_LINK` | `how-we-work-method` | `MISSING_OR_GENERATED` |
| `.claude/skills/solution-space-not-imposition/SKILL.md` | 71 | `MARKDOWN_LINK` | `solution-space-not-imposition` | `MISSING_OR_GENERATED` |
| `.claude/skills/solution-space-not-imposition/SKILL.md` | 71 | `MARKDOWN_LINK` | `solver-first-not-mechanism` | `MISSING_OR_GENERATED` |
| `AGENTS.md` | 30 | `STARTUP` | `.claude/skills/*/SKILL.md` | `DYNAMIC_OR_GLOB` |
| `CLAUDE.md` | 109 | `STARTUP` | `pytest tests/` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 133 | `MARKDOWN_LINK` | `solution-space-not-imposition` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 150 | `STARTUP` | `python3 -m pytest tests/` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 154 | `STARTUP` | `pytest tests/` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 189 | `MARKDOWN_LINK` | `apply-purist-logic-proactively` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 194 | `MARKDOWN_LINK` | `solver-first-not-mechanism` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 198 | `MARKDOWN_LINK` | `sweep-whole-not-fragments` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 202 | `MARKDOWN_LINK` | `session-handoff-pointer` | `MISSING_OR_GENERATED` |
| `CLAUDE.md` | 309 | `STARTUP` | `**LIVE.md` | `DYNAMIC_OR_GLOB` |
| `CLAUDE.md` | 311 | `STARTUP` | `PURSUIT_CHARTER_*.md` | `DYNAMIC_OR_GLOB` |
| `CLAUDE.md` | 315 | `STARTUP` | `PURSUIT_CHARTER_*.md` | `DYNAMIC_OR_GLOB` |
| `CLAUDE.md` | 317 | `STARTUP` | `python3 -m pytest tests/` | `MISSING_OR_GENERATED` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 2 | `MANIFEST` | `cold/UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 3 | `MANIFEST` | `cold/UDT_NATIVE_ACTION_COLD_PACKET.md` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 5 | `MANIFEST` | `stage1/arm_A/DRIVER_PROVENANCE_AND_AUDIT.md` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 6 | `MANIFEST` | `stage1/arm_A/OUTER_TRANSCRIPT.txt` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 7 | `MANIFEST` | `stage1/arm_A/PRELAUNCH_NETWORK_FAILURE_TRANSCRIPT.txt` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 8 | `MANIFEST` | `stage1/arm_A/SHA256SUMS.txt` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 9 | `MANIFEST` | `stage1/arm_A/cold_output/D0_D5.md` | `AMBIGUOUS_BASENAME` |
| `UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt` | 10 | `MANIFEST` | `stage1/arm_A/cold_output/UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md` | `AMBIGUOUS_BASENAME` |
| `cascade_bv10_reshoot.py` | 97 | `FILE_PATH` | `bv10_reshoot_results.npy` | `DYNAMIC` |
| `cascade_bv11_v1_root.py` | 48 | `FILE_PATH` | `bv11_fundamental_traj.npz` | `MISSING_OR_GENERATED` |
| `cascade_bv11_v1_root.py` | 50 | `FILE_PATH` | `{'dstar': dstar, 'astar': astar, 'suite100k': d100, 'suite200k': {k: d200[k] for k in d200 if k not ` | `DYNAMIC` |
| `cascade_bv11_v1_root.py` | 52 | `FILE_PATH` | `bv11_root.json` | `MISSING_OR_GENERATED` |
| `cascade_bv11_v1_scan.py` | 30 | `FILE_PATH` | `{'rows': rows, 'brackets': brs, 'shots': L.SHOTS['n']}` | `DYNAMIC` |
| `cascade_bv11_v1_scan.py` | 31 | `FILE_PATH` | `bv11_scan.json` | `MISSING_OR_GENERATED` |
| `tests/conftest.py` | 1 | `TEST` | `Shared fixtures/helpers for the P1 purity harness.\n\nAnti-hang: all tests are FORWARD residual/Eins` | `MISSING_OR_GENERATED` |
| `tests/test_branch_operator.py` | 34 | `TEST` | `A native-S^2 matter dn (the canon degree-1 winding n=x/r).` | `MISSING_OR_GENERATED` |
| `tests/test_hygiene_header.py` | 1 | `TEST` | `Structure hygiene — require HYGIENE HEADER on covered results docs.\n\nPhysics-blind: only checks th` | `MISSING_OR_GENERATED` |
| `tests/test_hygiene_header.py` | 17 | `TEST` | `__file__` | `DYNAMIC` |
| `tests/test_hygiene_header.py` | 21 | `TEST` | `simple_metric_*_results.md` | `DYNAMIC_OR_GLOB` |
| `tests/test_hygiene_header.py` | 22 | `TEST` | `simple_metric_*_results_*.md` | `DYNAMIC_OR_GLOB` |
| `tests/test_hygiene_header.py` | 23 | `TEST` | `lorentz_*_results.md` | `DYNAMIC_OR_GLOB` |
| `tests/test_hygiene_header.py` | 24 | `TEST` | `simple_metric_session_self_audit_*.md` | `DYNAMIC_OR_GLOB` |

## Interpretation limits

- `EXTERNAL_OR_STDLIB` is a static import classification, not proof that a package is installed.
- `MISSING_OR_GENERATED` often denotes an output path; it must be adjudicated before a move.
- `RESOLVED_BY_BASENAME` needs path normalization before relocation because the source did not name the full path.
- A dynamic expression is surfaced verbatim and never guessed.
- Markdown-link coverage does not convert plain prose references; exact root-name prose references are separate `TEXT_REFERENCE` edges.
