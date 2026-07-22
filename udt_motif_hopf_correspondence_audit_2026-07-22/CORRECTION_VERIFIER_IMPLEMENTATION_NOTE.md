# Correction-verifier implementation note

Date: 2026-07-22

The first execution of `verify_review_corrections.py` exited before writing any result. The symbolic
metric derivation reached its final connection/quotient assertion, where SymPy left

```text
exp(-2*phi)/(2*cosh(2*phi)) - 1/(exp(4*phi)+1)
```

unsimplified. Rewriting that expression in exponentials reduces it exactly to zero. The quotient
norm and full-range limit already reduced to `0` and `1` respectively.

Before changing the verifier, the registered implementation correction is: apply `.rewrite(exp)`
before simplifying the connection residual. No threshold, sample, metric, target formula, or result
classification changes. The full covariance computation will be rerun rather than recovered from
memory.

