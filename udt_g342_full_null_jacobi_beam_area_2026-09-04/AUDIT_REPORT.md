# G342 audit report — full null Jacobi and beam-area response

Date: 2026-09-04
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

Landing:
`FULL_METRIC_JACOBI_MAP_CLOSES__BOTH_SCREEN_RATES_AND_MEAN_EXPANSION_POSITIVE__SHEAR_ZERO_ONLY_ON_LONGITUDINAL_SYMMETRY_LOCUS_OR_VERTEX__EACH_COMPACT_LIFT_RETAINS_POSITIVE_AREA_WITH_PATH_LABEL__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED`

## Learned

The supplied G341 metric and source-normalized null cone uniquely give an exact diagonal
two-dimensional Jacobi map. Direct endpoint variation and an independent coordinate-curvature/RK
route agree. Both screen eigenresponses, their affine rates, the mean expansion, and the oriented
area are positive for every regular future point. Mixed and transverse rays have nonzero shear;
only the longitudinal symmetry family is shear-free. Every compact-lattice lift retains its own
positive map and explicit path label.

## Local gates

- preregistration: commit `b8d56fdd`, pushed before computation;
- production: `4720/4720` after the documented finite-axis approximation repair;
- implementation-distinct verification: `2080/2080`;
- hostile mutations: `10/10` caught;
- exact analytic global sign proof: supplied in `EXACT_DERIVATION.md`;
- external fresh adversarial review: accepted with no finding at any severity; the reviewer
  authenticated all 30 sealed payloads, reproduced every registered replay, and independently
  rederived the fixed-affine map, metric tide, Jacobi equations, global signs, and projective
  limits;
- current scientific-premise verifier: 325-row registry and historical/startup guards pass;
- repository regression suite: 220 passed, 1 expected xfail.

The initial production run's three transverse-limit misses and their bounded numerical repair are
preserved in `PREREGISTRATION_EXECUTION_NOTE.md`. No scientific formula, alternative, or threshold
was changed.

## Provenance audit

The evaluator chain is

```text
supplied four-metric -> metric null cone -> Levi-Civita curvature
-> quotient-screen tide -> two-dimensional Jacobi map
```

G188 is used only as the already classified general mathematical evaluator architecture. The
current tide and finite map were rederived from the G341 metric. No GR solution was imported at
this step; the exact spacetime remains conditional on the owner-adopted provisional vacuum arena.
No electromagnetic/light-transfer, luminosity, physical-distance, route-population, observation,
matter, scale, or `X_max` object entered.

## Maximum conclusion

This package establishes only the bounded geometric Jacobi/area classification on the exact
supplied G341 spacetime and supplied labelled null cone. The result is externally accepted within
that scope. It remains conditional on the supplied spacetime and does not select a physical
history, radiative law, route population, scale, `X_max`, or canon.
