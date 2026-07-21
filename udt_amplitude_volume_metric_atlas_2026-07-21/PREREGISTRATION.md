# UDT amplitude-volume metric atlas — preregistration

Date: 2026-07-21

Base: `32184b9648437d2c6954174914e0c4ff02f848c9`

Branch: `codex/udt-amplitude-volume-atlas-2026-07-21`

Mode: CPU-only deterministic configuration mapping. No action, EOM, ODE/PDE solve, relaxation,
physical evolution, ensemble interpretation, desired geometry, comparison target, or GPU work.

## Owner direction and ordering

Charles asked whether raw mapping remained before organizing the metric into an orchestra of sector
ensembles. It does. The independent-amplitude atlas proves eleven available configuration
directions, but its axes and two-level sign block sparsely cover the interior amplitude volume.
This package maps that raw interior and continuous radial changes first. It must not organize results
by base/angular/shift ensemble or interpret collective behavior as physics.

## Whole question

Within the same chosen regular analytic local chart and coefficient banks, what geometric classes
are actually visited inside the bounded eleven-amplitude cube, and how do those classes change along
fixed directions as the common radius grows continuously away from the constant origin?

This is metric-led configuration observation. No native dynamics exists in this package, so
“solution” means neither stationary nor time-live physical solution.

## Frozen parent construction

Inherit the ten independently controlled metric fields, separate signed `phi` control, latent-to-
slot map, coefficient banks `B0..B3`, and sample schedule from
`udt_independent_amplitude_metric_atlas_2026-07-21/`. The parent package manifest must remain
byte-identical. No field, slot, coordinate dependence, tolerance, or `phi` decoupling rule may be
changed.

## Interior design frozen before geometry

Generate exactly 64 deterministic Halton points in eleven dimensions. Use indices `1..64` and bases

```text
2,3,5,7,11,13,17,19,23,29,31.
```

For radical inverse `vdc(n,p)`, set each amplitude to `2*vdc(n,p)-1`. These dimensionless points lie
inside `[-1,1]^11`. Preserve zeros or near coincidences; do not jitter, reject, or optimize them.

Before geometry, certify:

- 64 distinct interior rows;
- metric design rank ten and complete design rank eleven;
- positive and negative coverage for every amplitude;
- exact deterministic reproduction; and
- no row selected or weighted by geometric outcome.

No low-discrepancy, uniformity, probability, density, or exhaustiveness theorem is claimed.

## Radial design frozen before geometry

Use the first 16 rows of the corrected parent `H32` eleven-column sign block, with zero-based columns

```text
1,2,4,8,16,3,5,6,7,9,10.
```

For each direction evaluate exactly five positive radii

```text
1/8, 1/4, 1/2, 3/4, 1.
```

Together with one shared zero-amplitude origin this gives `16*5+1 = 81` radial-design rows. Retain
the distinction between direction and radius. Antipodal or geometrically duplicate outcomes may not
be collapsed.

The complete design has exactly `64+81 = 145` amplitude identities.

## Bank and point schedule

Evaluate every amplitude identity in all four banks at two fixed points per bank:

```text
B0: P0,P4
B1: P1,P5
B2: P2,P6
B3: P3,P7.
```

The atlas therefore has exactly `145*8 = 1160` retained configuration records. The radial incidence
table has `16*5*8 = 640` directed edges, including origin-to-`1/8`.

## Observations fixed before evaluation

For every record preserve amplitudes, slot/metric/coframe/`phi` two-jets, determinant and inertia,
raw identity residuals, scalar and tensor contractions, Ricci and curvature-operator ranks, mixed
curvature, screen expansion/shear, shift twist, coordinate activity, and signed `phi`/`dphi` class.

Use inherited thresholds:

```text
raw identity tolerance = 2e-10
numeric rank/activity threshold = 1e-9
```

