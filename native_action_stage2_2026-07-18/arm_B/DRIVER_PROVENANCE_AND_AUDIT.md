# Arm B — Stage-II driver provenance and mechanical audit

**Stage:** II challenge addendum only. This record does not compare Arm B with Arm A and makes no
physics ruling.

## Outer-run provenance

- Runner: OpenAI Codex CLI `0.144.5`
- Model: `gpt-5.4`
- Reasoning effort: `high`
- Session: `019f74fe-4478-7e01-9ea0-81beddef6df7`
- Outer transcript start: `2026-07-18T07:30:47-04:00`
- Arm-recorded addendum timestamp: `2026-07-18T11:38:51Z`
- Outer transcript exit: `2026-07-18T07:44:29-04:00`, code `0`
- Stage-I external manifest hash:
  `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92`
- A1–A6 manifest hash:
  `85776969410e6dc8bee6b1aa901331dcc139e718dbdfd28c593df3f2054408b7`
- D6 SHA-256: `8675e851e9f39f9a60130fbffc9522a1ce01a3728db8a29a54095bdef7bd9d2a`
- Launch prompt SHA-256: `8ba485a7041455694f5ec64fba307a66a6874d89a6efc50a9dce745a4a573426`
- Launch script SHA-256: `a5e57830403805980541bd3da3ba1c2c8d447bef4a4f6e9d50b47c716fd6e7f5`
- Outer transcript SHA-256 before package manifesting:
  `e56c5196e6aaf23da82dcf6a8acf17d2bcfb3921e4b19612dfc3f6c96bd34172`

The model-visible D6 truthfully says that the isolated session did not expose a more specific model
or session identifier. The outer transcript supplies the exact runner metadata above; D6 was not
edited to retrofit it. The D6 timestamp was captured when output assembly began, so the outer
transcript exit is the authoritative completion time; this audit-visible label issue does not alter
the return.

## Isolation and disclosure evidence

- A separate fresh Bubblewrap namespace mounted only Arm B's frozen Stage-I package read-only at
  `/stage1`, the exact A1–A6 packet read-only at `/packet`, and its initially empty writable `/return`
  as project material. The repository, controller, other arm, LIVE/HANDOFF, and host temporary files
  were absent.
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
  and self-audit. It explicitly audits the illustrative Stage-I `S_rel`/`S_fol` signature,
  action/energy sign, ordered-index factor, stress convention, static reduction, coefficient mapping,
  and countermodel status without editing D0–D5.
- Both Stage-II scripts compile, exit zero on a fresh driver rerun, and reproduce their captured
  outputs byte-for-byte. No placeholders remain.
- A prohibited-context scan found only the arm's explicit negative exposure declarations and script
  shebangs; no unenumerated project content appears in the return.
- The complete outer transcript exits zero. `final_response.md` lists every final return file.
- The original Stage-I manifest still passes for all 15 entries and the entire Stage-I package has no
  writable entry.

The census uses the collective label `A1-A5` for the nine leading paths because the model-visible
prompt supplied their exact order but not the per-file subgroup mapping. The path-level census is
exact; the controller enumeration remains preserved in the launch and return records.

No cross-arm comparison, mathematical adjudication, Arm C run, GPU run, or repository reorganization
was performed as part of this audit.
