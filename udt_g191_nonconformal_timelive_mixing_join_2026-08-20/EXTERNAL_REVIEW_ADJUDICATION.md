# G191 external-review adjudication

The first external grade was `G191_REPAIR_REQUIRED` for a sealed-replay packaging defect. The
preregistered repair preserved the scientific artifacts byte-for-byte and made the bounded replay
self-contained.

This is a reproducibility and intake-packaging failure, not a scientific rejection. The reviewer
found no counterexample in the frozen artifacts to the bounded coframe, affine, frequency,
curvature, Jacobi, limit, or branch claims. However, the only authorized fresh replay failed before
those assertions because the intake moved sources below `sources/` while the verifier retained
repository-relative paths, then attempted to call a repository-wide premise verifier absent from
the bounded intake.

The authorized repair-only follow-up ran the registered replay successfully, compared the original
artifact hashes from the preserved first-review transcript, and returned:

```text
G191_ACCEPTED_WITH_STATED_BOUNDS
```

No repair remains within the preregistered scope. G191 is therefore
`EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS`. The landing remains one exact local analytic control,
not a physical history, observer population, radiative-transfer law, SNe prediction, global branch
classification, or `X_max` determination.
