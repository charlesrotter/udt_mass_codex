# G237 preregistration — joint dual-SNe relational-state freeze

Date: 2026-08-23

## Question and bounded regime

Given the externally retained G236 Pantheon+ and DES finite-resolution relative-state estimates,
construct their one common state under the same bounded central-static query and imported
transparent-transfer bridge. Freeze the primary `K=12` state for a later, separately typed held-out
query. Do not infer or fit a physical `R(phi)` law.

This is an observational state assembly, not a metric solve. The solved interval is exactly the G236
common support

```text
phi in [0.07077528204904217, 0.7627571949083936]
z in [0.07334, 1.14418]
```

with 768 de-overlapped Pantheon+ rows and 1,623 DES-only rows.

## Fixed inputs and premise tags

- `DERIVED_CONDITIONAL`: G236 transformation
  `m-10log10(1+z)=5log10R(phi)+catalog_offset`.
- `OBSERVED_PROCESSED_CONDITIONAL`: G236 shape estimates and within-release covariances.
- `CHOSE_NUMERICAL_RESOLUTION`: `K=12` primary and `K=8,16,24` controls, inherited from the
  pre-outcome G236 registration. These are measuring grids, not physical coefficients.
- `CHOSE_STATISTICAL_APPROXIMATION`: after exact-CID de-overlap, the unknown Pantheon–DES
  cross-release covariance is set to zero. This is not derived independence; shared calibration and
  processing systematics remain open.
- `FREE_AND_NOT_FIT`: one additive zero-point per release. Absolute `R` normalization remains open.
- `OMITTED`: P1, `X_max`, Lambda-CDM distance functions, physical-profile optimization, smoothing,
  monotonicity, post-readout angular correction, BAO/CMB outcomes, time-live/nonspherical sectors,
  and protected packages.

## Frozen construction

For each preregistered resolution, let the two relative-state estimates be
`theta_P, C_P` and `theta_D, C_D`. With the declared zero cross-release covariance,

```text
P_J = inverse(C_P) + inverse(C_D)
C_J = inverse(P_J)
theta_J = C_J [inverse(C_P) theta_P + inverse(C_D) theta_D].
```

The displayed inverse notation specifies the algebra; implementations must use stable solves or
factorizations. The relative ruler state at a knot is the derived display

```text
R(phi_i)/R(phi_min) = 10**(theta_J[i]/5).
```

No interpolation between knots is promoted to a physical law.

## Preregistered certification contract

1. Every frozen G236 source hash passes.
2. Each input and joint covariance is symmetric positive definite.
3. The minimized two-estimate quadratic equals the G236 shape-difference chi-square within `1e-8`.
4. A separate direct raw-data simultaneous GLS—with one common shape and two release offsets—agrees
   with the saved-estimate construction within:
   - `1e-8` for every relative-state coefficient;
   - `1e-8` for every covariance entry;
   - `1e-7` for joint raw chi-square.
5. Direct joint raw chi-square equals Pantheon raw chi-square plus DES raw chi-square plus the G236
   shape-disagreement chi-square within `1e-7`.
6. Duplicate-input, release-swap, and large-covariance-limit algebraic controls pass.
7. The output contains exactly 56 non-anchor state rows and an immutable primary `K=12` freeze.
8. No BAO/CMB outcome, P1, `X_max`, physical-profile optimizer, smoothing, or monotonicity gate enters.

Failure of a numerical or algebraic gate returns `IMPLEMENTATION_OR_ASSEMBLY_FAILURE`. Failure of
the cross-route agreement returns `JOINT_STATE_RECONSTRUCTION_MISMATCH`. Neither failure authorizes
a new physical mechanism or retuning.

## Maximum conclusion

At most:

```text
JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS
__BLOCK_DIAGONAL_CROSS_RELEASE_COVARIANCE_CHOSEN
__NO_PROFILE_LAW_PREDICTION_OR_HELDOUT_VALIDATION
```

The calculation cannot derive the universe's profile law, native radiative transfer, absolute
scale, observer population, physical history, `X_max`, or agreement with BAO/CMB.
