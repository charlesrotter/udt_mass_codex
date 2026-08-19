# G168 evidence gates

Date: 2026-08-18

## Gate 1 — preregistration

Passed. `PREREGISTRATION.md` and the ten-source frozen manifest were committed and pushed at
`1341994a` before production execution.

## Gate 2 — full or bounded space

Complete for all regular local germs consisting of a timelike clock tangent and a nonzero
clock-orthogonalizable separation tangent in Lorentz signature `(1,3)`. The primary-metric block
reconstruction is complete for their arbitrary radial/nonradial coordinate components.

Not covered: coincidence, null/degenerate strata, derivation of the germ from bare labels, global
event pairing, cross-query carry, path outputs, general ambient completion, or dynamics.

## Gate 3 — independent verification

- exact symbolic/source checks: 36/36;
- independent stdlib `Fraction` replay: 6,012/6,012 over 1,200 trials;
- semantic mutation catches: 11/11;
- repository regression: 125 passed, 1 registered xfail;
- fresh external review: open.

## Gate 4 — premise audit

Passed. `verify_current_scientific_premises.py` reports the complete 153-row registry and current
G167-extended guards passing. The result is explicitly stamped as a working semantic clarification
for the typed pair germ and a derivation only for the metric projection and plane.

The administrative package gate passes with 14 required files, ten frozen source hashes, all
production/independent/mutation checks, and the premise verifier. External review remains the only
open evidence gate.

## Current grade

```text
VERIFIED_WITH_CAVEATS__FRESH_EXTERNAL_REVIEW_OPEN
```
