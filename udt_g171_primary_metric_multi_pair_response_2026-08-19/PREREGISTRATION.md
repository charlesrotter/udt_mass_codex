# G171 preregistration — primary-metric multi-pair response

Date: 2026-08-19
Mode: metric-led, exact symbolic and independent rational replay

## Question

For several ordered observer pairs evaluated directly by the primary metric, does a shared observer
carry one pair-independent terminal reciprocal density, or can its endpoint readout depend on the
complete pair germ? What composition law, if any, follows without restoring scaffolded carry
machinery?

## Frozen inputs

Only the 12 sources in `SOURCE_MANIFEST.tsv` may control the derivation. G142--G160 and protected
local work are explicitly excluded from the derivation universe.

## Preregistered outcomes

Exactly one primary landing will be selected:

1. `OBSERVER_ONLY_ENDPOINT_POTENTIAL`: the primary metric forces every regular pair germ at a
   shared observer to return the same endpoint density, so arbitrary pair scalars telescope.
2. `PAIR_GERM_RELATIVE_NETWORK`: the primary metric evaluates every pair natively, reversal holds
   on the same pair, but a shared observer can have different endpoint densities in different pair
   germs; general triangle additivity is therefore not a native scalar requirement.
3. `MATCHED_SUBFAMILY_ONLY`: pair-germ dependence exists, but a precisely characterized native
   matched-germ subfamily forces a common endpoint density and telescoping.
4. `TYPE_OR_REGULARITY_FAILURE`: the requested multi-pair construction cannot be formed from the
   bounded primary-metric data.

Outcomes 2 and 3 may coexist only if 2 is the global landing and 3 is stated as its exact special
case.

## Exact tests

1. Derive for each pair `XY`

   ```text
   h_X^(XY) = pullback of g on the XY germ at X,
   Phi_X^(XY) = (1/4) log[(-det h_X^(XY))/(h00_X^(XY))^2],
   delta_XY = Phi_Y^(XY)-Phi_X^(XY).
   ```

2. Prove reversal by swapping the same two endpoint pullbacks.
3. Derive the exact three-pair scalar defect without assuming a common observer-only potential.
4. Test a same-event, same-clock, different-pair-germ rational witness in the primary metric.
5. Characterize the strongest sufficient condition for telescoping using equality of the actual
   shared endpoint pullbacks/readouts, without introducing an abstract carry.
6. Prove pair-chart covariance only inside each supplied pair; do not claim invariance under
   independently recalibrated pair charts.

## Catch proofs

The implementation must reject or expose:

- replacing pair-indexed endpoint densities by one observer-only symbol;
- reversing one pair by independently rebuilding its endpoint germs;
- forcing an arbitrary triangle defect to zero;
- dropping the angular Gram before terminal readout;
- calling nonadditivity a calibration failure, holonomy, or new force without derivation;
- importing G142--G160 carrier/carry variables;
- inserting `X_max`, a fit, path length, action, source, matter, or protected work.

## Certification contract

- exact symbolic identities;
- separate standard-library rational implementation over at least 10,000 regular trials;
- at least ten semantic/algebraic mutation catches;
- all 12 frozen source hashes verified against this preregistration commit;
- repository premise verifier and regression tests pass;
- fresh external review before any `VERIFIED` grade.

## Maximum conclusion

At most, G171 may classify the local regular multi-pair scalar response of the declared primary
static-spherical metric. It cannot select pair germs, derive a global distance metric, impose
arbitrary triangle additivity, or claim dynamics, completion, `X_max`, observations, or canon.
