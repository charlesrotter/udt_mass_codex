# Global founded-depth ownership/overlap audit

Date: 2026-08-05

Status: **VERIFIED_WITH_CAVEATS_BOUNDED_GLOBAL_FACTORIZATION_GROUPOID_AND_OWNERSHIP_NONSELECTION**

## Result first

Global stitching does not remove the local founded-depth factorization ambiguity on the supplied
smooth fixed-rank whole-coframe tile. It makes that ambiguity precise.

Independent local shifts of the factorized depth can be absorbed by the local reference coframes.
The reference overlap maps then change by an exact coboundary, while all physical complete coframes,
physical overlap maps, and triple-overlap cocycles remain unchanged. The result is a global groupoid
of equivalent factorized presentations, not one selected physical `phi` assignment.

Several real global structures survive this freedom: reversal parity, oriented affine periods, and
physical finite-cell endpoint/joint constraints. They classify or restrict global geometry but do
not choose local depth representatives.

## What can reduce the freedom

Three routes reduce it only after additional ownership data are supplied:

1. fixed reference transitions restrict shifts to their stabilizer;
2. independently physical pair-depth data fix relative endpoint values, leaving one common constant
   on a connected observer graph; and
3. a regular branch-derived selector can own depth on its stratum.

The current source record does not derive the fixed reference system or physical depth assignment,
and branch selectors are conditional and nonuniversal across defect/collision strata. These are
therefore conditional reductions, not a founded global assignment.

## Complete route census

All 12 preregistered routes are classified in `ROUTE_CLASSIFICATION.tsv`. None was removed for
failing to resemble the desired universe.

```text
O01 local factorization             derived presentation freedom
O02 fixed reference transitions     conditional stabilizer reduction
O03 two-sided cocycle               derived nonselection
O04 global scalar descent           arbitrary global-function freedom remains
O05 affine/reversal descent         class data, not a section
O06 query equivariance              transports every supplied depth
O07 fixed pair depths               conditional reduction modulo a constant
O08 endpoint composition            identically accepts every endpoint potential
O09 paths and periods               periods invariant but not selected
O10 finite-cell seam                physical glue does not fix factorization
O11 branch-derived section          conditional local ownership only
O12 trivial full-loop return        not founded; period restriction only
```

## Exact evidence

- Production SymPy calculation: 54/54 exact checks.
- Independent standard-library `Fraction` reconstruction: 46/46 exact checks, using a different
  three-chart witness and importing neither SymPy nor production code.
- Three unequal local shifts preserve all three complete coframes, all physical transitions, and
  the transformed reference cocycle.
- Connected three-chart scalar descent has rank two/nullity one per base point; two different base
  samples prove arbitrary global-function freedom remains.
- Both oriented and reversal-twisted affine cocycles survive arbitrary local shifts.
- Four-observer incidence and triangle ranks are `3/3`, with exact `C B=0`; fixed pair depths leave
  a one-dimensional constant kernel.
- Nonzero path-period and query-reset controls prevent vacuous composition/basicness conclusions.
- Oriented and reversal fixed-seam stabilizers are separated from presentation-varying seams.
- The fresh adversary found the initial variable-seam assertion was tautological. It was replaced
  by independent endpoint coframe/reference constructions: unequal endpoint shifts change the
  saved reference seam, preserve the physical seam relation, and leave both endpoint complete
  coframes unchanged. The verifier now rejects a witness whose before/after seams are made equal.
- A fresh focused read-only replay accepted that repair (`REPAIR_ACCEPTED`) after independently
  reproducing the 54/54 production, 46/46 independent, and 32/32 verifier results.
- Final verifier: 33/33 checks including 16/16 exercised mutation catches. The additional
  post-review check separates the fixed source universe from authorized current-navigation drift.
- The fixed source manifest is replayed from preregistration commit `2ddefb71065c692ffc396b09e01cef6594e664b7`;
  current drift is restricted exactly to the three source files that must route the banked result:
  `LIVE.md`, `HANDOFF.md`, and `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md`.
- Frozen universe: 12 routes, 16 premises, 23 source paths, and all 83 unrelated untracked metadata
  identities unchanged at the current check.
- Repository preservation replay: 1,114 current paths, 101 frontier targets, six frozen manifests
  covering 133 package paths, 161 checked Markdown links, and tests at 70 passed/1 xfailed.

## Interpretation boundary

This does not say `phi` is arbitrary in UDT. The abstract reciprocal depth and its character remain
derived from the founding comparison. The result says that the **complete coframe plus its ordinary
overlap consistency does not yet tell us which factorized representative is the physical depth
assignment**.

Nor does it prove that no future metric consequence can own the assignment. It says the present
overlap, query-composition, and supplied finite-cell relations do not.

## Rabbit-hole decision

The overlap/cocycle route is exhausted at this level. More local jets, curvature ranks, or longer
algebra would repeat the same presentation identity. The next justified work is conceptual and
source-level: determine whether the founding observer comparison already defines an equivariant
ownership map on query/path data, or whether a realized/branch-stratified reduction is an additional
physical premise.

No third-jet calculation, action ansatz, density bracket, time-live solve, or GPU work follows from
this audit.

## Maximum conclusion

```text
DERIVED_GLOBAL_FACTORIZATION_GROUPOID_FREEDOM_ON_THE_SUPPLIED_SMOOTH_COVER__
DERIVED_COCYCLE_CLASS_AND_PERIOD_INVARIANTS_DO_NOT_SELECT_A_SECTION__
CONDITIONAL_REDUCTIONS_REQUIRE_UNOWNED_REFERENCE_DEPTH_OR_BRANCH_SECTION_DATA__
NO_GLOBAL_PHI_OWNERSHIP_SELECTION
```

No physical `phi` field, action, source, carrier, boundary functional, bootstrap equation, density,
`X_max`, matter, mass, dynamics, signalling law, observation fit, or canon statement is derived.
