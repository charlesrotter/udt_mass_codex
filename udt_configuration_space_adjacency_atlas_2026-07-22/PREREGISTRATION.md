# UDT Configuration-Space Adjacency Atlas — Preregistration

Date: 2026-07-22

Base: `adf8f92d95c387cc647f04b16f1f3b17e1e670d2`

Branch: `codex/udt-configuration-space-adjacency-atlas-2026-07-22`

Status: `PREREGISTERED_BEFORE_CONFIGURATION_OUTCOME_INSPECTION`

## Whole question and mode

This is a metric-led adjacency map:

> When every certified active bank identity is joined to its same-carrier, same-mask companions
> through complete continuous coframe configurations, which pairs remain in one causal sector,
> which are separated by `s=g^-1(dphi,dphi)=0`, what regularity and multiplicity does every
> separator have, and which conclusions are invariant versus interpolation-chart dependent?

The atlas characterizes configuration geometry. It does not seek or assign a particle, force,
cosmic-background, ordinary-clock, carrier, action, preferred branch, or physical universe.

## Frozen endpoint universe

The endpoint universe is fixed from the verified phi causal-interface atlas:

- four registered banks `B0`, `B1`, `B2`, `B3`;
- all 48 registered deformation vectors;
- all eight active masks `M8` through `MF`;
- exactly one identity for every `(bank,carrier_id,mask_id)`;
- all six unordered bank pairs at fixed `(carrier_id,mask_id)`.

This gives:

- `384` matched carrier/mask groups;
- `2,304` bank-pair endpoint sheets;
- `1,152` spacelike–spacelike control pairs;
- `1,152` spacelike–timelike cross-sector pairs;
- no timelike–timelike pair, because the registry contains only one timelike bank.

No pair may be added or removed after outcome inspection.

## Configuration parameters

Every sheet has:

```text
u in [0,1]       source path parameter
lambda in [0,1]  configuration adjacency parameter
```

Both endpoint metrics use the same registered amplitude/deformation vector and active mask. Every
one of the ten metric latent fields and the phi field remains present exactly when its mask permits
it. All angular fields and all four base-angular shifts are retained.

Two configuration charts are frozen:

### J1 — generator/coefficient join

For a bank pair `(A,B)`:

- linearly interpolate every frozen polynomial coefficient tensor from bank `A` to bank `B`;
- linearly interpolate the registered coordinate chord `x_A(u)` to `x_B(u)`;
- evaluate every interpolated scalar field and its exact coordinate gradient at that interpolated
  point;
- build the metric through the complete exponential triangular coframe.

This chart preserves an explicit scalar phi and therefore an exact differential `dphi` for each
fixed `lambda`. It is `CHOSE_ANALYTIC_CONFIGURATION_CHART`, not a derived UDT trajectory or field
equation.

### J2 — evaluated-cofield join

At fixed `u`:

- evaluate both endpoint banks;
- linearly interpolate all ten latent coframe fields;
- linearly interpolate the four components of `dphi`;
- rebuild the complete metric through the same coframe.

This is a local cofield chart. It preserves the endpoint metrics and every coframe sector, but it
does not assert a globally integrated scalar field away from the endpoints. It is a chart-robustness
control, not a physical interpolation.

There are `4,608` chart-sheet presentations of the `2,304` endpoint pairs. Chart presentations must
never be counted as independent universes.

## Exact invariant and interface logic

For both charts the coframe determinant remains

```text
det(g) = -exp(2*(a+c+d+f)) < 0
```

at every finite configuration point. Thus the metric stays Lorentzian and nondegenerate by
construction.

The scalar

```text
s(u,lambda) = g^-1(dphi,dphi)
```

is continuous. Therefore any continuous cross-sector fiber with opposite endpoint signs must
contain at least one `s=0` point by the intermediate-value theorem. This exact existence statement
does not depend on J1 or J2. It does not establish uniqueness, regularity, global dynamics, or
physical interpretation.

At a regular null point:

```text
D = grad(phi) tensor dphi
D^2 = s D = 0.
```

If `dphi != 0`, `D` is a nonzero rank-one nilpotent endomorphism. `D/s` is forbidden.

## Sheet classifications

Every chart sheet is assigned exactly one primary class:

