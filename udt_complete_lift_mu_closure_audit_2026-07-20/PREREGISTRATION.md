# UDT complete-lift and global-cocycle `mu` closure audit — preregistration

Date: 2026-07-20

Base: `d5e4eac1a2c6e558442338c6d98732ef3e30cd98`

Branch: `codex/udt-complete-lift-mu-closure-audit-2026-07-20`

Mode: CPU-only exact full-coframe involution, cross-block, orientation, and cocycle audit

## Whole question

The preceding audit derived a conditional clock/radial soldering at the finite-cell seal and showed
that local nonzero angular coupling, CSN, unit-volume normalization, Cartan identities, and current
bootstrap do not fix the invariant magnitude

```text
mu=B^2/(A^2 b^2)>1.
```

It left one smaller possibility:

> Does any already-registered complete reciprocal/angular/normal/time-on lift, together with its
> orientation, overlap, corner, or finite-cell cocycle requirements, impose a metric-dependent
> global closure equation that fixes or rejects `mu`?

This audit must compare existing lift families. It may not invent a topology, period, boundary
functional, action, or new global mechanism.

## Objects that must remain distinct

1. the mixed base metric and its invariant `mu`;
2. the base depth-reversal involution;
3. the angular coframe involution;
4. a complete block involution;
5. metric isometry equations;
6. coframe fixed/anti-fixed multiplicities;
7. orientation of the complete coframe map;
8. overlap/corner group words;
9. metric-dependent Levi-Civita holonomy;
10. an abstract cocycle condition;
11. a chosen global cap, period, lattice, or topology; and
12. a bootstrap or dynamical closure equation.

An algebraic group word cannot be promoted to a metric-dependent selector if it contains no metric
invariant.

## Frozen candidate lift universe

The audit will test, without promoting any member:

1. angular identity `A=+I`;
2. angular minus identity `A=-I`;
3. the full angular axis-reflection conjugacy class;
4. the separately premised conditional Hopf-circle exchange, only to the extent its local linear
   involution is already recorded;
5. the direct transverse-identity reciprocal extension; and
6. every parity-compatible constant real base-angular cross block for the first three algebraic
   classes.

Normal and time-on lifts remain source-audited. If their executable maps are absent, that absence is
a result, not permission to invent them.

## Premise treatment

| Object | Treatment |
|---|---|
| Mixed base readout and pair invariant | `DERIVED_CONDITIONAL` |
| Seal-local base soldering and sign branch | `DERIVED_CONDITIONAL` |
| Angular `+I`, `-I`, and reflection lifts | complete registered algebraic candidate set in the stated isotropic real class |
| Conditional Hopf exchange | `CONDITIONAL_WITNESS`; topology/periods remain unselected |
| Positive CSN | `pinned-by-THEORY` |
| Orientation requirement | `free-and-explored`; must be sourced before use as selector |
| Corner commutation/finite order | `free-and-explored`; no angle or period may be inserted |
| Current global cocycle | exact registered algebra to be audited |
| Metric-dependent holonomy | `DERIVED_PER_REPRESENTATIVE`; not identified with abstract transition words |
| Bootstrap | retain exact current on-shell/admissibility status |
| Action, topology, boundary charge, carrier, mass, scale | excluded |

## Exact tests

### A. Complete algebraic lift and cross-block census

For

```text
G=[[H,C],[C^T,Q]],       R=diag(F,A),
```

derive the complete linear equations

```text
F^T H F=H,
F^T C A=C,
A^T Q A=Q
```

for `A=+I`, `A=-I`, and a representative axis reflection. Count free parameters and retain
nonzero cross-block witnesses.

### B. `mu` countermodels across every lift

For every algebraic lift, attempt exact Lorentzian witnesses with `mu=4` and `mu=9` sharing the
same angular metric, angular involution, cross-block pattern, orientation class, and calibration
convention. Distinct full pair invariants must be recorded where defined.

### C. Orientation and multiplicity

Compute complete determinant and fixed/anti-fixed dimensions. Determine whether any current
orientation statement uniquely selects a lift and whether selecting an orientation class fixes
`mu`.

### D. Overlap and corner cocycle

Derive products of preserving and inverting reciprocal transitions together with angular lift
products. Test commuting and noncommuting reflection corners, finite-order conditions, and closed
loop parity. Record exactly which equations contain `mu`.

### E. Normalized operational transition

Conjugate each seal map to the conditionally normalized operational frame where possible. Determine
whether the resulting transition/corner word retains `mu` or whether `mu` survives only in the
reciprocal generator/metric pair.

### F. Global-authority and tensor-type audit

Read the exact current finite-cell, coframe-cocycle, angular, Cartan, and bootstrap sources. A
selection claim requires an existing metric-dependent global equation involving the pair invariant,
not merely a missing cap/period placeholder.

## Frozen outcome classes

1. `ONE_COMPLETE_LIFT_SELECTED_BY_CURRENT_FOUNDATION`
2. `ORIENTATION_SELECTS_ONE_COMPLETE_LIFT`
3. `ORIENTATION_CLASS_LEAVES_MU_OPEN`
4. `CORNER_COCYCLE_SELECTS_MU`
5. `CORNER_COCYCLE_IS_MU_BLIND`
6. `ALL_REGISTERED_ALGEBRAIC_LIFTS_LEAVE_MU_OPEN`
7. `NONZERO_CROSS_BLOCKS_LEAVE_MU_OPEN_IN_EVERY_LIFT`
8. `NORMALIZED_SEAL_TRANSITIONS_SELECT_MU`
9. `NORMALIZED_SEAL_TRANSITIONS_ARE_MU_BLIND`
10. `CONDITIONAL_HOPF_LIFT_SELECTS_MU`
11. `CONDITIONAL_HOPF_LIFT_HAS_NO_CURRENT_MU_EQUATION`
12. `METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_PRESENT`
13. `METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_ABSENT`
14. `GLOBAL_COMPLETION_REMAINS_OPEN`
15. `AUDIT_INCONCLUSIVE`

Multiple scoped outcomes may apply.

## Falsification and certification contract

- Algebraic lift underdetermination requires exact `mu=4` and `mu=9` witnesses for every retained
  lift class, including nonzero cross blocks where parity allows.
- A corner or cocycle selector must contain the metric invariant after all legitimate basis changes;
  a group word involving only transition matrices cannot fix `mu` by assertion.
- Orientation may select a determinant class but cannot select `mu` unless its equations distinguish
  two witnesses within that same class.
- The Hopf lift may select `mu` only through an already-authorized metric-dependent equation; its
  name or topology cannot be used as the equation.
- Absence is restricted to current registered structures. A future derived cap, period, boundary
  functional, or bootstrap map could add a metric-dependent condition.

## Authority boundary

No topology/period/cap choice, action or field equation, boundary functional or charge, imported
holonomy-matter identification, observer mechanics, physical representative, `X_max`, carrier,
source, mass, GPU work, startup-control edit, `CANON.md` edit, repository reorganization, or
canonization is authorized.

Maximum conclusion:

`UDT_COMPLETE_LIFT_AND_GLOBAL_MU_CLOSURE_STATUS_CHARACTERIZED`.
