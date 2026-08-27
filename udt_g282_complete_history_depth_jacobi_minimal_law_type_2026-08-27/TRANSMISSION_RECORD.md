# G282 external-review transmission record

Date: 2026-08-27

## Authorized sealed intake

- intake: `/tmp/udt_g282_review_zo9gb8tc`
- physical files: 44
- manifest payloads: 42
- `REVIEW_SCOPE.json` SHA-256: `a9d9f9cc4aa491b6b7a8c6a0cc614381d7db34f7ff0cce9abf0849a089298114`
- `REVIEW_MANIFEST.tsv` SHA-256: `11d48a6adad9f0bcc54840ddc01b78067a0d31ac2f842d7c78a927611a6b1c4c`
- detached seal SHA-256: `edafc4a6035d30683c729d1abcd2a22f12d0c0abfb85cbcb669c659067de040e`

Charles explicitly authorized transmission to the external Codex reviewer (`gpt-5.4`) for fresh
read-only adversarial review. The reviewer could inspect only the sealed intake, run registered
no-write replays or bounded checks in a writable ephemeral copy, and could not edit evidence files
or continue the research.

## Isolation and return

- fresh reviewer session: `01a04481-0832-7d82-8cfc-193e48203dc3`
- runtime: `/tmp/udt_g282_external.VmvD1jS5`
- intake mounted read-only at `/intake`
- writable replay area mounted at `/work`
- writable return area mounted at `/return`
- repository and protected packages were not mounted
- web search was disabled
- raw final return SHA-256: `2c244ceb24fe6c5d0d66388e781c7ce50ba04b06c800c4c899e4ab48685d7a1a`
- complete transcript SHA-256: `b52eb934706b84c273176c700f3af00336528deacc0f9da9df84e4f7a99aeef6`

The output-file option replaced the detailed memo with the reviewer's short final return at process
exit. `EXTERNAL_REVIEW_RAW_RETURN.md` preserves that exact text with the repository's normal final
newline; the SHA-256 above belongs to the original 518-byte no-final-newline return. The reviewer-authored
detailed memo is preserved verbatim in `EXTERNAL_REVIEW_DETAILED_MEMO.md` from the complete hashed
transcript, where it appears as the written `/return/EXTERNAL_REVIEW_GPT54.md` patch and readback.

## Verdict

`ACCEPT-WITH-REPAIRS`

The reviewer accepted the bounded scientific landing, both mathematical witnesses, the frozen
18-source no-owner census, the retained coframe/connection alternative, and the no-import ledger.
It requested one certification repair: retype the seven `run_catch_proofs.py` catches as a schematic
claim-logic guard rather than an artifact-level mutation replay, unless the implementation is
actually upgraded to mutate and replay evidence artifacts.
