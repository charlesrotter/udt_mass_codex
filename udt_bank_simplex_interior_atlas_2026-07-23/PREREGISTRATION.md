# UDT Bank-Simplex Interior Atlas — Preregistration

Date: 2026-07-23

Base: `6597f3a50584d17b2a5248348e9a6ca471e1d179`

Branch: `codex/udt-bank-simplex-interior-atlas-2026-07-23`

Status: `PREREGISTERED_BEFORE_SIMPLEX_INTERIOR_OUTCOME_INSPECTION`

## Whole question and mode

This is a metric-led, nonselective configuration-space map:

> When all four registered causal banks are allowed to participate simultaneously, what causal
> regions, null sets, folds, pockets, tangencies, degeneracies, and connected components occur in
> the complete bank-weight tetrahedron for every registered carrier/mask group and both retained
> complete-coframe interpolation charts?

The atlas records what the bounded metric ensemble does. It does not seek or assign a particle,
force, cosmic background, ordinary-clock regime, carrier, action, preferred branch, scale,
boundary, or physical universe.

The six previously certified bank edges are boundary controls only. No edge result is promoted to
the tetrahedral interior.

## Frozen identity universe

The exact source state is:

| source | SHA-256 |
|---|---|
| `udt_configuration_space_adjacency_atlas_2026-07-22/ENDPOINT_PAIR_REGISTRY.tsv` | `bab9c0b7e5ba1966a9521cecd3aff5a576b0e83bb97bbf0e100065d661038ac7` |
| `udt_configuration_space_adjacency_atlas_2026-07-22/build_configuration_adjacency_atlas.py` | `121148082560c9ee17efeac7db942d00130e528db8d6a6155f8df85cefc92ec4` |
| `udt_phi_causal_interface_atlas_2026-07-22/IDENTITY_CAUSAL_CERTIFICATES.tsv` | `b1ff6dc3f63cc7d052b66ee1fea2cf0088e119965a04c089b5cb3aa106466189` |
| `udt_motif_hopf_correspondence_audit_2026-07-22/COHERENT_IDENTITY_REGISTRY.tsv` | `ffb624d1a4e01e181639e86993a550a3030b2050c547f6e563c14a462abfe45f` |
| `udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv` | `b1251073a9f8e916259d29ebcae71a9b86a5f8235c3b0b581430967d6aeadbe8` |

The candidate universe is fixed to:

- four banks `B0`, `B1`, `B2`, and `B3`;
- all 48 registered deformation vectors;
- all eight active masks `M8` through `MF`;
- exactly 384 matched `(carrier_id,mask_id)` groups;
- exactly two chart presentations per group;
- exactly 768 chart/group interior sheets.

No group or chart may be removed after outcome inspection. The two chart presentations are not
independent universes.

## Complete simplex and source-path domain

For each group, the bank weights obey

```text
w_i >= 0,
w_0 + w_1 + w_2 + w_3 = 1,
u in [0,1].
```

This complete tetrahedron is covered without rejecting any point by

```text
q_0 = 1-r,
q_1 = r(1-v),
q_2 = r v,
w_i = (1-t) q_i, i=0,1,2,
w_3 = t,
(u,r,v,t) in [0,1]^4.
```

The redundant coordinate values at `r=0` and `t=1` are retained and consistency-checked. Bank `B3`
is used as the radial vertex because the frozen endpoint certificates classify `B0..B2`
spacelike and `B3` timelike throughout `u`; this is a source-derived computational orientation,
not a physical preference. The base-face result and every radial result are outcomes, not inputs.

## Frozen configuration charts

### J1 — generator/coefficient barycentric chart

At fixed `(u,w)`:

- barycentrically mix all four frozen polynomial coefficient tensors;
- barycentrically mix all four registered coordinate chords;
- evaluate all scalar latent fields and the exact coordinate gradient of `phi`;
- construct the full exponential triangular coframe.

This retains an explicit scalar `phi` for each fixed bank-weight configuration. It is
`CHOSE_ANALYTIC_CONFIGURATION_CHART`, not a UDT trajectory, field equation, or dynamics.

### J2 — evaluated-cofield barycentric chart

At fixed `u`:

- evaluate all four bank endpoints;
- barycentrically mix all ten latent coframe fields;
- barycentrically mix all four components of `dphi`;
- reconstruct the same complete coframe.

This is a local cofield chart and does not assert a globally integrated scalar away from vertices.
It is a chart-robustness control, not physical interpolation.

Both charts retain all angular fields and all four base-angular shifts.

## Exact metric invariant and neutral object

The full coframe gives, for every finite latent configuration,

```text
det(g) = -exp(2*(a+c+d+f)) < 0.
```

The metric therefore remains Lorentzian and nondegenerate by construction. The neutral scalar to
map is

```text
s(u,w) = g^-1(dphi,dphi).
```

At a regular null point with `dphi != 0`, the dyad endomorphism satisfies

```text
D = grad(phi) tensor dphi,
D^2 = s D = 0,
```

so `D` is nonzero, rank one, and nilpotent. Division by `s` is forbidden.

## Classification registry

Every chart/group sheet receives exactly one primary class:

- `SINGLE_REGULAR_NULL_HYPERSURFACE_GRAPH`;
- `MULTIPLE_REGULAR_NULL_HYPERSURFACES`;
- `NULL_FOLD_OR_BRANCH_SET`;
- `ZERO_GRADIENT_NULL_SET`;
- `BASE_FACE_CAUSAL_POCKET_OR_INTERFACE`;
- `METRIC_DEGENERACY_OR_SIGNATURE_CHANGE`;
- `UNRESOLVED_FULL_COVER`.

