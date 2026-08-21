# G196 fresh adversarial review request

## Role and boundary

Act as a cold mathematical and computational reviewer. Inspect only the sealed intake. Do not edit
evidence or continue the research. The claim is bounded to one displayed longitudinally extended
affine complete-coframe family and one central outgoing observer-pair germ.

Claimed landing:

```text
NULL_DIRECTIONAL_DESCENT__FACTORIZATION_AND_NO_CAUSTIC_SURVIVE
```

Do not defend it. Try to falsify or regrade it.

## Load-bearing questions

1. Reconstruct the coframe, metric, central pair pullback, affine null ray, frequency, and screen.
2. Verify whether the connection and tide depend on longitudinal variation only through
   `D_plus=partial_eta+partial_z`. Search explicitly for separately weighted `partial_z`,
   `partial_eta-partial_z`, mixed-second-jet, rotation-derivative, and rotation-square terms.
3. Check the sign and basis convention in `C_s=2 Omega` and the self-adjointness of the tide.
4. Independently expand `(D_plus-2M^T)(D_plus+2M)Y` and compare it with the affine Jacobi equation.
5. Verify the noncommutative ordered representation `D=aLK`, including the transpose order in
   `K'=L^-1 L^-T`.
6. Audit the no-nonvertex-caustic proof for positive and negative ray parameter. Distinguish the
   exact Gram proof from the finite determinant census.
7. Audit the same-ray alias control. Does it prove directional restriction without falsely proving
   global field equality?
8. Determine whether the Torch/SciPy verifier is genuinely independent of the SymPy production
   derivation and whether its formula-driven IVP leg is described honestly.
9. Regrade any wording that promotes the bounded family/germ result to arbitrary complete metrics,
   all directions, a selected physical history, transfer, observations, or `X_max`.

## Registered replay

```bash
G196_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_package.py --no-write
```

## Required response

Return exactly one primary landing:

- `G196_DIRECTIONAL_DESCENT_ACCEPTED_WITH_CAVEATS`;
- `G196_RESULT_CORRECT_BUT_SCOPE_OR_GRADE_OVERSTATED`;
- `G196_DIRECTIONAL_DERIVATIVE_OR_FACTOR_ERROR_REQUIRES_REPAIR`;
- `G196_NO_CAUSTIC_PROOF_FAILS`;
- `G196_INDEPENDENCE_OR_EVIDENCE_GATE_FAILS`;
- or another precisely defined landing forced by the evidence.

Then state the strongest verified theorem, strongest defect or counterexample, algebra/typing
verdicts, evidence-independence verdict, required repairs, and maximum honest conclusion.
