# GR-to-UDT structural subtraction and reciprocal-connection audit — preregistration

Date: 2026-07-21

Base: `aa576614d1afe7514bdb0f316dfd5a6272af6c3f`

Branch: `codex/udt-gr-subtraction-reciprocal-connection-audit-2026-07-21`

Mode: CPU-only exact conformal-connection, reciprocal-structure, and intrinsic-obstruction audit

## Whole question

The preceding time-extendability audit showed that ordinary metric-plus-seal compatibility permits
nonconstant `mu`, while the stronger unselected premise of parallel reciprocal transport conserves
but does not select `mu`.

Instead of drilling through more isolated connection candidates, this audit asks one structural
question by subtracting the GR construction and adding only UDT-native data:

> A nondegenerate metric plus torsion freedom and exact metric compatibility selects the
> Levi-Civita connection. When one calibrated metric is replaced by UDT's CSN conformal class and
> the normalized reciprocal clock/ruler structure is added, does torsion-free compatibility select
> a unique native connection, or is there a precise existence/uniqueness obstruction?

GR field equations, stress energy, Hamiltonian constraints, and matter are not part of this
comparison. The Levi-Civita theorem is used only as a mathematical reference construction.

## Objects that must remain distinct

1. a chosen metric representative `g`;
2. the CSN conformal class `[g]`;
3. the Levi-Civita connection of one representative;
4. the affine family of torsion-free conformal/Weyl connections;
5. the normalized reciprocal generator/endormorphism `L`;
6. the reciprocal character `D(phi)=exp(phi L)`;
7. the reciprocal two-plane/splitting projector `P=L^2` in the complete lift;
8. exact parallelism of `L`;
9. recurrent or weighted preservation of `L`;
10. preservation only of `P` or of the reciprocal line in `End(TM)`;
11. the seal involution `R`, which reverses `L`;
12. a pointwise compatible connection;
13. a globally integrable connection and its holonomy;
14. an action-derived physical evolution law; and
15. a carrier/topological interpretation.

Uniqueness conditional on existence cannot be promoted to an existence theorem. Preservation of a
splitting cannot be promoted to preservation of its normalized reciprocal generator.

## Frozen bounded universe

The audit will test:

1. the exact torsion-free Weyl-connection family satisfying

   ```text
   nabla^A g = -2 A tensor g;
   ```

2. the complete pointwise linear maps from the Weyl one-form `A` into `nabla^A L` and
   `nabla^A P`;
3. exact, recurrent, weighted, projective-line, and splitting-only reciprocal preservation;
4. all four registered constant real isotropic complete lift representatives at `mu=4` and `mu=9`
   with nonzero allowed cross blocks;
5. a nontrivial static reciprocal metric jet with nonzero `d phi`;
6. CSN representative change and Weyl-one-form transformation;
7. seal compatibility and its available boundary data;
8. the exact current finite-cell, Cartan, projective-transport, bootstrap, and topology authority;
   and
9. the conditional Hopf/soliton structure only as a downstream diagnostic of a connection already
   derived without it.

Arbitrary affine torsion, nonmetricity beyond the conformal Weyl form, imported gauge fields,
actions, field equations, and time-live matter solves are excluded.

## Premise ledger

| Object | Treatment |
|---|---|
| Four-dimensional conformal-Lorentzian readout | `CONDITIONAL` with inherited stamps |
| Common-Scale Neutrality | `pinned-by-THEORY` |
| Reciprocal character and normalized ratio structure | `pinned-by-THEORY` in exact founding scope |
| Complete reciprocal generator `L4` | `DERIVED_CONDITIONAL` in registered lift scope |
| Seal-local clock/ruler soldering | `DERIVED_CONDITIONAL` |
| Torsion-free requirement | `free-and-explored`; GR reference premise, not silently adopted |
| Conformal/Weyl compatibility | complete mathematical candidate class for torsion-free `[g]` transport |
| Exact `nabla L=0` | `free-and-explored`; not current authority |
| Recurrent/weighted `nabla L=alpha tensor L` | `free-and-explored` |
| Splitting preservation `nabla P=0` | `free-and-explored` |
| Static reciprocal metric jet | exact UDT metric-led diagnostic, not a complete universe |
| Finite-cell seal and bootstrap | retain exact current limited/on-shell status |
| Hopfion/carrier | `POSIT/CONDITIONAL`; downstream diagnostic only |

## Exact tests

### A. GR subtraction

Re-derive algebraically:

