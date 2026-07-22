# UDT Motif-to-Hopf Correspondence Audit — Preregistration

Date: 2026-07-22

Parent: `50756174718908e1aa5fd0a721f5ae6c527c4c8e`

Branch: `codex/udt-motif-hopf-correspondence-2026-07-22`

Mode: CPU-only, metric-led correspondence audit. No action, EOM, relaxation, carrier adoption,
physical boundary choice, empirical target, GPU work, canonization, or repository reorganization.

## Whole question

Do the five pointwise metric/phi motifs already observed in the complete registered two-jet lattice
continue coherently from point to point, form smooth intrinsic distributions, and supply enough
global reciprocal-angular structure to define a Hopf connection or Hopf class without first
assuming the existing round-`S2` carrier or `L2+L4` action? Only after that question is answered may
any metric-derived object be compared with the existing conditional Hopf seed/soliton.

This audit is not allowed to search for a rare configuration that resembles the desired particle.
All registered coherent identities and all 31 instrument families receive equal treatment.

## Frozen sources

The following source identities must match before any new outcome is computed:

| source | required SHA-256 | role |
|---|---|---|
| `udt_instrument_motif_atlas_2026-07-21/SHA256SUMS.txt` | `97dac2c32317deb603a054cffd3d2162f537d8bc7806d2276fa7e8544dd22ed5` | complete pointwise motif vocabulary and algorithms |
| `udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt` | `3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757` | 48 carrier vectors, 16 masks, four analytic banks |
| `udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt` | `b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad` | metric/connection/curvature evaluator |
| `null_section_hopfion_metric_audit_2026-07-19/SHA256SUMS.txt` | `e195d14349407c23e4a050628ec84298d3d35e23e2c25b5cf285a5c81f8e989b` | reciprocal-toric compatibility witness and soldering obstruction |
| `angular_toric_closure_selector_2026-07-19/SHA256SUMS.txt` | `64d664a76a28c170cdc293626cd6a5011755ee4eeaa414a303ace7b6eec9ec50` | conditional global toric/cap closure classification |
| `native_hopfion_topology_audit_2026-07-19/SHA256SUMS.txt` | `6f03f82d485d4a20c2d2bfc13dc8979c1b229bf92c53f0eb36831abf3d75febc` | carrier provenance and topology controls |
| `noNull_energy.py` | `53110844b3925b9b46bb48a3865f1bf9f60290efdd01a5830e0e388aeb477444` | comparison-only conditional action implementation |
| `noNull_resolve.py` | `995df0c30e1595a83d1335050be8e3fbbfb22f02b6b5d6643787048cc2d7aa2b` | comparison-only conditional carrier/charge implementation |

No source may be edited.

## Tile A — complete coherent-path continuation

The structural ensemble contains exactly

```text
4 analytic banks * 48 carrier vectors * 16 ensemble masks = 3,072
```

coherent analytic configuration identities. For each bank use the already registered ordered point
pair `B0:P0->P4`, `B1:P1->P5`, `B2:P2->P6`, or `B3:P3->P7`. Evaluate the same analytic metric/phi
configuration at the 17 fixed affine nodes `t=j/16`, `j=0..16` along that line.

At every node classify all 31 nonempty subsets of `R,H,D,RG,WG` with the frozen motif algorithm.
Retain every motif and margin. Match primitive projectors only by a minimum-distance assignment
between adjacent nodes after requiring identical primitive rank/signature multisets. Record
births, deaths, degeneracies, motif changes, permutation holonomy, and continuation margins. No
path is rejected for changing class.

Required coverage: 52,224 metric/phi two-jets and 1,618,944 family classifications.

These are coherent local analytic paths, not EOM solutions, worldlines, physical evolution, or a
global finite-cell atlas.

## Tile B — complete local distribution test

At each path midpoint, evaluate symmetric coordinate stencils in all four coordinates at
`h=1e-4` and `h/2`. For every one of the 31 families whose primitive projector rank/signature
multiset is stable across the stencil, match the complete projector set and estimate projector
derivatives at both steps.

For every primitive rank-two or rank-three image and every unique complementary rank-two split,
compute the projector Frobenius obstruction

```text
Q^mu_nu (P^rho_alpha nabla_rho P^nu_beta
         - P^rho_beta nabla_rho P^nu_alpha).
```

The complementary distribution is tested separately. Rank-one distributions are recorded as
locally integrable by dimension, not as globally oriented vector fields.

Numerical classification thresholds, chosen only as certification controls:

- derivative convergence `<=5e-3`: converged;
- normalized Frobenius obstruction `<=1e-7`: numerically integrable;
- obstruction `>=1e-5`: numerically nonintegrable;
- the interval between them: retained uncertain.

No local integrability result may be promoted to periodicity, topology, a physical angular sector,
or a carrier.

## Tile C — global eligibility and reciprocal-toric control

A coherent local family is eligible for a Hopf-number calculation only if its source supplies all
of the following without post-outcome choice:

1. a compact or correctly compactified three-domain;
2. a globally smooth intrinsic time/rest split or an equivalent spatial construction;
3. globally oriented projectors or an explicit transition cocycle;
4. periodic/gluing/collapse data and regular endpoint behavior;
5. an intrinsic connection with gauge/frame covariance; and
6. a normalization making the Chern-Simons/Hopf integral topological.