- `UNIFORMLY_SPACELIKE_SHEET`;
- `FORCED_SINGLE_REGULAR_NULL_GRAPH`;
- `FORCED_MULTIPLE_REGULAR_NULL_GRAPHS`;
- `NULL_TANGENCY_OR_BRANCH_POINT`;
- `ZERO_GRADIENT_INTERFACE`;
- `INTERIOR_CAUSAL_POCKET_ON_SAME_SIGN_EDGE`;
- `METRIC_DEGENERACY_OR_SIGNATURE_CHANGE`;
- `UNRESOLVED_INTERVAL_GEOMETRY`.

Every null component records:

- certified `u` and `lambda` enclosures;
- sign on both lambda sides;
- whether `partial_lambda s` excludes zero;
- whether all four components of `dphi` can vanish;
- determinant/signature status;
- `D` rank and nilpotent status;
- endpoint pair and chart;
- whether the corresponding component is required by opposite endpoint signs or appears inside a
  same-sign control sheet.

## Certification contract

1. Reconstruct endpoints from the frozen rational generator and verified identity registry.
2. Use at least 80-decimal outward interval arithmetic on the complete coframe.
3. Certify endpoint signs over full `u` intervals independently of saved labels.
4. For same-sign sheets, certify the full two-dimensional sheet or retain unresolved boxes.
5. For cross-sector sheets, use adaptive interval boxes and interval `partial_lambda s` to prove
   each null graph's existence, uniqueness, and regularity. If uniqueness or regularity cannot be
   certified, retain the weaker forced-existence result and unresolved multiplicity.
6. Do not infer a continuous full instrument motif from the prior seventeen-node motif evidence.
7. Independently reconstruct load-bearing separators through the full 4-by-4 matrix
   adjugate/determinant route without importing the production builder.
8. Use direct frozen-generator probes as a source-integrity cross-check, not as interval proof.

No post-outcome tolerance retuning or candidate removal is allowed.

## Premise ledger

| object | status | use or limit |
|---|---|---|
| conditional Lorentzian coframe representative | `CHOSE_CONDITIONAL` | all causal claims are representative-scoped |
| full angular and shift sectors | `pinned-by-THEORY` | retained in every configuration |
| signed scalar phi and `D` | `pinned-by-THEORY` | no matter-carrier meaning |
| positive Common-Scale Neutrality | `pinned-by-THEORY` | preserves sign and zero set of `s` |
| all six matched bank pairs | `free-and-explored_WITHIN_FROZEN_REGISTRY` | complete bank-edge graph only |
| J1 and J2 interpolation charts | `CHOSE` | coordinate charts on a bounded configuration family |
| interface position, count, and shape | `free-and-explored` | no desired separator geometry |
| action, EOM, source, boundary, scale, density | `NOT_LOADED` | no dynamics or selection conclusion |
| particle/force/cosmic interpretation | `FORBIDDEN_AS_FILTER` | not used in candidate selection or grading |
| global bank-simplex interiors | `NOT_COVERED` | edges do not prove full simplex connectedness |
| arbitrary amplitude/carrier interpolation | `NOT_COVERED` | deferred, not silently inferred |

No physics premise is `pinned-by-HABIT`.

## Falsifiers and exercised catches

The verifier must reject:

- a missing or duplicated carrier/mask group, bank pair, or chart sheet;
- a spacelike–timelike edge with no retained null enclosure;
- a same-sign edge declared uniform from endpoint signs alone;
- a null root inferred only from sampled points;
- a multiple root silently reduced to one;
- a regularity claim with `partial_lambda s` containing zero;
- division by `s` at an interface;
- a zero-gradient event mislabeled a regular null dyad;
- a null covector event mislabeled metric degeneracy;
- omission of any angular or shift field;
- J1 and J2 counted as independent universes;
- chart-dependent interface shape promoted to an invariant;
- an edge result promoted to a complete bank-simplex or whole-solution theorem;
- a physical regime, action, carrier, scale, density, empirical anchor, or boundary condition used
  as a filter;
- source, prior-package, frozen-package, navigation, test-baseline, or original 54-path dirty
  metadata failure.

## Coverage and maximum conclusion

This atlas covers all matched registered bank edges for every active carrier/mask identity in two
complete-coframe configuration charts. It does not cover arbitrary metric configurations, simplex
interiors, an EOM solution space, physical time evolution, global finite-cell completion, or
physical regime identification.

Maximum conclusion:

`BOUNDED_REGISTERED_CONFIGURATION-SPACE_BANK-EDGE_ADJACENCY_CHARACTERIZED`

CPU only. No GPU work, time-live solve, physics fit, action/carrier adoption, canonization,
navigation update, repository reorganization, or artifact relocation.
