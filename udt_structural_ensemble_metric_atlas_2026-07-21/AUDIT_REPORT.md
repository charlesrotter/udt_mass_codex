# Structural-ensemble metric atlas — audit report

Date: 2026-07-21

Status: `VERIFIED-WITH-CAVEATS`

Maximum conclusion:

```text
BOUNDED_STRUCTURAL_ENSEMBLE_AND_MOBIUS_INTERACTION_ATLAS_CHARACTERIZED
```

## Whole question and bounded regime

The preceding atlases released all ten metric controls plus independent signed `phi`, then sampled
their bounded amplitude interior. This metric-led atlas asks how those controls behave when grouped
by their exact roles in the frozen regular `2+2` chart:

- `E0 BASE_BLOCK`: three base-metric latent controls;
- `E1 ANGULAR_SCREEN_BLOCK`: three positive-screen latent controls;
- `E2 SHIFT_CONNECTION_BLOCK`: four base–screen shift controls; and
- `E3 PHI_FIELD`: the independent signed `phi` control.

Every one of the sixteen ensemble masks is evaluated for 48 outcome-independent carrier vectors in
eight bank/point contexts. This gives 6,144 retained configurations. For every carrier/context, all
fifteen nonempty Boolean-lattice Möbius terms are computed for nine saved payloads, giving 5,760
interaction rows.

The partition is chart bookkeeping, not ontology. No action, field equation, solution, boundary,
topology, carrier, physical scale, empirical target, or physical interaction definition enters.

## Configuration-level atlas

Each mask has 384 records. The sampled class pattern is:

| mask content | observed local class |
|---|---|
| empty `M0` | 384 flat `R0_K0_S0_T0_M0` |
| base `M1` | 383 `R4_K6_S0_T0_M1`; one threshold-classified `R4_K5_S0_T0_M1` |
| angular screen `M2` | 384 `R4_K6_S2_T0_M1` |
| base + screen `M3` | 384 `R4_K6_S2_T0_M1` |
| shift and every core mask containing shift `M4..M7` | 384 `R4_K6_S2_T1_M1` per mask |
| phi only `M8` | 384 flat `R0_K0_S0_T0_M0` |
| each geometric mask plus phi `M9..MF` | same metric class as its phi-free partner |

`R`, `K`, `S`, `T`, and `M` are Ricci rank, curvature-operator rank, shear rank, twist rank, and
mixed base/screen curvature activity. They are diagnostic classes, not merit labels.

There are 120 retained numerical-uncertainty flags, all in the curvature-operator rank of the
base-only or screen-only masks and their exact phi copies. The two `K5` rows are the same metric jet
at `V013_B2_P2`, once without and once with phi, and are themselves `NUMERIC_UNCERTAIN`. No uncertain
record is discarded or promoted.

## Registered Möbius decomposition

For each saved payload, the atlas computes

```text
I_T[F] = sum over U subset T of (-1)^(|T|-|U|) F(U).
```

This reports which effects in the chosen chart are present only when specified ensembles are
enabled together. It is not a physical coupling, interaction energy, causal mechanism, or action
term.

### Slot and metric two-jets

At saved floating precision, the complete slot two-jets have only singleton terms: the three
geometric slot groups add independently in this construction. The metric two-jet has active singleton terms for all three geometric
ensembles and one active pair term:

| target | metric interaction rows | sampled span rank |
|---|---:|---:|
| base–screen `M3` | 0 / 384 | 0 |
| base–shift `M5` | 0 / 384 | 0 |
| screen–shift `M6` | 384 / 384 | 105 |
| base–screen–shift `M7` | 0 / 384 | 0 |

Thus, in the registered split formula, the screen and shift blocks already combine non-additively
when the metric is assembled. The span rank is only a finite component-space diagnostic in this
chart; it is not a count of invariant or physical degrees of freedom.

### Curvature

Curvature contains interactions not visible in the slot or metric addition pattern:

| target | active Riemann rows | sampled Riemann span rank | minimum active maximum component |
|---|---:|---:|---:|
| base–screen `M3` | 384 / 384 | 19 | `1.10e-3` |
| base–shift `M5` | 384 / 384 | 20 | `8.20e-4` |
| screen–shift `M6` | 384 / 384 | 20 | `2.32e-3` |
| base–screen–shift `M7` | 336 / 384 | 20 | `8.49e-6` |

All 48 inactive triple rows occur at `B0:P0`; their maximum discarded Riemann component is
`8.33e-17`. Every other registered triple context is active above `1e-9`. The three pair terms are
active in every carrier/context. Ricci, Weyl, and scalar-curvature interaction censuses follow the
same active/inactive pattern.

The pair curvature terms with zero pair metric terms are not contradictions. Curvature is a
nonlinear function of the complete metric and its derivatives, so separately additive metric
changes can have non-additive curvature. The triple term similarly records nonlinear assembly in
the sampled curvature, not a three-body force or dynamical coupling.

