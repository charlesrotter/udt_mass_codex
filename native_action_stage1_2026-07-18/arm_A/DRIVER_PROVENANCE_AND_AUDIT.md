# Arm A — driver provenance and mechanical audit

**Stage:** I only. This record does not compare Arm A with Arm B and makes no physics ruling.

## Outer-run provenance

- Runner: OpenAI Codex CLI `0.144.5`
- Model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Session: `019f72f1-8a16-7862-9573-d051361ae85f`
- Outer transcript start: `2026-07-17T21:57:39-04:00`
- Arm-authored completion time: `2026-07-18T02:10:54Z`
- Outer transcript exit: `2026-07-17T22:11:15-04:00`, code `0`
- Cold output D0–D5 SHA-256: `22804ff3c744b8857481908cd4cb7bc8775c67a158de58cf570c0fea924e4ddb`
- Outer transcript SHA-256 before package manifesting:
  `93c137b21c50f7f1126b2d3f8c939a56ce656f728cecdaa77b9d7a8bbe67a2fb`

The model-visible D0 truthfully says that the platform did not expose a more specific model build or
session identifier inside the session. The outer transcript supplies the exact runner metadata above;
the cold output has not been edited to retrofit it.

## Isolation evidence

- A fresh Bubblewrap mount namespace bound only the Arm A work directory at `/work`.
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

Arm A disclosed one literal prompt-scope deviation: its final self-check wrote and reread
`/tmp_check_output`. That path was in the namespace's private, initially empty tmpfs and contained
only fresh stdout from Arm A's own C0/C1-derived CAS scripts. It exposed no host file, project file,
other-arm output, or additional input. The deviation is retained verbatim in D0 and the transcript.
The driver therefore records it as noncontaminating but audit-visible; no Stage-II disclosure or cold
context entered the arm.

## Mechanical audit

- D0, D1, D2, D3, D4, and D5 are present once and in order; D1 MAP precedes D2.
- D0 contains both exact input hashes, a completion timestamp, initial inventory, and exposure
  declaration.
- Eleven standalone `cas_*.py` scripts have eleven matching nonempty `cas_*_out.txt` files.
- Every CAS script passed `python3 -m py_compile`, exited zero on a driver rerun, and reproduced its
  captured output byte-for-byte.
- D3 identifies what each script verifies and cannot verify.
- A mechanical prohibited-context scan found no repository/controller/Stage-II provenance leak in
  the arm-authored output.
- `final_response.md`, the complete successful outer transcript, and the complete failed-preflight
  transcript are present.

No mathematical adjudication, cross-arm agreement finding, Arm C run, Stage-II run, or GPU run was
performed as part of this audit.
