# UDT Complete Temporal-Soldering Atlas

Date: 2026-07-22

Status: `CORRECTED_VERIFIED_WITH_REGISTERED_SCOPE`

Maximum conclusion:

`BOUNDED_REGISTERED_TEMPORAL-SOLDERING_ATLAS_CHARACTERIZED__PHI-GRADIENT_BRANCH_BIFURCATION_DERIVED_LOCALLY__GLOBAL_PHYSICAL_THREADING_OPEN`

## Result first

The complete retained metric atlas does **not** supply one preferred clock direction everywhere. It
contains a structured temporal spectrum across all 95,232 instrument-family path presentations:

| local temporal class | path presentations | analytic identities represented |
|---|---:|---:|
| no proper intrinsic temporal subspace | 82,140 | 3,072 |
| Lorentzian two-plane only | 7,845 | 2,525 |
| spacelike line plus Lorentzian three-space | 2,160 | 1,152 |
| unique unoriented timelike line | 1,775 | 772 |
| transition or numerical uncertainty | 1,312 | 429 |

These are overlapping instrument presentations of 3,072 analytic metric identities, not 95,232
universes or mechanisms.

The 1,775 persistent timelike-line paths split sharply:

- all 720 `LINE_PLUS_THREE` paths have an integrable positive three-space at all 17 sampled nodes;
- all 1,055 `FOUR_LINES` paths contain robust nonintegrability in the timelike line's orthogonal
  three-space. There are 17,925 nonintegrable four-line nodes and ten derivative-margin nodes; every
  four-line path has other robustly nonintegrable nodes.

The `1+3` result has an exact explanation. Every one of its families contains the native scalar
gradient dyad

```text
s = g^{-1}(dphi,dphi),
D = grad(phi) tensor dphi,
D^2 = s D,
P_phi = D/s.
```

When `s<0`, `P_phi` is the unique timelike-line projector and `Q_phi=I-P_phi` is the positive
projector onto `ker(dphi)`. Because `d(dphi)=0`, `ker(dphi)` is locally integrable exactly. All 720
timelike-phi paths, 384 analytic identities, and 12,240 nodes reproduce this join; the worst direct
projector residual is `1.2760030334365347e-11`.

This gives a conditional local phi-clock construction. On any open region where `dphi` remains
timelike and nonzero, `phi=constant` supplies spatial leaves and `grad(phi)` supplies a mathematical
orientation. In the adapted choice `tau=phi`, the normal-flow lapse magnitude is

```text
N_phi = 1/sqrt(-s).
```

The shift is zero only in that chosen normal-flow chart. Physical future, clock scale under
reparameterization, interval-wide sign, and global gluing remain open.

The companion branch is equally clean and probably more relevant to the established static-depth
interpretation. All 2,160 `RANK_ONE_LINE_SPACELIKE__LORENTZ_COMPLEMENT` paths contain `D`; all 36,720
sampled nodes have `s>0`, and `P_phi=D/s` is exactly the spacelike depth line. Its level sets are
integrable but Lorentzian (`N1_P2_Z0`). Thus phi supplies depth without selecting time inside the
three-dimensional leaf. The smallest missing local object on that branch is a native rank-one
timelike projector (or equivalent line section) inside `ker(dphi)`.

The atlas therefore exposes a metric-native bifurcation rather than a universal time postulate:

```text
s < 0: phi is a local mathematical clock; phi-level leaves are spatial.
s > 0: phi is a local depth coordinate; phi-level leaves are Lorentzian and intra-leaf time is open.
```

Neither sign branch is selected as the physical universe by this audit.

## Four-line branch

The four-line motif is not a defective `1+3` foliation. Its native instruments distinguish four
one-dimensional axes, including one timelike line, while the perpendicular three-space is
nonintegrable on every retained path. It can therefore support a local clock congruence without an
ordinary stack of orthogonal spatial instants. Interpreting that twist as shift, rotation, transport,
or physics would require additional work; the atlas records only the geometric obstruction.

## Chart and coframe invariance

For a registered coordinate map with Jacobian `J`,

```text
g' = J^T g J,
P' = J^{-1} P J.
```

The projector image transforms covariantly and the metric restriction is congruent, so block rank
and signature are invariant. Internal Lorentz-coframe transformations leave the coordinate metric
and projector image unchanged. This exact rule covers all 1,142,784 registered
path-transformation presentations. An independent implementation tested four stable temporal-class
anchors under all twelve registered transformations (48 comparisons); the worst projector
identity/self-adjointness residual was `1.9226844506944154e-14`.

