# G194 second packaging-repair preregistration

Date: 2026-08-20

The first repair-only follow-up returned `G194_REPAIRS_REJECTED` solely because `R1` failed: Torch's
`torch.func.jacfwd` path lazily imports a distributed helper that calls
`tempfile.TemporaryDirectory()`.  `R2`, `R3`, and the unchanged bounded scientific landing were
accepted.

## R4 — write-free Torch metric-jet autodifferentiation

Replace only the two `torch.func.jacfwd` calls used to reconstruct first and second metric jets by
a local composition of `torch.autograd.functional.jacobian` using unvectorized reverse-mode
autodifferentiation and `create_graph=True` for the inner derivative.  The outer result must be
detached exactly where the existing forward-mode result was detached.

This is a verifier implementation repair.  It must not change:

- the coframe or any derived equation;
- the metric-jet evaluation points;
- the curvature reconstruction;
- any profile, seed, tolerance, assertion, hostile catch, result, or landing;
- the independent evidence class, which remains metric-jet autodifferentiation spotchecks plus a
  formula-driven matrix IVP rather than full interval metric-derived propagation.

Documentation and machine-readable implementation text must say `Torch autodifferentiation`, not
claim forward-mode specifically.

## Certification

The repair passes only if all of the following hold:

1. the fresh independent result is parsed-JSON identical to the frozen artifact except for the
   implementation-description string;
2. after regenerating the artifact with that truthful description, the full package replay passes;
3. the exact registered replay passes in a genuinely read-only external sandbox;
4. `.review_runtime` is empty before and after replay;
5. all evidence-file digests are unchanged during no-write replay;
6. `R2`, `R3`, 267 histories, 4,007 assertions, 22 hostile catches, tolerances, and the bounded
   landing remain unchanged.

Any mathematical or outcome change invalidates this repair-only cycle.  A fresh sealed follow-up
must verify only R4, retained R2/R3, and the unchanged scientific landing.
