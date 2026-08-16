# G105 sealed-review dispatch

Charles explicitly authorized the sealed 30-file intake:

```text
/tmp/udt_g105_two_route_review_m_c9fxp8
```

with `REVIEW_SCOPE.json` SHA-256:

```text
666dbe3bdf46405919398577f4ade0957d58f0b140931c32062efbabe76f4672
```

The first CLI invocation stopped before review because the installed client rejected an obsolete
approval flag. The corrected invocation used the same authorized intake and ran external Codex
`gpt-5.4` ephemerally with high reasoning, web disabled, and a read-only sandbox. It was forbidden
to edit, continue research, inspect the repository or protected packages, or open BAO/CMB outcomes.

The reviewer verified all 30 payload byte counts and hashes, replayed all four checks exactly, and
returned `PASS_WITH_CAVEATS`.
