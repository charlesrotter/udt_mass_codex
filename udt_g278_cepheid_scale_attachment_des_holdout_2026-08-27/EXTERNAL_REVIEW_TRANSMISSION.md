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
