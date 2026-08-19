# G178 external transmission record

Date: 2026-08-19

- Authorization: explicit user authorization for the exact sealed intake and the previously
  authorized read-only authentication-file mount.
- Intake: `/tmp/udt_g178_completed_pair_review_nczus9c7`.
- Total files: 50 (49 scoped files plus `REVIEW_SCOPE.json`).
- Scope SHA-256:
  `152c55aeac85d816a711f474a043a510dcfa808589237418ce8e8510262e0ffe`.
- Restrictions: intake only; read-only; no edits or research continuation; no internet; no
  repository or protected-package access.
- Isolation: read-only intake mount, isolated writable runtime and scratch, separate return mount,
  system runtime and certificate/resolver files, and the authorized read-only authentication file.
  The repository and protected packages were not mounted.
- Reviewer: fresh ephemeral external Codex `gpt-5.4`, high reasoning, approvals disabled, web
  search disabled.
- Session: `01a01bbb-fbe5-77c1-a7f5-1f4d57c0cb56`.
- Completion recorded: `2026-08-19T16:39:01-04:00`.
- Raw returned review SHA-256 before repository newline:
  `34368678571fe201b3e043e845d1eed2a94e5a0ee3fe43f72276a60777ab7822`.
- Banked review SHA-256:
  `490fd476149d5171c981e03829be67f3abc4913e1aa2e11268d7516aaf02fb15`.
- Exact successful transcript SHA-256 before compression:
  `7bec569fbf57d02b4e05e7db242be47d4ed41873f91540e42f82f09271be4480`.
- Deterministic gzip transcript SHA-256:
  `c43501c1c335dcff1c03959fb5a74229cc676f63afe7e775a0fc151c4a99d7ae`.
- Result: `G176_G177_ACCEPTED_WITH_STATED_BOUNDS`.

Two preflight-only launches ended before reviewer contact: the first exposed the current CLI approval
flag ordering, and the second required the standard Git-free intake flag. The successful run changed
only those invocation controls; payload, scope hash, restrictions, and model were unchanged.
