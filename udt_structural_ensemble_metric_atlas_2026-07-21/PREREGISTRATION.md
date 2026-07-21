# UDT structural-ensemble metric atlas — preregistration

Date: 2026-07-21

Base: `1d11d7645b651712e917cb55c535c5a544aacae9`

Branch: `codex/udt-structural-ensemble-atlas-2026-07-21`

Mode: CPU-only deterministic configuration mapping. No action, EOM, ODE/PDE solve, relaxation,
physical evolution, desired geometry, empirical comparison, carrier, or GPU work.

## Owner direction and method order

Charles's orchestra framing asks whether the complete metric acts through coordinated groups rather
than one function at a time. The independent-amplitude and volume atlases have completed the
registered same-chart raw amplitude tile. This package now organizes the controls into structural
ensembles and maps their joint tensor effects before any physical comparison or derivation.

This is `MAP -> OBSERVE`. It must not name an ensemble as matter, energy, gravity, source, force,
carrier, selector, or dynamical mechanism. It must preserve every configuration and interaction,
including zero, redundant, or unexpected results.

## Whole question

Within the frozen regular `2+2` coframe chart and finite analytic family, what local geometric
activity is supplied by each structural ensemble alone, by each pair, each triple, and all four
together? Which saved tensor components are additive across ensemble toggles, and which contain
nonzero higher-order inclusion-exclusion interactions?

The question is metric-led. It maps the complete metric/coframe and the independent signed `phi`
configuration branch. It does not load a target action, field equation, solution, or physical
selection rule.

## Frozen sources

Inherit the chart, amplitudes, coefficient banks, sample points, two-jet evaluator, thresholds, and
raw preservation rules from:

```text
udt_amplitude_volume_metric_atlas_2026-07-21/SHA256SUMS.txt
5182486f4a87080096532d9fe5ba999837ac79fac979c5694f216209ae41c112

udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt
b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad
```

Every entry of both manifests must replay. No parent field, chart, coefficient, point, sign,
tolerance, metric–`phi` independence rule, or evaluator formula may change.

## Structural partition frozen before outcomes

Partition the eleven independent controls exactly once:

| ensemble id | descriptive name | controls | chart role |
|---|---|---|---|
| `E0` | `BASE_BLOCK` | `alpha_0,alpha_1,alpha_2` | three latent controls of the two-dimensional base metric block |
| `E1` | `ANGULAR_SCREEN_BLOCK` | `alpha_3,alpha_4,alpha_5` | three latent controls of the two-dimensional positive screen metric |
| `E2` | `SHIFT_CONNECTION_BLOCK` | `alpha_6,alpha_7,alpha_8,alpha_9` | four base–screen shift/connection controls |
| `E3` | `PHI_FIELD` | `beta` | independent signed `phi` two-jet control |

This is a chart-level bookkeeping partition. `E0` contains the registered base arena in which
reciprocal structure may later be tested; the ensemble label does not impose or derive a reciprocal
law. `E1` is not assumed round, spherical, compact, or a carrier. `E2` is not assumed to be a force
or gauge field. `E3` remains the independent open `C02` branch and is not assumed to source the
metric.

Audit before geometry that all eleven controls occur exactly once, no ensemble is empty, and no
control is shared.

## Ensemble masks

Use four bits ordered `(E0,E1,E2,E3)`. Evaluate all sixteen masks `0x0..0xF`, including the empty
mask. A selected ensemble retains the carrier vector's amplitudes for all of its controls; an
unselected ensemble sets only its control amplitudes to zero. The constant baseline coframe, every
metric sector, and the full evaluator remain present for every mask.

The empty mask is a shared comparison configuration, not a rejected state. The fifteen nonempty
masks comprise exactly four singletons, six pairs, four triples, and one four-way combination.

## Carrier-vector design frozen before geometry

Select carrier vectors only by identities already fixed in the parent volume design, never by their
geometric outcomes:

- all sixteen Hadamard directions at radius `1/4`: `R00_1..R15_1`;
- all sixteen Hadamard directions at radius `3/4`: `R00_3..R15_3`; and
- the first sixteen Halton interior identities: `V001..V016`.

This gives exactly 48 carrier vectors. Preserve their complete eleven amplitudes, design kind,
direction, radius, and Halton index byte-for-byte from the parent table. The two radial magnitudes
test amplitude dependence; the interior rows test unequal amplitudes. No carrier is weighted or
filtered by outcome.

## Bank and point schedule

Evaluate every `(carrier, mask)` identity in the frozen schedule:

```text
B0: P0,P4
B1: P1,P5
B2: P2,P6
B3: P3,P7.
```

Required configuration count:

```text
48 carriers * 16 masks * 8 bank/point contexts = 6144.
```

Retain duplicate configurations and record both complete-configuration and metric-two-jet hashes.

## Möbius interaction definition

For a fixed carrier and bank/point context, let `F(S)` be a saved payload evaluated with ensemble
mask `S`. For every nonempty target mask `T`, compute the Boolean-lattice inclusion-exclusion term

```text
I_T[F] = sum over U subset T of (-1)^(|T|-|U|) F(U).
```

This is an exact finite-difference decomposition of the chosen chart payloads. It is not a physical
interaction energy, coupling constant, causal mechanism, perturbation expansion, or action term.

