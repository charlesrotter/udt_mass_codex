# UDT constructive metric-family atlas — preregistration

Date: 2026-07-21

Base: `093114f90721c6f176f78f1823455445a7db40f0`

Branch: `codex/udt-constructive-metric-family-atlas-2026-07-21`

Mode: CPU-only, exact/float64 constructive configuration observation. No action, EOM, ODE, PDE,
relaxation, physical evolution, comparison target, or GPU work.

## Owner correction controlling this package

Charles challenged the proposed axis-compatibility atlas as a possible escape from the slower task
of exploring what the complete metric actually does. That challenge controls this package.
Compatibility labels are not the organizing question. Explicit metric/coframe families and their
geometry are constructed first; any incidence relation is recorded only after it occurs.

## Whole question

Within a declared local/regional chart regime, what geometry is actually exhibited by broad,
explicit four-dimensional metric/coframe families when all ten metric functions, every coordinate,
the signed `phi` field, the angular screen, and every mixed shift are live?

This package observes configurations, not physical solutions. With no selected dynamics law there
is no EOM solution set to solve. The exact target is therefore a constructive continuation of P01
and P02 from isolated jets to correlated jets along coordinate and deformation paths.

## Constructive family registry frozen before outcomes

### R01 — regular all-slot split/coframe chart

Use six unrestricted latent scalar functions `(a,b,c,d,e,f)` and four shift functions
`(A20,A30,A21,A31)`. Define positive factors

```text
u=exp(a), w=exp(c), r=exp(d), t=exp(f)
```

and the base/screen blocks

```text
h00=-u^2
h01=-u b
h11=w^2-b^2

q22=r^2
q23=r e
q33=e^2+t^2.
```

The full split metric is constructed with all four shifts through the verified P01 interface. The
equivalent coframe is also constructed and passed through the Cartan evaluator. This chart has a
Lorentzian base and positive screen by construction and is only one regular open chart. It is not a
physical split, global reciprocal plane, preferred signature argument, or exhaustive metric chart.

The latent-to-slot Jacobian must have rank ten at every regular sample. Each of the ten latent
functions must have declared nonzero dependence on all four coordinates. No slot may be frozen or
dropped.

### R02 — deterministic coefficient banks and deformation paths

Use four fixed coefficient banks `B0..B3`. Their coefficients are generated from integer modular
formulae recorded in the builder; zeros are replaced by a fixed nonzero rational coefficient.
Every function contains linear terms in every coordinate, coordinate squares, and mixed monomials.
This is a reproducible coverage device, not a physical spectrum or stochastic inference.

Each bank is traversed at

```text
lambda = -1, -1/2, 0, 1/2, 1.
```

At `lambda=0` the family gives a constant reference coframe. That point is a deformation origin,
not a physical vacuum or acceptance target. No path is preferred.

### R03 — coordinate sample set

Evaluate each bank/path on the following dimensionless chart points:

```text
P0 = (0,0,0,0)
P1 = (1/3,-1/4,1/5,-1/6)
P2 = (-1/4,1/5,-1/6,1/7)
P3 = (1/5,1/6,-1/7,-1/8)
P4 = (-1/6,-1/7,1/8,1/9)
P5 = (1/2,0,-1/3,1/4)
P6 = (0,-1/2,1/4,-1/3)
P7 = (1/3,1/3,1/3,1/3).
```

The points bound one chart sample and have no physical scale. No conclusion extends beyond the
registered functions, parameters, or chart.

### R04 — signed `phi` overlays

Each bank carries one independent signed scalar two-jet with all four coordinate dependencies and
mixed monomials. The constant offsets cycle through negative, zero, and positive values. Record
`phi`, `dphi`, its causal norm where the metric is regular, horizontal/vertical support, Hessian,
and its incidence with screen expansion, shear, twist, and mixed curvature.

This is the `C02` independent-`phi` configuration branch only. No scalar action, metric-`phi`
constraint, distance interpretation, or physical seal is introduced. The metric-derived `phi`
branches remain open.

### R05 — CSN representative orbits

At preregistered anchor configurations apply positive local factors

```text
Omega=exp(kappa*sigma(x)),  kappa=-1/2,+1/2,
```

with a deterministic all-coordinate quadratic `sigma`. Record representative-dependent geometry
and the invariant status already established by P01/P02. These are orbit observations only; no
physical representative or scale is selected.

### R06 — coordinate and coframe-gauge orbits

At preregistered anchors apply two fixed nonsingular coordinate transformations and one fixed local
Lorentz two-jet. Verify tensor/Cartan covariance and do not count gauge-related records as new
geometries.

### R07 — degenerate and type-changing closure witnesses

Separately construct exact zero-jet paths in which one base or screen eigenvalue, or both, traverse
`-1,-1/2,0,1/2,1`. Preserve regular Lorentzian, other-signature, degenerate, and simultaneous-rank
branches. The inverse-based P01 evaluator must stop at singular points; singular records remain in
the atlas rather than being discarded.

These closure paths are bounded witnesses, not all-coordinate regular families and not evidence
that one signature is physically admitted or preferred.

## Observables fixed before evaluation

For every regular all-slot record preserve:

- ten slot values, all 40 first derivatives, and all 160 ordered second-derivative entries;
- metric/coframe values and jets;
- determinant, inertia, connection/Cartan identity residuals;
- scalar curvature, Ricci rank, curvature-operator rank, and tensor component norms;
- scalar, Ricci-square, Riemann-square, and Weyl-square contractions as signed Lorentzian
  contractions, never positivity tests;
