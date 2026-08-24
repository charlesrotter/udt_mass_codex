# G246 append-only banking integration preregistration

Date: 2026-08-24

## Trigger

G246 was preregistered, derived, independently verified, sealed, and externally accepted against
the exact 228-row premise registry whose SHA-256 is frozen in `SOURCE_MANIFEST.tsv`:

```text
e731b06847688c0466799d82c1ffbd3333250596e29bbadd21cb9e375c1142b5
```

Banking the accepted result requires one append-only `G246` row at the head of the live registry.
The resulting 229-row live registry must coexist with exact verification of the frozen pre-G246
source bytes.

## Authorized mechanical integration

1. Add exactly one `G246` row immediately after the registry header; do not alter prior rows.
2. Teach G246's verifier and intake builder to reconstruct the frozen registry as the header plus
   every row after the unique `G246` row when the live registry has append-only descendants.
3. Advance the current startup surface from G245 to G246 and 228 to 229 rows.
4. Add exact live-verifier guards for the accepted landing, inputs, local theorem, ribbon,
   reversal/return distinction, branch nonselection, no-fit/outcome boundary, source lineage, and
   no-write replay.
5. Rerun G244, G245, and G246 no-write package checks, the complete premise verifier, and the full
   test suite before banking.

## Forbidden changes

No saved scientific output, classification, witness, tolerance, earlier registry row, frozen source
digest, or observational boundary may change. Integration may not select a universal query, one
global branch, a source or detector law, an observer population, `X_max`, or a physical metric
history.

Maximum conclusion: append-only registry/startup integration of the externally accepted bounded
G246 theorem. No scientific claim is strengthened.
