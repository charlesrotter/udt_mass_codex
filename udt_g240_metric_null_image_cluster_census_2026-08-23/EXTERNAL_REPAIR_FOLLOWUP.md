# G240 external repair-only follow-up

Date: 2026-08-23

Reviewer: external Codex `gpt-5.4`, fresh repair-only context, high reasoning, web disabled.

Primary landing:

```text
G240_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
```

The reviewer verified that the repaired package has exactly one source-root contract: repository
replays use `REPOSITORY_ROOT`; sealed replays identified by root `REVIEW_SCOPE.json` use only
`SEALED_SOURCES_ROOT`. There is no multi-root probing or silent fallback.

The as-delivered sealed no-write replay passed. A builder replay in confined writable runtime space
also passed, while an intake lacking `sources/` failed closed with the preregistered assertion. All
eleven source hashes, 35 manifest payload rows, and manifest SHA-256
`f51fd6848b7680d0a23df0a8833cbf405cd73178208f21dbd5d5ec03707e6de9` matched.

The reviewer independently confirmed that the landing string was unchanged and that no
observational outcome, detector/transfer law, or broader physical claim entered. Remaining defect:
none inside R1.

Raw runtime final-message SHA-256:
`65e5a772f71b63bf7349aeb9d9042f0d6ad5c4cfbb82fdb7f2f1d520c3b2e1b9`.

The tracked transcription differs only by its terminating newline; its SHA-256 is
`9df1a23430be13bac17b56fde56a0e54af263e5462363ce84cee940da1be7777`.
