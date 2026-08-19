# G180 external transmission record

Date: 2026-08-19

- Authorization: explicit user authorization for the exact sealed intake and the previously
  authorized read-only authentication-file mount.
- Intake: `/tmp/udt_g180_family_descent_review_gwk8x763`.
- Total files: 28 (27 scoped files plus `REVIEW_SCOPE.json`).
- Scope SHA-256:
  `230a11ab1cc114841a5cdf009daaf9d422d02b62db96c44179068ed9ee5431a2`.
- Restrictions: intake only; read-only; no edits or research continuation; no internet use; no
  repository or protected-package access.
- Isolation: read-only intake mount, isolated writable runtime and scratch, separate return mount,
  system runtime and certificate/resolver files, and the authorized read-only authentication file.
  The repository and protected packages were not mounted.
- Reviewer: fresh ephemeral external Codex `gpt-5.4`, high reasoning, approvals disabled, web
  search disabled.
- Successful session: `01a01bf9-0789-7d11-bc70-73d1136c09d3`.
- Completion recorded: `2026-08-19T17:47:43-04:00`.
- Banked raw review SHA-256:
  `d12827e780a8f81028fd3ebc34c91b2509ca7bd7991222c974acba4f50482a39`.
- Successful transcript SHA-256 before compression:
  `7580aff35f628621f52ff7a759b76e36cc6196ba94a72d94d3fcd5967a4bb46e`.
- Deterministic gzip transcript SHA-256:
  `c1a9438b2025ea1d6aa6c9dcc6eeb2cda38ac72c8d5d950b0ba37e87e6d7c8c3`.
- Result: `G180_ACCEPTED_WITH_STATED_BOUNDS`; the theorem was retained and a sealed-replay packaging
  repair was required.

One preflight-only launch reached the correct isolated model but could not contact the provider
because the resolver runtime was not mounted. It was stopped without a returned review. The
successful run added only the missing read-only resolver mount; payload, digest, prompt, model, and
restrictions were unchanged.
