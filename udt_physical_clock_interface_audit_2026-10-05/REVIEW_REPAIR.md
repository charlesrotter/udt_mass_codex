# PIA1 source-preserving review clarifications

Both actual fresh reviewers accepted the algebra and identified precision
repairs below. INITIAL_CANDIDATE.md and its hash freeze remain unchanged as
discovery history. This document and the integrated central text control the
following readings; no FRI1 equations, domain, numeric outputs or grades change.

1. **Uniform coverage.** For each admitted fixed history/parameter in class C,
   require a stated measurement model with Pr(E | that history)>=1-p for the
   JOINT event E that all required record/calibration/source bounds hold. On E,
   the deterministic FRI1 inclusion holds, hence the procedure has at least
   that coverage within C. If C is instead treated as a random selection event,
   the requirement is Pr(E|C)>=1-p, not merely Pr(E)>=1-p. Valid conditional
   component failure bounds give a union bound without independence. No
   distribution, such guarantee, or data-dependent class selection is adopted.
2. **Base-control duration.** C=1 for long, C=.008 for short, K delta=.0005
   and q_seconds/K=.001 refer to the base H=.005 synthetic history. The other
   homothetic history has half C and half K delta on the SAME calibrated
   schedule, and a different q/K if the same drift allowance is retained.
   P2 holds for each history using its own C; physical durations remain unset.
3. **Exclusion requires a valid total ratio.** P1 can reject this domain for
   a specified pairing only with an independently justified upper bound on
   its actual total Z below54180. A nominal estimate or a frame/source-reduced
   proxy is not that bound. This audit does not perform an empirical exclusion
   using MCP medians, infer tail membership, or certify exact B_*=0 preparation.
4. **Actual instrument weights.** BACON's specific counters, filtering and
   common-uptime selection do not automatically produce rectangular equal-width
   FRI1 windows. Known weighting/gating, missing-data and estimator reduction
   must be included. P3 concerns ideal uniform phase-window integration under
   the stated regularity; it does not certify that published processing chain.

The repairs sharpen reporting/operational scope without adding a new physical
assumption. Both reviewers recheck these statements and final central bytes;
the ten unchanged arithmetic controls do not need a redundant rerun.
