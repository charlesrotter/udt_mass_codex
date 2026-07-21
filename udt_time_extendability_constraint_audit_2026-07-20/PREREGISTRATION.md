# UDT kinematic time-extendability constraint audit — preregistration

Date: 2026-07-20

Base: `cedd7b3992af1d2f52fef06ce3fc5bb941fa50d0`

Branch: `codex/udt-time-extendability-constraint-audit-2026-07-20`

Mode: CPU-only exact differentiated-constraint and connection audit

## Whole question

The frozen complete-lift audit proved that every registered constant real isotropic lift family
admits inequivalent mixed-family invariants

```text
mu=B^2/(A^2 b^2)>1.
```

That result concerns admissible geometric snapshots. This audit asks the smaller next question:

> When a complete UDT coframe, reciprocal generator, and finite-cell seal are allowed to vary along
> an evolution parameter, does preservation of reciprocity, clock/ruler soldering, positive CSN,
> the seal, and the complete metric generate a secondary consistency equation that fixes `mu`, or
> do inequivalent smooth `mu` histories remain kinematically extendable?

The evolution parameter is only a path label until the metric derives its physical clock meaning.
No action, field equation, lapse, shift, GR observer mechanics, or matter evolution may be supplied.

## Objects that must remain distinct

1. an instantaneously admissible metric/coframe snapshot;
2. a smooth path through admissible snapshots;
3. ordinary differentiation in a chosen moving coframe;
4. a connection used to compare neighboring coframes;
5. pointwise reciprocal compatibility;
6. covariant preservation of the metric;
7. covariant preservation of the reciprocal generator;
8. conservation of an invariant along a selected transport;
9. selection of the invariant's numerical value;
10. a dynamical equation from an action; and
11. physical time evolution of a carrier or soliton.

Conservation of `mu` cannot be promoted to selection of its value.

## Frozen bounded universe

The audit will test:

1. the exact two-dimensional mixed base family and its seal involution;
2. all four registered constant real isotropic complete angular lift representatives;
3. their complete parity-compatible cross-block families;
4. exact smooth paths with nonzero angular coupling;
5. fixed-volume/CSN normalization by metric scaling;
6. time-dependent frame conjugations of the complete coframe;
7. the differentiated involution, isometry, reciprocal-inversion, and determinant constraints;
8. metric-compatible and, separately, metric-plus-reciprocity-compatible transport; and
9. the exact current authority for whether such transport is required or selected.

Field-dependent global bundles, arbitrary anisotropic angular metrics, topology, boundary
functionals, actions, and matter histories remain outside the bounded universe.

## Premise ledger

| Object | Treatment |
|---|---|
| Mixed reciprocal readout and `mu` | `DERIVED_CONDITIONAL` |
| Seal-local clock/ruler soldering | `DERIVED_CONDITIONAL` |
| Four complete lift representatives | complete registered set only in the stated isotropic real class |
| Evolution parameter | `free-and-explored`; not physical time by assumption |
| `mu(t)>1` | `free-and-explored` |
| Complete cross-block functions | `free-and-explored` subject to exact parity and Lorentz signature |
| Positive CSN | `pinned-by-THEORY`; exact current tensor meaning to be source-audited |
| Fixed four-volume normalization | `CHOSE` only as a stronger diagnostic convention, not identified with all of CSN |
| Connection | derive the complete compatible family; no familiar connection may be selected by habit |
| Covariant preservation of reciprocity | test separately; require source authority before promotion |
| Seal/asymptotic boundary | retain current exact status; no boundary law may be invented |
| Action, EOM, topology, carrier, source, mass, scale | excluded |

## Exact tests

### A. Differentiate every pointwise constraint

For complete metric `G(s)`, seal `R(s)`, and reciprocal generator `L(s)`, derive and verify the
linearized identities following from

```text
R^2=I,
R^T G R=G,
R L R=-L,
det(G)=constant
```

