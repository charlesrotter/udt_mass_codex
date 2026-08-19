# G172 ponder map — smooth primary-metric pair families

Date: 2026-08-19

## Whole question

Starting only from the declared primary static-spherical metric, determine whether the local
pair-germ response verified in G171 persists coherently along a smooth changing-separation family.
The metric must construct every pair pullback before terminal reciprocal readout.

The tested architecture is

```text
primary static-spherical metric g
+ one supplied smooth time-orthogonal pair family
+ metric-owned areal-radius calibration on the dr != 0 stratum
    -> smooth rank-two pullback h(r)
    -> pair incidence density Phi(r)
    -> endpoint response delta(r1,r2)=Phi(r2)-Phi(r1).
```

This is not a search for a preferred path, dynamics, an observational fit, a universal observer
potential, or an `X_max` profile.

## Exact bounded regime

- declared primary static-spherical four-metric with arbitrary supplied smooth finite `phi(r)`;
- dimension-matched static time coordinate `x0=c_E t`;
- smooth time-independent pair surfaces `F(x0,r)=(x0,r,gamma(r))` on an interval with `r>0`;
- arbitrary smooth angular curve `gamma:I->S2`, retained through its full unit-sphere speed;
- nonzero radial component, uniquely calibrated by the areal radius so `dr(s)=1`;
- regular Lorentzian pullbacks only;
- center approached only as a one-sided limit; no center-smoothness theorem;
- no pure-angular/turning-point, null, singular, cut, topology-changing, nonspherical,
  ambient-time-dependent, micro, or global-completion claim.

## Premise and choice ledger

- primary metric: `WORKING/DECLARED`, pinned by `SIMPLE_METRIC_MACRO.md`;
- areal radius: metric-owned in the declared spherical slice;
- static time-orthogonal surface form: `CHOSE_BOUNDED_CLASS`, not a universal pair family;
- monotone areal-radius parameterization: `DERIVED_CALIBRATION` on the `dr(s)!=0` stratum after
  choosing outward orientation;
- `phi(r)`: `SUPPLIED_FREE_FUNCTION`; no profile equation or value is inserted;
- `gamma(r)`: `FREE_AND_CHARACTERIZED`; no angular curve or coefficient is selected;
- terminal readout and endpoint difference: `DERIVED_CONDITIONAL` from G167/G170/G171;
- co-presence, G142--G160 scaffolding, `X_max`, action, source, matter, bootstrap, observations,
  radiative transfer, and signalling: omitted and inactive.

## Completeness boundary

This is one kinematic tile: static spherical ambient metric, time-orthogonal monotone-radial pair
families, scalar terminal channel. Dropped sectors—time-live pair shift, radial turning points,
pure-angular families, general ambient mixing, non-scalar transport, singular strata, and physical
family ownership—could contain additional structure and remain explicit blind spots.
