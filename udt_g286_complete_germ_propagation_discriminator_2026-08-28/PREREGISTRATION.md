# G286 preregistration — complete-germ propagation discriminator

Date: 2026-08-28

## Question

Do current owned identities uniquely continue a regular complete metric from a fully shared prior
region, or can two regular complete metrics share that prior region and every joining-surface jet
while carrying different future curvature and tidal values?

## Frozen witnesses

On `u in [-1,1]`, define

```text
b(u) = 0                    for u <= 0
     = exp(-1/u^2)          for u > 0

T0(u) = 0
T1(u) = epsilon b(u) diag(1,-1),  epsilon = 1/5.
```

Insert each into the G283 metric family. No outcome-dependent alternative witness is allowed.

## Competing landings

1. `CURRENT_IDENTITIES_PROPAGATE_TESTED_COMPLETE_GERM_UNIQUELY`
   if the second witness fails regularity or an owned compatibility/carry identity.
2. `SAME_WHOLE_PRIOR_METRIC_REGION_AND_ALL_JOIN_JETS_ADMIT__GEOMETRICALLY_INEQUIVALENT_FUTURE_CONTINUATIONS__CURRENT_IDENTITY_EVALUATOR_LAYER_IS_NOT_UNIQUE_PROPAGATION`
   if both witnesses are regular, coincide for `u<=0` and to every jet at `u=0`, pass the inherited
   identity layer, and differ invariantly for some `u>0`.
3. `G286_WITNESS_INCONCLUSIVE`
   for any uncategorized failure or insufficient separator.

## Certification contract

- Analytically prove smooth flatness of `b` and exact equality of both metrics on `u<=0`.
- Use the inherited exact G283 result `R_uiuj=T_ij(u)` as the invariant future separator.
- Check symmetry and trace-free structure, fixed metric determinant/signature, and nonzero future
  curvature in a dependency-free production implementation.
- Diagnose path-labelled Jacobi/frame transfer with two numerical methods and require:
  - production symplectic defect `< 2e-11`;
  - independent symplectic defect `< 2e-8`;
  - production/independent final transfer difference `< 2e-6`;
  - nonzero future transfer difference from the flat witness `> 1e-5`.
- The numerical transfer is supportive only. The exact curvature separator carries the conclusion.

## Maximum conclusion

Landing 2 would show only that the currently owned compatibility/evaluator layer is not a unique
propagation law on this bounded smooth family. It would not exclude a stronger native UDT law,
select a candidate, prove a global theorem, or authorize observational fitting.
