# G143 preregistration — single-pair domain carry ownership

Date: 2026-08-17

## Whole bounded question

Determine whether one supplied regular calibrated pair realization already supplies G142's carrier
carry through its own domain chart/trivialization, and separate that internal same-query carry from
cross-query, cross-branch, or observer-network identification.

For a supplied pair immersion `F:Sigma->M` with calibrated ordered coordinates `y=(y0,y1)` on one
chart containing endpoint parameters `A,B`, let `R_i` be the positive-diagonal upper-triangular
terminal factor of `h=F^*g` at `i`. Test whether the shared coordinate coefficient space gives the
same-chart presentation `M_BA=I` and hence `C_BA=R_B R_A^-1`, while a flag-preserving coordinate
change with endpoint Jacobians `J_i` gives

```text
R_i' = R_i J_i^-1,
M_BA' = J_B M_BA J_A^-1,
C_BA' = C_BA.
```

## Frame and premise ledger

- Method: exact type/algebra audit of a supplied calibrated pair domain; no fit, dynamics, action,
  connection, path selector, or new coefficient.
- `DERIVED_CONDITIONALLY`: `h=F^*g`, terminal factors on the regular calibrated stratum, G142 total
  comparison and endpoint-gauge law.
- `SUPPLIED/CHOSE`: pair realization, one ordered calibrated domain chart/trivialization spanning
  the compared parameter points, and restriction to flag-preserving `B^+(2)` changes.
- `WORKING`: co-presence as membership in one supplied complete solution.
- `OPEN/OMITTED`: metric selection of `F`, query population, cross-query/branch identification,
  physical restriction to `B^+(2)`, generic atlas/path connection, singular/null/cut strata,
  history, `X_max`, proper length, observations, light/EM, action, source, bootstrap, matter, mass,
  and dynamics.

## Preregistered theorem tests

1. In one supplied calibrated chart, endpoint tangent coefficient vectors use one model `R^2`, so
   identity carry is a lawful same-chart presentation.
2. Under endpoint Jacobians `J_A,J_B` induced by a flag-preserving chart change, the carry becomes
   `J_B J_A^-1`, endpoint factors become `R_i J_i^-1`, and total `C` is unchanged.
3. For three parameter points, induced carries compose exactly.
4. Carry grading shifts by endpoint Jacobian grading while total grading stays invariant.
5. A smooth explicit strip reparameterization realizes unequal endpoint Jacobians and a nonidentity
   carry without changing the underlying pair realization or total comparison.
6. A pair manifold or pair metric without a spanning trivialization does not canonically identify
   separated tangent fibers; identity carry must not be promoted to a coordinate-free theorem.
7. Distinct query domains, branches, or pair realizations have no induced carry unless an overlap,
   gluing map, common atlas, or separately supplied transport identifies them.

## Certification and falsification

Production will use exact SymPy matrices and a symbolic smooth reparameterization witness. An
independent stdlib/Fraction replay must reconstruct the finite claims without importing production.
Falsify or narrow if the coordinate law fails, the same-chart identity is claimed invariant, the
explicit reparameterization is not integrable, or the sources already derive a cross-query carry.

Maximum possible conclusion:

```text
ONE_SUPPLIED_CALIBRATED_PAIR_CHART_OWNS_A_SAME_QUERY_IDENTITY_CARRY_PRESENTATION__
FLAG_PRESERVING_REPARAMETERIZATION_MOVES_THAT_CARRY_TO_ENDPOINT_JACOBIAN_RATIO__
TOTAL_G142_COMPARISON_REMAINS_INVARIANT__
PAIR_METRIC_ALONE_DOES_NOT_CANONICALLY_IDENTIFY_SEPARATED_TANGENT_FIBERS__
CROSS_QUERY_BRANCH_NETWORK_CARRY_AND_PHYSICAL_HISTORY_REMAIN_OPEN
```
