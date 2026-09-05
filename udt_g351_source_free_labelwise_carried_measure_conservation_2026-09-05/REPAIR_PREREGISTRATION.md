# G351 R1 scientific-scope repair preregistration

Date: 2026-09-05
Trigger: fresh blind adversarial verification before banking
Status: `PREREGISTERED_REPAIR_PENDING_EXECUTION`

## Defect found

The owner-adopted premise allows every finite nonnegative additive measure on label space, but the
regular-density derivation wrote `dmu=s(lambda) dlambda` without explicitly restricting that step
to the absolutely continuous part. A finite point-mass measure is a counterexample to existence of
an ordinary sheet-area density even when the screen Jacobian is positive. Also, the ratio
`n_j/n_i` is undefined where `n_i=0`; the division-free density equality is the correct universal
statement.

## Frozen counterexample

Take label space `[0,1]`, regular constant Jacobians `J_i=1`, `J_j=2`, and conserved
`mu=delta_(1/2)`. The measure is finite, nonnegative, additive, and conserved, but singular with
respect to both regular sheet-area measures. No ordinary Radon--Nikodym density of the full measure
exists, so a density exponent cannot be assigned to that singular component.

## Preregistered repairs

1. Keep the owner-adopted conservation premise unchanged for the full finite measure.
2. State the inverse-area theorem only for the absolutely continuous part in a regular label chart,
   equivalently wherever `mu_ac=s(lambda) dlambda` exists.
3. Replace the universal ratio statement by the division-free equality
   `n_j=A_ji^-1 n_i` almost everywhere. Use ratios only on nonzero-density support.
4. State that the singular part remains a singular carried measure and has no ordinary `q`.
5. State that `q=-1` is uniquely forced for any nonzero absolutely continuous carried-density
   component inside G350's declared full independent positive `(R,A)` character domain. Zero
   content remains zero but cannot identify an exponent by itself.
6. Strengthen production and independent verification with explicit finite atomic/singular
   counterexamples and coefficient recovery from conservation probes, rather than treating a
   hard-coded residual as independent proof.
7. Add hostile mutations for promoting the full arbitrary measure to a density and for using a
   zero-density ratio.

## Frozen invariants

- The owner-adopted premise is not derived and is not canon.
- The full conserved label measure and pushforward remain defined through rank loss.
- On nonzero absolutely continuous regular density, the candidate remains `R^p A^-1` and `p`
  remains arbitrary.
- Metric, reciprocal kernel, angular sector, and bounded response equation remain unchanged.
- No light, energy, source, population, detector, distance, history, scale, `X_max`, or canon is
  selected.

## Acceptance contract

- The atomic counterexample must be reproduced independently.
- Coefficient recovery must return `(a-w,q+1)=(0,0)` from independent frequency-only and area-only
  probes without assuming `q=-1` in the solver.
- Division-free equality must cover zero density; ratio checks must be restricted to positive
  density.
- All previous valid identity, sewing, reversal, covariance, multiplicity, source, and caustic
  checks remain passing.
- Aggregate no-write replay changes no bytes and emits no bytecode.

Maximum conclusion: a repaired, narrower theorem for the nonzero absolutely continuous regular
density component, alongside conservation of the full finite label measure. No broader physical
promotion.
