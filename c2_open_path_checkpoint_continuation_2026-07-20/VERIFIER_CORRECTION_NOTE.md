# Verifier correction note

The first full verifier invocation recomputed all expensive scientific groups and then stopped at the
`open_promoted_rejected` mutation. `validate_raw` compared the stored top-level status-count object to
its expected value but did not independently recount the statuses in the path rows, so mutating one
row to `NO_SOLUTION` while leaving the summary unchanged escaped that catch.

Before any verdict was banked, the verifier was amended to recount both path statuses and endpoint
classes. A hash-bound replay checkpoint was also added after the expensive groups. The complete
3,919-state and twelve-profile replay was then run again; all five groups and fourteen catches passed.

This was a verification-harness defect. It did not alter the raw solver output, equations, controls,
or scientific census.
