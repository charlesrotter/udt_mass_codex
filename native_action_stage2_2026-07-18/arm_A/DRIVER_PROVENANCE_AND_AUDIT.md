# Arm A — Stage-II driver provenance and mechanical audit

**Stage:** II challenge addendum only. This record does not compare Arm A with Arm B and makes no
physics ruling.

## Outer-run provenance

- Runner: OpenAI Codex CLI `0.144.5`
- Model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Session: `019f74fe-5ca5-7860-9918-bc1c499b1897`
- Outer transcript start: `2026-07-18T07:30:53-04:00`
- Arm-authored D6 completion time: `2026-07-18T11:52:01Z`
- Outer transcript exit: `2026-07-18T07:52:08-04:00`, code `0`
- Stage-I external manifest hash:
  `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19`
- A1–A6 manifest hash:
  `85776969410e6dc8bee6b1aa901331dcc139e718dbdfd28c593df3f2054408b7`
- D6 SHA-256: `3380ace0a38f46eaff2401213cab12aa13750be1df38f61211435caf73d6bd93`
- Launch prompt SHA-256: `e0ca11ae3011d321a4b8598a2848329e4997b434e79796c450aaf5fd63c8349d`
- Launch script SHA-256: `f93face54d32cdaa22786d890ee99d6f74d4b8d99badeb8dfadc4fc95eb569ad`
- Outer transcript SHA-256 before package manifesting:
  `a9e137093369780c3072ef2d30c36deeafcca4d317bba21b8267600d0b3f9ffd`

The model-visible D6 truthfully says that the isolated session did not expose a more specific model
or session identifier. The outer transcript supplies the exact runner metadata above; D6 was not
edited to retrofit it.

## Isolation and disclosure evidence

- A fresh Bubblewrap namespace mounted only Arm A's frozen Stage-I package read-only at `/stage1`,
  the exact A1–A6 packet read-only at `/packet`, and its initially empty writable `/return` as project
  material. The repository, controller, other arm, LIVE/HANDOFF, and host temporary files were absent.
- `/tmp` inside the namespace was a private tmpfs. The ephemeral `/home` contained runner state and
  authentication only, no project record; the arm did not inspect it.
- The received manifest is byte-identical to
  `UDT_NATIVE_ACTION_STAGE2_A1_A6_SHA256SUMS_2026-07-18.txt`: 134 files, no symlinks, manifest hash
  `85776969410e6dc8bee6b1aa901331dcc139e718dbdfd28c593df3f2054408b7`.
- The arm verified its Stage-I manifest before historical review and read its own D0–D5 before A1–A6.
- Web search was disabled. Provider connectivity existed only to run the model session. Bubblewrap
  exposed no host GPU device, and no GPU work ran.

The first launch attempt failed before a model response because the current CLI no longer accepted
the preregistered `-a never` shorthand. Its complete transcript is preserved separately. The launcher
was changed only to the current noninteractive CLI flag; mounts, prompt, model, and disclosure packet
were unchanged, and the successful return directory was still empty at launch.

## Mechanical audit

- `D6.md`, the received manifest, final response, two standalone `cas_stage2_*.py` scripts, and two
  matching captured outputs are present.
- `D6_DISCLOSURE_CENSUS.tsv` has one header plus exactly 134 data rows, seven tab-separated fields on
  every row, 134 unique paths, and a path set exactly equal to the A1–A6 manifest.
- Every census disposition is one of `SURVIVING`, `CONDITIONAL`, `OPEN`, `SUPERSEDED`,
  `ALGEBRA-ONLY`, or `OUT-OF-SCOPE`.
- D6 contains the required provenance, disclosure map, own-result classifications,
  carrier-covariance route, three distinct mass/virial statements, revision ledger, algebra limits,
  and self-audit. It retains the `-2.7%` finite-box fact, supersedes the old `0.05%` match, and keeps
  the boundary theorem and infinite-volume closure open.
- Both Stage-II scripts compile, exit zero on a fresh driver rerun, and reproduce their captured
  outputs byte-for-byte. No placeholders remain.
- A prohibited-context scan found only the arm's explicit negative exposure declarations and script
  shebangs; no unenumerated project content appears in the return.
- The complete outer transcript exits zero. `final_response.md` lists every final return file.
- The original Stage-I manifest still passes for all 29 entries and the entire Stage-I package has no
  writable entry.

The census uses the collective label `A1-A5 leading set` for the nine leading paths because the
model-visible prompt supplied their exact order but not the per-file subgroup mapping. The path-level
census is exact; the controller enumeration remains preserved in the launch and return records.

No cross-arm comparison, mathematical adjudication, Arm C run, GPU run, or repository reorganization
was performed as part of this audit.
