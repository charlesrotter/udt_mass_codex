# Exact derivation — global relation-family structures on complete branches

Date: 2026-08-10

## 1. Type of the result

This audit classifies structures already owned by the frozen branch evidence. It does not select a
physical universe branch.

A branch may own any of three relevant geometric objects:

1. a single shared calibration state over the branch, producing an endpoint coboundary;
2. composable path-labelled arrows, with a possibly nonidentity loop return; or
3. a stratified or set-valued family whose type changes on an explicit wall.

These are weaker than ownership of the physical non-isometric calibrated observer-pair arrow. The
latter must additionally provide the enriched query objects, the middle-state transition, and the
reciprocal scalar reduction required by G35--G40.

## 2. Common endpoint calibration

On the W02 static generic-lapse control, the metric owns one global nonvanishing timelike Killing
line. If its norm is `N`, then the banked conditional clock depth is

```text
delta_K(p,q) = log(N(p)/N(q)).
```

For any three points in the same regular branch,

```text
delta_K(p,q) + delta_K(q,r) = delta_K(p,r).
```

The shared Killing field supplies the middle clock-calibration state, so this is a genuine global
endpoint relation on the clock line. It is classified
`COMMON_CALIBRATED_ATLAS_OWNED` at that limited scope. It does not own the ruler line, pair surface,
or the condition `T L=1` needed to identify this clock relation with the complete terminal pair
readout.

## 3. Path-labelled geometric family

On W01 and the general-screen S3 family, the supplied smooth complete coframe and metric own their
Levi-Civita path transports. For composable paths,

```text
P_(gamma_2 o gamma_1) = P_gamma_2 P_gamma_1.
```

The W01 regular family also owns the intrinsic global clock/ruler projector and its rank-two screen
complement. Its full ambient lift has nontrivial sampled Lorentz holonomy and is not a parallel
endpoint reduction. Nonidentity loop return is therefore valid path geometry, not a failure of
associativity. These branches are classified `PATH_BRANCH_GROUPOID_OWNED`.

The limitation is load-bearing: Levi-Civita transport is isometric. It does not by itself produce
the non-isometric comparison arrow whose terminal reciprocal imbalance could be the physical
mixed-geometry `c_eff` relation. The owned object is the geometric path groupoid, not the completed
physical pair functor.

## 4. Stratified families

Two different bounded stratified structures survive.

- FC04 is an aggregate completion class containing actual S3 members with different outcomes:
  W02 has an endpoint clock relation; W01 and the general-screen family have path-labelled
  transport; other members have zero response, nonuniqueness, or degeneration. The class is a
  `STRATIFIED_MIXTURE_OWNED` catalogue, not one selected relation.
- The toric dual-systole family owns a global unordered shortest-line set. Away from tie walls it
  has a singleton line; at a tie the single line is not owned and the unordered pair survives.
  This is a `STRATIFIED_MIXTURE_OWNED` projector family. No complete calibrated observer arrow or
  scalar depth follows from it.

The slice-null W05 control is not promoted to this class: it identifies a transition stratum but
does not supply a complete arrow family through the stratum.

## 5. Exact three-observer controls

For a genuine common atlas, let

```text
J_AB = [[2,1],[1,1]],
J_BC = [[1,1],[2,3]],
J_AC = J_BC J_AB.
```

Then

```text
Omega_A = J_AC^-1 J_BC J_AB = I.
```

For the same composable path arrows, take the nontrivial Lorentz matrix

```text
H = [[5/3,4/3],[4/3,5/3]]
```

and a direct path arrow `J_AC_path = J_AC H`. The loop return becomes

```text
Omega_A_path = J_AC_path^-1 J_BC J_AB != I.
```

Both products are associative. The difference is common-atlas descent versus path holonomy. An
explicit nonidentity middle transition `M_B` changes the composite from `J_BC J_AB` to
`J_BC M_B J_AB`; it may not be omitted by silently identifying separately built B states.

The exact Fraction implementation is in `classify_relation_families.py`; the independent
reconstruction is in `verify_relation_families_independent.py`.

## 6. What does not survive as owned

- Nine completion entries remain topology, cap, seam, monodromy, or stratification schemas without
  enough typed metric/overlap evidence.
- Four entries are singular, local, absent, or a transition stratum rather than complete relation
  families.
- Five complete controls contain local or global candidate objects but no owner for one complete
  relation family.
- FC12 requires rederivation with the complete phi+orchestra semantics and completed endpoint data.

No evidence row supplies a universal physical calibrated pair relation, a general scalar character
on mixed arrows, or a selected `c_eff` law. The terminal reciprocal evaluator remains downstream of
an owned calibrated pair metric.

## 7. Maximum conclusion

```text
GEOMETRIC_RELATION_FAMILY_STRUCTURES_CLASSIFIED:
PATH_HOLONOMY_FAMILIES_SURVIVE_ON_THE_TWISTED_AND_GENERAL_SCREEN_S3_BRANCHES;
A_GLOBAL_ENDPOINT_CLOCK_CALIBRATION_RELATION_SURVIVES_ON_THE_UNIQUE_KILLING_LINE_CONTROL;
A_GLOBAL_SET_VALUED_STRATIFIED_PROJECTOR_FAMILY_SURVIVES_ON_THE_TORIC_CHAMBER_AND_TIE_STRUCTURE;
NO_COMPLETE_PHYSICAL_OBSERVER_PAIR_RELATION_OR_UNIVERSAL_SCALAR_RECIPROCAL_REDUCTION_IS_SELECTED.
```
