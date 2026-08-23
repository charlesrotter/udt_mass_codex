# G237 audit report — joint dual-SNe relational-state freeze

Date: 2026-08-23

## Landing

```text
JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS
__BLOCK_DIAGONAL_CROSS_RELEASE_COVARIANCE_CHOSEN
__NO_PROFILE_LAW_PREDICTION_OR_HELDOUT_VALIDATION
```

## What was learned

The two G236 processed SNe projections can be assembled into one covariance-weighted relative state
on their common depth interval without introducing P1, `X_max`, a Lambda-CDM distance curve, a
physical-profile optimizer, smoothing, monotonicity, or a post-readout angular correction.

The primary `K=12` joint raw residual is

\[
\chi^2=2145.8547911347\quad\text{for}\quad2378\text{ degrees of freedom},
\]

below the preregistered conservative ceiling `2722.818793`. The `K=8,16,24` numerical-resolution
controls also pass.

The primary state is frozen in `FROZEN_PRIMARY_K12_STATE.json` for a future separately typed
held-out query. It may not be refit there.

## What was not learned

G237 does not derive a physical `R(phi)` law, predict SNe, select a complete metric history, derive
native radiative transfer, determine an absolute scale or `X_max`, or validate UDT against BAO/CMB.
It also does not prove the releases statistically independent. Their unavailable cross-release
covariance is set to zero only after exact-CID de-overlap, with shared calibration and processing
systematics retained as an explicit caveat.

The four knot counts are numerical grids. They are not four physical families and do not license
interpolation as a law.

## Evidence and external review

- preregistration committed and pushed before computation at `ad49b9c8`;
- all seven frozen G236 source hashes pass;
- saved-estimate Cholesky combination and independent raw simultaneous GLS agree to
  `6.40e-13` in state coordinates, `2.78e-17` in covariance entries, and `2.47e-10` in raw
  chi-square;
- the exact joint-raw decomposition identity has zero recorded residual;
- all four resolution controls pass the raw-residual ceiling;
- duplicate, release-swap, weak-catalog, and five validator-mutation controls pass;
- no optimizer, P1 value, or `tanh` profile enters either implementation.

Fresh external `gpt-5.4` review accepted the scientific core and found no scientific, type,
source-provenance, or hidden-fit failure. It required one wording repair and one self-contained
chronology-replay repair. Both are implemented under `REPAIR_PREREGISTRATION.md`:

- the lay report no longer calls the releases statistically independent;
- a minimal raw Git object bundle now proves the commit-to-preregistration chain without live Git;
- the review-intake builder is included in the payload;
- the independent machine artifact now carries the full chosen-covariance caveat.

`REPAIR_CERTIFICATION.json` proves that the three frozen primary artifacts are byte-identical and
that the independent artifact changed only in its covariance-premise label.

## Current grade

```text
EXTERNALLY_VERIFIED_WITH_CAVEATS
__G237_REPAIRS_ACCEPTED
__SCIENTIFIC_LANDING_RETAINED
```

## Next gate

The frozen state is now bankable. Define one independently typed held-out query before reading its
outcome, then carry the primary `K=12` state without refitting. BAO and CMB still require their own
source/operator typing; neither is silently licensed as a standard ruler or acoustic scale.
