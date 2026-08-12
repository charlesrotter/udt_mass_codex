# G80 preregistration — reverse ordered-pair reciprocity on the G79 control

Date: 2026-08-11

Base: `e5a4a652a62c77d41bb26e7e0d662ebba97fdd41`

## Whole question

On the exact G79 metric, endpoint pair, and null branch, does reversing the ordered comparison and
renormalizing at the former source reproduce the inverse endpoint frequency ratio and the
transpose/rescaling law of the complete two-column Jacobi map?

This is a metric-led consistency test of one already-chosen control query. It is not a new profile,
endpoint, fit, `X_max`, CMB-temperature, or signalling calculation.

## Frozen bounded regime

1. Retain `G75_AM_S01_E05` exactly: `A=1-x^2/4`, `h=x^6/20`.
2. Retain the G79 endpoint pair `x_r=1/4`, `x_s=1`, equatorial radial sky branch, complete angular
   mixing, and full nonlinear null/screen/Jacobi equations.
3. Reproduce the G79 forward solve first. At its endpoint, define the reverse mathematical branch
   by the full affine tangent `k_rev=-k_s/omega_s`, not by flipping only a spatial component.
   This is the past-directed reversal of the same spacetime curve, normalized to unit source
   frequency magnitude. It is not a future-directed material signal.
4. Initialize the reverse parallel screen with the transported forward endpoint screen, and the
   reverse Jacobi columns with `J=0`, covariant derivative `P=E`.
5. Integrate to the first inward crossing of `x=1/4` with fixed DOP853 controls and the
   `1024/2048/4096` maximum-step ladder.
6. Keep `c_E` as the observed clock/ruler calibration and `R` symbolic. The numerical calculation
   may use dimensionless units only after the scale powers are stated.

## Preregistered identities and gates

Let the G79 forward quantities be `Z=1+z=omega_s/omega_r` and `D_f`. For the reverse branch,
preregister:

```text
omega_r^(rev)/omega_s^(rev) = 1/Z
phi_rev = -phi_f
D_rev = Z transpose(D_f)
d_A_rev/R = Z (d_A_f/R)
```

The last two identities are the affine-normalized Jacobi reciprocity prediction in the forward and
reverse parallel-screen bases. A basis-orientation sign may occur only if explicitly traced to a
screen reflection; absolute area must still obey the registered positive ratio.

Certification thresholds:

- both endpoint crossings succeed with finite state and no post-origin caustic;
- reverse endpoint coordinate mismatch `<1e-8` after accounting for the original endpoint values;
- maximum null residual `<1e-9`;
- relative Killing-energy drift `<1e-10`;
- maximum screen Gram/ray residual `<1e-8`;
- reciprocal frequency-product error `<1e-10`;
- `|phi_rev+phi_f|<1e-10`;
- reverse-screen return relative error `<1e-8`, allowing only an explicitly reported orientation
  matrix;
- full Jacobi reciprocity relative error `<1e-8` in the production route;
- `1024/2048/4096` results reported without retuning;
- a separately written direct-Christoffel neighboring-ray reverse check must agree to `<2e-4`
  before any verified grade.

Hostile catches must reject: spatial-only reversal; missing source-frequency normalization; the
wrong redshift ratio; omitted transpose; omitted factor `Z`; zeroed mixing; `x=1` promotion to
`X_max` or last scattering; future-signal language; P1 insertion; and `cmb_temp` activation.

## Scope not covered

No other profile, ray direction, endpoint, source/receiver worldline, cut-locus branch, time-live
geometry, physical `R`, `X_max` curve, luminosity law, SNe fit, source population, CMB field,
action, matter source, bootstrap rule, or local signalling law is tested.

## Maximum conclusion

At most:

`DERIVED_CONDITIONAL_RECIPROCITY_ON_ONE_FROZEN_GEOMETRY_AND_ONE_ORDERED_PAIR`

If any registered identity or independent gate fails, bank the scoped failure without changing the
metric or tolerances.