Absence of those data is recorded as `GLOBAL_DATA_ABSENT`, not converted into a zero Hopf charge.
No coordinate cube may be silently compactified and no local polynomial coordinate may be declared
periodic.

Separately use the already disclosed conditional reciprocal-toric class as a positive algebraic
control:

```text
g = -dt^2 + A(phi)^2 dphi^2
    + Omega(phi)^2 [exp(-2phi) dxi1^2 + exp(2phi) dxi2^2].
```

`A` and `Omega` remain arbitrary positive functions on the open orbit region. The audit will derive
the `R/H/D` motif/projector structure generically, identify every degeneracy condition, and test
whether the transverse axes are recovered without using a carrier. Periods, full phi range,
diagonal/anti-diagonal circle action, and cap cycles remain separately `CONDITIONAL`; the control
must report results both with and without them.

## Tile D — connection, twist, and Hopf class

Only when the Tile-C eligibility gates are met may the metric-dual connection and its curvature be
formed. For the reciprocal-toric control, compute the general finite-endpoint Chern-Simons integral
before taking any cap limit. Report nonintegral finite-endpoint values, same-cycle/no-cap cases, both
orientations, and every discrete ambiguity. A unit class may be called conditional only after the
full registered toric/cap premises are supplied.

The metric motif projectors must not be credited with selecting the equal-weight diagonal generator
unless that selection follows from the tested geometry. If the projectors recover axes but not the
circle action, the selector remains open.

## Tile E — comparison with the existing Hopf branch

Construction remains blind to the internal `S2` field and `L2+L4` functional. After Tiles A-D are
frozen, compare any eligible metric quotient map with:

- the exact `hopf_seed` formula in `hopfion_arc_scripts_2026-07-05/fs_hopfion.py`;
- the toroidal seed only as a same-class comparison;
- the banked relaxed `Q approximately 1` configuration only at its existing evidence grade; and
- the corrected no-null action only as a conditional downstream model.

Exact seed equivalence, if present, is not equivalence to the relaxed field, not derivation of the
full configuration space `Map(S3,S2)`, and not derivation of `L2+L4`, stability, source, mass, or
time-live persistence.

## Premise ledger

| item | status | bounded meaning |
|---|---|---|
| four-dimensional Lorentzian metric plus signed phi | `pinned-by-THEORY / CONDITIONAL CURRENT ARENA` | inherited current arena |
| 3,072 coherent identities | `free-and-explored` | complete registered analytic family identities |
| 17 affine path nodes | `FREE NUMERICAL COVERAGE CONTROL` | not a physical trajectory |
| all 31 instrument subsets | `pinned-by-COMPLETENESS` | no motif family filtered |
| projector matching | `FREE COVARIANT NUMERICAL DIAGNOSTIC` | assignment by invariant projectors, not coordinate eigenvectors |
| finite-difference steps and tolerances | `pinned-by-HABIT / NUMERICAL ONLY` | convergence checked and margins retained |
| global domain/boundary/periodicity/caps | `OPEN` | may not be supplied to local families |
| reciprocal-toric control | `CONDITIONAL PRIOR WITNESS` | comparison/control, not selected universe |
| `S2` carrier and `L2+L4` | `POSIT / CONDITIONAL / COMPARISON ONLY` | excluded from construction |
| action, source, mass, scale, dynamics | `OPEN / EXCLUDED` | no conclusion allowed |

## Falsification and catch contract

A verified bounded result requires:

1. all frozen source hashes pass before outcomes;
2. exact 3,072/52,224/1,618,944 path coverage with no filtered family;
3. endpoint rows reproduce the frozen pointwise motif atlas classifications;
4. every continued projector remains idempotent, mutually annihilating, complete, metric
   self-adjoint, and operator-invariant within the frozen tolerances;
5. projector matching is invariant under stored coordinate transformations at blind anchors;
6. both stencil steps are preserved and every failed convergence or degeneracy is retained;
7. local configurations lacking global data never receive a zero or nonzero Hopf number;
8. reference-only toric premises remain explicit in every conditional unit-class row;
9. the connection calculation is independent of `Omega` where claimed and retains finite-endpoint
   dependence;
10. direct carrier relabeling without frame/connection data is rejected;
11. exact Hopf-seed comparison cannot promote the carrier/action to native;
12. catches reject a missing family/path, projector permutation error, dropped degeneracy,
    manufactured periodicity, manufactured compactification, omitted circle-action premise,
    forced `Q=1`, false seed/relaxed-field identity, and an imported `L2+L4` construction.

An independent implementation must recompute the load-bearing toric algebra and a preregistered
hash-selected subset of coherent path/stencil identities without importing the production builder.

## Maximum allowed conclusion

At most:

`BOUNDED_METRIC_MOTIF_TO_HOPF_CORRESPONDENCE_CHARACTERIZED`.

The audit may establish a metric-native local projector ingredient, an exact conditional global
Hopf witness, or a scoped missing-data obstruction. It may not claim native carrier emergence,
matter emergence, a selected universe, an action, a source, mass, stability beyond the existing
conditional branch, or a physical boundary theorem.
