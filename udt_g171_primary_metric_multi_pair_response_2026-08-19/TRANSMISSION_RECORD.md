# G171 external-review transmission record

Date: 2026-08-19

Charles authorized the sealed 31-file intake:

```text
/tmp/udt_g171_primary_metric_review_un8mfrc6
```

with `REVIEW_SCOPE.json` SHA-256:

```text
a0b50e0139a4f9ea037ec59a0de95596ba334ec0026e15477ebc641352fac8c3
```

Three launcher preflights failed before a review completed: obsolete CLI approval syntax, the
expected no-Git intake check, and a missing read-only resolver mount. Their exact logs are retained.
The successful fresh external `gpt-5.4` run used high reasoning, web search disabled, approvals
disabled, a read-only intake mount, isolated scratch/return paths, the system runtime, and the
previously authorized read-only authentication-file mount. The repository and protected packages
were not mounted. The scope hash remained unchanged after return.

Raw return SHA-256:

```text
f24fdd59e78841f819d9062ca002968fed5d57ccfb7f29443cfc915cb80d2bb9
```

Transcript SHA-256:

```text
04bd395505423a4f78e1f52d2fed23dd76c87ab9524f245f8333c24e686efeb2
```

The reviewer retained the scientific landing and exposed a sealed-versus-repository verifier
ambiguity. Its repair was preregistered before implementation.

## Packaging-repair follow-up

Charles authorized the corrected sealed 42-file intake:

```text
/tmp/udt_g171_primary_metric_review_18qqhs99
```

with `REVIEW_SCOPE.json` SHA-256:

```text
87b2b95e58515ed96d9644aa7547eb813ba35d6c2afee23f2281e92687e8b8aa
```

The fresh repair-only `gpt-5.4` reviewer received only the read-only seal, with web disabled and no
repository or protected-package mount. It returned:

```text
PACKAGING_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
```

Raw return SHA-256:

```text
98c18483cfc007a1f2e3ec0189deea5ee8965f23227f2b20d7ce3f7322254bb5
```

Transcript SHA-256:

```text
5870c024ddce4673eb01c66b64a357cbd50ef36499b1d05e56ed27b086a77b16
```

The transcript content is exact; CRLF line endings from the external PTY were normalized to LF
before banking.
