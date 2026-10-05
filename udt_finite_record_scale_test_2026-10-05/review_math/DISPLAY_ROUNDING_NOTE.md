# Reporting clarification at final review

SAVED_REPLAY_REVIEW.md displayed some interval endpoints rounded to nearest for
readability. They must not be interpreted as independently certified tighter
bounds. Source numerical precision is retained in SAVED_REPLAY_RESULT.json;
conservative outward-rounded displays of its long intervals are

    E=1:  [.004972583595655605, .005067684169969094]
    E=10: [.004972299857938959, .005067399010009680].

The final central display uses coarser outward rounding as requested by the
fidelity reviewer. This is a reporting clarification, with no changed equation,
computation, decision threshold or numerical rerun. The former note is preserved
as actual review history. Exact continuum inequalities and finite-precision
computed examples retain their distinct evidence types.
