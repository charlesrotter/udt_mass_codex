# G250 evidence gates

Date: 2026-08-24

1. **Preregistered:** PASS — initial contract pushed at `7361cf38`; execution-boundary note pushed
   at `7170556f`, both before calculation.
2. **Bounded whole space:** PASS WITH SCOPE — all frozen anchor classes and all integer homothety
   weights used by them are classified on the one-dimensional constant-positive G249 scale orbit.
   General local conformal freedom, history selection, and anchor measurement are outside scope.
3. **Independent verification:** PASS internally — standard-library rational implementation imports
   neither production code nor production output. Fresh external adversarial review is pending.
4. **Premise audit:** PASS internally — every candidate is graded by dimension, homothety weight,
   provenance, and operational attachment. The premise registry verifier must pass before banking.

The present grade is `INTERNALLY_VERIFIED_WITH_CAVEATS__EXTERNAL_REVIEW_PENDING`.

Recorded pre-review replays:

- package verifier: 24/24 PASS;
- current 232-row scientific-premise verifier: PASS;
- repository suite: 153 PASS, 1 registered XFAIL;
- startup catch-proof and readability regressions exposed by the first full-suite run were repaired;
  the complete suite then passed.
