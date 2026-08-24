# G251 external-review transmission record

Date: 2026-08-24

- reviewer: external Codex `gpt-5.4`, reasoning effort `high`;
- session: `01a0357e-e142-7ef0-b453-ffccf04e0a18`;
- intake: `/tmp/udt_g251_review_l574xcyu`;
- file count: 35 including `REVIEW_SCOPE.json`;
- scope SHA-256: `c4cbc21dda756b2b71c768af0c7cf3c872e55c505e7d58155cd0af393e89de40`;
- sandbox: read-only;
- approval policy: never;
- internet: disabled;
- result: `ACCEPT_WITH_REPAIRS`;
- scientific landing: retained;
- requested repairs: explicit cited machine-readable `E/I/C/W` ledger and a sealed rerunnable premise-registry gate.

The first launcher attempt exited before review because Codex CLI `0.144.5` no longer accepts the
legacy `-a` option. The corrected launch used the same authorized intake and restrictions. The
reviewer verified all 34 payload hashes and ran all three registered scientific replays plus the
package verifier without writes.
