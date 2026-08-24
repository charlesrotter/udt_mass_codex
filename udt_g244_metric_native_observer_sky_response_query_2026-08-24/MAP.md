# G244 map — metric-native observer-sky response query

Date: 2026-08-24

## Whole question

Once a complete Lorentz metric history, observer event, and regular null observation sheet are
supplied, do the already-derived G188 Jacobi operators define a coefficient-free angular response
on the observer sky, without selecting G225 transport, fitting an angular amplitude, or consulting
an observational outcome?

This is a `METRIC_LED` evaluator question. It asks what the metric does on a supplied query. It does
not ask the metric to fit a target curve or select a physical history.

## Exact bounded regime

- one supplied smooth time-oriented Lorentz metric;
- one supplied metric-unit observer at one event;
- one supplied smooth regular affine null observation sheet over a sky patch;
- G188 observer normalization and vertex-normalized matrix Jacobi map;
- finite, noncaustic endpoint: `det(D) != 0`;
- a supplied positive sky reference measure and bounded symmetric angular-bin kernels;
- one labelled regular sheet for the primary theorem; finite branch families may be retained
  branchwise but are not assigned physical weights.

## Metric-native chain

```text
complete metric
  -> Levi-Civita curvature on the supplied null sheet
  -> G188 matrix Jacobi map D
  -> observer-sky pullback tensor H=D^dagger D
  -> area A=sqrt(det H)=abs(det D)
  -> determinant-one shape C=H/A and shear power
  -> coefficient-free reference-projected geometric area query
```

All orchestra channels enter through the complete metric before `D`. No angular term is attached
after reciprocal or terminal readout.

## Premise visibility

- `pinned-by-THEORY`: the complete metric, Levi-Civita connection, G188 quotient screen, tidal
  operator, matrix Jacobi IVP, endpoint `O(2)` covariance, and G226 full-phase composition.
- `QUERY_SUPPLIED`: metric history, observer/source incidence, affine null sheet, endpoint/source
  screen, regular branch labels, reference measure, and angular-bin kernels.
- `CHOSE_CONTROL`: the normalized geometric-area projection used to test the operator algebra. It
  is not a detector or source-population law.
- `OMITTED_OPEN`: caustics and critical strata, continuous/infinite image fibers, source density,
  radiative transfer, detector selection, physical history, BOSS/CMB outcomes, and global
  completion.
- `FORBIDDEN`: fitted angular coefficients, P1, G116/G189 transfer, `X_max`, Lambda-CDM distances,
  G225 transport promotion, post-readout orchestra factors, protected work, and outcome-driven
  representation choice.

## Conclusion ceiling

At most G244 may derive a conditional, screen-gauge-invariant, coefficient-free angular response
query on a supplied regular metric/null sheet. It cannot claim a catalogue prediction, BAO or CMB
origin, physical source law, selected metric history, selected transport, or UDT validation.

