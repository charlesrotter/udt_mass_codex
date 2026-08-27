# G278 external-review transmission record

Date: 2026-08-27

## Authorized intake

- intake: `/tmp/udt_g278_review_k5kl2ds_`
- physical file count: `48`
- manifest payload rows: `47`
- `REVIEW_SCOPE.json` SHA-256:
  `a66da444c9be988cb7560470cc719a81826c36ed4b97bc6369cc42a08c732555`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `03772e058a2009bd0a94786e199032df130b8e79626f4c524915027402ea7e29`

Charles authorized transmission to external Codex `gpt-5.4` for fresh read-only adversarial review.
The reviewer was restricted to the sealed intake, registered replays or bounded checks in a writable
ephemeral copy, and was forbidden to edit evidence files or continue the research.

## Execution

- model: `gpt-5.4`
- reasoning effort: `high`
- web search: disabled
- intake sandbox: read-only
- fresh session id: `01a0433b-4953-7cb1-8e25-82c3e2893ed1`
- raw response: `/tmp/udt_g278_external_runtime_lzB8wx/work/final_response.md`
- raw response SHA-256:
  `33f115f9820fa8f536da4216d0fd04268cdb12c8439dbbfbca48eb015ac14178`
- transcript: `/tmp/udt_g278_external_transcript_z0MlD2.txt`

## Return

Verdict: `ACCEPT-WITH-REPAIRS`

The reviewer independently reproduced the primary scale, resolution failure, calibrator-subset
controls, serialization control, DES no-retuning score, hostile controls, shared-data covariance,
and Pantheon-to-DES uncertainty propagation. It found no scientific regrade and requested three
sealed-package repairs: correct the copied source layout, add an outer/detached manifest seal, and
remove or include the unavailable repository premise-verifier command.

Scientific conclusion changes: none.

## Repair-only follow-up

- intake: `/tmp/udt_g278_review_41nmmnpj`
- physical file count: `53`
- manifest payload rows: `51`
- `REVIEW_SCOPE.json` SHA-256:
  `886f5ccddc871faa5ebec03878dfd844253a106dc25247ce8816e9583f2cea63`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `3ac5ff91435eb4c8fcb8b87db45c1cc41c59475bacb1a25085c7b56620fce864`
- `REVIEW_MANIFEST.sha256` SHA-256:
  `e924a6c1ec98be9542c88c0b5246d3a49aaffa3ec0e97a560ce0130e9f70bf0c`
- fresh session id: `01a04355-6204-7a41-86da-17f9e0897b0f`
- raw response: `/tmp/udt_g278_followup_runtime_FFCjwo/work/final_response.md`
- raw response SHA-256:
  `1a17543f1c74ea3818f8b1f91c23ee2fccca136721d0f027f34721e1e99d0d53`
- transcript: `/tmp/udt_g278_followup_transcript_hAKpI1.txt`
- verdict: `ACCEPT`

The follow-up verified R1--R3, all five registered replays, and the unchanged bounded scientific
landing. Remaining repair defects: none.
