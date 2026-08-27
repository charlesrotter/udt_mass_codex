# G278 audit report — Cepheid scale attachment and DES holdout

Date: 2026-08-27

Grade: `INTERNALLY_VERIFIED__FRESH_EXTERNAL_REVIEW_PENDING`

## Landing

```text
SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE
```

The exact failing control is resolution sensitivity; the calibrator-subset and covariance-
serialization controls pass.

## What was learned

The Cepheid-host route does identify one positive homothety scale at every frozen G236 numerical
resolution without changing the relative state. The primary `K=12` result is

\[
M=-19.24888454,
\qquad
a=5\log_{10}(\ell/\mathrm{Mpc})=12.28378313\pm0.03900777,
\]

or, under the supplied Cepheid ladder and transparent-transfer bridge,

\[
\ell=286.2573\ \mathrm{Mpc}
\]

with a local delta-method one-sigma scale uncertainty of `5.1423 Mpc`.

The calibrator residual is regular:

```text
chi2_cal = 57.1347
dof_cal  = 76
ceiling  = 137.6441
```

The full two-column design has rank two, the reduced covariance is positive definite, all 46
registered calibrator selections pass, and the largest subset displacement is `3.1115` of its
exact common-data standard deviation. Reflected lower/upper covariance serialization changes the
scale coordinate by at most `3.57e-8 mag`, far inside the `1e-4 mag` gate.

The four frozen numerical resolutions give:

| K | ell (Mpc) | local delta-method sigma (Mpc) |
|---:|---:|---:|
| 8 | 299.2588 | 4.9983 |
| 12 | 286.2573 | 5.1423 |
| 16 | 282.3532 | 5.3112 |
| 24 | 279.0210 | 5.5867 |

Their exact correlated comparison gives `chi2=60.4054` against the preregistered ceiling
`15.2474` for rank three. Therefore G278 does not own one resolution-independent numerical scale.

## Held-out DES result

No DES parameter was fitted. At the primary resolution,

```text
chi2_DES = 1434.5793
dof_DES  = 1623
ceiling  = 1907.8684
```

All four registered resolutions pass that same no-retuning adequacy rule. The primary raw residual
mean is `+0.1759 mag`, proving that the check did not silently force a DES offset to zero.

This is a conditional cross-release consistency result, not an independent UDT scale measurement:
the DES `MU` column carries the collaboration's published `H0=70` normalization, and the optical
transfer remains imported.

## What did not change

- the metric and completed-pair reciprocal kernel are unchanged;
- `phi=log(1+z)` remains the direct redshift channel;
- no G236 state coefficient was changed by a calibrator row;
- no DES offset, scale, state, or kernel coefficient was fitted;
- no `P1`, angular coefficient, post-readout orchestra, Lambda-CDM distance, or `X_max` entered;
- no complete history or CMB interpretation was selected.

## Verification

- outcome-blind preregistration committed and pushed at `8366e111`;
- 10/10 frozen source hashes pass;
- all four symmetric-mean G236 state reconstructions reproduce their frozen coefficients within
  `6.49e-13` (gate `1e-10`);
- a direct-NumPy implementation independently reproduces all four scale values to
  `3.20e-13 mag`, the resolution statistic to `1.11e-10`, and the primary DES score to
  `6.9e-13`;
- all ten independent checks pass;
- all eight hostile non-vacuity controls pass;
- the full 260-row premise registry passed immediately before production;
- fresh external adversarial review remains pending.

## Honest interpretation

This is a strong positive lead for the route, not a final calibrated UDT length. It shows that the
native relative curve can be given an observational absolute normalization and can pass a second
SNe release without retuning. It also shows that defining `ell` at the sparsely constrained first
knot leaves a material numerical-resolution dependence.

The outcome-informed follow-up is preregistered separately. It asks whether the sensitivity is
mostly confined to that boundary normalization or persists through the physical absolute-radius
curve. It may not regrade this landing.

## CMB-temperature route retained for later

With a supplied mean source temperature `3000 K` and observed temperature `2.725 K`, the direct
thermal relation is simply

\[
1+z_T=3000/2.725\simeq1100.9,
\qquad
\phi_T\simeq7.00.
\]

G278 does not use that relation to choose or repair its scale.
