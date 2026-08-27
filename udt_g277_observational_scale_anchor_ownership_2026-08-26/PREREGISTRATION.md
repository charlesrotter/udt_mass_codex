# G277 preregistration — observational scale-anchor ownership

Date: 2026-08-26

## Frozen question

Classify the information type of Pantheon+, DES-Dovekie, and `cmb_temp` with respect to the single
constant homothety scale left by G275. Do not use fit quality or a preferred numerical answer.

## Acceptance classes

Each candidate receives exactly one primary class.

### `DIRECT_NONZERO_WEIGHT_ANCHOR`

All of the following must hold:

1. the datum is independent of metric self-evaluation;
2. the physical object/segment is identified with the modeled object;
3. its homothety weight is known and nonzero;
4. no free additive or multiplicative catalog normalization remains;
5. no unowned source, transfer, detector, or operational-distance law is needed to compare it with
   the modeled geometric quantity.

### `CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR`

Items 1--4 can hold only after an explicit observational or operational bridge is supplied. The
bridge must be named and may not be relabelled as metric-derived.

### `RELATIVE_ONLY`

An arbitrary additive/multiplicative zero point remains, or the release states a conventional
normalization that would have to be imported as physics.

### `NOT_CURRENTLY_SCALE_TYPED`

The observable is invariant under the homothety, has no declared map to a metric length, or requires
an unowned source state whose scale is degenerate with the metric response.

## Preregistered candidate tests

### Pantheon+ Cepheid-host route

Check, without fitting:

- the exact presence and typing of `CEPH_DIST` and `IS_CALIBRATOR`;
- whether the collaboration treats calibrator rows as Cepheid-host distances rather than as a
  cosmological-redshift distance;
- whether the released covariance includes Cepheid-host uncertainty;
- whether `CEPH_DIST` is a distance modulus and therefore converts to a positive physical length
  only after the published distance-ladder calibration is accepted;
- whether comparing that distance with UDT requires an optical/luminosity/areal-distance bridge.

The route is direct only if the last item is already metric-owned. Otherwise it is conditional.

### Pantheon+ noncalibrator and DES routes

Check whether an arbitrary magnitude/distance offset survives. Combining two relative releases is
not allowed to manufacture an absolute scale. DES's stated `H0=70` normalization counts as release
cargo, not as a UDT-derived anchor.

### `cmb_temp` route

Check the existing G79/G80 typing. A temperature ratio may constrain reciprocal depth only after a
source temperature and transfer law are supplied. It fixes `ell` only if a currently owned,
nonzero-weight map from that thermal datum to the same metric object exists.

### Direct clock/geometric routes

Retain G250/G276 as positive type controls. No observational instance will be invented.

## Falsification contract

Reject the proposed classification if:

- a supposedly absolute SNe route remains invariant under a joint shift of distance scale and
  magnitude zero point;
- a supposed direct metric anchor needs an unowned luminosity, detector, or distance interpretation;
- two relative catalogs are claimed to create scale merely by combination;
- `cmb_temp` is used without an independently supplied source temperature/transfer law;
- `c_E` alone is used as a length or a metric-generated value is called independent calibration.

## Evidence contract

1. exact local source hashes and column-schema checks;
2. primary collaboration documentation for every catalog-field interpretation;
3. algebraic homothety/offset-rank checks with no observational fit;
4. an implementation-distinct verifier that does not import production code or read its output;
5. hostile controls that flip each ownership criterion;
6. full premise audit before any result is banked.

## Decision table frozen before data-value inspection

| candidate | provisional expectation, not outcome | reason to test |
|---|---|---|
| Pantheon+ `CEPH_DIST` calibrators | conditional anchor | absolute host-distance information exists, but the UDT operational-distance/transfer join may remain supplied |
| Pantheon+ noncalibrators | relative-only | magnitude zero point was deliberately marginalized in G236/G237 |
| DES-Dovekie alone | relative-only | release states an `H0=70` normalization and fitted global nuisance parameters |
| two relative SNe releases together | relative-only | shared comparison can constrain shape but not create a missing zero point |
| `cmb_temp` | not currently scale-typed | source temperature and complete observation/transfer query are open |
| exact G276 clock datum | direct type control | already proved to have homothety weight `+1` when independently supplied |

No numerical value from a calibrator row, no scale estimate, and no observational goodness-of-fit
has been inspected for this decision table.
