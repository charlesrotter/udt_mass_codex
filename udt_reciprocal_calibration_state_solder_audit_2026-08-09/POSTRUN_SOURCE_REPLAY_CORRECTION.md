# Post-run source-replay correction

Date: 2026-08-09

The preregistered source set included `CURRENT_SCIENTIFIC_PREMISES.tsv` at base commit
`30bdb020`. After the audit was banked, the separately authorized startup integration correctly
added G36 to that live registry. Comparing the frozen input hash to the now-updated worktree path
would therefore fail and would also be circular: the audit's output would be mistaken for its
input.

The source row and its SHA-256 are unchanged. The primary, independent, and repository verifiers
now replay that one mutable source with:

```text
git show 30bdb020:CURRENT_SCIENTIFIC_PREMISES.tsv
```

All other source rows continue to replay from their worktree paths. The scientific question,
candidate set, exact checks, landing, and status ledgers are unchanged. The repository gate is
rerun against the post-integration 36-guard / 85-pass baseline.
