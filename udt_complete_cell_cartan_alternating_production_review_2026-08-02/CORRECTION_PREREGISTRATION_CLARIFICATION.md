# Correction preregistration clarification after first fail-closed replay

Date: 2026-08-02

The initial correction preregistration incorrectly required “exactly 12 mixed rows under both
closure pivots.” The first implementation failed that requirement before producing a correction
result:

```text
FORWARD pivot = the reviewer's 12 reverse-normal-form rows plus 8 additional mixed rows
```

The fresh review return had stated more carefully that the **reverse-closure normal form** has the
listed 12 rows, both pivots have zero narrow leg-aligned projections, and raw mixed-monomial
attribution is closure-normal-form dependent. It did not require the raw mixed-row sets to agree.

The correction contract is therefore clarified, not tuned to a desired physical outcome:

1. the reverse pivot must reproduce the exact 12-row list in the cold return;
2. the forward pivot must retain and report its independently obtained full row set;
3. both pivots must retain zero narrow leg-aligned projections;
4. any difference between raw mixed-row sets must be explicit evidence of normal-form dependence;
5. no pivot-dependent raw monomial count may be promoted to a tensorial no-go or invariant count.

The failed assertion and its eight-row symmetric difference are preserved in the working record via
this clarification. The parent package remains unchanged.

