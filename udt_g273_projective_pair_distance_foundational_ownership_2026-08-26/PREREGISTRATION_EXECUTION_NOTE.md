# G273 preregistration execution note

The first production symbolic run failed closed on three identities because SymPy did not simplify
principal-branch `tanh`/`atanh` expressions to their exponential or rational forms. The independent
standard-library/Fraction reconstruction had already passed all 24,000 cases.

Before accepting any outcome, the three production checks were replaced by branch-free exact forms:

1. the projective contrast was compared to the exponential definition of `tanh`;
2. composition was checked rationally using positive reciprocal-leg ratios `r1`, `r2`, and `r1*r2`;
3. the conditional metric factor was checked directly between the exponential depth and its
   projective contrast.

No premise, candidate, tolerance, result class, or conclusion wording changed.
