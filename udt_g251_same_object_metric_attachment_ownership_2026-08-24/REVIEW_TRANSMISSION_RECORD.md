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

## Repair-only follow-up

- reviewer: external Codex `gpt-5.4`, reasoning effort `high`;
- session: `01a035b8-c661-7312-a188-7b3faf49e226`;
- intake: `/tmp/udt_g251_repair_followup_hwdq4_lu`;
- file count: 41 including `REVIEW_SCOPE.json`;
- scope SHA-256: `0489833008672f937e914e1ee4c3715f1774358f45cbe3f0c1e378f3690552b9`;
- sandbox: read-only;
- approval policy: never;
- internet: disabled;
- result: `REPAIRS_ACCEPTED`;
- scientific landing: unchanged;
- remaining defects: none within the authorized R1/R2 scope.

The reviewer verified all 40 scoped payload hashes, 72/72 cited `E/I/C/W` legs, independence of the
ledger reconstruction, all five registered no-write replay classes, 26/26 hostile catches, and the
exact sealed 233-row premise registry.
