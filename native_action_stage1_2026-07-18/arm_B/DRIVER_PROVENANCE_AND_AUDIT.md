# Arm B — driver provenance and mechanical audit

**Stage:** I only. This record does not compare Arm B with Arm A and makes no physics ruling.

## Outer-run provenance

- Runner: OpenAI Codex CLI `0.144.5`
- Model: `gpt-5.4`
- Reasoning effort: `high`
- Session: `019f72f1-db2a-7ed0-9eac-b861d4f320ec`
- Outer transcript start: `2026-07-17T21:58:00-04:00`
- Arm-authored completion time: `2026-07-18T02:04:37Z`
- Outer transcript exit: `2026-07-17T22:04:50-04:00`, code `0`
- Cold output D0–D5 SHA-256: `07f9519049d0993d35dbbc68f86ffe1f7da1339e1eb888dbdfe90a75ac34ba68`
- Outer transcript SHA-256 before package manifesting:
  `dc5a4526b7bab08ce537a1baa29c9189609ab99f40d074a299a77da8e30c3004`

The model-visible D0 truthfully says that the platform did not expose an opaque API session ID or
run UUID inside the session. The outer transcript supplies the exact model and session metadata
above; the cold output has not been edited to retrofit it.

## Isolation evidence

- A fresh Bubblewrap mount namespace bound only the Arm B work directory at `/work`.
- The repository, controller dispatch, LIVE/HANDOFF, historical packet, other arm, and host temporary
  directories were absent from the arm's filesystem view.
- `/tmp` inside the namespace was a new private tmpfs, not host `/tmp`.
- The arm's initial inventory recorded exactly C0 and C1 and no other file.
- C0 SHA-256: `6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192`
- C1 SHA-256: `d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0`
- Web use was disabled. Provider connectivity existed only to run the model session.
- Bubblewrap exposed no host GPU device, and no GPU work ran.

The first network preflight failed before a model response because the namespace lacked its resolver
mount. Its complete transcript is preserved separately. The successful session began fresh after the
resolver mount was corrected; the preflight did not produce or alter cold output.

A proposed cross-provider Arm B launch was rejected before execution because third-party packet
transfer lacked explicit approval. No packet bytes were sent and no external Arm B session existed.
This separately isolated `gpt-5.4` session is the approved-provider fallback recorded before launch.

## Mechanical audit

- D0, D1, D2, D3, D4, and D5 are present once and in order; D1 MAP precedes D2.
- D0 contains both exact input hashes, a completion timestamp, initial inventory, and exposure
  declaration.
- Four standalone `cas_*.py` scripts have four matching nonempty `cas_*_out.txt` files.
- Every CAS script passed `python3 -m py_compile`, exited zero on a driver rerun, and reproduced its
  captured output byte-for-byte.
- D3 identifies what each script verifies and cannot verify.
- A mechanical prohibited-context scan found no repository/controller/Stage-II provenance leak in
  the arm-authored output.
- `final_response.md`, the complete successful outer transcript, and the complete failed-preflight
  transcript are present.

No mathematical adjudication, cross-arm agreement finding, Arm C run, Stage-II run, or GPU run was
performed as part of this audit.
