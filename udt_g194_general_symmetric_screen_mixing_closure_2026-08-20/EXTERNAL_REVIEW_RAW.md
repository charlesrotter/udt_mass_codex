# G194 fresh external adversarial review

Date: 2026-08-20

Reviewer: external Codex `gpt-5.4`, high reasoning, fresh ephemeral context, web disabled,
read-only sealed intake.

## Landing

`GENERAL_SYMMETRIC_CLOSURE_ACCEPTED_WITH_CAVEATS`

## Findings

- The registered no-write replay was not reproducible in the read-only sandbox.  The command
  failed during `torch`/`dill` import because Python found no writable temporary directory.  The
  reviewer classified this as an environmental limitation, not a scientific refutation.
- The package verifier conditionally consults the ambient root premise verifier when it is present.
  That makes the package replay incompletely sealed in a normal repository-root run.
- The interval-scale numerical leg is only partially independent: it independently reconstructs
  metric jets/Riemann values at registered points, but the direct and ordered interval IVPs both
  use the same disclosed closed-form tide between those points.  It is implementation-drift
  evidence, not full interval-by-interval independent curvature propagation.
- The reviewer found no successful refutation of the bounded algebra, symmetric tide formula,
  ordered factorization, matrix ordering, or exact sign-definite Gram no-caustic proof.

## Replay result

The exact registered replay was attempted and exited nonzero before the independent computation
because the read-only environment supplied no writable temporary directory acceptable to
`torch`/`dill`.  No unregistered workaround was run.

## Maximum conclusion

On the sealed record, G194 closes arbitrary smooth symmetric `2 x 2 M(eta)` only for the displayed
coframe family and supplied central `+z` germ.  The reviewer accepted

`D=a L K`, `L'=-2 M L`, and `K=int L^-1 L^-T`

as yielding `det D>0` for every nonvertex point in the declared connected regular interval.  No
extension was granted to antisymmetric rotation, arbitrary complete coframes, other pair germs,
global completion, or physical-history claims.

The original intake-local absolute links were omitted because the sealed intake is ephemeral.  The
complete terminal transcript is retained separately.
