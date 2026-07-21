# Chart/Coframe Invariance Atlas — Preregistration

Date: 2026-07-21

Branch: `codex/udt-chart-coframe-invariance-atlas-2026-07-21`

Parent commit: `ba572f589eae83c9f74de1b93b34d389529b27b7`

## Whole question

For the complete 6,144-configuration structural-ensemble atlas already banked at the parent commit,
which recorded structures are unchanged tensor geometry, which merely change components under an
invertible chart or Lorentz coframe transformation, which depend on the supplied coordinate 2+2
partition, and which become undefined when that supplied partition leaves its admitted signature
domain?

This is a bounded invariance atlas. It does not select a chart, coframe, partition, action, source,
carrier, boundary condition, or desired physical branch.

## Mode and scope

- Method order: `MAP -> OBSERVE -> PONDER -> DERIVE`.
- Question type: metric-led representation and supplied-partition audit.
- Compute: CPU-only algebra over saved configuration jets. No relaxation, fitting, GPU work, or new
  solution search.
- Parent configuration universe: all 48 carriers, all 16 ensemble masks, and all 8 contexts,
  totaling 6,144 configurations.
- Parent interaction universe: all 48 carriers, all 15 nonempty ensemble subsets, and all 8
  contexts, totaling 5,760 Möbius targets per transformation.
- Transformation universe: the twelve transformations fixed below. Therefore the required coverage
  is 73,728 configuration-orbit rows and 69,120 interaction-orbit rows.
- Every transformation/configuration and transformation/interaction combination is retained.
  Invalid or marginal supplied splits are outcomes, not grounds for exclusion.

## Frozen source evidence

The build must verify these manifests before reading outcomes:

| source | required manifest SHA-256 |
|---|---|
| `udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt` | `3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757` |
| `udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt` | `b7d61760e3ac3dc9dc2a51a7a505f02dad964fe8d7dfc1f1ed8df3cc3eb1b543` |
| `udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt` | `17780f41355121df4ecf86bd81606ef597cc6f5f26d90c0e443a5d2eac24d13a` |

The parent raw shards, registries, and Möbius ledger are immutable inputs. This package may not
rewrite them.

## Fixed transformation registry

### Constant coordinate charts

Convention: `x = J x'`; covariant coordinate indices therefore acquire a right factor `J`. All
matrices are constant, invertible probes.

1. `C00_IDENTITY`: `J = I4`.
2. `C01_BLOCK_GENERAL`:

   ```text
   [[1, .2, 0, 0], [.1, 1, 0, 0],
    [0, 0, 1, -.15], [0, 0, .25, 1]]
   ```

3. `C02_BLOCK_GENERAL_INVERSE`: the mathematical inverse of `C01_BLOCK_GENERAL`.
4. `C03_CROSS_GENERAL`:

   ```text
   [[1, 0, .12, 0], [0, 1, 0, -.18],
    [.07, 0, 1, 0], [0, .09, 0, 1]]
   ```

5. `C04_CROSS_GENERAL_INVERSE`: the mathematical inverse of `C03_CROSS_GENERAL`.
6. `C05_SWAP_DEPTH_SCREEN`: permutation exchanging coordinate indices 1 and 2.
7. `C06_SWAP_TIME_SCREEN`: permutation exchanging coordinate indices 0 and 2.

`C01/C02` preserve the supplied base/screen distributions. `C03/C04` mix them while retaining the
new first-two/last-two coordinate split as an independently reported supplied split. `C05/C06`
re-seat that supplied split. A split invalidated by signature is still retained and classified.

### Internal Lorentz coframes

Convention: `e' = Lambda e`, with internal signature `diag(-1,1,1,1)`. A boost generator `K0a` has
`K[0,a] = K[a,0] = 1`. The screen-rotation generator has `K[2,3] = -1`, `K[3,2] = 1`.

1. `F01_CONSTANT_BASE_BOOST`: `exp(.31 K01)`.
2. `F02_LOCAL_BASE_BOOST`: `exp(theta K01)` with, at the sampled point,
   `theta=.31`, gradient `[.07,-.04,.03,.05]`, and Hessian

   ```text
   [[.02,.01,0,-.005], [.01,-.015,.004,0],
    [0,.004,.01,.006], [-.005,0,.006,-.012]]
   ```

3. `F03_CONSTANT_CROSS_BOOST`: `exp(.27 K02)`.
4. `F04_LOCAL_CROSS_BOOST`: `exp(theta K02)` with `theta=-.22`, gradient
   `[-.03,.06,.02,-.05]`, and Hessian

   ```text
   [[.011,-.004,.003,0], [-.004,.018,0,-.006],
    [.003,0,-.009,.005], [0,-.006,.005,.014]]
   ```

5. `F05_LOCAL_SCREEN_ROTATION`: `exp(theta K23)` with `theta=.37`, gradient
   `[.04,.02,-.06,.03]`, and Hessian

   ```text
   [[-.008,.003,0,.004], [.003,.012,-.005,0],
    [0,-.005,.016,.002], [.004,0,.002,-.011]]
   ```

Local first and second coframe jets must include the registered derivatives of `Lambda`; metric
jets must nevertheless remain unchanged. No Lorentz coframe map redefines the coordinate split.

## Payloads and classifications

For every configuration the atlas records:

- metric, first and second metric jets;
- Riemann, Weyl, Ricci, scalar curvature, and metric determinant/inertia;
- Cartan curvature in the internal coframe;
- scalar-field value, gradient, and Hessian;
- supplied-split validity, inverse/reconstruction residual, slot jets, shear, and twist whenever
  the transformed split is admitted.

