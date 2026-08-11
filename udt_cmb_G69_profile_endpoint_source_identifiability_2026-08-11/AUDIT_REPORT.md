# G69 profile–endpoint–source identifiability atlas — audit report

## Landing

`GEOMETRICALLY_SEPARATING__OBSERVATIONALLY_SOURCE_DEGENERATE`.

Evidence state: `INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.

Within the complete registered three-channel geometric readout, endpoint position, lapse profile,
and mixing amplitude are locally independent in all `15/15` preregistered sensitivity cells. But
an unrestricted source covariance can exactly compensate every invertible geometric map. The
metric instrument distinguishes the controls; the currently unowned source prevents a sky
covariance from selecting them.

## Main observations

- All `21 x 15 = 315` saved profile/endpoint cells were reconstructed without a new ODE solve.
- The PCHIP and independently coded cubic-spline maps agree to `1.0141e-10` relative.
- The official G68 endpoint maps replay to `3.7445e-16` relative.
- Every map is invertible; minimum singular value is `0.0496135`.
- All `15/15` three-channel sensitivity matrices are `FULL_RANK_OBSERVED` under the frozen rule.
- The rank is often poorly conditioned: normalized condition numbers span `66.82` to `2156.08`.
- All `945/945` source-covariance constructions replay with maximum relative error
  `2.8306e-16` and remain positive definite.
- No observational anchor, fit, new coefficient, ODE solve, eigensolve, or GPU process was used.

## What this means

The G68 profile effects are not merely one generic blur: inside the complete geometric instrument,
changing the endpoint, lapse, or mixing amplitude points in a different local direction. That is
useful structure.

It does not yet identify the real universe. An unknown source pattern can be reshaped so that
different geometric maps produce the same observed local covariance. Scalar TT also does not
directly read every channel used in the full-rank test. A later observational anchor can constrain
a small coefficient set only after the source/state and channel ownership are typed tightly enough
that this exact compensation freedom has been reduced.

## Four evidence gates

1. **Preregistered:** yes, at `8b7340cb`; sensitivity conventions clarified before calculation at
   `88ab9381`.
2. **Full or bounded:** complete over the exact 21 saved profiles, 15 endpoints, 315 maps, 15
   sensitivity cells, and 945 covariance reconstructions. It is not all profiles, queries, or
   source models.
3. **Independent:** a separate explicit metric/readout implementation using cubic splines instead
   of PCHIP reproduces all cells and the covariance identity. Both routes share the frozen G68 path
   samples; fresh semantic external review remains pending.
4. **Premises:** audited. Every profile, endpoint, covariance example, and rank convention is a
   declared control. Physical profile, endpoint, source/state, spectrum, and coefficients remain
   `OPEN`.

## Authority boundary

This is a local identifiability result for a bounded control tile and a `2 x 2` screen-covariance
identity. It does not select last scattering, `X_max`, a CMB profile, a source covariance, a peak,
TT/TE/EE/BB power, polarization, an action, bootstrap closure, time-live history, or local signal
physics. It does not prove that full CMB data are globally non-identifying.

## Next gate

Adversarially review the finite-tile rank and the exact source-covariance theorem. If they survive,
the next metric-led question is which restrictions on source/state or endpoint/profile are already
owned by the complete query and geometry. Only after that ownership map may a small preregistered
set of observationally anchored coefficients be introduced, with held-out channels.
