# P03G global kinematic assembly atlas

Date: 2026-07-21

Base: `c89708eec3e415e4f0a052d93c02ab4ad1088512`

## Result first

The point-local UDT metric atlas does **not** yet define a global finite-cell configuration space.
The present foundations constrain the way local reciprocal data may be stitched, but they do not
supply the stitch pattern, complete coframe lift, boundary tangent space, topology, or physical
representative.

The exact bounded result is:

```text
CURRENT_GLOBAL_KINEMATIC_ASSEMBLY_CONDITIONS_AND_OPEN_BRANCHES_CHARACTERIZED
```

More specifically:

- all 12 preregistered assembly axes are represented;
- all seven local realization branches `C01`--`C07` remain in the atlas;
- zero local branches have global existence established;
- zero local branches have been globally excluded;
- zero global branches or topologies are selected;
- the exact two-channel reciprocal transition group is `Z2`-graded;
- an identity cocycle cannot have odd reversal parity, and three inverting maps cannot close a
  triple overlap;
- even reversal parity is necessary, not sufficient: the actual cover, transition assignment,
  continuous data, and global class remain open;
- the scalar static seal rule does not select a complete four-dimensional lift or boundary
  polarization; and
- P04 dynamics was neither selected nor launched.

This is a real narrowing of admissible **stitching data**, not a narrowing of the 89 point-local P02
metric strata.

## What the metric data already do globally

For the audited constant real two-channel class, define

```text
G_a = diag(a,1/a),
F_b = [[0,b],[1/b,0]].
```

Exact multiplication gives

```text
G_a G_d = G_ad,
F_b F_c = G_(b/c),
G_a F_b = F_(ab),
F_b G_a = F_(b/a).
```

The `G` component preserves reciprocal-depth orientation; the `F` component reverses it. Hence an
identity-valued closed product has even `F` parity. In particular,

```text
F_b F_c F_d = F_(bd/c) != I,
F_b F_c G_(c/b) = I.
```

That is an exact global-compatibility condition. It says how proposed overlap maps must multiply.
It does not say which charts exist, which overlaps carry `F` rather than `G`, or which global
cocycle class the finite cell realizes.

## The complete assembly type signature at this tier

The global object requires simultaneous data in 12 distinct axes:

1. one of the seven registered local field realizations;
2. a cover, nerve, overlaps, corners, and boundary incidence;
3. reciprocal transition components and their continuous moduli;
4. a closed-path cocycle and global reversal class;
5. CSN overlap factors and the question of a global representative;
6. a global patching law for signed `phi`;
7. complete four-dimensional coframe soldering and angular lift;
8. the seal involution and boundary tangent/polarization;
9. topology, caps, periods, quotient, or no-cap data;
10. regular, degenerate, type-changing, and singular completion branches;
11. Levi-Civita versus independent connection/torsion data; and
12. the downstream physical representative, scale, `X_max`, matter, mass, volume, and bootstrap
    outputs.

The first 11 are not interchangeable. For example, knowing the transition group does not create a
cover; knowing the scalar seal does not select the action on angular directions; and knowing that
the domain is finite does not choose its caps or topology. The twelfth axis is not presently
evaluable because the complete matter-bearing global object does not yet exist.

`GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv` records the exact scope and exhaustiveness stamp of every axis.
`UNCOUNTED_GLOBAL_MODULI.tsv` prevents the still-functional or topological degrees of freedom from
being hidden behind a finite table.

## Seal and angular sector

The current static rule remains exactly:

```text
phi = 0 at the seal,
delta phi = 0 for the registered parity-preserving variation,
normal derivative of phi free.
```

It removes one scalar metric-tangent direction, leaving a nine-dimensional symmetric tangent in
the registered readout. It is not a complete involution. The four retained constant local lifts are:

| angular action | coframe fixed/anti-fixed | metric even/odd | status |
|---|---:|---:|---|
| `+I` | `3/1` | `7/3` | conditional, unselected |
| `-I` | `1/3` | `7/3` | conditional, unselected |
| axis reflection | `2/2` | `6/4` | conditional, unselected |
| local Hopf exchange | `2/2` | `6/4` | conditional, unselected |

Axis reflection and local Hopf exchange are locally conjugate. Global periods, an integral basis,
the cover, or quotient data would be needed to distinguish them. None is supplied. Dirichlet and
Neumann/mixed boundary witnesses also remain compatible with the scalar seal wire, so the variation
domain is not selected by kinematics.

The exact odd family `phi(n)=a n` preserves `phi(0)=0` for every `a`; its normal derivative is `a`.
This continues to block the ordinary-wall shortcut.

## Topology and degeneracy

The bounded source evidence contains no-cap/boundary-retained, `p=0`, `p=1`, `p=3`, `p=5`, and
general toric/lens alternatives. It does not classify all global completions. P03G therefore adds an
explicit `OTHER_UNENUMERATED` remainder instead of turning a witness list into an exhaustive space.

Regular local metrics also do not erase the P02 degenerate and signature-changing closures. A
global admissibility rule for degeneracy loci and singular or stratified completion is absent. Those
branches are retained without claiming that a complete solution exists in any of them.

## Countermodel result

Twelve implication-specific countermodels challenge the common shortcuts. The load-bearing pairs
are:

- the same local transition algebra with different or unspecified covers;
- an exact `F,F,G` triple product before a global bundle is supplied;
- conditional mirror readouts with both `mu=4` and `mu=9`;
- four inequivalent complete lifts preserving the same scalar seal rule;
- at least two boundary polarizations preserving that rule;
- primitive cap witnesses with `p=1`, `p=3`, and `p=5`;
- arbitrary seal slope `a`; and
- all seven local field realizations remaining compatible with the current premise census.

These witnesses do not purport to be complete UDT universes. They establish only that the proposed
consequences do not follow from the named antecedents alone.

## Interpretation

The objective map has reached a clean boundary. Current kinematics provide a grammar for reciprocal
stitching, not a completed global sentence.

This corrects the earlier temptation to treat the next task as choosing a familiar dynamics law.
No action, field equation, GR limit, particle criterion, or desired curvature class participated in
the candidate universe or acceptance logic. Nothing here favors `C^2`, EH, a two-stage bridge, or
any other dynamics lane.

It also shows that there is not presently one demonstrated “last scalar selector.” Several kinds of
global data remain logically independent in the current evidence. They may ultimately be joined by
one elegant metric theorem, but that theorem has not been found merely by listing what it must do.

## Evidence gates

1. **Preregistered:** yes, commit `57f9125`, before the assembly tables and algebra were generated.
2. **Full space or bounded scope:** complete for the 12 preregistered assembly axes, all seven
   registered local realization branches, the constant real two-channel `G/F` algebra, four
   registered constant seal lifts, and the cited topology witnesses; explicitly not exhaustive over
   arbitrary covers, field-dependent `4x4` solderings, topologies, or singular completions.
3. **Independent verification:** a separate standard-library implementation replays exact rational
   group products and tangent combinatorics without importing the generator. **Fresh adversarial
   context remains open:** the read-only Codex attempts returned no final review, and no external
   provider received repository evidence without Charles's explicit authorization.
4. **Premise audit:** every cover, topology, coframe, seal, connection, scale, matter, and dynamics
   choice is stamped; no physical value or familiar law was loaded.

Grade: `LEAD_INDEPENDENT_REPLAY_FRESH_ADVERSARIAL_OPEN`.
