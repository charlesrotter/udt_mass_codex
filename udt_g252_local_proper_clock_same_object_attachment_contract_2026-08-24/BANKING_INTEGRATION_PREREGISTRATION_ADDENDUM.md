# G252 banking integration preregistration addendum

Date: 2026-08-24

Before implementation, add the one omitted startup-test surface to the frozen integration scope:

- `tests/test_startup_surface.py` may be changed only from the G251 dependency ceiling to G252 and
  to require the new G252 token.

Because the current full verifier live-replays G251 against the evolving premise registry,
`verify_current_scientific_premises.py` may run that already-reviewed G251 package in an ephemeral
copy whose registry differs from the current registry only by removal of exactly one `G252` row.
This preserves the G251 live replay after G252 banking without editing G251 evidence or weakening
its frozen 233-row source hash.

No other test, package, scientific claim, or startup file is added to scope. The maximum conclusion
and all closed observational/protected boundaries in the primary preregistration are unchanged.
