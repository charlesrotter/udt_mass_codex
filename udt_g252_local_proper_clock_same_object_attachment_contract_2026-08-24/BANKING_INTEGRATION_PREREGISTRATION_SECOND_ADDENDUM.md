# G252 banking integration preregistration second addendum

Date: 2026-08-24

Observed integration failure: the full current-premise verifier reached the frozen G250 live package
replay, whose historical-registry compatibility accepts its already banked G250/G251 rows but
correctly rejects the new G252 row. This is the same evolving-registry integration boundary already
preregistered for G251.

Before repair, authorize only this additional current-verifier change:

- replay the unchanged G250 package in an ephemeral copy after removing exactly one G252 registry
  row, using the already added generic helper;
- keep every G250 file and scientific/evidence assertion unchanged;
- require the unchanged G250 package replay to return `PASS`.

The G252 scientific landing, startup content, test scope, observational closures, and protected-work
boundaries are unchanged.
