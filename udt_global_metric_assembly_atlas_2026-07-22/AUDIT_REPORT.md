# UDT Global Metric-Assembly Atlas

Date: 2026-07-22

Status: `FRESH_REVIEW_CORRECTIONS_APPLIED__INTERNAL_REPLAY_PASS__FRESH_CORRECTION_REVIEW_PENDING`

Maximum conclusion:

`BOUNDED_REGISTERED_GLOBAL_METRIC_ASSEMBLY_ATLAS_CHARACTERIZED__GLOBAL_QUOTIENT_SELECTION_OPEN`

## Result first

The atlas closes the first four requested mapping stages inside its preregistered registry, audits
the fifth selector stage, and stops at the activation gates for Stages 6 and 7.

The most important positive result is a metric-compatible continuous transport law for any smooth
complete projector motif. For mutually annihilating metric-self-adjoint projectors `P_a`, define

```text
K = sum_a (nabla_T P_a) P_a,
nabla_T U = K U.
```

Differentiating projector completeness and idempotence gives

```text
K is metric-skew,
[K,P_a] = nabla_T P_a.
```

Therefore `U` preserves the endpoint metric and intertwines the projector subspaces. This is a
native geometric connection for the motif bundles. It is not physical time evolution.

Across all 83 populated stable `(motif,instrument-family)` strata, deterministic dense anchors were
integrated at 33, 65, and 129 nodes. Seventy-six pass all preregistered transport gates. Seven retain
strict derivative-level numerical margins; their endpoint intertwining, metric-isometry, and RK4
refinement residuals remain small, but they are not promoted. Exact symbolic Lorentzian and
reciprocal-toric controls pass, and a separate `DOP853` implementation independently reproduces one
`FOUR_LINES`, one `LINE_PLUS_THREE`, and one `TWO_PLUS_TWO_LINES` transport anchor.

The finite-cell-path follow-up also found a coherent subfamily. Every one of the 1,536 frozen
midpoint-integrable `1+1+2` identity/family rows remains locally integrable on both complementary
rank-two sides at all nine sampled path nodes. This is not a midpoint accident.

Its provenance sharply limits the interpretation: all 1,536 rows come from structural mask `M8`,
where only `PHI_FIELD` is active. They are eight instrument-family presentations of 192 analytic
identities. Thus the coherent integrable branch is the orderly `phi`-field/Hessian solo already
suspected to form nested surfaces. It is not a full metric-angular orchestra, not two commuting
periodic generators, and not a metric-derived torus or carrier.

The global taxonomy retains 12 parametric completion families, including physical boundaries,
one-cap boundaries, determinant-zero same-cycle caps, determinant-one `S3`, all determinant-`p>1`
lens families, nonprimitive/singular caps, general `GL(2,Z)` torus bundles, mirror lifts,
nonorientable gluing, projector strata, nonintegrable distributions, and the conditional globally
diagonal reciprocal-toric class. No family is removed for failing to resemble matter or the desired
universe.

Registered Reciprocity, Common-Scale Neutrality, finite-cell/seal data, bootstrap, and the current
scale/matter inventory do not select one quotient class. Accordingly:

- Stage 6: `NOT_ACTIVATED__GLOBAL_QUOTIENT_NOT_SELECTED`;
- Stage 7: `NOT_ACTIVATED__NATIVE_DYNAMICS_UNDEFINED`;
- CPU time-live evolution runs: `0`;
- GPU runs: `0`.

## Stage 1 — continuous projector transport

The frozen atlas contains 95,232 identity/family paths:

| stable motif | paths |
|---|---:|
| full irreducible four-dimensional weave | 70,812 |
| scalar/silent | 11,328 |
| `1+1+2` | 7,845 |
| `1+3` | 2,880 |
| four lines | 1,055 |

There are 93,920 stable sampled paths and 1,312 transition or uncertain paths. All appear exactly
once in `PATH_ASSEMBLY_CENSUS.tsv.gz`. Transition paths receive no invented fine bundle.

The connection theorem follows directly from the complete projector algebra. With
`sum_a P_a=I`, `P_a P_b=delta_ab P_a`, and metric compatibility:

```text
K^dagger = sum_a P_a nabla_T P_a = -K,
[K,P_a] = nabla_T P_a.
```

The numerical equation in coordinates is

```text
dU/ds = (K-Gamma_T) U.
```

The dense-anchor census is:

