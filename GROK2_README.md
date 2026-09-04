# `grok2` branch isolation and role

This branch is the **external-auditor seat** for Charles's `grok` workstation.
It is not the driver. It does not canonize. It does not edit `CANON.md`.

Charles steers `grok`. A restarted session on `grok2` resumes as second-look:
pull `grok`, read its `LIVE.md` current block, report nativeness / stamps /
remainder, return here. Do not launch a derive, fit, GPU job, or G-tile unless
Charles explicitly asks.

## Isolation (do not break)

Shared names (`LIVE.md`, `HANDOFF.md`, `MEMORY.md`, `INDEX.md`, `CANON.md`,
`AGENTS.md`, `CLAUDE.md`, `CURRENT_SCIENTIFIC_PREMISES.*`) stay **byte-identical
to `origin/grok`** on this branch. Checking out or merging therefore cannot
overwrite the other workstation's orientation.

On `grok2`, read these unique files instead:

1. `GROK2_README.md` (this file)
2. `GROK2_LIVE.md` — current auditor claim (wins on this branch)
3. `GROK2_HANDOFF.md` — lean resume
4. `GROK2_STARTUP.md` — restart protocol
5. `GROK2_MEMORY.md`
6. `GROK2_INDEX.md`

New work on this branch goes only under uniquely named paths (`GROK2_*` or
`udt_session_dilation_skeleton_2026-08-14/`).

Do not merge `grok2` into `grok` unless Charles asks. A later merge should
only **add** these files.

The unbanked dilation skeleton in `udt_session_dilation_skeleton_2026-08-14/`
is background, not the live dispatch.
