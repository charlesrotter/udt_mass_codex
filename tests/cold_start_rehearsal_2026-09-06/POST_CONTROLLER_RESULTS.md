# Executed controller checks — post-restart 2026-09-06

Scope: operational restart acceptance, not scientific review or adoption.
Source HEAD at execution: `76a8d249d96082b36e02ee65b0d3677ad26a080d`.
Raw narrow runtime/Git/host evidence is in `POST_CONTROLLER_CHECKS.json`.
The results below transcribe this fresh controller's tool results; they are
not copied pre-reboot pass counts. The current controller session is
`01a076f6-afa1-7411-87e7-82a25d358913`; only its runtime metadata was inspected,
not the old scientific conversation.

## Synchronization and preservation

Executed the mandatory sequence in order: `git status --short --branch`,
`git checkout grok`, `git fetch origin`, `git pull --ff-only origin grok`,
`git status --short --branch`, `git log -8 --oneline`.

The initial sandbox fetch failed with `cannot open .git/FETCH_HEAD: Read-only
file system`. An authorized automatically reviewed host fetch succeeded;
the fast-forward-only pull reported `Already up to date`. HEAD and
`origin/grok` both resolved to the source above; ahead/behind was `0/0`.
Tracked and staged changes were absent. Initial status had 46 untracked
entries: `8_25/`, three other owner work orders, and payload filenames in the
three protected packages. No protected payload was opened or hashed.

All 35 registered worktree commits exist and all 35 recorded branch refs
still match. Two working directories remain: production and the clean
`.claude/worktrees/p4-routeB`. The other 33 `/tmp` directories are absent;
their registrations were not pruned. Both upstream-less branches survive:
`stageA-complete-metric-sweep` at `33d3a508c49d7c8c84e397a0ccbb06e486a1d759`
and `whole-metric-3d-gate` at `32e2ff892edba8bef40b4dc98bf501df3f705601`.
All four protected directory paths are present. Directory presence does not
establish protected payload integrity, completeness, or backup recovery.

## Actual checks

`python3 verify_current_scientific_premises.py` completed with exit 0:

```text
PASS: G242/G243/G244/G245/G246/G247/G248/G249/G250/G251/G252/G253/G254/G255/G256/G257/G258/G259/G260/G261/G262/G263/G264/G265/G266/G267/G268/G269/G270/G271/G272/G273/G274/W5/G275/G276/G277/G278/G279/G280/G281/G282/G283/G284/G285/G286/G287/G288/G289/G290/G291/G292/G293/G294/W6/G295/G296/G297/G298/G299/G300/G301/G302/G303/G304/G305/G306/G307/G308/G309/G310/G311/G312/G313/G314/G315/G316/G317/G318/G319/G320/G321/G322/G323/G324/G325/G326/G327/G328/G329/G330/G331/G332/G333/G334/G335/G336/G337/G338/G339/G340/G341/G342/G343/G344/G345/G346/G347/G348/G349/G350/G351/G352 startup and premise guards; PASS: 335-row premise registry, current bounded startup route, archive integrity, relational-depth/orchestra guards, X_max semantics, 754 historical dispositions, and corrected DOF semantics
```

`python3 verify_metric_kernel_account.py` completed with exit 0:

```text
PASS metric-kernel account: 335 rows; roles={'BOUNDARY_RESULT': 76, 'CONTROL_ONLY': 57, 'MAIN_ARGUMENT': 65, 'OUTSIDE_SCOPE': 12, 'SUPERSEDED_HISTORICAL': 2, 'SUPPORTING_LEMMA': 123}
```

Executed:

```text
python3 -m pytest tests/test_startup_surface.py tests/test_guardrail_policy.py tests/test_metric_kernel_account.py -q -k 'not test_full_foundational_premise_verifier_is_in_pytest' -p no:cacheprovider
85 passed, 1 deselected in 1.01s
```

The deselected test duplicates the full verifier already executed above.
The account source-invalidation regression ran its ordinary updater and
simulated review only inside its existing isolated temporary fixture. No
production updater was run. Relevant test fixtures/imports and the account
verifier's nonwriting path were inspected; the premise verifier performs
saved-package replays and creates temporary scratch. It is not a new solve.
Its existing aggregate verification does not independently re-prove all
accepted science.

All 13 entries in `REPAIRED_SOURCE_HASHES.sha256` matched. Additional hashes:

| Record | SHA-256 |
|---|---|
| CANON.md | `047b7fbbc1acacf01d2716e3c98cdefd0b9b20136ac4a3306f55dd6775465250` |
| UDT_METRIC_KERNEL_DEVELOPMENT.md | `3b625d8f43620a37c99d9f4f0fdc9390c3a12306b1da87281c143ce84d40a81e` |
| UDT_METRIC_KERNEL_COVERAGE.tsv | `b9a8d84d58b60dd6381af6512d89a63c8fa26750f0068e444dd039d329e74bc4` |

