# G69 external-review adjudication

Date: 2026-08-11

External landing: `VERIFIED_AS_BOUNDED`.

Effective evidence state: `EXTERNALLY_VERIFIED_AS_BOUNDED`.

The original reviewed package remains frozen by `REVIEW_MANIFEST.tsv`. This additions-only layer
supersedes only its historical `EXTERNAL_REVIEW_PENDING` status; it changes no atlas, equation,
control, numerical result, or scientific scope.

## What the reviewer independently reproduced

- all `37/37` manifest rows and the sealed `38`-file intake;
- `21` profiles, `15` endpoints, `315` profile/endpoint maps, `15` sensitivity matrices, and `945`
  covariance controls, with no missing or duplicate cell;
- production PCHIP replay at `1.9259e-34` relative, official `x=1` endpoint replay at
  `3.7444e-16`, and PCHIP/CubicSpline disagreement at only `1.0141e-10`;
- exact F01 zero anisotropy and zero polar rotation, with minimum map singular value
  `0.04961347467704763`;
- all `15/15` sensitivity cells as `FULL_RANK_OBSERVED`, with normalized
  `sigma_min/sigma_max` from `4.6381e-4` to `1.4965e-2` and condition numbers from `66.8237` to
  `2156.0777`;
- the rank persists under the reviewer's raw-matrix and separate-amplitude challenges, so the
  registered midpoint and normalization conventions did not manufacture it;
- exact invertible-map covariance congruence, with maximum reconstruction relative error
  `2.8305e-16` and minimum constructed source eigenvalue `1.56159`.

## Exact status ledger

- `DERIVED`: `D_AB=E_A^mu g_mu_nu J_B^nu` on the supplied saved state; covariance congruence
  `C_obs=D C_src D^T`; positive-definite preservation for invertible `D`; rank obstruction for a
  singular `D`.
- `OBSERVED`: the bounded census, interpolation agreement, invertibility, numerical sensitivity
  ranks, conditioning, and replay residuals above.
- `CHOSE_CONTROL`: profiles, endpoint grid, control tile, readout channels, midpoint/secant rules,
  column normalization, thresholds, and algebraic covariance examples.
- `CONDITIONAL`: later coefficients may be anchored only after source/state, endpoint/profile, or
  independent-channel ownership restricts the exact compensation freedom, with at least one
  genuinely independent holdout.
- `OPEN`: physical CMB profile, physical endpoint or last-scattering surface, source/state,
  TT/TE/EE/BB spectra, polarization transport and population law, action, bootstrap, `X_max` value,
  and signalling law.

## Wording guard

The package's independent route is an independent reconstruction and algebra check on the same
frozen G68 paths. It is not independent geodesic or Jacobi path integration. The sealed reviewer
did independently replay the load-bearing saved-state algebra and numerics.

The three-channel rank result uses azimuthal carry. Removing that channel leaves a `2 x 3` map and
therefore cannot identify all three controls. Scalar TT does not automatically observe that third
channel.

## Authority boundary and next gate

The bounded landing remains
`GEOMETRICALLY_SEPARATING__OBSERVATIONALLY_SOURCE_DEGENERATE`: this frozen geometric instrument
distinguishes its three registered control directions locally, while an unrestricted local source
covariance can absorb every invertible `2 x 2` screen map. This is not a full-CMB no-go and selects
no physical model.

The next justified metric-led question is an ownership atlas: determine which restrictions on the
source/state, endpoint/profile, or independently read observation channels are already supplied by
the complete typed query and geometry. Only then may a small preregistered observational parameter
set be introduced with held-out tests. No fit or FD2 restart is authorized by this review.

## Evidence gates

1. Preregistered: yes (`8b7340cb`, with precalculation clarification `88ab9381`).
2. Full/bounded: full over the declared 21-by-15 saved control universe; explicitly not global.
3. Independent: internally reconstructed and now cold externally replayed on the sealed intake.
4. Premises: audited; every physical CMB owner remains conditional or open as stated above.