Preserve `L2` and maximum-absolute norms of `I_T` for:

- complete slot two-jet;
- complete metric two-jet;
- lowered Riemann tensor;
- lowered Weyl tensor;
- Ricci tensor;
- scalar curvature;
- the two screen-shear tensors represented by their three symmetric trace-free coordinates;
- the two-component shift twist; and
- complete signed `phi` two-jet.

For each target mask and payload, stack all 384 interaction vectors
(`48 carriers * 8 contexts`) and report finite sampled span rank and singular margins. Scalar
curvature has one component and is treated as a one-column payload. These component-space ranks are
coordinate/chart diagnostics, not invariant degrees of freedom or field counts.

Use the inherited numeric threshold `1e-9`. Record interactions within a factor of 100 of the
threshold as `NUMERIC_UNCERTAIN`; retain them. Uniformity, zero/nonzero patterns, or expected `phi`
decoupling are observations, never pass criteria.

## Configuration observations

For every one of the 6,144 configurations preserve the carrier amplitudes, effective masked
amplitudes, mask membership, slot/metric/coframe/`phi` two-jets, determinant and inertia, raw
identity residuals, full saved curvature tensors, scalar contractions, Ricci and curvature-operator
ranks, screen expansion/shear, twist, mixed base/screen curvature, coordinate activity, and signed
`phi`/`dphi` class.

Build objective class censuses by mask, carrier family, bank, and point. No class is assigned
physical merit.

## Premise and choice ledger

| item | tag | bounded meaning |
|---|---|---|
| four-dimensional conformal-Lorentzian arena | `pinned-by-THEORY / CONDITIONAL CURRENT ARENA` | inherited current arena |
| regular factorized coframe chart | `pinned-by-VERIFIED TOOL / CHOSEN CHART` | not a global theorem |
| four-ensemble partition | `FREE STRUCTURAL BOOKKEEPING CHOICE` | must be audited, not physicalized |
| 48 carrier identities | `FREE NUMERICAL COVERAGE CONTROL` | selected by prior identities only |
| all 16 masks | `PINNED-BY-COMPLETENESS` | exhaustive Boolean masks for this partition |
| Möbius decomposition | `FREE EXACT DIAGNOSTIC` | algebraic finite-difference bookkeeping |
| coefficient banks and points | `FREE COVERAGE CONTROLS INHERITED` | finite analytic family |
| independent `phi` | `OPEN CONFIGURATION BRANCH C02` | no source or metric feedback law |
| action, source, boundary, topology, carrier, scale | `OPEN / EXCLUDED` | not sampled |
| coordinate dependence | `CONFIGURATION DEPENDENCE ONLY` | not physical evolution |
| physical/GR/particle merit | `EXCLUDED` | no ranking criterion |

No untagged `pinned-by-HABIT` physical choice is allowed.

## Required evidence

- exact source lineage and manifest replay;
- `ENSEMBLE_REGISTRY.tsv` and one-row-per-control coverage;
- `CARRIER_VECTOR_REGISTRY.tsv` and exact parent reconciliation;
- `ENSEMBLE_MASK_REGISTRY.tsv` with all sixteen masks;
- `CONFIGURATION_OBSERVATIONS.tsv` and complete raw JSONL;
- `MASK_GEOMETRY_CENSUS.tsv`;
- `MOBIUS_INTERACTIONS.tsv` with all `48*8*15 = 5760` target/context rows;
- `INTERACTION_SPAN_RANKS.tsv`;
- `INTERACTION_ORDER_CENSUS.tsv`;
- `NUMERIC_MARGIN_LEDGER.tsv`;
- coverage, ten-criterion scope, and anti-imposition ledgers;
- deterministic machine-readable result and transcript;
- an independent design/mask/Möbius reconstruction, all-record tensor reconciliation, and fresh
  adversarial review.

## Fail-closed checks and catch-proofs

Reject a missing/duplicate/shared control, wrong ensemble membership, missing/duplicate carrier,
carrier-vector drift, missing/duplicate mask, missing configuration, filtered class, wrong
bank/point schedule, missing interaction target, incorrect subset sign, corrupted interaction norm,
incorrect span rank, source/manifest drift, ensemble physicalization, action/EOM promotion,
dynamics promotion, `phi` source promotion, genericity/exhaustiveness promotion, or GPU use.

## Falsification and certification contract

Design/mask/identity/source failures are tooling failures and stop the atlas. Once geometry begins,
all outcomes are retained. Unexpected zero interactions, ubiquitous interactions, changing class
patterns, duplicate rows, or rank loss are reportable observations and cannot fail the computation.

Independent verification must reconstruct the design from the committed preregistration and parent
registries, replay every raw hash, independently recompute every saved interaction from the mask
lattice, and reconstruct full curvature at preregistered anchors spanning singleton, pair, triple,
and full masks. A fresh context must challenge chart dependence, shared-code independence, numeric
margins, and any claim of cooperation.

## Scope ceiling

Maximum conclusion:

```text
BOUNDED_STRUCTURAL_ENSEMBLE_AND_MOBIUS_INTERACTION_ATLAS_CHARACTERIZED
```

This is not a genericity theorem, complete metric solution space, physical interaction law,
coupling, action, selector, source, carrier, boundary, dynamical solution, matter model, or universe
model.

