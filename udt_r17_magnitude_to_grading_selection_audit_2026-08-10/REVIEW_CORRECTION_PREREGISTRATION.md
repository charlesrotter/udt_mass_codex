# External-review correction preregistration

Date: 2026-08-10

First external-review verdict: `ACCEPT_ONLY_AS_COMPLETE_COFRAME_CONDITIONAL`

Preserved raw-review SHA-256:

```text
5107d2e3888249ac97ec3917b3067e3a83e6b5a4a16230cb0dd57d6a73229fef
```

## Defects to correct

The first reviewer accepted the bounded uniqueness algebra but identified one real verification
weakness and made one demonstrably false intake statement.

1. **Real weakness:** the standard-library verifier mixes independent Fraction algebra with semantic
   checks that read booleans from the production result. Those boolean comparisons are regression
   checks, not independent reconstruction.
2. **False intake statement:** the reviewer says the 17 manifest targets are absent and point
   outside the intake. All 17 are present at their exact manifest-relative paths under the intake
   root. The sealed intake contains 34 files: 17 package files and 17 source files.

## Preregistered repair

- Preserve the first raw review unchanged.
- Rewrite the independent verifier so its mathematical and status result is reconstructed without
  reading `DERIVATION_RESULT.json`.
- Add exact projector-stabilizer rank checks across all six supplied `lambda` strata, including
  `lambda=+/-1`.
- Make source presence and hash closure explicit and fail closed at the intake root.
- Clarify every result document to use the reviewer-required grade
  `COMPLETE_COFRAME_CONDITIONAL_VERTICAL_METRIC_CLASS_MOD_SO2`; do not call the complete-coframe
  realization unconditional.
- Retain founding pair-only screen nonuniqueness and every open physical-arrow seam.
- Build a fresh read-only sealed intake and explicitly prove all 17 source paths exist before a
  fresh external review.

No candidate class, physical premise, tolerance, scope, or desired conclusion will be changed to
obtain acceptance.
