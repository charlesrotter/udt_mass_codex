# Frozen repair controls for the preregistered Gram spectral/subspace map

Date: 2026-08-12  
Status: committed before the missing Gram diagnostics are evaluated

The cold adversarial review correctly found that the original result files recorded registered-
split residuals and classes but did not fulfill the preregistered requirement to record each
Gram endomorphism's full spectrum, rank/Jordan diagnostics, and intrinsic spectral subspaces.
This is a completeness repair, not a new scientific question and not permission to alter the
original preregistration.

The saved production and independent full tensors are the inputs. No derivative is rerun, no
metric control changes, and no row is removed.

## Fixed diagnostics

For each of the `3 x 1221 = 3663` mixed endomorphisms `A=g^-1 K`, each route must record:

- all four complex eigenvalues;
- numerical operator rank;
- real-eigenvalue count and complex-conjugate-pair count;
- algebraic and geometric multiplicities of every spectral block;
- total Jordan defect `sum(algebraic-geometric multiplicity)`;
- real spectral-block dimensions and Lorentz signatures;
- the coframe-component Euclidean projector of every real spectral block;
- every spectral-block sum having real dimension two, including all six two-line groupings when
  four simple real eigenlines survive;
- pair/screen defects and Lorentz signature for every such candidate two-plane.

A repeated eigenspace is recorded as one block. Arbitrary subspaces inside a repeated scalar
eigenspace are not called intrinsic.

## Fixed thresholds

```text
operator/generalized-nullspace rank tolerance     1e-8 * max(1, norm(A))
eigenvalue imaginary tolerance                    1e-8 * max(1, norm(A))
eigenvalue clustering tolerance                   1e-7 * max(1, norm(A))
fivefold unresolved band                          applies to all three thresholds
production/independent eigenvalue error            <= 5e-3
production/independent spectral-projector defect   <= 2e-3
```

The independent route uses separately coded SciPy eigensystem/nullspace logic; production uses
NumPy eigensystem/SVD logic. Both operate on their own already-saved `K` tensors and independently
reconstruct the coframe-registered mixed endomorphism.

If ranks, spectral block dimensions, Jordan defect, candidate-plane counts, or matched projectors
disagree, that endomorphism is `SPECTRALLY_UNRESOLVED`. Thresholds may not be tuned afterward.

## Conclusion ceiling

This repair can complete the local spectral/subspace atlas and refine which alternative structures
are robust. It cannot promote an alternative spectral plane to a physical pair plane, select a
history/query/realization, or change any downstream premise.

