# G343 preregistration execution note

Date: 2026-09-04

## Discarded first execution

After preregistration commit `3f182b86`, an initial production implementation returned
`8088/8088` and an initial implementation-distinct route returned `2640/2640`. Those runs are not
accepted as evidence.

Before banking, the driver found that the first regular-direction presentation had written

```text
rho = A^2/(A^2+B^2)
```

for momentum combinations whose ratio is the dimensionful G341 parameter `lambda`. The code's
constant `1` therefore represented an undeclared `T_*=1` reference. Although all tested identities
were scale-covariant in normalized variables, the written definition could be read as adding unlike
dimensionful quantities and could conceal a preferred scale.

## Preregistered repair before rerun

The corrected chart uses one explicit supplied positive-time reference event on the same ray:

```text
rho = T_*^2/(T_*^2 + lambda^2)
nu = (dT/ds) at T_*
```

The computation must now keep `T_*` explicit and pass a new reference-event covariance gate.
Changing the reference event converts `rho` and `nu` while holding `lambda` and the affine tangent
fixed; the resulting `4 x 4` propagator must be unchanged.

No primary or secondary alternative, tolerance, endpoint domain, path-label rule, or maximum
conclusion has been changed after seeing the discarded outputs. The revised implementation and all
evidence will be run only after this repair is committed.

## First corrected-chart execution

After repair commit `71db75f4`, the first corrected production execution passed every new
composition, symplectic, reversal, reference-event covariance, affine-gauge, and principal-limit
check but failed all 400 G342 vertex-recovery component checks. The cause was mechanical and exposed:
the independent old-chart comparison still used `lambda=sqrt((1-rho)/rho)` instead of the repaired
dimensional conversion `lambda=T_0 sqrt((1-rho)/rho)` when `T_*=T_0`. Its maximum mismatch was
`2.861212942267234`.

The old-chart control is corrected before the next execution. No production propagator formula,
alternative, tolerance, sample, or conclusion is changed.
