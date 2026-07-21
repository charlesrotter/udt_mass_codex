# P05 conditional full-equation and variation build — preregistration

Date: 2026-07-21

Base: `39dda1aac9a8dab16428f7d031e1668b9bc7fde0`

Branch: `codex/udt-p05-conditional-operator-builds-2026-07-21`

Registered stage: `P05 / FULL_EQUATION_AND_VARIATION_BUILD`

Authorized lanes:

- `P05-L01 / PRE_SCALE_C2_BACH_BULK`
- `P05-L02 / POST_SCALE_EH_BULK`

Excluded lane: `L03 / TWO_STAGE_BRIDGE_OPEN`, because P04 found no action, operator, selection
functional, or matching map to vary.

Protocol maximum: `NAMED_DYNAMICS_OPERATOR_COMPLETE_IN_EXACT_PREMISE_CLASS`

Preregistered fallback maximum if the finite-cell variational problem cannot close:
`NAMED_BULK_OPERATORS_AND_VARIATION_OBSTRUCTIONS_CHARACTERIZED`

## Frozen parent evidence

- P04 tip: `39dda1aac9a8dab16428f7d031e1668b9bc7fde0`
- `SHA256(P04/SHA256SUMS.txt) = d01d65fc5abcc35078c961d0d3fc0eec7ad26e205735a77f7d83e2b45121de3f`
- `SHA256(P04/RULING_RESULT.json) = d524a993798ec8148421f5b2099358354025dae331fcef5388f6ad4c4c256039`
- `SHA256(Arm-C/SHA256SUMS.txt) = 99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f`
- frozen Arm-C variation-domain witness:
  `084511961b6c69270278c64ae69f58942b044f106990e7071a5003f8535aee7e`
- frozen Arm-C conditional-action witness:
  `33e804e990fad69e49b3471adc8443f8037e7d4b5f617999dd1579286c3e430c`
- frozen Arm-C boundary witness:
  `e29f017a354275b62d415961365583d165bffc9637303b1a3ae9feb17510184d`

The Arm-C scripts are provenance and regression anchors. P05 must implement its load-bearing algebra
independently rather than import them.

## Whole question

For each P04-authorized conditional bulk lane, what is the complete unrestricted metric Euler
operator, its Noether identities, nonlinear principal character, raw covariant boundary current,
constraint projections, and field-realization compatibility **before any symmetry reduction**?

Does current UDT authority also supply enough finite-cell boundary and extra-field information to
turn either bulk operator into a complete differentiable P05 action?

## Question provenance

`CONDITIONAL-LAW / OBSERVING`: the laws are not being derived from UDT here. P04 authorized them as
premise-stamped mathematical arenas. P05 observes their complete operator footprints and failure
surfaces. It does not test whether they reproduce GR, particles, solitons, cosmology, or any desired
solution.

## Exact bounded regime

- CPU-only exact symbolic tensor identities, finite-dimensional chain-rule witnesses, and ledger
  construction; no numerical solution.
- Four-dimensional regular Lorentzian metric branch is `CONDITIONAL`.
- Curvature convention is fixed for reproducibility:
  `R^a_bcd = partial_c Gamma^a_db - partial_d Gamma^a_cb + Gamma^a_ce Gamma^e_db - Gamma^a_de Gamma^e_cb`.
- Metric variation variable is `h_ab = delta g_ab`; indices on `h` use the unvaried metric.
- Antisymmetrization carries weight one-half.
- `alpha`, `kappa`, the cosmological coefficient `Lambda`, and Euler coefficient `beta` remain
  symbolic `free-and-explored`; no numerical or physical normalization is chosen.
- `L01` action inventory is the conditional family `alpha C_abcd C^abcd + beta E4`.
- `L02` action inventory is the conditional family `kappa (R-2 Lambda) + beta E4`.
- The four-dimensional Euler density has no bulk metric equation but its boundary current is retained.
- Sources and carriers are absent, not set to zero as a physical claim. Their field branches remain
  explicit blocked extensions.
- The full ten-component metric is varied before any reciprocal, static, spherical, diagonal,
  homogeneous, or gauge reduction.
- Principal symbols are classified both ungauge-fixed and on explicitly diagnostic gauge quotients;
  gauge fixing is not adopted as UDT physics.
- All seven P04 field realizations and all 12 P03G global axes remain visible.
- No boundary polarization, boundary functional, topology, orientation, normal, corner rule, physical
  representative, scale, `X_max`, matter, or source is selected.

## Premise tags