Record the smallest singular value for Ricci and the six-dimensional curvature operator. Values
within a factor of 100 of the rank threshold are `NUMERIC_UNCERTAIN`; no uncertain record may be
promoted, discarded, or retuned.

For each radial edge record changes in determinant, scalar curvature, curvature magnitude, Ricci
rank, curvature-operator rank, shear rank, twist rank, mixed-curvature activity, and `dphi` causal
class. “Transition” means only a change in this recorded diagnostic tuple, not a phase transition or
physical bifurcation.

## Premise and choice ledger

| item | tag | bounded meaning |
|---|---|---|
| four-dimensional conformal-Lorentzian arena | `pinned-by-THEORY / CONDITIONAL CURRENT ARENA` | inherited parent arena |
| parent metric/coframe evaluator and independent amplitudes | `pinned-by-VERIFIED TOOL` | same chosen regular chart |
| Halton bases and 64 indices | `FREE NUMERICAL COVERAGE CONTROL` | deterministic interior sample |
| sign directions and five radii | `FREE NUMERICAL COVERAGE CONTROL` | finite radial sample |
| amplitude cube `[-1,1]^11` | `FREE BOUNDED REGIME` | no physical amplitude scale |
| coefficient banks and points | `FREE COVERAGE CONTROLS INHERITED` | finite analytic family |
| independent `phi` branch | `OPEN CONFIGURATION BRANCH C02` | no metric–`phi` law |
| action, source, boundary, topology, carrier, scale | `OPEN / EXCLUDED` | not sampled |
| coordinate time dependence | `CONFIGURATION DEPENDENCE ONLY` | not evolution |
| sector ensembles | `DEFERRED` | orchestra organization begins later |
| physical/GR/particle merit | `EXCLUDED` | no ranking criterion |

No untagged `pinned-by-HABIT` physical choice is allowed.

## Characterize, never filter

Retain every registered record and transition, including duplicates, flat or curved cases, all
numeric ranks, zero/nonzero shear or twist, every `phi` sign and `dphi` causal class, and any
unexpected loss or gain of diagnostic rank. No record is accepted or rejected for resembling a
particle, stable matter, GR, cosmology, a boundary, or a desired UDT result.

## Required evidence

- `AMPLITUDE_VOLUME_DESIGN.tsv`
- `SAMPLE_SCHEDULE.tsv`
- `CONFIGURATION_OBSERVATIONS.tsv`
- `RAW_CONFIGURATION_JETS.jsonl`
- `RADIAL_INCIDENCE.tsv`
- `GEOMETRIC_CLASS_CENSUS.tsv`
- `NUMERIC_RANK_MARGINS.tsv`
- `COVERAGE_LEDGER.tsv`
- `TEN_CRITERION_SCOPE.tsv`
- `ANTI_IMPOSITION_AUDIT.tsv`
- deterministic result/transcript;
- independent design reconstruction, raw-hash replay, all-record tensor/rank/census reconciliation,
  and at least three independent curvature reconstructions spanning origin/interior/radial records;
- mutations for missing/duplicate designs, changed bases/directions/radii, lost records or edges,
  rank/census corruption, filtered classes, ensemble promotion, physical transition wording,
  dynamics, and finite-exhaustiveness claims.

## Falsification and certification contract

If the design loses rank or differs from the frozen construction, stop as a tooling/design failure
before geometry. Once geometry begins, preserve all outcomes. Bank `MAP_OR_TOOLING_FAILURE` if raw
identity residuals fail, hashes disagree, a registered record/edge disappears, or independent
reconstruction fails. Numeric class diversity or uniformity is never a pass/fail condition.

## Scope ceiling

Maximum conclusion:

```text
BOUNDED_ELEVEN_AMPLITUDE_INTERIOR_AND_RADIAL_CONFIGURATION_VOLUME_CHARACTERIZED
```

This is not a genericity theorem, measure statement, complete metric solution space, ensemble law,
physical solution, action, selector, boundary, matter source, or universe model.
