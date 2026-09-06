# Finite pre-freeze diagnostic — 2026-09-06

The first author symbolic run exited 1 at
`projection_radial_transverse_eigenvalues`, after fourteen preceding guards.
Its capture is `author_symbolic.{json,stdout,stderr}` and will not be overwritten.
This plan is frozen before the diagnostic execution under solver-first.

Question: is the failed equality a different mathematical Jacobian, or Sympy
structural equality of algebraically equivalent expressions?

Preserve the original script as `check_symbolic_initial_failed.py`. Recompute
the original flat incoming flow Jacobian at `(r0,0,0)`, with `r0>0`, and print
both matrices, structural equality, all simplified entrywise differences and
the determinant. One CPU child, 512 MiB, 60 seconds, no search or fitting.
The original metric, phase, sign, coordinate domain and expected Jacobian stay
fixed. No protected work or metric development is involved.

Possible outcomes: nonzero differences require an argument/sign/domain audit;
zero differences identify a representation-level implementation defect. Only
in the latter case replace structural equality with exact entrywise symbolic
zero testing, then rerun all original guards and the four frozen mutations.
No tolerance may be introduced. Preserve all failures and report this as a
pre-freeze implementation correction, not independent verification or a
changed physical premise. Stop for an unresolved mathematical discrepancy.
