# G252 external-review transmission record

Date: 2026-08-24

- reviewer: external Codex `gpt-5.4`, reasoning effort `high`;
- session: `01a0364e-9607-7011-8a0b-97a101c139dd`;
- intake: `/tmp/udt_g252_review_fkrgolx8`;
- file count: 29 including `REVIEW_SCOPE.json`;
- scope SHA-256: `28872ada2aafbb51648dbde88d4163def9231b56e4b6947558b92bde50aafda6`;
- sandbox: read-only;
- approval policy: never;
- internet: disabled;
- result: `ACCEPT_WITH_REPAIRS`;
- scientific landing: retained;
- repair: sealed-source relocation resolution in production, independent, and package verifiers,
  followed by regenerated evidence and a fresh repair-only intake.

The reviewer verified all 28 payload hashes. The hostile replay passed; the remaining registered
replays failed because they searched only the repository-root source layout rather than the sealed
`sources/` layout.
