# UDT independent-amplitude metric atlas — preregistration

Date: 2026-07-21

Base: `155a6430df21a55861c41d9913bccd0ccc5efa95`

Branch: `codex/udt-independent-amplitude-metric-atlas-2026-07-21`

Mode: CPU-only, deterministic float64 configuration observation. No action, Euler equation, ODE,
PDE, relaxation, time evolution, boundary condition, physical selector, empirical target, or GPU
work.

## Owner authorization and controlling correction

Charles authorized releasing the common deformation parameter used by the immediately preceding
constructive atlas. This package must independently vary ten metric amplitudes and the separate
signed `phi` amplitude. It remains a solution-space mapping tile, not a search for a desired UDT
mechanism or a preferred universe.

## Whole question

In the same declared regular local `2+2` chart, does replacing the single shared deformation
parameter by ten independent metric amplitudes actually produce a rank-ten family of complete
metric two-jets, while an eleventh independently controlled amplitude varies `phi` without changing
the metric?

This is metric-led. It characterizes constructed configurations. Because no native dynamics is
selected, it does not define or solve a dynamical solution space.

## Frozen chart and function basis

The chart, base values, four coefficient banks `B0..B3`, coordinate-polynomial basis, and eight
sample points `P0..P7` are inherited byte-for-byte in meaning from
`udt_constructive_metric_family_atlas_2026-07-21/PREREGISTRATION.md`. For latent metric field
`z_j`, coefficient-bank polynomial two-jet `F_{b,j}(x)`, and signed scalar two-jet
`F_{b,phi}(x)`, replace the shared `lambda` by

```text
z_j(x) = z_j,base + alpha_j F_{b,j}(x),       j=0,...,9
phi(x) = phi_b,offset + beta F_{b,phi}(x).
```

The ten `alpha_j` are mutually independent configuration parameters. `beta` is an eleventh
parameter and is absent from the metric/coframe construction. The factorized chart remains a
chosen regular coordinate/coframe representation, not selected physics.

## Amplitude design frozen before outcomes

Use exactly 60 eleven-component amplitude rows, in this order:

1. one origin row with every amplitude zero;
2. twenty metric-axis rows `+e_j,-e_j`, with `beta=0`;
3. two scalar-axis rows with all metric amplitudes zero and `beta=+1,-1`;
4. thirty-two sign-balanced rows formed from columns 1 through 11 of the Sylvester `H32` matrix,
   multiplied by `3/4`; and
5. five scalar-sweep rows with
   `alpha=(1,-1/2,3/4,-1,1/2,-3/4,1,-1/2,3/4,-1)` and
   `beta=(-1,-1/2,0,1/2,1)`.

The Sylvester construction is `H1=[1]` and `H_{2n}=[[H_n,H_n],[H_n,-H_n]]`. No row may be
discarded or replaced after observation.

Before geometry is evaluated, the builder must certify:

- exactly 60 unique amplitude identities;
- rank ten for the metric-amplitude design and rank eleven for the complete design;
- exact pairwise orthogonality of the selected eleven columns in the registered `H32` subdesign;
- positive and negative variation of every parameter;
- an explicit zero setting for every parameter;
- exact metric-axis isolation rows for all ten fields;
- exact scalar-axis isolation rows; and
- five records sharing one metric-amplitude vector while sweeping only `beta`.

These certify the sampled parameter design, not exhaustive Cartesian coverage of eleven real
parameters.

## Bank and coordinate schedule

Evaluate every one of the 60 amplitude rows in every bank at exactly two points:

```text
B0: P0,P4
B1: P1,P5
B2: P2,P6
B3: P3,P7.
```

The registered regular atlas therefore contains exactly `60*4*2 = 480` configuration records.
This schedule covers all banks and all points without claiming that the finite product is dense,
generic, probabilistic, or exhaustive.

## Load-bearing independence diagnostics

For every record preserve:

- the eleven amplitudes;
- all ten slot values, 40 first derivatives, and 160 ordered second derivatives;
- the metric and coframe two-jets;
- the complete `phi` two-jet;
- connection/Cartan identity residuals and the same curvature, mixed-sector, shear, twist, and
  signed-`dphi` observations used by the preceding atlas;
- the rank and singular values of the `10 x 10` slot-value tangent with respect to the ten metric
  amplitudes;
- the rank and singular values of the `210 x 10` complete-slot-two-jet tangent;
- the rank and singular values of the complete configuration tangent after adding the `phi`
  two-jet and `beta`, which must have eleven columns; and
- exact configuration and metric-jet hashes.

The complete-slot-two-jet vector is the concatenation of 10 slot values, 40 first derivatives, and
160 ordered second derivatives. Parameter tangents may be computed numerically by preregistered
centered differences with step `1e-6`, but the independent verifier must reconstruct at least one
anchor symbolically and compare its analytic parameter derivatives.

