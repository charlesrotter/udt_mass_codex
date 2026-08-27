# G278 resolution follow-up report

Date: 2026-08-27

Status: `OUTCOME_INFORMED_DIAGNOSTIC`

Landing:

```text
PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS
```

The original G278 landing remains unchanged.

## Result

All three interior-90% RMS differences are smaller than their full-support values, but none of the
maximum differences lies in the excluded outer five-percent boundary bands. The maxima instead
occur at support fractions `0.818`, `0.933`, and `0.826`. Thus the first-knot scale coordinate is
not the whole problem.

Against `K=12`:

| K | full RMS (mag) | interior RMS (mag) | max abs (mag) | midpoint abs (mag) | midpoint z |
|---:|---:|---:|---:|---:|---:|
| 8 | 0.0650 | 0.0612 | 0.2368 | 0.00159 | 0.184 |
| 16 | 0.0328 | 0.0322 | 0.1560 | 0.00908 | 1.082 |
| 24 | 0.1040 | 0.0911 | 0.4771 | 0.02081 | 1.186 |

The fixed midpoint is comparatively stable. The upper-depth reconstruction is not: `K=24` moves
farther from `K=12` than `K=16` does, and the consecutive `K=16` to `K=24` RMS is `0.1024 mag`.

## Interpretation ceiling

G236 deliberately used unregularized piecewise-linear hats as a numerical observational
reconstruction, not a physical profile. G278 now shows that this flexible reconstruction cannot be
promoted into a unique calibrated native UDT curve by selecting a knot count. No preferred `K`,
smoothing penalty, averaged scale, or new fit is authorized.

The diagnostic does not challenge the metric-native projective state or direct redshift law. It
narrows the next conceptual gate: determine whether the provisional projective physical position
has a metric-owned identification with the SNe areal/optical distance channel. If it does, its exact
dimensionless shape should replace the nonparametric G236 reconstruction in the one-scale test. If
it does not, that identification must remain an explicit conditional bridge rather than being
smuggled in as a numerical curve choice.
