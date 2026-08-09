# FD1 independent outside-family semantics correction

Date: 2026-08-09
Status: preregistered semantic correction; no numerical rerun and no changed threshold

`phase2_independent_verification_failed_outside.json` is preserved as an 8/10 return. All 12 fixed
inside configurations passed independently, but 7 of 24 individual outside configurations crossed
the historical 3.1% line under the alternate grid/method. The added rule “every outside
configuration must be outside” therefore failed, and the schema key tied to it failed as well.

That added rule was stricter than the controlling family definition frozen before the first pass:

```text
an interval is inside only if all three SNe-conditioned n samples are inside;
therefore a family point is outside if not all three n samples are inside.
```

The logical negation of `all(n_inside)` is `any(n_outside)`, not `all(n_outside)`. This correction
does not relabel a family after the fact; it restores the exact all-three-`n` semantics used to build
the original intervals. The stricter individual-row failure remains useful evidence that the
`q/qcrit=0.75` edges are method-sensitive.

The corrected validator is limited to the saved independent records. It must require:

- exactly 12/12 inside configurations independently inside;
- each of the 8 outside family points has exactly three `n` records and is not all-inside;
- the preserved independent frequency/residual, actual-trough, and one-scale caveat gates pass;
- both earlier failed artifacts remain disclosed as failed;
- catch-proofs reject a missing/duplicate identity, one failed inside row, an all-inside outside
  family, removed offset/one-scale disclosures, or erased prior failures.

No exact boundary is certified. Maximum conclusion remains strict interior existence with unresolved
and demonstrably method-sensitive edge locations.
