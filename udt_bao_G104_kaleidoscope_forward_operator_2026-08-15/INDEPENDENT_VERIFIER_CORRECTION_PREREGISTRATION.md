# G104 independent-verifier aggregation correction

Date: 2026-08-15

The first independent replay computed every mathematical check successfully but its final `all(...)`
aggregation included the intentionally false metadata field

```text
imports_production=false.
```

That field certifies implementation independence; it is not a required-true predicate. The frozen
repair is to exclude exactly `imports_production` and `outcome_artifacts_read` from the boolean
aggregation. No fixture, source, equation, witness, landing, coefficient status, or outcome scope may
change. The corrected verifier must then be rerun from the beginning.
