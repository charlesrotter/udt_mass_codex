# Presolve Path-Ledger Correction

Date: 2026-07-20

This correction was committed before generating the authoritative complete-ledger return.

The first official 51-path run completed with 29 validated round endpoints and 22 time-limited
paths.  Its raw JSON and transcript are preserved unchanged as
`RAW_HOMOTOPY_PATHS_INCOMPLETE_LEDGER.json` and
`HOMOTOPY_INCOMPLETE_LEDGER_TRANSCRIPT.txt`, with SHA-256 values:

- `05583c69d82ed8afb713fa17094a790b7c30146012f4616ef32ed22d5f57586c`;
- `b3bde058d0b4c1890e166f629647bb8e20b96d51d02b0dcf89d829b3895c15e4`.

The numerical return itself was complete, but its accepted-step ledger retained coefficient norms,
residuals, arclengths, and tangent-lambda components rather than the full coefficient and tangent
vectors.  That prevents an independent verifier from recomputing every intermediate homotopy
residual.  The authoritative run will therefore repeat the exact frozen census while adding only:

- the full coefficient vector, tangent vector, and action at every accepted point;
- the full coefficient vector at every endpoint-Newton iteration;
- predictor, last-corrector, and per-iteration states for every rejected step.

No metric, action, homotopy, seed, ordering, CPU-worker count, tolerance, step control, time limit,
classification, or conclusion gate changes.  The observed first-run counts are not used to tune the
rerun.  Agreement of the two status/endpoint identity sets is a required regression gate; any
disagreement leaves the result unresolved rather than selecting the more favorable run.
