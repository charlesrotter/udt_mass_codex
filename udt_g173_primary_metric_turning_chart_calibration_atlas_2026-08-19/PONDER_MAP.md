# G173 ponder map — primary-metric turning-chart calibration atlas

Date: 2026-08-19

## Whole question

G172 used areal radius itself as the ruler along a supplied pair family. That ruler is lawful only
where the radial component does not vanish. G173 asks what the primary metric actually does when a
smooth pair surface turns radially or moves purely angularly.

The whole object is

```text
primary static-spherical metric g
+ supplied smooth static time-orthogonal immersion F(x0,sigma)
    -> full pair tensor h=F^*g in an arbitrary regular sigma chart
    -> exact chart-change law
    -> classification of all scalar readouts after a nonvanishing calibration density is declared.
```

The task is not to pick a convenient new ruler. It is to determine whether the metric uniquely
supplies one, supplies an atlas of inequivalent lawful calibrations, or loses rank at the turn.

## Exact bounded regime

- declared primary static-spherical metric with supplied smooth finite `phi(r)`;
- `r>0`, excluding the spherical center;
- supplied smooth time-independent surface
  `F(x0,sigma)=(x0,r(sigma),gamma(sigma))`;
- arbitrary smooth sphere curve `gamma(sigma)`;
- time-orthogonal pair chart, with no ambient time dependence or pair shift;
- regular spatial tangent, meaning `dr/dsigma` and `dgamma/dsigma` are not simultaneously zero;
- arbitrary regular reparameterizations of `sigma`;
- scalar terminal channel only;
- no physical-family selection, global completion, nonspherical metric, time-live assembly,
  non-scalar transport, center/cut/null/singular stratum, or observational claim.

## Premise and choice ledger

- primary metric: `WORKING/DECLARED`, pinned by `SIMPLE_METRIC_MACRO.md`;
- supplied pair surface and its tangent: `SUPPLIED_CONDITIONAL`, not selected by the metric;
- static time-orthogonal class: `CHOSE_BOUNDED_CLASS`;
- arbitrary `sigma`: `FREE_AND_CHARACTERIZED`;
- areal radius and unit-sphere metric: `METRIC_OWNED` in the declared spherical slice;
- any scalar calibration density: initially `OPEN`; candidates must be constructed from declared
  metric/germ invariants and audited rather than selected for a desired response;
- pointwise `phi(r)`: `SUPPLIED_FREE_FUNCTION`;
- G167 terminal formula and G170 endpoint difference: `DERIVED_CONDITIONAL` on one consistently
  calibrated family;
- co-presence, `X_max`, G142--G160, fitting, observations, action, source, matter, bootstrap, and
  signalling: omitted and inactive.

## Observe, do not target

The calculation characterizes the tensor, coordinate-density law, regularity strata, and lawful
calibration space. It will not filter calibrations by whether they preserve a desired angular
effect or resemble observations. If more than one metric-built calibration survives, that is the
result rather than a reason to choose one.
