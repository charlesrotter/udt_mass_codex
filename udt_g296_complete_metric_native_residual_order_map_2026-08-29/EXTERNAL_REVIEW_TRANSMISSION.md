# G296 external-review transmission record

Date: 2026-08-29

Charles authorized transmission of the sealed 39-file intake at
`/tmp/udt_g296_review_2j5tinam` and read-only use of the local Codex authentication file solely to
launch the isolated external reviewer.

Integrity values:

- `REVIEW_SCOPE.json` SHA-256:
  `f1613ee254f994e706d6189aabc538ec43e708ac1653f50937dba5921548a245`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `ffe57f365f3a91232d2a6c6271cc62853899ee7641ce8081262e9126552ed0ed`
- detached seal SHA-256:
  `7a58ca9592bf2b60398e3a36d5c27fdf9f44369acffdd39240d99800441ea9e6`

The reviewer was launched with the intake and authentication file mounted read-only, web disabled,
the repository and protected packages absent, and only ephemeral `/work` and `/return` writable.
The reviewer returned `G296_ACCEPT_WITH_REPAIRS` and did not edit repository evidence or continue
the research.