For every interaction cube it recomputes the exact four-ensemble Möbius interaction for:

- metric two-jet;
- Riemann, Weyl, Ricci, and scalar curvature;
- Cartan curvature;
- scalar-field two-jet;
- supplied-split slot two-jet, shear, and twist when all required vertices admit that split.

Each row receives exactly one primary status:

- `TENSOR_COVARIANT_COMPONENT_CHANGE`;
- `METRIC_INVARIANT_COFRAME_GAUGE`;
- `SUPPLIED_SPLIT_RESEATED_DEFINED`;
- `SUPPLIED_SPLIT_UNDEFINED_SIGNATURE`;
- `SUPPLIED_SPLIT_MARGINAL`;
- `NUMERIC_COVARIANCE_FAILURE`.

Tensor geometry and supplied-split diagnostics must be reported on separate axes. A coordinate
change is never counted as a new geometry. A newly re-seated first-two/last-two split is not silently
identified with the push-forward of the original distributions.

## Premise ledger

| item | tag | scope/source |
|---|---|---|
| Four-dimensional conformal-Lorentzian coframe/metric | `pinned-by-THEORY`, conditional realization | parent complete-metric map and canonical evaluator |
| Existing 48 x 16 x 8 jet universe | `pinned-by-EVIDENCE` | parent ensemble atlas |
| Exact twelve finite transformations | `free-and-explored` | bounded probes fixed above before outcomes |
| Constant coordinate transformations only | `free-and-explored` limitation | nonlinear charts are not covered |
| Lorentz internal coframe transformations | `pinned-by-THEORY` as metric redundancy | parent redundancy ledger G01/G02 |
| Coordinate diffeomorphism representation equivalence | `pinned-by-THEORY` as representation redundancy | parent redundancy ledger G03 |
| First-two/last-two 2+2 split | `CHOSE`, conditional | parent realization G06; audited rather than promoted |
| Ensemble identity attached to parent histories | `CHOSE` | masks are transformed after construction; they are not re-fit or re-parameterized |
| Absolute component activity threshold `1e-9` | `pinned-by-HABIT`, inherited numeric rule | parent ensemble atlas; margins must be reported |
| Split eigenvalue/signature tolerance `1e-9` | `pinned-by-HABIT` | numeric classification only |
| Relative covariance/reconstruction tolerance `1e-10` | `pinned-by-HABIT` | certification gate |
| Action, source, carrier, section, boundary, physical scale | `OPEN` and not sampled | outside atlas |

## Certification and falsification contract

The build fails closed unless:

1. all frozen input manifests match;
2. all 6,144 parent configurations and 5,760 parent interactions are accounted for;
3. all 73,728 configuration and 69,120 interaction transformation rows exist uniquely;
4. every registered `J` is invertible and every registered `Lambda` preserves the internal metric;
5. `C01/C02` and `C03/C04` round trips have relative error at most `1e-10`;
6. metric, curvature, scalar, and Cartan covariance residuals are at most `1e-10`, otherwise the row
   is retained as `NUMERIC_COVARIANCE_FAILURE` and the atlas cannot certify invariance;
7. local Lorentz coframe jets reproduce unchanged metric two-jets to `1e-10` on an independently
   fixed anchor set containing every carrier/context pair and both empty/full masks;
8. every admitted transformed split reconstructs the transformed metric two-jet to `1e-10`;
9. no undefined or marginal split is imputed, discarded, or included in a defined-only span rank;
10. Möbius tensors agree with the corresponding linear tensor representation to `1e-10` wherever
    that comparison is defined;
11. activity-concordance and span-rank statements include threshold margins and defined-row counts;
12. a fresh independent verifier recomputes the load-bearing transformation and split algebra without
    importing the atlas builder.

Required exercised catch-proofs must reject a missing transformation row, duplicate row, singular
chart, non-Lorentz coframe, wrong inverse pairing, omitted local-Lorentz derivative, tensor-index
permutation error, invalid split silently treated as valid, undefined split imputation, mutated parent
input, altered ensemble mask, Möbius cube omission, threshold-margin omission, and claim escalation.

## Required outputs

- deterministic builder and independent verifier;
- exact transformation registry;
- one configuration-orbit shard and one Möbius-orbit shard per transformation;
- shard registries with row counts and SHA-256 values;
- aggregate invariance, split-domain, interaction-order, span-rank, and numeric-margin censuses;
- premise/status ledgers, anti-imposition audit, machine-readable result, transcripts, commands,
  repository gates, manifest, technical audit report, lay report, and next-decision record.

Compact transformed ledgers are permitted instead of duplicating full transformed tensor arrays,
because each transformed tensor is deterministically reconstructible from the immutable parent raw
jets plus the exact transformation registry. The compact rows must retain the transform, object,
status, norms, residuals, activity, split-domain status, and source identity needed to reproduce every
aggregate.

## Maximum allowed conclusion

`BOUNDED_CHART_COFRAME_AND_SUPPLIED_SPLIT_INVARIANCE_ATLAS_CHARACTERIZED`

The atlas may classify invariant tensor content, component dependence, coframe gauge behavior, and
supplied-partition dependence within the registered finite transformation set. It may not claim a
globally selected chart, coframe, 2+2 split, carrier, boundary, action, matter law, physical universe,
or proof over the full diffeomorphism/Lorentz groups.
