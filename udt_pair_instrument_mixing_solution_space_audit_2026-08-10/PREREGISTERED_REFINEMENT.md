# Preregistered refinement — matrix-valued instrument atlas

Date: 2026-08-10

Parent preregistration commit: `b6fb1883`

The first exact bivector calculation has been run. Before interpreting it, dimensional counting
shows that determinant/area components alone may not classify the complete split-relative pair
Jacobian. This additions-only refinement registers the required completeness test without changing
the original candidate landings or conclusion ceiling.

Write the complete pair Jacobian in a supplied metric-orthogonal reciprocal/angular split as

`V = (X;Y)`,

where `X` is the `2 x 2` reciprocal block and `Y` is the `2 x 2` angular block. The audit will test
the matrix-valued channels

`H_R = X^T diag(-1,+1) X`,

`H_A = Y^T Y`.

## Added exact tests

1. Verify `h=H_R+H_A` with no frozen component.
2. Verify `H_R` and `H_A` are individually invariant under the split-preserving proper frame group.
3. Verify `det(H_R)=-B01^2`, `det(H_A)=B23^2`, and the remaining determinant cross-term is the
   registered signed mixed bivector norm.
4. On the generic invertible stratum, test whether equality of `(H_R,H_A)` implies equality of the
   Jacobian orbit up to `O(1,1) x O(2)`, with proper-component signs recorded separately.
5. Derive `phi_pair`, `kappa`, and `beta` from `H_R+H_A` and show exactly how the complete angular
   matrix can modulate all three pair-state coordinates.
6. Determine whether a time-live curve of these matrices is supplied by algebra alone. It must be
   reported `OPEN` unless an evolution or global pair-family owner is independently present.

## Unchanged ceiling

Even a complete matrix-valued orbit atlas does not authorize a positive scalar instrument weight,
a physical regime assignment, an evolution law, or a selected universe branch. The strongest
allowed landing remains a conditional, split-relative solution-space atlas.