These match the saved completion record. Hashes establish correspondence,
not scientific truth or an independent review. `git diff --check` passed.

## Runtime and environment

`type -a codex`, `readlink -f`, `codex --version`, `codex login status`,
`codex features list`, installed help, current-session metadata, and host
`/proc/5687/exe` agree: standalone Codex 0.153.4 is selected at
`/home/udt-admin/.local/bin/codex`. The separate `/usr/local/bin/codex`
installation is not selected. The old checkpoint recorded 0.144.5.
Current configuration and turn metadata both select `gpt-6-astra`, `xhigh`,
OpenAI provider; no profile argument or profile setting was found. ChatGPT
login is active. No credentials were printed or changed.

Base config SHA-256 before the subjects was
`98bc63e1d1443e0944bd4e896125deda4c4c9705e65ab9221edf3924fa067b47`;
the checkpoint's earlier config hash was
`077ba05204af01b533a300ede8b6c213ebf3461176ce89caf3cfc5d3ba71bc6a`.
After subject launch the hash is
`c6e7b59e42df903baad68727d7bdd1ede9dc833147d415bf86400e4188eddb1a`.
The only byte changes are two project `trust_level = "trusted"` blocks for
the disposable R2/R3 clone paths. Removing those exact blocks in memory
reproduced the pre-subject hash; the disk config was not rewritten by this
comparison. Model, reasoning, provider, and all other prior configuration
bytes are unchanged. These launch-related local-state additions are
disclosed and retained; configuration is not claimed byte-identical across
the trials. No manual config/authentication change was performed.
`CODEX_HOME` is unset in the command environment; runtime files are in
`/home/udt-admin/.codex`. Memory and external-agent-memory-import features
report disabled. Current thread metadata has no fork parent and starts
after the new host boot. No resume/fork command was executed.

Host boot: `2026-09-06 09:43:01`; kernel `6.8.0-138-generic`.
User/workspace: `udt-admin`, `/home/udt-admin/udt_mass_codex`.
Python remains `/usr/bin/python3.10`, Python 3.10.12, without an active
virtual/Conda environment in the inspected command context.

Initial sandbox process/GPU/mount queries were insufficient: process
visibility was isolated and NVIDIA access failed. Approved read-only host
checks found a Tesla V100-PCIE-32GB, 32768 MiB total, 4 MiB used, 0% GPU
utilization and no compute process. Only this controller and its explicitly
launched verifier/rehearsal descendants appeared in the project-relevant
process inventory; no UDT scientific solve, Jupyter, OCCT, or Claude process
was found in that inventory. This is a point-in-time check, not continuous
monitoring or proof of the disposition of pre-reboot unsaved state.

ScratchDisk is detected as the 3.6 TiB ext4 partition `/dev/nvme1n1p1`, but is
unmounted. The registered BOSS archive path is unavailable. No mount action
was attempted. A separate USB volume is mounted; its contents were not
inspected and it is not thereby a verified backup. Repository free space
was approximately 703 GiB. Optional external data absence does not block
these repository/CPU checks.

## Instructions and limits

The actual current session's automatic user-instruction block was compared
programmatically with disk: full stripped-text match, 14,164 bytes on disk,
including the tail. No global/root override, active nested instruction,
project config, custom instruction-file/fallback, or named profile was
found on the inspected launch path. The default documented project limit
is 32 KiB; no configured override was found. See the
[official instruction-discovery documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Explicit reads: disk AGENTS.md; only current LIVE/HANDOFF blocks; current
research program; premise guide and required verifier; CLAUDE.md How we
work, DRIVER TRIGGERS, Repo discipline (plus its compact orientation);
triggered completeness-map and verifier-before-record skills; INDEX and
MEMORY; orientation report; then this work order, restart checkpoint and
load-bearing operational/test records. OpenAI Docs was used for narrow
configuration/instruction-loading verification, with official documentation.
No scientific premise came from a skill. Claude hooks remain inactive and
live Claude testing is not applicable.

Runtime system/developer instructions and the installed skill/plugin catalog
also participated. Official web documentation was consulted after orientation
for operational facts; therefore this controller is an as-deployed fresh
session, not a pure repository-only isolation trial. No prior conversation
or memory summary was used as scientific authority. Managed execution uses
restricted workspace writes and automatic review for necessary host checks;
the launch turn metadata itself records on-request/workspace-write. These
are recorded separately rather than assuming configuration alone describes
every effective permission layer.

Omitted: full historical scientific re-review, all unrelated test suites,
live Claude hooks, payload hashing/copying, full backup restore, external
dataset contents, GPU computation, software/authentication changes, mount
changes, and a new scientific solve. None is silently labeled passed.
