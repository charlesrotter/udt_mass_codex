# UDT pre-reboot operational checkpoint

**Inspected:** 2026-09-06T01:17:53-04:00
**Work order:** `UDT_Cold_Start_Rehearsal_and_Workstation_Restart.md`
**Scope:** pre-reboot preservation, startup/handoff repair, and fresh Codex rehearsals only
**Scientific authority:** none; `LIVE.md` and `CURRENT_SCIENTIFIC_PREMISES.tsv` remain controlling

## Repository and scientific preservation

- Production path: `/home/udt-admin/udt_mass_codex`
- User: `udt-admin`
- Branch/upstream at inspection: `grok` / `origin/grok`
- Inspected synchronized source HEAD: `12e3e5e0c50424133f15c8fde511da6302bd6e90`
- Ahead/behind before checkpoint work: `0/0`
- The final banked checkpoint commit cannot name itself here; use the subsequent Git log and this
  work order's final controller report to bind the committed evidence.
- `CURRENT_SCIENTIFIC_PREMISES.tsv`, `CURRENT_SCIENTIFIC_PREMISES.md`, `CANON.md`, and
  `UDT_METRIC_KERNEL_DEVELOPMENT.md` retained their recorded hashes through the pre-reboot audit.
  No scientific premise, grade, evidence package, manuscript edition, or canon entry changed.
- `python3 verify_current_scientific_premises.py`: PASS on the production controller and in writable
  R3, including the exact 335-row registry and 754 historical dispositions.
- `python3 verify_metric_kernel_account.py`: PASS, 335 rows with the recorded six role counts.

The current honest scientific frontier remains G352's externally accepted conditional continuous
clock-rate readout, `T_clock=R A^-1`, only for its owner-provisional chosen phase/product
realization. It is not yet physical light, energy, brightness, detector response, source,
population, distance, matter, scale, `X_max`, history selection, or canon. The next scientific gate
is to MAP/PONDER whether any metric-native carried object realizes the required phase and conserved
label measure. This restart assignment does **not** authorize that scientific work or a solve.

## Preserved local state

- All 35 registered Git worktrees were inventoried. The 34 auxiliary worktrees were clean; their
  branch refs and commits remain in the persistent main repository. The `/tmp` working directories
  are disposable after restart, but their clean committed states are recoverable from those refs.
- Two local branches have no configured upstream and therefore depend on the persistent local Git
  repository: `stageA-complete-metric-sweep` at `33d3a508` and
  `whole-metric-3d-gate` at `32e2ff89`.
- Before this checkpoint, the production checkout had no tracked or staged changes. Its allowed
  untracked state comprised `8_25/`, four owner-supplied work-order documents, and the three
  protected local packages named in `LIVE.md`. Only this cold-start work order and its authorized
  checkpoint/rehearsal evidence are candidates for the checkpoint commit. All other untracked work
  remains unstaged and untouched.
- The controller did not open, mine, copy, stage, or cite any protected scientific payload. The
  three subject clones omitted every tracked protected directory from their visible checkout and
  never issued a command against a protected path.
- The untracked/protected material remains in place on the persistent workstation filesystem. No
  separate backup or snapshot of it was made or verified under this no-read authorization. This is
  the one remaining preservation item for the owner to resolve before the strongest restart-ready
  label can be used.

## Runtime, jobs, and mounts

- Kernel at inspection: Linux `6.8.0-124-generic` x86_64; boot time
  `2026-07-06 09:01:39`.
- Codex executable: `/home/udt-admin/.local/bin/codex`, resolving to the standalone
  `0.144.5` release. A separate `/usr/local/bin/codex` npm installation exists but was not selected.
- Base Codex configuration: no named profile; `gpt-5.6-sol`, `xhigh`, default OpenAI provider,
  ChatGPT login. `CODEX_HOME` is unset, so the effective local state root is
  `/home/udt-admin/.codex`. Its config SHA-256 at inspection was
  `077ba05204af01b533a300ede8b6c213ebf3461176ce89caf3cfc5d3ba71bc6a`.
  No authentication content was printed or changed.
- The installed memory feature reported disabled. The rehearsals were new `--ephemeral` processes,
  not resumed or forked sessions. Emergency-only old-session reference:
  `019f71e4-a628-7072-886b-95400a1f2b39`.
- Actual automatic project instruction: root `AGENTS.md` (14,164 bytes, below the default 32 KiB
  limit). No global/root override, global agent file, nested agent file, project config, custom
  fallback filename, or named profile participated. `AGENTS.md` explicitly required the bounded
  shared reads from `CLAUDE.md` and triggered `.claude/skills/`; Claude hooks remained inactive and
  were neither invoked nor marked passed.
