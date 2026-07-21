# Independent-amplitude metric atlas — audit report

Date: 2026-07-21

Status: `VERIFIED-WITH-CAVEATS`

Maximum conclusion:

```text
TEN_METRIC_AMPLITUDES_AND_PHI_VARIED_INDEPENDENTLY_WITHIN_REGISTERED_CONFIGURATION_DESIGN
```

## What was tested

The preceding constructive atlas moved all ten metric functions and `phi` with one shared
deformation parameter. This package releases that correlation. It assigns a separate amplitude to
each of the ten latent metric fields and an eleventh amplitude to the independent signed `phi`
field. A preregistered 60-row design is evaluated in four coefficient banks at two points per bank,
giving 480 retained configuration records.

No action, field equation, boundary condition, physical scale, carrier, empirical target, or
stability criterion is loaded. Coordinate dependence is not called physical time evolution.

## Pre-outcome design correction

The original preregistration chose contiguous `H32` columns `1..11`. The mandatory design check,
run before any geometry, found that those columns were orthogonal and rank eleven but produced only
16 distinct rows. The historical preregistration was preserved. A separate correction commit fixed
the columns to

```text
1,2,4,8,16,3,5,6,7,9,10.
```

The corrected block has 32 distinct rows and eleven exactly pairwise-orthogonal columns; its column
rank is eleven. This was a
pre-observation coverage correction, not outcome retuning.

## Load-bearing result

The finite design has metric rank ten and combined metric-plus-`phi` rank eleven. For every one of
the 480 configurations:

- the complete `210 x 10` metric-slot two-jet tangent has rank ten;
- the combined `231 x 11` metric-plus-`phi` tangent has rank eleven;
- `beta -> metric` feedback is exactly zero in the construction;
- `alpha_j -> phi` feedback is exactly zero in the construction; and
- the chart's latent-to-slot map remains regular with Lorentzian inertia `(1,3,0)`.

The lower `10 x 10` slot-value tangent has rank ten in 420 records and rank zero in the 60 records
at `P0`. This is not a contradiction. Every registered coordinate polynomial vanishes in value at
`P0`, but its derivative and Hessian jets remain live. The complete two-jet tangent restores rank
ten there. The verifier reproduces this distinction symbolically at `O00_B0_P0`.

The independent verifier does not import either atlas builder. It proves the all-record rank through
the invertible prolonged latent-to-slot map, reconstructs the `P0` tangent symbolically, and
recomputes the curved `H17_B2_P6` Riemann tensor directly. It also independently re-contracts and
ranks the saved tensors/slots for all 480 records and reconciles every geometry, family, and axis
census. The all-record numerical singular values remain builder evidence; their ranks are
independently supported by the structural proof rather than by a second finite-difference
implementation.

## Objective geometry census

All 480 records are retained. The finite census is:

| observation | count |
|---|---:|
| metric-zero records | 24 |
| metric-zero records with flat curvature | 24 |
| nonzero-metric records | 456 |
| Ricci rank four | 456 |
| curvature-operator rank six | 296 |
| shear rank two | 296 |
| twist rank one | 360 |
| nonzero mixed curvature | 456 |
| `phi` negative / near zero / positive | 158 / 44 / 278 |
| `dphi` timelike / zero / nonzero-near-null / spacelike | 76 / 176 / 0 / 228 |

The design-family decomposition adds useful contrast:

- The origin and two phi-axis families leave the metric flat.
- Every isolated metric-axis record has Ricci rank four and nonzero mixed curvature, but none has
  full curvature-operator rank six.
- Isolated latent fields `0,1,3,4,6,7,8,9` give curvature-operator rank five; isolated fields `2,5`
  give rank three in this finite family.
- Isolated fields `0,1,2` show no sampled screen shear or twist; fields `3,4,5` show rank-one shear
  without twist; shift fields `6..9` show rank-one shear and twist.
- All 256 orthogonal multi-amplitude records and all 40 fixed-metric phi-sweep records have
  curvature-operator rank six, shear rank two, and twist rank one.

These are observations about the registered basis and points. They reveal how the simultaneous
all-slot pattern decomposes when controls are separated; they are not field equations, causal
mechanisms, or evidence that one class is physically preferred.

There are 476 unique complete configuration hashes among 480 records. The four duplicate pairs are
the zero-amplitude origin evaluated at two points within each bank; its metric and `phi` are constant
there. Duplicates were retained. There are 425 unique metric two-jets because independent `phi`
sweeps intentionally repeat metrics.

## What this corrects

The shared-lambda caveat of the preceding atlas is closed inside this registered chart and function
basis. The ten metric controls now span ten independent complete-two-jet directions, and `phi` is a
separate eleventh direction.

This does not validate the stronger phrase “complete metric solution space.” It establishes an
independent local parameter chart over a finite analytic family. It does not release the chosen
factorized chart, polynomial basis, finite amplitude design, regional/global atlas, topology,
boundary, or dynamics.

## Evidence gates

1. **Preregistered:** yes; the design defect was corrected and separately committed before geometry.
2. **Full space or bounded scope justified:** bounded 60-design/4-bank/8-point local chart; no full-space claim.
3. **Load-bearing premise independently verified:** yes; structural prolonged-jet proof, symbolic anchor, and independent curvature reconstruction.
4. **Premise audit:** every registered construction choice is ledgered and checked; action, boundary, topology, scale, carrier, and global completion remain explicitly excluded rather than audited as physics.

Grade: `VERIFIED-WITH-CAVEATS`. The caveat is scope, not a failed rank gate.

## Authority stop

No UDT action, equation, selector, matter source, stability result, boundary law, scale, mass, or
universe model follows. Nothing is canonized. The next step remains an owner `PONDER` decision about
which unexamined mapping axis to release.