Use rank threshold `1e-9`. Singular values within a factor of 100 of the threshold are
`NUMERIC_UNCERTAIN`. Slot-value rank is observed rather than required: at `P0`, all registered
polynomials vanish in value while their derivative jets remain live, so slot-value rank can be
lower without reducing complete-two-jet independence.

The intended independence classification requires complete-slot-two-jet rank ten and combined
metric-plus-`phi` rank eleven. If either fails, preserve the records and classify the map as
`PARAMETERIZATION_RANK_DEFICIENT`; do not tune coefficients, points, thresholds, or amplitudes.

## Phi decoupling checks

The five scalar-sweep rows must produce identical metric two-jets and distinct `phi` two-jets at
each bank/point. The two scalar-axis records must share the origin metric two-jet. The verifier must
also demonstrate that changing a metric amplitude with fixed `beta` changes no registered
definition of `beta` or `phi` amplitude. These checks establish configuration-level independence;
they do not derive a physical metric–`phi` relationship.

## Premise and choice ledger

| item | tag | bounded meaning |
|---|---|---|
| four-dimensional conformal-Lorentzian arena | `pinned-by-THEORY / CONDITIONAL CURRENT ARENA` | current parent geometry |
| P01 metric/Cartan evaluator | `pinned-by-VERIFIED TOOL` | supplied representative only |
| regular factorized `2+2` chart | `CHOSE REPRESENTATION` | one local chart; not selected physics |
| ten metric amplitudes | `free-and-explored WITHIN REGISTERED DESIGN` | independent columns; finite sampling |
| separate `phi` amplitude | `free-and-explored C02 CONFIGURATION BRANCH` | no action or metric join |
| coefficient banks and polynomial basis | `FREE COVERAGE CONTROLS INHERITED` | smooth finite family only |
| amplitude rows and sample points | `FREE NUMERICAL COVERAGE CONTROLS` | dimensionless deterministic design |
| rank threshold and finite-difference step | `FREE NUMERICAL DIAGNOSTIC CONTROLS` | independently anchored; no physical meaning |
| physical scale, boundary, topology, carrier, action | `OPEN / EXCLUDED` | not sampled |
| time dependence in coordinate jets | `CONFIGURATION DEPENDENCE ONLY` | not evolution |
| GR or empirical comparison | `EXCLUDED` | no merit criterion |

No untagged `pinned-by-HABIT` physical choice is permitted.

## Characterize, never filter

Every registered configuration remains in the output, including flat, curved, low-rank,
high-rank, twisting, twist-free, shearing, shear-free, mixed, diagonal-at-a-point, positive/zero/
negative `phi`, and every causal class of `dphi`. No configuration is accepted or rejected for
resembling a particle, stable matter, a cosmology, GR, a finite-cell seal, or an expected UDT
answer.

## Required evidence

- `AMPLITUDE_DESIGN.tsv`
- `SAMPLE_SCHEDULE.tsv`
- `PARAMETER_DEPENDENCY.tsv`
- `CONFIGURATION_OBSERVATIONS.tsv`
- `PARAMETER_TANGENT_RANKS.tsv`
- `PHI_DECOUPLING.tsv`
- `SECTOR_ACTIVITY.tsv`
- `RAW_CONFIGURATION_JETS.jsonl`
- `COVERAGE_LEDGER.tsv`
- `TEN_CRITERION_SCOPE.tsv`
- `ANTI_IMPOSITION_AUDIT.tsv`
- deterministic result/transcript;
- separately written independent verification with symbolic parameter derivatives; and
- exercised mutations for missing/duplicate design rows, a shared-amplitude regression, lost
  metric axis, lost scalar axis, rank promotion, phi feedback into the metric, omitted sector,
  changed tolerance, filtered record, dynamics/physics promotion, and finite-exhaustiveness claims.

## Certification and falsification contract

Banking stops on a tooling or evidence failure if:

- the amplitude design or 480-record census differs from the frozen registry;
- a metric field or `phi` lacks its independent control column;
- raw residual exceeds `2e-10`;
- raw hashes or independently reconstructed tensors disagree;
- a record is dropped because of its geometry;
- a rank miss is hidden or repaired after observation;
- a time-dependent configuration is called physical evolution; or
- a desired physics outcome is used to rank the records.

If the design is correct but complete-two-jet rank is below ten or the combined rank is below
eleven, the scientific return is the preserved negative
`PARAMETERIZATION_RANK_DEFICIENT_IN_REGISTERED_REGIME`.

## Scope ceiling

Maximum positive conclusion:

```text
TEN_METRIC_AMPLITUDES_AND_PHI_VARIED_INDEPENDENTLY_WITHIN_REGISTERED_CONFIGURATION_DESIGN
```

This cannot be promoted to generic metric behavior, complete solution-space coverage, a physical
solution, dynamics, a `phi` equation, action selection, boundary selection, matter emergence, or a
universe model.
