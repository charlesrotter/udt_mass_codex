# Cold adversarial review and repairs

Date: 2026-08-12  
Verdict: **VERIFIED-WITH-CAVEATS after required repairs**

An isolated reviewer independently rebuilt the exact founding formulas and replayed the full
production/finite-difference package in a clean temporary directory. The 1,806 ledger rows, 1,221
unique-jet count, tensor errors, Petrov counts, and proper-subset landing reproduced.

The reviewer found one load-bearing classification bug: 21 type-I rows were labelled merely as
finite aligned Weyl candidates even though their Ricci block residual and spectral gap satisfied the
preregistered Ricci-ownership gate. They are now labelled
`RICCI_DERIVED_WITH_WEYL_ALIGNMENT`. This changes the interpretation, not the metric tensors or
Petrov census. The numerical-atlas owner counts are now:

```text
WEYL_AND_RICCI_AGREE_ON_SPLIT               588
RICCI_DERIVED_WITH_WEYL_ALIGNMENT             21
CURVATURE_ALIGNED_BUT_NOT_UNIQUE                3
SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS   1194
```

Additional repairs:

- added conservative `NUMERICALLY_UNRESOLVED` bands around algebraic and eigenvalue thresholds;
- made the missing zero-shift Kruskal A05 second jet an explicit status row;
- made catch proofs validate the untouched baseline before applying mutations;
- added the machine-readable premise authority to the source manifest;
- restricted frame-covariance wording to split-preserving frame changes;
- retained the distinction between 1,806 provenance rows and 1,221 distinct metric jets.

The reviewer confirmed that no current row lies in an unresolved threshold band and that no
history, query, realization, or physical-admissibility selection follows.