The atlas separately records:

- the sign census on the complete `B0-B1-B2` base face;
- signs and zero multiplicity along every radial fiber to `B3`;
- whether `partial_t s` excludes zero at and away from the null set;
- connected components of certified positive, negative, null, and unresolved cells;
- whether the null set is a graph over `(u,q)` or has folds/branches;
- whether any component has `dphi=0`;
- boundary agreement with all six prior edge sheets;
- chart-invariant topology versus chart-dependent interface position/shape;
- exact determinant/signature status.

No shape is discarded for failing to resemble expected physics.

## Frozen computational and certification contract

The production calculation must:

1. reconstruct all 384 groups directly from the frozen carrier and identity sources;
2. evaluate the complete coframe in both charts;
3. cover the full four-cube `(u,r,v,t)` with outward binary64 intervals and explicit platform,
   library, and rounding-scope disclosure;
4. begin with the fixed dyadic grid
   `N_u=8, N_r=8, N_v=8, N_t=16`;
5. subdivide every interval-indeterminate cell along its widest mapped simplex coordinate, with
   deterministic tie order `t,u,r,v`, through total depth 18;
6. never infer a sign, root count, derivative sign, or topology from point samples alone;
7. retain every depth-18 indeterminate cell as unresolved;
8. use at least 80-decimal interval arithmetic on frozen boundary controls and on a deterministic
   set of at least 24 load-bearing interior boxes spanning charts, masks, carriers, and extremal
   margins;
9. independently reconstruct the load-bearing scalar from the full `4 x 4` coframe matrix,
   determinant, and adjugate rather than the production inverse-coframe formula;
10. replay all six prior bank edges and require classification agreement; and
11. emit raw cell certificates sufficient to reproduce every sheet classification.

Pointwise float64 sampling may guide diagnostics and visualization, but it cannot certify a sign or
exclude an unobserved component. GPU reconnaissance is permitted only as a frozen, bounded,
non-certifying map after this preregistration; CPU interval coverage and independent high-precision
anchors remain the evidence gates.

No tolerance, grid, candidate, class, or maximum conclusion may be changed after inspection without
a separately committed correction preregistration.

## Premise and ansatz ledger

| object | status | use or limit |
|---|---|---|
| positional dilation / reciprocal exponential core | `pinned-by-THEORY` | exact founding/derived-conditional premise stamps retained |
| conditional Lorentzian coframe representative | `CHOSE_CONDITIONAL` | all causal classifications are representative-scoped |
| ten latent coframe fields plus signed `phi` | `pinned-by-THEORY_WITHIN_REGISTERED_ENSEMBLE` | no carrier or matter meaning |
| all 384 carrier/mask groups | `free-and-explored_WITHIN_FROZEN_REGISTRY` | complete bounded identity census |
| all four bank weights | `free-and-explored` | no bank omitted or favored as an outcome |
| source path `u` | `free-and-explored` | full registered interval |
| J1 and J2 | `CHOSE` | two bounded configuration charts, not physical paths |
| simplex radial coordinates | `CHOSE_NUMERIC_METHOD` | surjective cover; not a physical radial law |
| interval grid/depth/tolerances | `CHOSE_NUMERIC_METHOD` | certification controls, not physics |
| action, EOM, source, boundary, scale, density | `NOT_LOADED` | no dynamics or selection conclusion |
| particle/force/cosmic/clock regime | `FORBIDDEN_AS_FILTER` | may be discussed only after the neutral atlas is banked |
| arbitrary metric functions and amplitudes outside the registry | `NOT_COVERED` | no whole-metric theorem |
| global finite-cell completion and time-live evolution | `NOT_COVERED` | no global or dynamical inference |

No physical premise is `pinned-by-HABIT`.

## Preregistered falsifiers and catch-proofs

The verifier must reject:

- a missing or duplicated stable group, chart, or simplex sheet;
- a missing bank weight or an off-simplex weight;
- any gap in the complete four-cube cover;
- overlap/coordinate redundancy counted as a new physical component;
- a base face declared uniform from edge signs alone;
- a radial graph declared from endpoint signs or samples alone;
- a multiple root, fold, tangency, pocket, or unresolved cell silently reduced to one graph;
- a regularity claim whose `partial_t s` interval contains zero;
- a null component with possibly zero `dphi` labeled regular rank-one;
- division by `s` at a null interface;
- a null covector mislabeled metric degeneracy;
- omission of an angular or shift field;
- J1 and J2 counted as independent universes;
- chart-dependent location or shape promoted to an invariant;
- edge agreement promoted to interior proof;
- an unresolved cell omitted from the result;
- a physical regime, action, carrier, scale, density, empirical anchor, or boundary condition used
  to select or grade a configuration;
- a full-simplex result promoted to arbitrary metrics, global solutions, or dynamics;
- source, package, navigation, test-baseline, or original dirty-checkout metadata failure.

## Completeness map and maximum conclusion

This atlas covers one bounded local-configuration tile:

- `FIELDS`: all ten registered coframe amplitudes and `phi` are retained subject to each frozen mask;
- `DOMAIN`: complete bank simplex times the complete registered source path;
- `BRANCH`: all 384 registered identities in both charts;
- `REGIME`: the frozen analytic polynomial/coframe ensemble only.

It does not supply an action, Euler-Lagrange equations, physical boundary/regularity selection,
topological sector, dynamics, stability spectrum, global completion, or arbitrary functional
metric space.

Maximum conclusion:

`BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_CAUSAL_GEOMETRY_CHARACTERIZED`

No physics interpretation, action/carrier adoption, time-live solve, canonization, navigation
update, repository reorganization, or artifact relocation is authorized by this package.
