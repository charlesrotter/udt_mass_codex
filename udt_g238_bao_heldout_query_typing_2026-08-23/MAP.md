# G238 outcome-blind map

## Observing frame

This is a source/operator ownership audit. It is not a BAO fit or a profile solve.

## What is frozen

- G237 `K=12` state and covariance, byte-for-byte.
- No SNe refit and no state interpolation.
- The already registered BOSS observer-coordinate catalogue and estimator semantics.
- No BOSS numerical outcome inspection.

## Metric-led versus template-led

The metric-native chain is the complete-coframe null clock and Jacobi evaluator on supplied metric
histories and supplied branches. Landy--Szalay is a borrowed observational estimator. Any source
population, branch weight, profile interpolation, or outcome-selected angular response would be an
extra premise rather than a metric derivation.

## Immediate risk

The G237 object is a finite one-source radial state. The BOSS object is a two-source,
reference-projected angular correlation. Equality of the word “pair” in these two descriptions does
not make their mathematical types equal.

## Proposed bounded action

Audit each arrow in the candidate forward chain, prove a finite-state nonuniqueness theorem if the
first arrow is missing, and stop before opening BOSS outcomes unless the entire operator is owned.

