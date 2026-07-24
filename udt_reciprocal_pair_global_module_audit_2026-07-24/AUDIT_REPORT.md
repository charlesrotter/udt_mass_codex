# Reciprocal-pair global-module audit

Date: 2026-07-24

Base: `a93f928f66d260bee1df1a9c5156269afa1952b7`

Preregistration: `1758199`

Mode: preregistered CPU-only exact algebra, transition-group census, and
completion classification

## Result first

The reciprocal pair is real geometry, but it is not a newly derived smaller
carrier.

At a generic two-way shortest wall, the two primitive character lines are
unimodular. Their integral span is therefore exactly the complete rank-two
torus character module:

```text
Z w1 + Z w2 = Lambda*.
```

That full module descends under arbitrary `GL(2,Z)` torus cocycles wherever
an integral torus exists. The special **co-shortest pair** does not:

- it exists as a two-element minimum only on a wall;
- it is no longer a pair of minima in either adjacent chamber;
- it is nonunique at a three-way vertex; and
- a global unordered splitting requires an everywhere two-way-wall branch
  plus monodromy in the order-eight signed-permutation subgroup.

The exact scoped ruling is:

```text
FULL_TORIC_CHARACTER_MODULE_DERIVED
TWO_WAY_SHORTEST_PAIR_IS_A_WALL_LOCAL_UNIMODULAR_BASIS_NOT_A_SMALLER_MODULE
GLOBAL_UNORDERED_SHORTEST_SPLITTING_REQUIRES_AN_EVERYWHERE_TWO_WAY_WALL
AND_SIGNED_PERMUTATION_MONODROMY
INVOLUTIVE_EXCHANGE_FIXED_CIRCLE_AND_ABS_C1_ONE_REMAIN_CONDITIONAL
ON_AN_UNSELECTED_GLOBAL_LIFT_AND_FC04_COMPLETION
CARRIER_ACTION_SOURCE_MASS_REMAIN_OPEN
```

Grade: `VERIFIED-WITH-CAVEATS`. Exact production and independent
standard-library implementations agree. No fresh external model review was
authorized.

## New exact structure

The unordered pair has an exact order-eight stabilizer: the signed
permutation matrices. This makes pair-associated Gram, quadratic, connection,
and curvature doublets available on a pair-reduced branch.

The four integral lifts that exchange the two unoriented lines separate into:

- two involutions, `J` and `-J`, each with a primitive fixed circle; and
- two order-four lifts, each with no nonzero fixed lattice.

The pair itself sees all four only as “exchange.” It therefore does not
select a fixed circle.

If an involutive exchange is separately supplied, its fixed and anti-fixed
primitive lattices have index two in the full character lattice. This is a
new exact integral `Z2` residue, not a physical particle parity claim.

## Sharpened conditional Hopf relation

The already conditional toric Hopf chain becomes cleaner:

1. normalized reciprocal weights give two positive amplitudes with ratio
   `exp(2phi)`;
2. two supplied periodic phases make the known unit `S3` spinor coordinate;
3. a supplied global involutive exchange has a primitive fixed circle;
4. in supplied `FC04`, that circle acts freely; and
5. the quotient is a smooth `S2` bundle with `abs(c1)=1`.

No individual shortest character is needed for that conditional chain.
However, the global involutive angular lift, phases, periods, full range,
opposing primitive caps, orientation, and completion are still unselected.
`J` and `-J` are sign-basis conjugate and give opposite oriented classes, so
the honest invariant remains the previously established conditional
absolute unit class.

A quotient `S2` is still not a selected physical `S2`-valued field. The
carrier-section type gap remains.

## Meaning for mass emergence

The prior “orchestra” intuition survives, but with a correction. At the tie,
the metric is not constructing a new two-component matter carrier. It is
showing the complete two-dimensional angular character system without
preferring one instrument.

That full system contains a mathematically clean route to the Hopf bundle
once a global involutive exchange and the correct cap completion exist. The
metric has not selected those global data, and the bundle does not supply a
section or action.

Therefore this audit does not close mass and does not justify a density
scan. It does remove the need to search for a single-character tie-break as
a prerequisite for the conditional Hopf topology.

## Completion census

All twelve registered completion families are classified exactly once in
`COMPLETION_MODULE_ATLAS.tsv`.

- Full `GL(2,Z)` character local systems survive on toric interiors.
- Boundary framing, cap isotropy, quotient congruence, monodromy,
  orientation, rank, and Frobenius conditions remain explicit.
- Only the supplied `FC04` plus a global involutive exchange supports the
  free-fixed-circle `abs(c1)=1` chain.
- No completion is promoted or selected.

## Verification

- 44/44 frozen source identities reproduced;
- 36/36 exact production controls passed;
- 30/30 local objects classified;
- 16/16 transition classes classified;
- 18/18 associated invariants classified;
- 12/12 completions classified;
- 14/14 conditional Hopf steps typed;
- independent stdlib/Fraction implementation imported neither SymPy nor the
  production module;
- 26/26 registered failure mutations were rejected;
- zero carrier, action, density, mass, GPU, canon, or reorganization
  promotions.

Repository gates are recorded separately.

## Four evidence gates

1. **Preregistered:** yes, commit `1758199` before production outcomes.
2. **Full or bounded:** complete for the frozen 30 objects, 16 transitions,
   12 completions, and 14 conditional Hopf steps; future nonlocal laws and
   complete field equations are outside scope.
3. **Independent:** yes, by a separate stdlib/Fraction implementation and
   exercised mutation catches; no fresh external model.
4. **Premises:** all 26 registered premises are audited.

No canonization follows.
