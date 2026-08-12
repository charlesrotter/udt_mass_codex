# Fresh adversarial review

Date: 2026-08-12

Reviewer context: fresh, read-only subagent with no inherited conversation or package conclusions.

Verdict: **VERIFIED WITH CAVEATS**

## Independent return

The reviewer rederived the determinant, forward terminal map, inverse Gram reconstruction,
necessary-and-sufficient reachability inequality, rank strata, coordinate projections, and
factorization fibers. It then ran fresh exact arithmetic:

```text
forward PSD cases                         2,279
Lorentzian / degenerate / positive        1,366 / 19 / 894
A-terminal / nonterminal                  948 / 1,331
independent admitted inverse targets      776
inverse ranks zero / one / two            1 / 21 / 754
Loewner-order comparisons                 7,050
nonzero comparable increments             6,815
nonzero increments strictly raising phi   6,815
stored atlas rows replayed                 324 / 324
```

A second fresh exact reviewer independently reproduced the same theorem, including the subtle
`h00=0` Lorentzian stratum, the full coordinate projections, the factorization fibers, and the
strict Loewner-order result while the A chart persists. It found no additional correction.

## Required corrections applied

1. Reciprocal-depth monotonicity is stated only for additions remaining in the same A-terminal
   chart; outside that chart the A-terminal `phi` readout is unavailable.
2. The hostile base test now checks the uniquely reconstructed zero Gram matrix and rejects a
   shifted impostor, rather than merely confirming that the base is reachable.
3. Congruence covariance is separated from calibration dependence: completed `h`, inertia, and
   Gram rank are covariant; terminal coordinates and the inequality answer the declared
   A-calibrated query.
4. The package makes no claim about a physical history, branch, material signal, `X_max`, dynamics,
   or cosmology.

## Caveat retained

The exact rational generator was not frozen in preregistration. The analytic theorem is therefore
load-bearing; the rational atlases are broad exact regression evidence. The theorem covers the
entire pointwise `PSD(2)` image for one symbolic A-calibrated base, not derivative or global
solution space.
