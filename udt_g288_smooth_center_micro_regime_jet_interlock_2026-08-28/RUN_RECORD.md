# G288 run record

Date: 2026-08-28

1. Preregistration was committed and pushed at `0d57f458` before outcome computation.
2. Production rebuilt the current primary metric geometry and passed 21 initial checks.
3. The independent exact-Fraction route passed 16,513 assertions, but manual inspection found an
   unused displayed scalar-numerator constant initialized with the wrong sign.  It had not entered
   any tested scientific coefficient or tensor comparison.  The ledger construction and an exact
   zero-constant assertion were repaired; the rerun passed 16,517 assertions.
4. An exact constant-sectional-curvature Ricci check was added to both routes.  Final counts are
   22 production checks and 18,117 independent assertions.
5. Nine hostile mutations were all rejected.
6. The aggregate verifier twice failed closed on its own scope: first because it prohibited the
   production script from writing its own result, then because it compared a multiline displayed
   landing without whitespace normalization.  Both verifier-only defects were repaired.  The
   aggregate package then passed.
7. The 272-row premise/startup verifier passed after the G288 row and replay guard were registered.
8. The first full repository suite found one 234-character G287-era `INDEX.md` line against the
   220-character startup-surface limit.  The line was shortened without changing its pointers.
   The focused test passed, followed by a full pass: 192 passed, one expected xfail.

No long solve, GPU, observation, fit, protected input, Planck cutoff, source, action, field equation,
matter model, physical mass, history, or `X_max` value entered.
