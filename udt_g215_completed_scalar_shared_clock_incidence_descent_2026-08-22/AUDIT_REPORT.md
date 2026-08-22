# G215 audit report — completed scalar shared-clock incidence descent

Date: 2026-08-22

## Landing

```text
COMPLETED_SCALAR_DESCENDS_TO_SHARED_CALIBRATED_OBSERVER_CLOCK
__G171_ANGULAR_SCALAR_DEFECT_REGRADED_AFTER_G176_COMPLETION
__NETWORK_SCALAR_CYCLES_CLOSE_WITHOUT_A_FULL_PAIR_METRIC_PRODUCT
__INDEPENDENT_CLOCK_RECALIBRATION_IS_THE_REMAINING_EXACT_SCALAR_DEFECT
```

Status: `DERIVED_CONDITIONAL__PREREGISTERED__INDEPENDENTLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.

## Result

For every G176-completed regular pair incidence,

\[
\Phi_s=-\log T,
\qquad T^2=-g(u,u).
\]

Consequently, incident pair germs with one shared calibrated observer clock germ have one endpoint
potential even when their ruler directions, angular participation, densities, shifts, and pair
planes differ. Directed depth is the difference of these observer-clock potentials, so all cycles
on a common-clock network telescope exactly.

This materially narrows the G171/G214 incidence gap. G171's angular witness has raw terminal values
`1` and `59/25` in the exponentiated scalar, but both become exactly `1` after G176 completion
because both use `T=1`. Its density and shift differences survive. A nonzero completed scalar defect
now requires independently calibrated clock factors at a shared observer incidence.

The full pair metrics still do not multiply. Scalar carry remains strictly weaker than G182 pair-
metric and immersion-germ carry.

## Evidence

- Preregistered and pushed at `f7faa1c2` before outcome execution.
- Production: 28 dependency-free exact rational checks.
- Independent: 10,000 exact rational cases and 190,000 assertions in a separate implementation.
- Hostile controls: 13/13 caught.
- Source provenance: 14/14 frozen G168/G170/G171/G174/G176/G182/G214 files matched.
- One independent witness-generator defect was caught before banking and repaired without changing
  the theorem or production equations.

## Four gates

1. **Preregistered:** PASS.
2. **Full space or bounded scope:** PASS WITH CAVEATS — regular G176-completed incidences and supplied
   shared calibrated clock germs only.
3. **Independent verification:** PASS — separate exact `Fraction` implementation.
4. **Premise audit:** PASS WITH CAVEATS — G176 remains a working clarification; pair germs and clock
   network are supplied.

## Maximum conclusion

The scalar incidence bridge closes conditionally on common observer-clock calibration. This does
not populate observers or pair germs, determine the metric's values or profiles, identify full
pair planes, or produce a history evolution.
