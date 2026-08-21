# G195 fresh adversarial review request

## Role and boundary

Act as a cold mathematical and computational reviewer.  Inspect only the sealed intake.  Do not
edit evidence or continue the research.  The result is intentionally bounded to one displayed
time-dependent affine complete-coframe family and one central outgoing observer-pair germ.

The claimed landing is

```text
ROTATION_CARRIES_COVARIANTLY__GENERAL_REAL_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE
```

Do not defend it.  Try to falsify or regrade it.

## Load-bearing questions

1. Reconstruct the coframe, metric, affine null ray, central screen, and Levi-Civita screen
   connection.  Is the coordinate-screen connection really `C_eta=2 Omega` with the stated sign
   and index convention?
2. Recompute the coordinate-screen curvature tide.  Is

   \[
   T_c=\tau_0I+a^{-4}(2S'-4S^2-4[S,\Omega])
   \]

   correct and self-adjoint?  Do any `R'` or `R^2` curvature terms actually survive?
3. Check the parallel-screen construction `O'=-2 Omega O`.  Does conjugation really give

   \[
   T_p=\tau_0I+a^{-4}(2\widetilde S'-4\widetilde S^2)?
   \]

   Audit all basis/component conventions; do not accept a sign merely because the two supplied
   scripts share it.
4. Expand independently

   \[
   (\partial_\eta-2M^T)(\partial_\eta+2M)Y=0.
   \]

   Is it equivalent to the affine Jacobi equation for arbitrary real `M=S+Omega` in this family?
5. Verify or break the representation

   \[
   D_c=aLK,\quad L'=-2ML,\quad
   K=\int_0^\eta L^{-1}L^{-T}\,ds.
   \]

   Pay special attention to transpose order and the derivative of `L^{-T}`.
6. Audit the exact no-nonvertex-caustic proof for both `eta>0` and `eta<0`.  Does negative
   definiteness of `K` for negative `eta` still imply positive determinant in two screen
   dimensions?  Are orientation and regularity hypotheses sufficient?
7. Determine whether the independent verifier actually reconstructs metric jets, Riemann
   curvature, and the screen connection independently of production, and whether its
   formula-driven adaptive IVP leg is described with sufficient caveats.
8. Audit the maximum conclusion.  Identify any wording that improperly promotes a theorem for the
   displayed family into a theorem for arbitrary complete UDT metrics or physically selected
   profiles.

## Registered replay

The package exposes a no-write replay:

```bash
G195_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g195_antisymmetric_screen_rotation_boundary_2026-08-20/verify_package.py --no-write
```

The full replay is CPU-heavy.  You may instead run bounded direct algebra or inspect the frozen
artifacts, but distinguish inspection from independent recomputation.

## Required response

Return exactly one primary landing:

- `G195_ROTATION_CLOSURE_ACCEPTED_WITH_CAVEATS`;
- `G195_RESULT_CORRECT_BUT_SCOPE_OR_GRADE_OVERSTATED`;
- `G195_FACTOR_OR_FRAME_ERROR_REQUIRES_REPAIR`;
- `G195_NO_CAUSTIC_PROOF_FAILS`;
- `G195_INDEPENDENCE_OR_EVIDENCE_GATE_FAILS`;
- or another precisely defined landing forced by the evidence.

Then give:

1. the strongest verified theorem with exact hypotheses;
2. the strongest defect or counterexample;
3. algebra/typing verdicts for questions 1–6;
4. evidence-independence verdict;
5. required repairs, if any;
6. maximum honest conclusion and smallest next adjacent calculation.
