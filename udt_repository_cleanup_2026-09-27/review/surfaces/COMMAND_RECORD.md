# Commands and read depth

Commands were run from `/home/udt-admin/udt_mass_codex`; no scientific subprocess was launched. The tool transcript records their raw output. Repository artifacts here retain the independently checked metadata and classifications.

- `git status --short --branch`, `git rev-parse HEAD`, `cat AGENTS.md`.
- Bounded LIVE marker extraction initially failed; corrected with `sed -n '3,113p' LIVE.md`.
- `sed -n '9,83p' CLAUDE.md`; `sed -n '121,151p' CLAUDE.md`.
- `cat .claude/skills/completeness-map/SKILL.md .claude/skills/verifier-before-record/SKILL.md` and cleanup `WORK_ORDER.md`.
- `git ls-files -z`, filtering exact root paths only; `Path.stat()` gave candidate byte sizes.
- Every `FULL_PROSE` row in SURFACE_CLASSIFICATION was read with `cat` (some batched), except README/INDEX/MEMORY jointly read as navigation. The two truncated fidelity receipt displays were repeated individually.
- `sed -n '1,55p' PONDER_MATH_ELEGANCE_2026-07-31.md`.
- The eight `FIRST_14_LINES_AND_LITERAL_CONSUMERS` rows were read with `Path.read_text().splitlines()[:14]` and emitted for scope classification only; implementation did not emit or interpret remaining text.
- Literal metadata search: `git grep -n -I -F -f <candidate-name-file> -- .` with four explicit `:(exclude)<protected-directory>/**` pathspecs. Machine output kept only candidate/consumer/line and is in the two LITERAL_CONSUMERS tables.
- Known candidate paths only were matched to CSV-parsed `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`; rows saved as KNOWN_PATH_LEDGER_ROWS.tsv. No full ledger entered model context.
- Table correspondence checks used `git show 8aac11e13a2311347771e11f507f4f2042ea02a2:<path>`, SHA-256, `git rev-parse <baseline>:<path>`, and direct byte equality to each working file. Only declared90 nonprotected tracked paths were hashed.
- Final metadata: `git status --short --branch --untracked-files=all`, `git rev-parse HEAD`, `git diff --name-status`.

The parent performed synchronization and baseline premise verification. This reviewer did not claim those as independent reruns, did not run any inherited launch recipe, and did not inspect unrelated untracked payloads.
