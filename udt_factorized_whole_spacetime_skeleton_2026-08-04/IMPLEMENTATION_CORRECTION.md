# Sparse-verifier implementation correction

The first production verifier included a direct determinant of the fully symbolic generic metric
`E.T * eta * E`. Although the scientific check was elementary, that representation expanded enough
to exceed the preregistered one-minute design budget. It was interrupted manually without a result.

This is recorded as an operational implementation failure only. It is not evidence for or against
the factorized skeleton.

The corrected verifier retains the exact sparse block determinant and inverse identities, evaluates
the metric determinant at an exact rational anchor, and separately checks the structural determinant
factorization. An independent standard-library rational implementation checks the full numeric block
identity without importing the production script.

Corrected production performance on the recorded workstation:

```text
elapsed = 0.40 seconds
maximum resident set = 49,312 KiB
```

The correction changes no scientific premise or expected result. It demonstrates why factorized
representations, rather than fully expanded generic expressions, are the governing resource rule.