1. why torsion-free exact metric compatibility has no connection difference freedom;
2. why torsion-free conformal compatibility leaves one arbitrary one-form `A`; and
3. how `A` transforms under `g -> exp(2 sigma) g`.

No GR field equation may enter.

### B. Reciprocal reduction: uniqueness conditional on existence

For two torsion-free conformal connections differing by a one-form `B`, derive the complete linear
map

```text
B -> [C(B),L].
```

Compute its kernel for the normalized complete reciprocal structure. Repeat for `P=L^2` and for
recurrent/weighted preservation. Test every registered full lift and both `mu` witnesses so that
base-angular cross coupling is not silently dropped.

### C. Existence and intrinsic obstruction

For a supplied `(g,L)`, solve

```text
nabla^LC L + [C(A),L] = 0.
```

Define the exact residual/quotient obstruction when no `A` exists. Test a flat constant witness and
the nontrivial static reciprocal metric jet with `d phi !=0`. If the latter fails, identify which
components cannot be canceled; do not add torsion or a gauge field to repair it.

### D. Character and weight audit

Test whether recurrence of normalized `L` is genuinely weaker or collapses to exact parallelism
because its eigenvalue traces are fixed. Separately derive the covariant derivative of
`D(phi)=exp(phi L)` and determine what is identity, what is connection choice, and what could carry
new law content.

### E. Seal/global/topology authority

Determine whether the seal, finite-cell boundary, CSN, current bootstrap, or global cocycle supplies
the missing bulk compatibility/existence equation. The conditional Hopf/soliton package may test a
derived connection's consequences but may not select the connection by desired stability.

## Frozen outcome classes

1. `CSN_PLUS_RECIPROCITY_SELECTS_UNIQUE_TORSION_FREE_CONNECTION`
2. `RECIPROCAL_COMPATIBILITY_UNIQUE_IF_IT_EXISTS`
3. `RECIPROCAL_COMPATIBILITY_HAS_CONNECTION_FREEDOM`
4. `RECURRENT_NORMALIZED_RECIPROCITY_COLLAPSES_TO_EXACT_PARALLELISM`
5. `SPLITTING_PRESERVATION_IS_STRICTLY_WEAKER`
6. `FOUNDATIONAL_STATIC_RECIPROCAL_JET_ADMITS_COMPATIBLE_WEYL_CONNECTION`
7. `FOUNDATIONAL_STATIC_RECIPROCAL_JET_HAS_NONZERO_INTRINSIC_OBSTRUCTION`
8. `SEAL_OR_FINITE_CELL_REMOVES_THE_OBSTRUCTION`
9. `SEAL_OR_FINITE_CELL_DOES_NOT_SUPPLY_BULK_CONNECTION_EXISTENCE`
10. `CONNECTION_UNIQUENESS_WITH_EXISTENCE_OPEN`
11. `CONNECTION_EXISTENCE_AND_UNIQUENESS_BOTH_OPEN`
12. `CONDITIONAL_HOPF_STRUCTURE_DIAGNOSES_BUT_DOES_NOT_SELECT_CONNECTION`
13. `AUDIT_INCONCLUSIVE`

Multiple premise-scoped outcomes may apply.

## Falsification and certification contract

- Uniqueness requires a zero kernel of the complete connection-difference map, not a preferred
  solution returned by a solver.
- Existence requires exact consistency of the overdetermined full tensor system. Rank deficiency or
  a least-squares fit is not existence.
- A static-jet obstruction must survive CSN representative change and independent exact
  reconstruction; otherwise it is a gauge artifact.
- Recurrent transport is genuinely weaker only if nonzero recurrence survives the fixed trace/eigenvalue
  identities of normalized `L`.
- A seal/global selector must provide an actual bulk or boundary-to-bulk equation in current source
  authority. A named missing boundary cannot be used as that equation.
- The soliton may be used only after the connection is derived independently. Stability or Hopf
  resemblance cannot be an acceptance criterion for connection selection.
- Failure of torsion-free Weyl compatibility does not prove that UDT requires torsion, a gauge
  field, or another mechanism. Those remain separate future branches.

## Authority boundary

No torsion, new gauge field, action, field equation, GR dynamics, stress-energy, topology, carrier,
source, boundary functional, physical time law, mass, scale, `X_max`, GPU work, startup-control edit,
`CANON.md` edit, repository reorganization, or canonization is authorized.

Maximum conclusion:

`UDT_GR_SUBTRACTION_RECIPROCAL_CONNECTION_STATUS_CHARACTERIZED`.
