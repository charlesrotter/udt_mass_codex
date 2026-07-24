# Preregistration correction: lowercase LaTeX and fixed-base census

Date: 2026-07-24

Original preregistration commit:
`824280a`

Fixed candidate base:
`696cf401c441fdd3aefea6f3de188e6425ae5636`

## Defect

The first census matched plain `Xmax`/`X_max` spellings and uppercase
LaTeX `X_{\max}`, but failed to include lowercase LaTeX `x_{\max}` and
plain-braced `x_{max}`. It therefore omitted 53 base-commit paths,
including `CANON.md`.

After the original preregistration commit, scanning the working tree would
also allow the audit's own generated records to enter its candidate
universe. That contradicts the registered selection rule.

## Correction registered before semantic classification continued

The deterministic matcher is:

```text
x_?max | x_{\max} | x_{max}, case-insensitive
```

The script reads paths and bytes from the exact pre-audit base commit, not
from current `HEAD` or the working tree. The corrected candidate universe is
therefore fixed, replayable, and cannot contain its own generated records.

Expected corrected count: `907`.

The original 854-row census remains visible in commit history. This layer
supersedes its completeness count without changing any scientific
classification or outcome.
