# G79 preregistration — one same-geometry dimensional SNe query

Date: 2026-08-11

Base: `26f90fc22271c682fe00ef350eac01b3113a5b9e`

## Whole question

Can one already-frozen G75/G77 geometry, without importing the fitted SNe P1 relation into its
metric, return a dimensionful observer-pair reciprocal depth and angular-distance readout under one
fully typed stationary source/receiver query?

This is a metric-led ownership test, not a profile fit and not a CMB-spectrum calculation.

## Frozen bounded regime

1. Select exactly one G75 geometry by the outcome-independent rule: the first data row of the
   frozen `PROFILE_ATLAS.tsv` whose `shape_id` is not `ZERO`. The selected identity and parameters
   will be reported only after this preregistration is committed.
2. Retain the exact complete stationary axial metric used by G75--G77. Its lapse, mixing profile,
   angular sector, and live coordinate couplings remain on. No term may be zeroed for convenience.
3. Retain the historical receiver position `|X|=1/4` and first outward crossing of the control
   sphere `|X|=1`. These are `CHOSE_CONTROL`; neither is a physical cosmic location, last-scattering
   surface, or `X_max`.
4. Use the outward radial member of the receiver's complete metric-orthonormal sky and the full
   resulting null path. The receiver and source germs are coordinate-stationary, future-oriented
   observers proportional to the stationary Killing field wherever it is timelike.
5. Normalize the ray by unit receiver-measured frequency. Integrate the null path, a parallel
   screen, and the full two-column Jacobi system to the registered source crossing.
6. Keep `c_E` as the observed clock/ruler calibration and `R` as a positive symbolic physical
   length. Dimensionless integration may set their numerical control values to one only after their
   powers are derived explicitly.

## Premise ledger before calculation

- UDT stationary axial metric and exact chosen profile: `pinned-by-THEORY` only in the sense of the
  frozen bounded control family, not selected physical geometry.
- `c_E`: `OBSERVED` calibration anchor.
- `R`: `free-and-explored` symbolic scale; no numerical value and no identification with `X_max`.
- receiver, source sphere, stationary endpoint observers, radial sky direction, and first crossing:
  `CHOSE_CONTROL` by this registered query.
- full nonlinear null, parallel-screen, curvature, and Jacobi equations: `pinned-by-THEORY` from the
  supplied metric and query.
- SNe P1: inactive during derivation; afterward `CONDITIONAL_COMPATIBILITY_ANCHOR_ONLY`.
- thermal source temperature and spectrum: not supplied. Only the conditional redshift multiplier
  of a supplied one-parameter thermal spectrum may be recorded.
- source state, luminosity law, photon population, opacity, polarization, detector response,
  bootstrap, action, matter source, and `X_max` value: `OPEN` and inactive.

## Derived outputs requested

Before any P1 inspection or comparison, return:

1. the stationary-observer frequency ratio and `phi_pair = log(1+z)`;
2. the exact power of `R` in the Jacobi/area readout;
3. the dimensionless angular-distance coefficient `d_A/R` for the selected path;
4. null, Killing-energy, screen-orthonormality, and Jacobi residuals;
5. a type ledger stating whether the frozen P1 distance has the same type as this `d_A` output.

Only if the types match without a new premise may a one-point, no-fit compatibility expression be
written. Otherwise the numerical comparison is blocked and the exact type mismatch is the result.

For the user's older CMB-temperature picture, record only the conditional identity

```text
T_observed/T_source = 1/(1+z) = exp(-phi_pair)
```

when a supplied thermal spectrum transforms solely by the derived frequency ratio. This does not
derive the CMB source temperature, temperature anisotropies, peak powers, or thermalization law.

## Certification contract

- deterministic profile-selection rule reproduced exactly;
- source manifest `16/16` at the frozen base;
- endpoint crossing succeeds with no nonfinite state;
- maximum null residual `< 1e-9`;
- relative Killing-energy drift `< 1e-10`;
- analytic stationary-endpoint redshift agrees with direct endpoint contraction to `< 1e-10`;
- maximum screen metric/orthogonality residual `< 1e-8`;
- `d_A/R` is finite and the `1024/2048/4096` refinement sequence is reported without retuning;
- an independently written endpoint-bundle or neighboring-ray check is required before any
  `VERIFIED` grade; otherwise bank `LEAD` or `OBSERVED_WITHOUT_INDEPENDENT_CERTIFICATION`;
- hostile catches must reject a different profile, a zeroed mixing term, an `x=1 -> X_max`
  promotion, an inserted P1 lapse/profile, a hidden numerical `R`, a redshift-sign reversal, a
  failed refinement, and a CMB-temperature/source promotion.

## Maximum conclusion

At most:

`DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY`

No physical profile, `R`, endpoint, `X_max`, source state, SNe fit, CMB temperature field, spectrum,
action, matter law, or bootstrap selector may be claimed.