- base/screen expansion, both shear components/ranks, nonlinear shift curvature/twist, and
  time/depth/angular derivative activity;
- signed `phi`, full gradient, causal norm, Hessian, and horizontal/vertical support;
- mixed base-screen curvature activity without setting any component to zero; and
- deformation-neighbor changes and exact configuration identity.

Ranks use the preregistered float64 singular-value threshold `1e-9`. Values within a factor of 100
of that threshold are marked `NUMERIC_UNCERTAIN`; they are never discarded or promoted to an exact
zero. Raw residual certification uses `2e-10`, inherited from P01. A residual miss is recorded as a
tooling failure and stops banking; it is not a physics rejection.

## Premise and choice ledger

| item | tag | scope |
|---|---|---|
| four-dimensional conformal-Lorentzian arena | `pinned-by-THEORY / CONDITIONAL CURRENT ARENA` | current metric parent |
| P01 Levi-Civita/Cartan evaluator | `pinned-by-VERIFIED TOOL` | geometry per supplied representative |
| conditional `2+2` slots | `CHOSE REPRESENTATION` | regular chart only; not selected physics |
| all ten functions and all four coordinates | `free-and-explored WITHIN REGISTERED BASIS` | no slot or coordinate frozen |
| coefficient banks and chart points | `FREE NUMERICAL COVERAGE CONTROLS` | dimensionless; no physical value |
| deformation parameter bounds | `FREE NUMERICAL COVERAGE CONTROLS` | finite bounded paths only |
| regular split factorization | `CHOSE CHART` | released by gauge and degeneracy-closure tests |
| signed independent `phi` | `OPEN CONFIGURATION BRANCH C02` | no action or metric join |
| positive CSN factors | `pinned-by-THEORY orbit / FREE sampled representative` | no section selected |
| smooth polynomial/exponential family | `CHOSE BASIS` | nonsmooth, nonanalytic, and arbitrary-function remainder open |
| boundary/topology/global completion | `NOT SAMPLED / OPEN` | no local record closes finite cell |
| L01/L02/L03 dynamics | `EXCLUDED` | status only; no residual or branch ranking |
| carrier, matter, mass, GR, empirical readout | `EXCLUDED` | no merit criterion |

No untagged `pinned-by-HABIT` physics choice is allowed.

## Characterize, never filter

All generated records remain in the output. The following are classifications, never acceptance
criteria: flat, curved, high/low component magnitude, regular, near-degenerate, type-changing,
twisting, twist-free, shearing, shear-free, mixed, diagonal at an isolated point, time dependent,
static at an isolated point, `phi` positive/zero/negative, spacelike/null/timelike/uncertain
`dphi`, and numeric-rank uncertain.

No diagnostic asks for a lump, particle, mass, spectrum, smooth seal, round screen, GR solution,
cosmology, stable object, or expected UDT answer.

## Required outputs

- `FAMILY_DEFINITIONS.tsv`
- `SAMPLE_POINTS.tsv`
- `CONFIGURATION_OBSERVATIONS.tsv`
- `RAW_CONFIGURATION_JETS.jsonl`
- `SECTOR_ACTIVITY.tsv`
- `PHI_ANGULAR_OBSERVATIONS.tsv`
- `DEFORMATION_INCIDENCE.tsv`
- `CSN_ORBIT_OBSERVATIONS.tsv`
- `GAUGE_ORBIT_CHECKS.tsv`
- `DEGENERACY_CLOSURE.tsv`
- `COVERAGE_LEDGER.tsv`
- `TEN_CRITERION_SCOPE.tsv`
- `ANTI_IMPOSITION_AUDIT.tsv`
- deterministic result/transcript and independent verification with exercised corruptions.

## Falsification and certification contract

Banking stops if:

- any regular-family latent function lacks a coordinate dependence;
- the latent-to-slot map loses rank ten in a registered regular record;
- a mixed shift, screen off-diagonal, time derivative, angular derivative, shear, or twist channel
  is omitted from the generator or observation schema;
- raw P01/Cartan residual exceeds `2e-10`;
- a singular closure record is deleted because inverse geometry is unavailable;
- a gauge orbit is counted as new geometry;
- a rank threshold becomes a physical filter;
- any outcome is ranked, preferred, or compared with desired physics;
- finite witnesses are called exhaustive; or
- a time-dependent configuration is called physical evolution.

The independent verifier must reconstruct at least one full all-slot family using separately
written SymPy differentiation, replay saved raw jets, check the coframe/split identity, verify
coordinate and local-Lorentz covariance, audit all coverage counts, and exercise mutations for every
load-bearing exclusion.

## Scope ceiling

Permissible classifications:

- `CONSTRUCTIVE_ALL_SLOT_CONFIGURATION_FAMILIES_OBSERVED_IN_REGISTERED_LOCAL_REGIME`;
- `MAP_INCOMPLETE_OR_SECTOR_OMITTED`; or
- `TOOLING_OR_IDENTITY_FAILURE`.

Maximum conclusion:

```text
CONSTRUCTIVE_METRIC_CONFIGURATION_FAMILIES_CHARACTERIZED_NOT_DYNAMICAL_SOLUTIONS
```

No physical completion, compatibility law, action, boundary condition, representative, scale,
`X_max`, matter structure, or universe is selected.
