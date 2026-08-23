# G233 startup-surface repair preregistration

Date: 2026-08-23

The mandatory root test suite passed 134 tests with one expected xfail and exposed two
documentation-only regressions:

1. `test_catch_missing_current_dependency_spine` still asks for the superseded literal
   `G166--G231` rather than current `G166--G232` and does not separately catch deletion of `G232`.
2. `LIVE.md` is 994 words against the existing 900-word readability ceiling.

Frozen repair:

- update only that catch-proof tuple to `G166--G232` and add `G232`;
- shorten `LIVE.md` below 900 words without changing premise grades, formulas, protected paths,
  open scope, or the G233 next gate;
- rerun the entire root suite and require 136 passes plus the same one expected xfail.

No G233 equation, output, landing, or scientific status may change under this repair.