where each identity is actually authorized. Separate algebraic consequence from any added
parallel-transport condition.

### B. Exact arbitrary-history countermodels

Use at least two inequivalent exact trajectories, including `k_1(s)=2+s/10` and
`k_2(s)=3+s/10` on `0<=s<=1`, so `mu_i(s)=k_i(s)^2>1`. For every registered lift class, construct
smooth Lorentzian full-coframe witnesses with nonzero allowed cross blocks, exact seal isometry,
reciprocal inversion, and fixed-volume normalization. A single endpoint comparison is insufficient.

### C. Moving-frame realization

Apply a nonconstant complete-frame conjugation. Derive its connection contribution and verify that
the moving-frame terms preserve the constraint surface without importing SR/GR observer mechanics.

### D. Compatible-connection census

Solve the linear equations for connections satisfying:

1. metric compatibility alone;
2. metric plus seal compatibility; and
3. metric plus seal plus reciprocal-generator compatibility.

Determine whether each level allows arbitrary `dot(mu)`, forces only `dot(mu)=0`, or fixes a
numerical `mu`.

### E. CSN, boundary, and authority audit

Determine whether current CSN, finite-cell, bootstrap, coframe, Cartan, or boundary evidence
actually selects one of those transport levels or supplies an additional metric-dependent evolution
equation. Missing authority must remain `OPEN`.

## Frozen outcome classes

1. `POINTWISE_TIME_PRESERVATION_SELECTS_MU`
2. `POINTWISE_TIME_PRESERVATION_ALLOWS_INEQUIVALENT_MU_HISTORIES`
3. `METRIC_COMPATIBILITY_SELECTS_MU`
4. `METRIC_SEAL_COMPATIBILITY_SELECTS_MU`
5. `FULL_RECIPROCAL_PARALLELISM_SELECTS_MU`
6. `FULL_RECIPROCAL_PARALLELISM_ONLY_CONSERVES_MU`
7. `CSN_OR_SEAL_SUPPLIES_A_VALUE_EQUATION`
8. `TIME_EXTENDABILITY_EXCLUDES_SOME_FROZEN_LIFTS`
9. `ALL_REGISTERED_FROZEN_LIFTS_HAVE_KINEMATIC_TIME_EXTENSIONS`
10. `PHYSICAL_TRANSPORT_LAW_REMAINS_OPEN`
11. `KINEMATIC_TIME_EXTENDABILITY_REMAINS_UNDERDETERMINED`
12. `AUDIT_INCONCLUSIVE`

Multiple premise-scoped outcomes may apply.

## Falsification and certification contract

- Arbitrary pointwise time-extendability requires exact nonconstant histories in every registered
  lift class, nonzero parity-compatible cross blocks, Lorentz signature throughout the stated
  interval, and differentiated residuals identically zero.
- Fixed-volume normalization must be explicit and may not be called the whole CSN principle.
- A connection claim requires solving its linear compatibility equations, not naming a familiar
  connection.
- Conservation requires an exact invariant derivative of zero under the stated parallelism
  premise. It is not numerical selection.
- A value selector requires an equation with isolated admissible `mu`; `dot(mu)=0` is insufficient.
- Any claimed physical transport law must be cited from current UDT evidence. Otherwise only the
  mathematical consequences of each candidate transport level may be classified.
- A static negative is regraded only if a time-dependent consistency equation excludes its exact
  witnesses; no lack of dynamics may retroactively falsify a pointwise algebraic result.

## Authority boundary

No physical-time identification, action, field equation, GR/SR evolution or observer mechanics,
topology, boundary functional, carrier, source, mass, `X_max` value, physical scale, GPU work,
startup-control edit, `CANON.md` edit, repository reorganization, or canonization is authorized.

Maximum conclusion:

`UDT_KINEMATIC_TIME_EXTENDABILITY_STATUS_CHARACTERIZED`.