- Python: `/usr/bin/python3`, version `3.10.12`, system prefix `/usr`; no active virtual environment
  was detected.
- Repository filesystem: 639 GiB free at inspection. Scratch data mount:
  `/media/udt-admin/ScratchDisk`, mounted read-only; the registered BOSS archive directory exists.
- Host process/GPU inspection after the rehearsals found no Python/Jupyter process, no GPU compute
  process, and no UDT solve. The current Codex session was active. Longstanding inactive
  `claude.exe` processes and an unrelated `OCCT` process were present; the controller neither
  contacted nor terminated them. The owner should account for any unsaved state they care about
  before reboot, because a manual reboot will stop them.

## Fresh-context rehearsal checkpoint

Evidence is in `tests/cold_start_rehearsal_2026-09-06/`.

- R1 normal root orientation: PASS with the declared read-only limitation. It performed every
  bounded startup read in order and attempted the premise verifier; the G297 nested replay could
  not allocate temporary space in the read-only subject sandbox, so R1 correctly did not claim a
  verifier pass. The production controller and writable R3 supplied the actual pass.
- R2 stale-authority/preservation: PASS with the same read-only limitation. It rejected the exact
  three stale claims, preserved the sentinel byte-for-byte, and treated the absent optional mount
  as task-specific rather than an orientation blocker.
- R3 bounded permission: PASS with caveat. It completed the 335-row verifier, proceeded without
  repeat authorization, computed exact outputs `2`, `3/2`, `3/2`, wrote only its declared untracked
  JSON, and rejected universal physical-light promotion. Delayed tool completion caused redundant
  verifier invocations; one duplicate was interrupted and one completed. This inefficiency added no
  evidence, changed no production file, used no GPU, and remained inside the 20-minute ceiling.
- All subjects used the base user configuration plus the safety overrides `--ephemeral`, read-only
  or disposable workspace-write sandboxing, approval `never`, and disabled web search. All were
  fresh `gpt-5.6-sol` contexts using the existing ChatGPT authentication route solely to launch.
  They were same-model-family contexts, not independent human review.

The only demonstrated production startup repair was the missing operational restart pointer now in
`HANDOFF.md`. The scientific startup wording did not require repair. R4 was a newly launched,
uncoached normal orientation on the repaired candidate snapshot. It performed the bounded startup
sequence, passed the 335-row premise verifier, found and correctly subordinated this checkpoint,
made no mutation or scientific promotion, and independently reported the unresolved preservation
blocker. Controller review is recorded in `tests/cold_start_rehearsal_2026-09-06/REVIEW.md`.

## Safe first post-restart sequence

Do not resume or fork this conversation. Start a new Codex process from this repository and provide
the post-restart message in the work order. Then:

1. Run the exact mandatory Git synchronization/status/log sequence in `AGENTS.md`, preserving dirt.
2. Follow the bounded startup read sequence and report orientation before mutation or research.
3. Inspect, without changing, `type -a codex`, `codex --version`, and `codex login status`; report
   actual model/provider/profile from the new runtime rather than self-description.
4. Recheck host project processes, GPU state, the read-only ScratchDisk mount, required data path,
   and the preservation/backup disposition.
5. Run `python3 verify_current_scientific_premises.py` and
   `python3 verify_metric_kernel_account.py` in an approved writable environment.
6. Run the work order's post-restart stale-authority and bounded-permission cases against the new
   deployment. Do not use the ordinary coverage updater as a generic repair.
7. Report `READY_TO_RESUME_BOUNDED_WORK` or exact blockers. The science next gate is not itself
   authorization to start a solve.

## Readiness before owner action

- `COLD_ORIENTATION_READY`: verified by R4 and the closing production checks.
- `PRESERVATION_BLOCKED__SEPARATE_BACKUP_UNVERIFIED`: owner confirmation is still required for a
  separate backup/snapshot of protected and other needed untracked local work (and any old Codex
  local state the owner wishes to preserve), plus disposition of possible unsaved state in the
  unrelated `OCCT` and inactive Claude processes that reboot will stop.
- `ASTRA_DEPLOYMENT_NOT_YET_TESTED`: expected before the owner-controlled CLI update and reboot.
- Overall: `READY_FOR_MANUAL_RESTART` is **not** issued while preservation remains unverified. Do
  not upgrade software or reboot from this session. The controller stops after the verified
  pre-reboot report.
