# G270 external-review repair report

Date: 2026-08-26
Repair preregistration commit: `6bd94cff`
Scientific landing: unchanged

## R1 — implementation mutation evidence

`run_catch_proofs.py` now launches the production derivation in no-write mode and mutates its exact
frame, pullback, completion, screen, frequency, and mutual-readout formulas. The unmutated production
baseline passes. All eight registered production-implementation mutations are caught by their
targeted invariant:

- omitted tilt contribution in `Gamma`;
- flipped longitudinal offset;
- dropped null normalization;
- injected tilt into the intrinsic pullback;
- wrong completed density;
- reversed frequency ratio;
- zeroed transported-screen projection;
- direct rather than inverse mutual readout.

Five non-algebraic status mutations remain useful but are now reported separately as typed-ledger
consistency checks. They are not represented as implementation mutation evidence.

## R2 — full ribbon regularity

The production derivation now proves

\[
\det F^*g
=-
\frac{(4\lambda^2+4\lambda+2)\tau^2+2\tau+1}{(1+\lambda)^2}<0
\]

for `lambda>=0` and every real `tau`, using an exact completed-square positivity identity. The
implementation-distinct rational replay adds 40,040 nonzero-`tau` cases over `-4<=tau<=4` to the
1,001 axis cases. All pass.

## Repaired evidence totals

- 39 production symbolic checks;
- 368,165 independent exact-rational assertions;
- 12,000 independent frame cases;
- 1,001 ribbon-axis cases;
- 40,040 off-axis ribbon cases;
- 8/8 formula-level implementation mutations caught;
- 5/5 separately labelled typed-ledger mutations caught.

The repairs add no observation, fit, coefficient, distance attachment, history law, source, matter,
`X_max`, transfer, signalling, or canonization.