| status | anchors |
|---|---:|
| `DENSE_TRANSPORT_PASS` | 76 |
| `DENSE_TRANSPORT_NUMERIC_MARGIN_RETAINED` | 7 |

The seven margins are listed in `NUMERIC_MARGIN_LEDGER.tsv`. They arise in finite-difference checks
of the exact metric-skew/commutator identities. The largest endpoint metric-isometry residual among
them is about `2.26e-9`, and the largest 65-to-129-node transport refinement is about `1.39e-7`.
The largest derivative identity residual is about `2.85e-6`, above the fixed `2e-7` gate. The exact
theorem remains valid; those numerical rows remain unresolved at the registered threshold.

Scalar and full-irreducible motifs transport the whole tangent space but supply no distinguished
proper subbundle. An open path supplies transport, not holonomy.

## Stage 2 — following the locally integrable candidates

The frozen midpoint atlas contains:

- 8,205 `1+1+2` identity/family rows;
- 6,669 with nonintegrable Lorentz/two-line complementary planes at the midpoint;
- 1,536 with both sides integrable there.

All 1,536 candidate rows were followed at `t=j/8`, `j=0..8`, retaining the original two stencil
steps and thresholds. The result is exactly 13,824 node rows, all
`BOTH_SIDES_SAMPLED_INTEGRABLE`.

The complete provenance is:

```text
structural mask: M8 = PHI_FIELD only
unique analytic identities: 192
instrument-family presentations per identity: 8
identity/family rows: 1,536
```

The eight families all contain `H`; any listed `R`, `RG`, or `WG` operator is zero in this
structural mask. This is why the rows must not be interpreted as 1,536 independent geometric
mechanisms. The result strengthens the `phi`-foliation observation and simultaneously weakens its
claim to be the missing angular/Hopf assembly.

The generic full orchestra remains dominated by the irreducible four-dimensional weave. The exact
reciprocal-toric axis/Hopf witness is consequently still a special conditional commuting stratum,
not a branch selected or even reproduced by the `PHI_FIELD`-only integrable census.

## Stage 3 — global completion catalogue

`COMPLETION_CLASS_REGISTRY.tsv` records 12 parametric families. Infinite cap and monodromy families
are represented by exact rules plus bounded arithmetic witnesses.

The cap witness census uses every canonical primitive vector with coefficients bounded by three,
giving 256 ordered pairs:

| class | bounded witnesses |
|---|---:|
| dependent/same-cycle `p=0` | 16 |
| determinant-one `S3` | 58 |
| lens `p>1` | 182 |

These counts are arithmetic controls, not frequencies and not an exhaustion of the infinite cap
family. The exact general rule remains `p=|det(v_-,v_+)|`.

Eight explicit `GL(2,Z)` controls cover identity, finite elliptic, parabolic, hyperbolic, and
orientation-reversing mapping-torus classes. The parametric family is not reduced to those eight
witnesses. Their corrected class census is three finite elliptic witnesses (including the exact
order-two element `-I`), one nontrivial parabolic witness, one identity, one hyperbolic witness, and
two orientation-reversing witnesses.

Every one of seven motif/transition/control classes is crossed with every completion family in the
84-row `MOTIF_COMPLETION_ATLAS.tsv`. A cross-row records compatibility requirements; it is not an
assertion that the local analytic polynomial already supplies a complete global metric witness.

## Stage 4 — bundle and holonomy data

The atlas keeps four objects separate:

1. Kato transport of metric-derived projector bundles;
2. Levi-Civita tangent holonomy of a complete metric;
3. integral torus-lattice monodromy and cap-cycle data; and
4. principal-circle characteristic data after a free circle action is supplied.

The local analytic paths provide object 1. They do not close into loops and therefore do not supply
holonomy. The completion registry supplies parametric data for object 3. Object 2 remains
profile-dependent until a complete metric is supplied. Object 4 exists only in the conditional
reciprocal-toric control after periods, action, caps, orientation, and normalization are disclosed.

In that control, the depth-path coordinate projectors are covariantly constant, so their Kato
generator is zero. The metric-dual principal connection still has the separate normalized fraction

```text
f(phi)=1/(1+exp(4 phi)),
Q_finite=f(phi_minus)-f(phi_plus).
```

Common angular scale cancels, but finite endpoints remain boundary-dependent. Unit class remains
conditional on the full global premises.

## Stage 5 — registered UDT selector audit

The 84-row selector matrix applies seven exact selector/status axes to all 12 completion families.

