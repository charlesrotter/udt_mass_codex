# G181 external transmission record

Date: 2026-08-19

- Authorization: explicit user authorization for the exact sealed intake and the previously
  authorized read-only authentication-file mount.
- Intake: `/tmp/udt_g181_endpoint_review_q8382u0j`.
- Total files: 28 (27 payloads plus `REVIEW_SCOPE.json`).
- Scope SHA-256:
  `9400b62615361814425617919bd7a0564fe6571a6aa3dfdd0032c8b3e8958524`.
- Restrictions: intake only; read-only; no edits or research continuation; no internet; no
  repository or protected-package access.
- Isolation: read-only intake mount, isolated writable runtime and scratch, separate return mount,
  system runtime and resolver files, and the authorized read-only authentication file. The
  repository and protected packages were not mounted.
- Reviewer: fresh ephemeral external Codex `gpt-5.4`, high reasoning, approvals disabled, web
  search disabled.
- Successful session: `01a01c5f-145f-7b11-88dd-ac3f13be4e59`.
- Banked raw review SHA-256:
  `213ce52f7e7c69ed6e568bc84ce48e77a80b419ea972778fa277416d33b7233e`.
- Successful transcript SHA-256 before compression:
  `eed4fd411bf6c43b777f077a290729f52e6b0ceb3e72bd4d061fc10a79087415`.
- Deterministic gzip transcript SHA-256:
  `69377bc60b3abffb90b16ad92fd73dee77809ce71a51d0529e57c08d3806da18`.
- Result: `G181_REQUIRES_REPAIR`.

The bounded geometry was not refuted. The review rejected the evidence layer because the sealed
production replay required unavailable SymPy and the registered 33-catch count included
tautological and metadata-presence checks rather than only executable mutations.

## Corrected repair-only follow-up

- Authorized intake: `/tmp/udt_g181_endpoint_review_6sm70o49`.
- Total files: 34 (33 payloads plus `REVIEW_SCOPE.json`).
- Scope SHA-256:
  `8cbd6fdb199e8ae2782f11960566282abad47d722b5497b04a29fd8b07a54acf`.
- The first follow-up process, session `01a01c6d-f4c0-7841-9b99-fa81d5839e6a`, ended during
  validation without returning a verdict. Its transcript SHA-256 before compression is
  `b61438f51cc4f45ea6ff0f5717729c0ab5a16f7c42b72094fde1170f88f831a4`.
- The second fresh follow-up, session `01a01c6f-600a-7c80-a1a6-3b1e77a77dbc`, passed all displayed
  commands but exhausted its context after dumping documents and returned
  `G181_REPAIR_INCOMPLETE` without naming a failed repair. Raw response SHA-256:
  `f5482f7774a9eae1ea6fc346eeb36c755e3ec2c2fa9a3d1c140b416d49d6669a`; transcript SHA-256 before
  compression: `ba6c77f17a789792a6e8a9625754e588675fecafe8e13669ddfbdb6112dcf77e`.
- A third fresh recovery review, session `01a01c72-b720-7233-b069-25f9af4cd63b`, was constrained
  not to dump documents and independently reran every registered repair check. It returned
  `G181_REPAIR_ACCEPTED`. Raw response SHA-256:
  `fd2b5cf31f8a550555d96c917c260cf5a8fe280b1827f3061bca584514765625`; transcript SHA-256 before
  compression: `7d09f747dd629600b7a9f5a6d1c652a4368b541b11e95d7b6e58a5bf3b3f227a`.
- Accepted-review result: all isolated scripts and verifiers passed; 28 executable mutants and six
  separate semantic guards passed; the intake hashes were unchanged after every replay; the
  formulas, 19 witnesses, seven sources, landing, premise grade, and maximum conclusion were
  retained.
