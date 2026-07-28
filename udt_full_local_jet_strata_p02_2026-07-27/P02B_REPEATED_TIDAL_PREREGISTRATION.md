# P02-B preregistration: repeated-tidal Hessian-response completion

Status: `PREREGISTERED AFTER P02-A; BEFORE P02-B SOLVES`

## Candidate universe

Freeze every P02-A attempt satisfying both:

```text
status = CONSTRUCTED
requested collective_Hessian_rank = 0.
```

The frozen P02-A artifact gives exactly 4,198 bases: 2,880 dynamic and 1,318
coordinate-static.  No base may be removed based on its curvature.  For each
base solve all three registered screen-tidal targets

```text
T_AB = lambda delta_AB,
lambda = -shell^2, 0, +shell^2.
```

This gives exactly 12,594 P02-B candidates.  Negative, zero, and positive are
construction labels, not physical signs or selected branches.

## Exact response question

At fixed point values and first jets, the Riemann tensor is affine in the
amplitude Hessians.  Compute the full numerical response of

```text
(T22,T23,T33) = (R_2020,R_2030,R_3030)
```

to every allowed independent Hessian component:

- 80 components for a dynamic base;
- 48 purely spatial components for a coordinate-static base.

Use the frozen GPU curvature evaluator, one-unit basis responses, and a
float64 SVD least-norm solve with `rcond=1e-12`.  Re-evaluate the solved Hessian
through the full metric curvature rather than trusting the linear system.

Classify each candidate exactly one of:

- `CONSTRUCTED_REPEATED_TIDAL` when all three re-evaluated components meet
  scaled residual `1e-8`;
- `RESPONSE_RANK_INSUFFICIENT` when the affine response cannot span the target;
- `RESIDUAL_FAILED` when the solve does not re-evaluate within tolerance;
- `NUMERICALLY_NONFINITE` when any response, solution, or check is nonfinite;
- `ILL_CONDITIONED_LARGE_HESSIAN` when the solution Frobenius norm exceeds
  `1e6`; retain the solution but do not call it a reliable witness.

Record response rank, singular values, Hessian norm, resulting collective
Hessian rank, curvature-operator rank, causal residual, repeated-tidal
residual, pair/screen mixing, scalar curvature, and Kretschmann scalar.

## Controls

1. Recompute the P02-A zero-Hessian tidal vector exactly.
2. Verify affine superposition on 64 fixed bases with two independent Hessian
   combinations; scaled disagreement must be at most `1e-10`.
3. Re-evaluate every accepted witness through the full curvature path.
4. Independently reconstruct 32 accepted witnesses using the existing NumPy
   four-dimensional finite-difference method; metric and scalar tolerances
   remain those in `CLASSIFICATION_CONTRACT.tsv`, and repeated-tidal component
   scaled error is at most `2e-4`.
5. Preserve every candidate and failure; do not retune the target or choose a
   different base.

Production uses one V100 process, float64, response-base batches no larger than
8, evaluation batches no larger than 512, projected peak below 2 GiB, and a
15-minute stop.

## Maximum conclusion

P02-B may establish local constructibility or sampled response obstruction of
the three normalized repeated-tidal targets across the exact frozen base
universe.  It cannot select repetition, a sign, a global section, a finite-cell
completion, a carrier, an action, dynamics, or physics.