The finite transformation registry is not an exhaustive proof over all charts or coframes.

## What is and is not reconstructed

The conditional Lorentzian representative supplies a local null cone. A unique negative projector
supplies a unit timelike line up to sign. The phi-gradient branch supplies more locally because the
underlying scalar retains the vector `grad(phi)`, not merely its unoriented projector.

It still does not automatically supply a physical UDT observer or a global connector:

- seventeen samples do not certify the sign of `s` on every point of an interval;
- no current projector-line transition cocycle glues the local lines through caps, mirrors, or
  quotient seams;
- the current seal-lift ledger says all four lifts fix an already conditional base line, but it
  selects no lift and no physical future;
- Levi-Civita holonomy remains profile-dependent for all twelve completion families and is not fixed
  by any of the eight lattice-monodromy controls;
- lapse and shift outside the adapted local phi-clock construction require a selected time function,
  slicing, and thread congruence.

Accordingly, zero global line bundles, global time orientations, and complete optical connectors are
derived here.

## Selector audit

- The complete metric plus registered native instruments distinguishes a local line on a bounded
  subset; it does not select that subset as physical.
- Reciprocity constrains ratios and transition parity, not a negative projector image or future
  sign.
- Common-Scale Neutrality preserves projector images and signatures under positive common scale.
- The finite cell constrains the domain but does not choose boundary, cap, quotient, or line gluing.
- The static seal constrains an already supplied line conditionally; its lift remains unselected.
- The current bootstrap is on-shell admissibility and has no off-shell functional that ranks the
  temporal branches.

For the likely spatial-depth branch, the smallest genuinely missing selector is therefore not an
action and not a new mechanism: it is a metric-native rule selecting a timelike line inside the
Lorentzian phi leaf, together with compatible global transition data. Whether other full-metric
instrument ensembles already provide that rule remains the next metric-led question.

## Corrections and independent verification

The original production atlas is preserved. Its first two stencil levels contained two
cross-implementation threshold disagreements: one route called a node integrable while the other
called it uncertain, in opposite directions for two rows. A separately committed correction froze
those exact rows before `h/4` and `h/8` were inspected. Both production and independent routes then
placed the last two values below `1e-7`, resolving both as integrable. The consolidated layer records
the refinement without rewriting the original table.

The independent verifier:

- reclassified all 95,232 paths and 1,618,944 source nodes;
- recomputed all 30,175 complement nodes through a frozen nonproduction motif algebra and separate
  analytic Jet reconstruction;
- reproduced exactly the two preregistered threshold conflicts and no others;
- passed 20 exercised corruption catches;
- kept raw-value agreement separate from exact signature/class agreement;
- reported maximum auxiliary numeric difference `2.703188856880014e-7` within the preregistered
  `1e-6` cross-implementation value tolerance.

The failed verification attempts and their preregistered corrections are preserved. They concern
an over-tight auxiliary value comparison, the genuine two-node threshold refinement, and an
overbroad holonomy-ledger assertion. None changed the candidate universe or imported a physical
mechanism. After a fresh adversarial review, both twenty-case catch suites were corrected to perform
explicit in-memory evidence mutations and require rejection through their fail-closed validators;
the original tautological catch implementation is retained in git history, not as current evidence.

## Scope and lane guards

- The analytic paths are metric configurations, not action/EOM solutions or physical evolution.
- The timelike-phi branch is not declared physical merely because it supplies a clock.
- The spacelike-phi branch is not declared physical merely because it resembles the static UDT depth
  interpretation.
- No action, carrier, source, boundary polarization, information law, SNe data, or fit was loaded.
- CPU only; GPU runs: zero.
- Existing SNe results are unchanged and were not recalibrated.

## Four banking gates

1. Preregistered: **YES**, including committed scope and correction preregistrations.
2. Full space or bounded scope justified: **YES** for every retained path, node, registered
   transformation presentation, and frozen threshold conflict; not exhaustive beyond the registry
   or between sampled path nodes.
3. Independently verified: **YES** for all load-bearing path, signature, projector, Frobenius, and
   phi-gradient joins through a separate analytic implementation.
4. Every premise audited: **YES** in `PREMISE_STATUS_LEDGER.tsv`; physical branch, future, scale,
   global gluing, action, and matter remain explicitly open.

This is a corrected verified-with-scope structural atlas, not canonization.