| object | tag | role |
|---|---|---|
| four-dimensional Lorentzian arena | `CONDITIONAL_BRANCH` | required by both named classifications |
| metric-only bulk field | `ADDED_CLASS_PREMISE` | defines the two named bulk operators |
| local diffeomorphism covariance | `ADDED_CLASS_PREMISE` | yields the metric Noether identity |
| pre-scale exact CSN | `ADDED_L01_CLASS_PREMISE` | admits the conditional `C^2` direction |
| unrestricted variation before scale | `ADDED_L01_CLASS_PREMISE` | gives the Bach operator |
| selected physical representative | `OPEN_REQUIRED_L02_INPUT` | EH cannot be evaluated physically without it |
| unrestricted post-scale variation | `ADDED_L02_CLASS_PREMISE` | gives Einstein-Lovelock bulk equations |
| locality and derivative inventory | `ADDED_CLASS_PREMISE` | fourth order L01; at-most-second order L02 |
| coefficients | `free-and-explored` | symbolic; no value or normalization selected |
| finite cell and scalar seal wire | `pinned-by-THEORY_SCOPED` | demands boundary accounting; supplies no complete polarization |
| complete boundary action/variation | `free-and-explored / OPEN` | must not be imported by habit |
| field realization `C01`--`C07` | `free-and-explored` | no field removed |
| topology, cover, degeneracy, connection | `free-and-explored` | P03G carryforward |
| source, carrier, mass, charge | `EXCLUDED_FROM_P05` | no matter action authorized |
| comparison or merit target | `EXCLUDED_FROM_P05` | no feedback into operator construction |

## Frozen candidate and equation universe

P05 must account for, without ranking:

1. both complete ten-component metric bulk variations;
2. the Euler/topological coefficient and its boundary-only effect;
3. the free cosmological coefficient in L02, including the `Lambda=0` subcase;
4. Euler tensors and their trace/divergence Noether identities;
5. normal-normal, normal-tangential, and tangential projections before any foliation is selected;
6. raw covariant symplectic-potential/boundary-current channels in `h_ab` and `nabla h_ab`;
7. every missing finite-cell boundary polarization, corner, reference, and normalization;
8. all 21 lane/field pairs inherited from P04 for L01/L02 plus L03 exclusion status;
9. all 12 free global axes;
10. ungauge-fixed principal degeneracies and diagnostic gauge-reduced principal factors;
11. restrict-then-vary, multiplier, and unrestricted-then-restrict domains; and
12. an exercised reduced-action scar showing that projected Euler equations need not imply the full
    equations.

No source, solution ansatz, boundary condition, or desired output may be added after algebra is seen.

## Registered outputs

- `lane_L01/ACTION_AND_CONVENTIONS.md`
- `lane_L01/BULK_OPERATOR.tsv`
- `lane_L01/BOUNDARY_CURRENT.tsv`
- `lane_L01/NOETHER_AND_CONSTRAINTS.tsv`
- `lane_L01/PRINCIPAL_CHARACTER.tsv`
- corresponding five `lane_L02/` records
- `FIELD_EQUATION_COMPLETENESS.tsv`
- `VARIATION_DOMAIN_MATRIX.tsv`
- `REDUCED_ACTION_SCAR.tsv`
- `GLOBAL_AXIS_CARRYFORWARD.tsv`
- `OPERATOR_DEPENDENCY_GRAPH.json`
- `STATUS_LEDGER.tsv`
- exact main algebra, an independent implementation, corruption catches, reports, repository gates,
  commands, and SHA-256 manifest

## Falsification and certification contract

P05 fails closed if any of the following occurs:

1. the metric is reduced before its ten Euler equations and boundary current are recorded;
2. the Bach or Einstein operator is labeled native, derived from UDT, or physically selected;
3. the Bach result escapes the L01 premise class or EH escapes the post-scale L02 class;
4. the Euler density is erased merely because its four-dimensional bulk equation vanishes;
5. `Lambda` is silently set to zero or assigned a value;
6. a source or carrier is inserted;
7. an independent extra field is silently discarded or called governed by a metric-only bulk;
8. unrestricted, hard-restricted, multiplier, and restrict-then-vary equations are conflated;
9. a projected/reduced Euler equation is treated as the full tensor equation;
10. a standard boundary term, Dirichlet rule, asymptotic reference, topology, or corner condition is
    imported as native finite-cell data;
11. raw boundary-current channels are omitted or called differentiable without a declared
    polarization/completion;
12. an ungauge-fixed principal operator is called nondegenerate, hyperbolic, or elliptic;
13. regular inverse-metric results erase degenerate/type-changing branches;
14. any P03G global axis is fixed;
15. an ODE, PDE, solution, comparison, GPU job, bridge operator, or canonization is launched;
16. a parent artifact changes; or
17. deterministic replay, independent algebra, or any exercised mutation catch fails.

## Stop and maximum conclusion rule

If the raw bulk operators and currents are exact but current UDT authority does not select the
complete boundary variation or equations for extra fields, P05 must stop at the preregistered
fallback conclusion. It may not award the protocol-level “operator complete” conclusion to either
lane.

No P06 branch decomposition or solve follows without a new explicit dispatch.
