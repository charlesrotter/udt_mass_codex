# `grok2` branch isolation

This branch must **not** edit files that `grok` also owns.

Shared names (`LIVE.md`, `HANDOFF.md`, `MEMORY.md`, `INDEX.md`, `CANON.md`,
`AGENTS.md`, `CLAUDE.md`, `CURRENT_SCIENTIFIC_PREMISES.*`) stay **byte-identical
to `origin/grok`** on this branch. Checking out or merging therefore cannot
overwrite the other workstation's orientation.

On `grok2`, read these unique files instead:

1. `GROK2_README.md` (this file)
2. `GROK2_LIVE.md`
3. `GROK2_HANDOFF.md`
4. `GROK2_STARTUP.md`
5. `GROK2_MEMORY.md`
6. `GROK2_INDEX.md`
7. `udt_session_dilation_skeleton_2026-08-14/`

New work on this branch goes only under uniquely named paths
(`GROK2_*` or `udt_session_dilation_skeleton_2026-08-14/`).

Do not merge `grok2` into `grok` unless Charles asks. A later merge should
only **add** these files.
