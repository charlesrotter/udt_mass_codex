# G81 preregistration — nonradial and endpoint-screen covariance controls

Date: 2026-08-12

Base: `f112a32e4fbc5319de4e964e869f9024e9bdb1b9`

Status before calculation: `PREREGISTERED__NO_OUTCOME_INSPECTED`

## Whole bounded question

On the exact frozen G79/G80 stationary metric, does reverse ordered-pair Jacobi reciprocity retain
its covariant form when (a) the null ray has live radial, polar, and azimuthal components and (b)
the reverse source screen and receiver projection screen are independently rotated?

This is a metric-led covariance stress test. It characterizes two declared observer-query
controls. It does not select a profile, endpoint, direction, screen, scale, source, or observable.

## Exact frozen universe

The universe contains exactly the two rows in `CONTROL_UNIVERSE.tsv`; no direction, rotation,
endpoint, or tolerance may be changed after either outcome is inspected.

Common metric and query:

```text
profile                    G75_AM_S01_E05
A(x)                       1-x^2/4
h(x)                       x^6/20
receiver                   x=1/4, theta=pi/2, psi=0
endpoint event             first outward x=1 crossing
forward normalization      receiver frequency = 1
reverse tangent            k_reverse = -k_source/Z
```

At the receiver use the stationary-observer orthonormal spatial triad
`(e_r,e_theta,e_psi)` already defined by the frozen G68 engine.

- `C0_RADIAL_ROTATED`: `n=(1,0,0)` with forward screen `(e_theta,e_psi)`.
- `C1_FULL_ANGULAR`: `n=(12,3,4)/13`. Its forward screen is
  `s1=(0,4,-3)/5` and `s2=(-5/13,36/65,48/65)` in the same triad. These vectors are an exact
  oriented orthonormal basis perpendicular to `n`.

The reverse initial source screen and the independent receiver projection screen are fixed as

```text
A = [[3/5,-4/5],[4/5,3/5]]
B = [[5/13,-12/13],[12/13,5/13]].
```

Both are orientation-preserving orthogonal controls. They are `CHOSE_CONTROL`, not physics.

## Exact identities under test

For each control that reaches the registered endpoint regularly, production must test

```text
Z_reverse = 1/Z_forward
phi_reverse = -phi_forward
D_reverse_unrotated = Z_forward transpose(D_forward)
D_reverse_AB = Z_forward B transpose(D_forward) transpose(A)
d_A_reverse/d_A_forward = Z_forward.
```

Here `D_reverse_AB` is built from Jacobi fields seeded by `A` times the carried source screen and
projected at the receiver onto `B` times the original receiver screen. The unrotated and rotated
relations are separate checks; rotation may not be absorbed by diagonalizing `D`.

## Premise and parameter ledger

| Item | Status | Ownership |
|---|---|---|
| reciprocal clock/ruler character and `c_E` calibration | `DERIVED` / `OBSERVED` | current premise registry |
| stationary axial metric/profile | `CHOSE_CONTROL` | frozen G79/G80 control, not selected physics |
| receiver and endpoint surfaces | `CHOSE_CONTROL` | numerical comparison query, not `X_max` |
| two direction rows | `CHOSE_CONTROL` | exact bounded covariance probes |
| screen rotations `A,B` | `CHOSE_CONTROL` | gauge probes only |
| past-directed affine reversal | `CHOSE_QUERY` | mathematical reversal, not signal |
| DOP853, tolerances, step ladder | category-A numerical method | soundness controls, not physics |
| source, scale `R`, `X_max`, SNe/CMB observable | `OPEN` | absent from the calculation |

No matter, action, bootstrap, source, fit, thermal field, or signalling law enters.

## Numerical and independent-verification contract

Production uses DOP853 with `rtol=2e-13`, `atol=2e-15`, and the exact maximum-step ladder
`1/1024`, `1/2048`, `1/4096`. A crossing branch is certified only if:

- forward and reverse integrations reach their registered endpoint events;
- maximum endpoint return is below `1e-8`;
- frequency-product, tangent-return, and carried-screen-return residuals are below `1e-8`;
- both unrotated and rotated matrix-reciprocity residuals are below `1e-8`;
- the area-ratio residual is below `1e-8`;
- null, screen-Gram, screen-ray, and Wronskian residuals retain the G80 registered bounds;
- refinement is reported without choosing the most favorable row.

The independent route must rebuild first metric derivatives and Christoffels directly, integrate
central plus finite-difference neighboring rays in both orientations, and must not call the
production Riemann/Jacobi equation. Its registered matrix/area tolerances are `2e-4`.

If `C1_FULL_ANGULAR` does not reach `x=1`, turns, crosses a coordinate singularity, or develops a
caustic, it is classified exactly as observed. Its direction may not be replaced. C0 cannot be
used to claim a nonradial result.

## Catch-proof contract

The final verifier must reject: a missing/duplicate control; a changed direction or rotation;
partial instead of full tangent reversal; omitted `Z`; omitted transpose; omitted `A` or `B`;
silent diagonalization; future-signal wording; a retuned nonradial row; a physical-profile,
endpoint, `X_max`, source, or observable promotion; and mutation of any frozen source.

## Maximum conclusion

If both controls pass all gates:

`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`

This means only that generic Jacobi/Wronskian reciprocity is represented covariantly by the
declared complete-metric observer queries. It is not a UDT-specific selector, physical profile,
endpoint law, `X_max` relation, SNe/CMB result, source, action, matter, bootstrap, or signalling
law. A one-control outcome is reported only for that control.
