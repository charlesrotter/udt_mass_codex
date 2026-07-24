# Pair-space metric-transform and SNe-readout audit

Date: 2026-07-24

Base: `148f84ea467d9716f8706c161efd45d0a381ecaa`

Preregistration: `9f34e799388d7b59539f95fc666d0d7aaed2f778`

Clerical source-hash correction:
`9d95652c70a2e43adcd80e3291aa038a2afef27f`

Grade: **VERIFIED-WITH-CAVEATS**

## Result

The three exact bounded profiles already found in the repository all define
valid bounded metric transforms when they are composed with an independently
supplied base metric:

- projective `tanh`;
- WR-L proper exponential `1-exp(-s)`;
- conditional round B19 `(2/pi)atan(sinh(2s))`.

This is a genuine structural result. A finite, uncrossed maximum pair distance
does not require a preferred center. It can arise by applying a saturating
metric-preserving transform to an unbounded base observer distance.

It is not yet a physical `X_max` derivation. All three profiles pass, and the
base metric, event pairing, profile, `kappa`, and scale `X` remain unselected.

## The important SNe clarification

The SNe success does **not** belong to the WR-L proper-distance exponential.
It belongs to a different assembly of readouts from the same WR-L lapse:

```text
clock:          1+z=exp(phi)
areal radius:   r/X=1-exp(-2phi)
optics:         d_L=(1+z)^2 r
```

Together these give `d_L/X=z(z+2)`.

The observed full-covariance replay is:

```text
WR-L areal/optical      chi2/dof 0.9098574003059212, RMS 0.15816422433950028
projective areal J1     chi2/dof 2.166501637078457,  RMS 0.3074025916996164
```

Thus the data favor the complete registered WR-L clock/areal/optical assembly
over the complete registered projective J1 assembly. They do not choose among
the abstract pair-metric transforms.

This gives precise content to the suggestion that several effects overlap:
the clock, radial length, areal radius, and optical distance are distinct
faces of one metric. Combining the correct faces is physically load-bearing;
counting one face twice or substituting proper distance for areal distance
changes the prediction.

## Candidate disposition

- `WRL_AREAL_OPTICAL`: observed near the SNe data under its registered
  conditional static premises.
- `PROJECTIVE_AREAL_J1`: observed shape failure under its registered complete
  comparator premises.
- `WRL_PROPER_PAIR_TRANSFORM`: valid conditional pair metric; not an SNe law
  without a new optical identification.
- `B19_ROUND`: valid conditional pair transform; no clock/redshift/optical
  solder and therefore not scored.
- `FC12`: free profile; compatible by choice, not selected.
- conditional temporal-phi separation family: supplies a possible base
  observer distance only on its stated branch; full cosmological readout open.
- retired `P_ell`: excluded.

## What is learned

1. Bounded pair distance is mathematically compatible with no preferred
   center.
2. Metric-transform validity does not select the positional law.
3. Saturated pair comparison is generally nonlocal and is not ordinary
   integrated path length.
4. The strong SNe clue is branch-assembly-specific: it points to WR-L's
   joined clock, areal, and optical readouts.
5. BAO, CMB anisotropy, the CMB dipole, and black-hole behavior are not
   consequences of this result. They remain future independent tests if a
   global branch is derived.

## Remaining gate

The smallest missing object is no longer “some bounded formula.” It is a
metric-derived, center-free two-observer optical construction that determines
in one structure:

- which events on two observer histories are compared;
- the base observer-rest separation;
- clock comparison;
- angular/area transport and cut-locus behavior;
- whether its supremum is the physical `X_max`.

The WR-L SNe result is a strong calibration clue for that construction, but
must not be used to impose it.

## Authority boundary

No universal profile, global `X_max`, BAO/CMB/black-hole explanation, action,
source, carrier, boundary, density response, or mass law is derived here. No
GPU work, canonization, or repository reorganization was performed.