### Shear and twist

- Screen and shift singletons each produce sampled shear.
- Their pair has active shear interaction in 336 of 384 contexts; the 48 inactive rows are again
  exactly `B0:P0`. The minimum active maximum component is `1.36e-4`.
- Base-related shear interactions vanish at the registered threshold.
- Twist occurs in the shift singleton and has no higher-order Möbius term in this chart.

### Independent phi branch

The phi two-jet has exactly one active singleton term, `M8`, in all 384 contexts. Every higher-order
phi interaction is zero at the registered threshold. Every metric, curvature, shear, and twist term
containing phi is also zero, with the four-way Riemann maximum no larger than `2.78e-17`.

This confirms, at the registered threshold, the independence built into the present `C02`
configuration branch. It does
not show that physical UDT requires phi to be decoupled. A native metric–phi relation remains open.

## What the orchestra framing gained

Within the registered chart, the Boolean decomposition records:

1. their primitive slot controls are independently additive;
2. screen and shift combine during metric assembly;
3. all three geometric pairs produce additional curvature content; and
4. the three-way combination produces an additional curvature term in seven of eight sampled
   bank/point contexts.

For this chosen partition, reconstructing the sampled full-mask curvature from its Boolean
components includes pair and triple remainders; the singleton responses alone do not reproduce it.
That is an algebraic identity of the finite chart/payload decomposition. Nonlinear curvature can
produce such remainders without any exchange of energy or physical coupling between ensembles. It
is not a law telling the ensembles how to evolve or which metric is physical.

## Independent verification

The verifier does not import the ensemble builder. It independently reconstructs:

- all eleven control memberships, 48 parent carrier vectors, sixteen masks, and eight contexts;
- all 6,144 primitive slot and phi two-jets directly from the registered analytic polynomials,
  reassembles every metric two-jet, and reconstructs every curvature, Weyl tensor, rank, shear,
  twist, and class;
- all 5,760 Möbius interaction rows directly from the raw mask cubes; and
- all 135 interaction span ranks, margin rows, class censuses, and order censuses.

It passes 38 checks and 30 exercised negative tests: 27 mutate copied package structures and three
test an algorithm or expected digest. Maximum primitive disagreement is zero in the package replay;
maximum metric reassembly disagreement is `4.44e-16`; maximum curvature disagreement from the
reassembled metrics is `3.05e-16`; and maximum kinematic disagreement is zero. All raw records are
preserved in eight preregistered, hashed bank/point shards.

The anti-imposition table is a declared scope ledger whose consistency is machine-checked. Its
semantic content was separately inspected in the fresh adversarial review; the verifier does not
pretend that rereading the declaration alone proves the absence of every possible hidden physical
assumption.

A fresh correction review then used a separate direct-polynomial implementation. It independently
reproduced all 6,144 configurations and 5,760 Möbius rows, with maximum primitive, metric, curvature,
kinematic, Möbius-L2, and span-singular disagreements of `2.22e-16`, `4.44e-16`, `3.05e-16`,
`4.16e-17`, `4.46e-16`, and `1.78e-15`, respectively. Its verdict is
`PASS-WITH-CAVEATS`, with no blocking algebraic or evidence-ledger defect.

## Scope and remaining caveats

The ensemble partition is adapted to one chosen factorized coframe chart. A different coframe,
base/screen split, field basis, nonlinear reparameterization, or regional chart can redistribute
Möbius terms. Component span ranks are likewise chart dependent. The atlas samples 48 finite
carrier vectors and eight contexts, not arbitrary functions, continuum amplitude space, global
completion, boundaries, or evolution.

All rank and activity calls use the preregistered absolute `1e-9` threshold; they have not yet been
regraded under normalized or high-precision rank tests. The load-bearing pair and triple component
margins are comfortably separated from that threshold, but the two saved `K5` configuration labels
remain explicitly uncertain.

Consequently the atlas establishes a verified finite Möbius map, not an invariant ensemble theorem
or physical interaction map. The natural next gate is to audit which decomposition statements survive admissible
coframe/chart changes before treating the ensemble decomposition as a clue to a native law.

## Four evidence gates

1. **Preregistered:** yes; partition, masks, carriers, formula, evidence, and ceiling were committed
   before geometry; eight-way raw sharding was separately committed before outcomes.
2. **Full space or bounded scope justified:** bounded finite chart/carrier/context atlas only.
3. **Load-bearing premise independently verified:** yes; all 6,144 primitive and metric two-jets,
   curvatures, and all 5,760 Möbius rows were reconstructed, with 30 exercised negative tests.
4. **Every premise audited:** the registered finite-construction premises were audited. Coframe and
   chart invariance, normalized-rank robustness, native metric–phi relation, action, boundary,
   topology, scale, carrier, and dynamics remain explicitly open.

Grade: `VERIFIED-WITH-CAVEATS`. The caveats are the explicit chart, finite-design, and
configuration-not-dynamics scope.
