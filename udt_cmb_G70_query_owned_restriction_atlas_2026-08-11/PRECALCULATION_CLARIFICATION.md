# G70 precalculation clarification

Date: 2026-08-11

This clarification is registered after the primary preregistration and before writing or running
the production atlas. It changes no source control, sensitivity center, rank threshold, allowed
landing, or authority boundary.

1. Every non-profiled observation model will report the full three-parameter rank and all three
   two-parameter column restrictions:

   ```text
   (x,a), (x,epsilon), (a,epsilon).
   ```

   These answer the conditional algebraic question “what if the omitted parameter were independently
   selected?” No omitted parameter will be chosen after seeing the ranks.
2. For a rectangular `m x n` sensitivity matrix, singular values are padded with exact zeros to
   length `n`; therefore fewer than `n` output coordinates cannot be misclassified as full column
   rank.
3. Column normalization and the frozen `1e-6`/`1e-8` ratio thresholds apply separately to every
   full matrix and every two-column restriction. A zero column is rank deficient.
4. The positive-definite matrix logarithm is evaluated by a symmetric eigen-decomposition. Any
   nonpositive eigenvalue, nonfinite result, or reconstruction residual above `2e-12` fails the
   package.
5. The fixed observer-screen basis is part of the supplied G68 control query. `(S1,S2)` are smooth
   coordinates in that fixed basis; their rank is invariant under a fixed nonsingular linear
   recombination, but no physical detector ownership is inferred.
6. Saved `psi` is used directly only after verifying that every finite-difference stencil lies in
   one unwrapped chart with no `2 pi` crossing. It remains a geometric carry channel, not scalar-TT
   ownership.
7. `R05_KNOWN_SOURCE_PLUS_CARRY` uses all four coordinates `(A,S1,S2,psi)` in its rank test. No
   result-dependent three-row subset is allowed.
8. `R06_TWO_FIXED_SHAPE_CHANNELS` uses all four shape coordinates and independent unknown
   amplitudes. It assumes both source shapes and their channel association are supplied controls.
9. “Known source covariance” means the exact dimensionless control matrix including normalization;
   it is not a claim that UDT or observation currently supplies such knowledge.