- Reciprocity constrains reciprocal ratios and transition parity. It does not supply a cover,
  periods, cap vectors, orientation, or a circle action.
- CSN removes positive common scale from normalized pre-material structure. It does not select a
  topology; its cancellation from the toric connection is compatibility, not selection.
- The finite-cell canon removes spatial infinity and supplies a physical mirrored-cell setting. It
  does not choose retained boundary versus cap, cap cycles, or a complete seal lift.
- The static seal statement constrains `phi`, while several complete coframe/angular lifts survive.
- Current bootstrap is on-shell admissibility. It has no off-shell functional that ranks the atlas
  branches.
- Current scale/matter evidence supplies no native carrier, mass, source, normalized boundary
  charge, or action coefficient that could close the selection loop.
- Density cannot be a native selector while its mass numerator is undefined.

Multiple current-compatible or conditional branches therefore remain. `S3` and the free Hopf
action remain unique only inside their previously supplied toric eigencap premises.

## Density/bootstrap chicken-and-egg audit

The density issue has a type-correct possible resolution, but not yet an equation.

The desired noncircular closure would solve the complete geometry, native matter fields, physical
scale, boundary data, and bootstrap simultaneously, then define

```text
rho_solution = M_native[g,fields] / V_proper[g]
```

from that same solution. Requiring the resulting density to reproduce the branch that generated it
could be a genuine fixed-point or eigenvalue condition. Density would be an output fed back in a
simultaneous solve, not an observed number inserted at the start.

The assembly atlas can supply branch-dependent candidate volume and boundary objects. It supplies no
native mass functional. Current compactness relations also remain rank one: writing density as
`M/V` does not create an independent scale equation when `V` scales as `X_max^3`.

Accordingly the simultaneous density/bootstrap route is a `POTENTIAL_FUTURE_SELECTOR`, while its
native mass, varied closure, response map, and independent scale breaking remain `OPEN`.

## Stages 6 and 7

The preregistered gate for Stage 6 requires one selected quotient together with its distribution,
gluing/periodicity, action, orientation status, and boundary completion. That gate fails because no
quotient is selected. No configuration space or metric-induced reduced action was invented.

Stage 7 additionally requires a native nonlinear evolution law, constraints, boundary flux, and raw
residual. Those objects are absent. No relaxation trajectory was relabeled as time, no CPU
time-evolution solve was run, and GPU work was not launched.

## Verification and fresh-review status

The internal independent verifier:

- reproduces all 95,232 path identities and 83 deterministic anchors;
- independently reconstructs the exact 1,536-row candidate set and its `M8` provenance;
- reruns three nontrivial transport anchors with a different integrator;
- checks all cap determinants and all monodromy witnesses;
- verifies all 84 motif/completion and all 84 selector rows;
- exercises 20 corruption catches, including the exact `-I` class and pinned CSN source; and
- reproduces both fail-closed stage gates.

The first verifier output had a report-only motif-label reuse bug. Its result and transcript are
preserved. The correction was separately preregistered and the full verifier rerun successfully.

The preserved fresh zero-context review returned `PASS-WITH-CAVEATS`. It independently reproduced
the load-bearing counts and algebra and found two bounded defects: `-I` was grouped with the
parabolic witnesses, and the CSN matrix cited an unpinned dispatch instead of the already-frozen
angular-toric audit. Correction scope was separately preregistered at commit `cab6ec6`. The package
now classifies `-I` as finite elliptic, pins all CSN rows to the frozen source, and exercises explicit
mutation catches for both failures. Internal deterministic regeneration and verifier replay pass.
Fresh independent review of the applied correction remains pending at this report revision.

## Four banking gates

1. Preregistered: **YES**, commit `8bf1906`; verifier-label correction preregistered at `4700c68`;
   fresh-review corrections preregistered at `cab6ec6`.
2. Full space or bounded scope justified: **YES FOR THE REGISTERED TAXONOMY**, not arbitrary global
   four-geometries, actions, or EOM solution space.
3. Independently verified on the load-bearing premise: **YES IN PACKAGE**; the fresh reviewer
   reproduced the principal claims, with independent correction replay still pending.
4. Every premise audited: **YES FOR THE DECLARED ATLAS**, including the local/global, transport/
   holonomy, phi-solo/orchestra, density-input/output, and Stage-6/7 boundaries.

Current bankable grade: `VERIFIED-WITH-CAVEATS PENDING FRESH CORRECTION REVIEW`.
