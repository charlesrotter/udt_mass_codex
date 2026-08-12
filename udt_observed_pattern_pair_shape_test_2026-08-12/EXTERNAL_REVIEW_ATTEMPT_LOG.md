# External-review attempt log

Date: 2026-08-12
Reviewer model: Codex `gpt-5.4`, high reasoning
Web: disabled
Filesystem: read-only

## Attempt 1 — invalid layout interpretation; stopped without a verdict

Session: `019ff840-098a-7821-8db1-761a4eb47014`

The initial prompt told the reviewer to use `REVIEW_SCOPE.json`, but it first looked for that file
under `package/` instead of at the sealed root. It consequently began treating the copied
`repository_sources/` and `external_sources/` files as absent. A terminal-input correction was only
echoed and did not become a model message. The attempt was interrupted before any final verdict and
is rejected as review evidence.

Raw terminal transcript:

```text
original bytes: 91804
SHA-256: d3b73495aff500666e0e87280ee2b28eb27aeb66f1fe9ae2c5a8c45ef574ba36
```

## Attempt 2 — accepted

Session: `019ff841-86e4-76c0-bd34-293edf3954bf`

The corrected initial prompt required the reviewer to open `./REVIEW_SCOPE.json` before every other
file and explicitly identified `package/`, `repository_sources/`, and `external_sources/` as the
sealed intake. The reviewer complied, independently recomputed the raw likelihood, and returned
`SUSTAINED_VERIFIED_WITH_CAVEATS`.

Final output:

```text
original bytes: 5515
SHA-256: ff36e0a730b80aa1c0b7a55b6fece7aff4f2574b8a5489c3e7b470d5e14c9ba9
```

The committed Markdown adds the conventional final LF only:

```text
committed bytes: 5516
SHA-256: 064be91fe0c9e346812043448136796929ebf77cd768c7e9c2af2887e0e85e20
```

Raw terminal transcript:

```text
original bytes: 168633
SHA-256: b151ce88eef6056344576c7ba01c2805bfeed872c7cd6e51456418cdf91f27c9
```

The committed transcript is the same terminal record with CRLF normalized to LF:

```text
normalized bytes: 165072
SHA-256: 3404aedf7445182370aa704f10553c2cd741534365dcfe50d6d1eef2476db381
```

## Intake-layout documentary defect

The sealed scope recorded seven repository-source `intake_path` values without their physical
`repository_sources/` prefix. The actual copied files were inside that directory, all 29 payload
hashes matched the scope, and the accepted reviewer inspected only those sealed copies. This did not
change the source universe or bytes, but it made the manifest paths misleading. The intake builder
is corrected prospectively in this package; the authorized sealed scope is preserved unchanged.
