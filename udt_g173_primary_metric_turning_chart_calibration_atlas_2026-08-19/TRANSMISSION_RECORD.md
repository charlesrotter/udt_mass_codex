# G173 external transmission record

Date: 2026-08-19

- Authorization: explicit user authorization for the sealed 34-file intake.
- Sealed intake: `/tmp/udt_g173_turning_chart_review_20y546ml`.
- Total files: 34 (33 scoped tree files plus `REVIEW_SCOPE.json`).
- `REVIEW_SCOPE.json` SHA-256:
  `9b589fbd701fe3e5a8e7ad3a074eee5788b3c74356593b8c2d5d5f9bb1bd02c2`.
- Restrictions: intake only; read-only; no edits or research continuation; web search disabled; no
  repository or protected-package access.
- Isolation: read-only intake mount, isolated `/tmp`, separate writable return mount, system
  runtime, resolver data, and the previously authorized read-only authentication-file mount. The
  repository and protected packages were not mounted.
- Reviewer: fresh ephemeral external Codex `gpt-5.4`, high reasoning, approvals disabled.
- Completion: `2026-08-19T14:07:56-04:00`.
- Session: `01a01b30-22f7-7811-8228-eaa99b582150`.
- Raw returned review SHA-256 before the repository-standard terminal newline:
  `aa7f642dd063838976b025c8763bfc81c04c7e8e385b07c4d2942e996f4bb0d1`.
- Banked review SHA-256 after adding that newline:
  `6328b1d416f03870661185e9d3da4d4c49fa2be9c00131a6bcbc40ba0271a9aa`.
- Exact execution transcript SHA-256 before compression:
  `ddb1fd3ab1d2f586015f7d61c52bc2719915ba12b3f4328a8ab9b4ec6fc1c684`.
- Deterministic gzip transcript SHA-256:
  `fe0b04caa336cb7234c267d4d80172b851b65074a95e896091bf3024347bcf3b`.
- Result: `G173_ACCEPTED_WITH_STATED_BOUNDS`.

The reviewer reproduced the sealed verifier, the load-bearing algebra, the exact turning witness,
and the independent replay. It identified two malformed LaTeX escapes, repaired after return, and
correctly noted that the repository-side outer verifier is not intended to be reproducible inside
the sealed intake. `verify_sealed_intake.py` is the sealed-boundary verifier.
