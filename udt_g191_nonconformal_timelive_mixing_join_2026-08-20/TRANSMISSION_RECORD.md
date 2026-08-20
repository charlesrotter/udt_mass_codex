# G191 external-review transmission record

Date: 2026-08-20

## First authorized intake

- intake: `/tmp/udt_g191_review_e1g5k7b2`
- total files: `30`
- `REVIEW_SCOPE.json` SHA-256:
  `527ae85a7be70da6c0af711491b1394b5d4e7dc5f785fcc490a8315894503185`
- sealed tree SHA-256:
  `933ef2c3b0cca424a5ee567e57d8d1c952bf4746671ad452f06f96fcbb6e0f07`
- reviewer: external Codex `gpt-5.4`, high reasoning
- sandbox: read-only
- internet: disabled
- restrictions: inspect only the intake; run only the registered no-write replay; do not edit
  files; do not continue the research

The declared payload hashes, total file count, and tree digest were rechecked after the review and
remained byte-identical.

## First-review result

- process exit code: `0`
- primary grade: `G191_REPAIR_REQUIRED`
- scientific formula repair: none forced
- blocking defect: the sealed source layout and package verifier paths made the authorized
  no-write replay non-self-contained

The reviewer reported that the cached sealed scientific artifacts were internally consistent, but
correctly refused acceptance until the same replay finishes end-to-end inside a corrected intake.

## Preserved first-review evidence

- verbatim final message: `EXTERNAL_REVIEW_RAW.md`
  - SHA-256: `2b25e78856decb8cbdf1a4d8a56d44aa4dbb844d2f261bb04f140afc13ce871d`
- raw terminal transcript before compression:
  - SHA-256: `f16bb1b12e92c85735242e2f4970ac000d8294dc744ab8c6b8db6b46ba2d6381`
- deterministic gzip transcript: `EXTERNAL_REVIEW_TRANSCRIPT.txt.gz`
  - SHA-256: `9400170f7786dbc714f953e9c31da04eee5d527bddf135757bf7dbd32aa75776`

## Corrected repair-only follow-up

- intake: `/tmp/udt_g191_review_cm9ezs6t`
- total files: `36`
- `REVIEW_SCOPE.json` SHA-256:
  `a5ff51e34888e35a51391e4fc90fdcd824cadfb64532f32ac45a285e442e1a10`
- sealed tree SHA-256:
  `bf4856edb5fa06947fb0d4cb2c40de510d2ecff416c73b3d5dd9c6305bd21ec8`
- registered no-write replay: `PASS`
- payload and tree identity after review: `PASS`
- primary grade: `G191_ACCEPTED_WITH_STATED_BOUNDS`
- remaining repair: none within the preregistered packaging scope

The reviewer recovered the first-intake hashes from the preserved transcript and confirmed that
`PRODUCTION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, and `CATCH_PROOF_RESULT.json` were
byte-identical across the repair. The premise/status ledgers and audit report were also unchanged.

## Preserved follow-up evidence

- verbatim final message: `EXTERNAL_FOLLOWUP_REVIEW_RAW.md`
  - SHA-256: `048063b93a63db1e8147bc639a7723a992e4289ebb147dceab7dafca22edab3e`
- raw terminal transcript before compression:
  - SHA-256: `9ec4e0c44211b504a17639300388aafd08a9cf0cb780fc46f96af375a9d1a126`
- deterministic gzip transcript: `EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt.gz`
  - SHA-256: `9e18372cdde90f7927fd1e3b71f7aacbb05b545fe7dab7a9639658e891bd8a0a`

After acceptance, banking G191 added its exact premise row to the current registry and therefore
refreshed the registry hash in `SOURCE_MANIFEST.tsv`. This is post-review authority routing only.
The three reviewed scientific artifact hashes remain exactly the values verified above.
