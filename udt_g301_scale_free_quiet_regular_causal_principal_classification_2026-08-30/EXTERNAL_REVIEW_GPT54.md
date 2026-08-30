# Fresh external G301 review — gpt-5.4

Date: 2026-08-30

The text below is the reviewer's final response, preserved verbatim except for this provenance
header and conversion of intake-local links to plain references.

---

## Findings

1. Yes. Differentiability at `0` plus exact positive degree-one homogeneity forces exact linearity
   on the star-shaped quiet domain: `DF_0(K)=F(K)` for each admissible `K`, so no smooth nonlinear
   degree-one counterexample survives the frozen hypotheses.

2. Yes. In the declared unoriented metric-only symmetric rank-two two-jet lane, the linear natural
   basis is exactly `Ric_ab` and `R g_ab`; equivalently
   `Hom_O(1,3)(AlgCurv,S^2)` is 2-dimensional here. The package's proof is brief but correct.

3. Yes. The trace-adjustment map on symmetric tensors has eigenvalues `a` on the traceless sector
   and `a+4b` on the trace line, so it is invertible exactly when `a != 0` and `a+4b != 0`. That
   whole continuum is one residual-equivalence class.

4. Yes. The `a+4b=0` class is genuinely inequivalent, operator-scale-free, and carries one
   constant scalar-curvature datum per connected solution region via contracted Bianchi.

5. Yes, but only at the level claimed in the derivation: it justifies the nonzero-frequency
   quiet-principal comparison, not causal completeness, gauge-fixed well-posedness, or global
   dynamics. The text is appropriately narrow on that point.

6. Yes. The scalar-only class `a=0, b!=0` fails the preregistered complete-metric principal gate
   because it only imposes `R=0` and leaves arbitrary traceless Ricci directions unconstrained.

7. I do not see a silent promotion of identity divergence freedom, W3, W6, GR dynamics, source,
   scale, action, or observation in the G301 package text. The package consistently marks them as
   comparison-only, candidate, or excluded.

8. No. Under the frozen hypotheses, I cannot construct a residual outside the generic and
   trace-free Ricci classes that still survives the complete-principal gate. Sections 2-4 of the
   derivation block that route.

9. No. The scripts do not independently test the full scientific claim. They can false-pass a
   conceptual defect because they assume the `a Ric + b R g` form and mostly verify downstream
   algebra or string presence. The clearest examples are the tautological differentiability test
   in `verify_principal_class_independent.py`, the vacuous `C06_integration_constant_erased` catch
   in `run_catch_proofs.py`, and the token-presence checks in `verify_package.py`.

## Landing

`VERIFIED-WITH-CAVEATS`

Selected preregistered landing: `INTERNAL_CERTIFICATION_FAILURE`.

Maximum defensible scientific claim inside the bounded lane is still
`TWO_OR_MORE_INEQUIVALENT_CLASSES_SURVIVE`: the generic Ricci-flat class and the inequivalent
trace-free Ricci class with one connected-region constant scalar-curvature datum. But as packaged,
G301 does not internally certify that claim, because its "independent" and "hostile-catch" scripts
do not independently cover the load-bearing reduction from a general admissible `F:K->S2` to
`a Ric_ab + b R g_ab`.

No metric changed. No reciprocal kernel changed. No foundational premise changed.

## Repairs

- Narrow the claims of `verify_principal_class_independent.py`: it is an independent replay of the
  coefficient-strata algebra after accepting the ansatz, not an independent test of the full
  scientific claim.
- Replace `C06` in `run_catch_proofs.py` with a real witness-based check that the trace-free class
  admits nonzero pure-trace Ricci data rejected by the generic class.
- Replace `C08` and the token checks in `run_catch_proofs.py` and `verify_package.py` with checks
  that actually detect premise promotion in the argument, not just ledger labels or wording.
- Expand `EXACT_DERIVATION.md` with an explicit invariant-theory proof of the `Ric_ab`, `R g_ab`
  basis.

Package-local replay from `/work` passed `py_compile`, production (`27,829` assertions), independent
replay (`49,609` assertions), hostile catches (`12/12`), and package verifier (`51` checks). The
reviewer did not run the repository premise verifier because repository-root access was barred.
