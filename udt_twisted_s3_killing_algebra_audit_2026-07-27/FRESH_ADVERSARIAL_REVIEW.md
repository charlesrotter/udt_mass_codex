# Fresh adversarial review

Reviewer context: `killing_algebra_adversary`, fresh context, no file edits.

Final grade: **VERIFIED-WITH-CAVEATS**.

## Independently accepted

- The unit-quaternion coframe convention gives `kappa=-2` (up to orientation), and the primary
  Maurer-Cartan jets are correct through the required total degree.
- A third metric jet is sufficient for first derivatives of curvature; the inverse, Christoffel,
  Riemann, Ricci, and Ricci-power invariant contractions are consistent.
- Direct recomputation from the recorded matrix gives the exact nonzero determinant in the report.
- Rank three annihilates every spatial component of an unrestricted Killing field on an open set;
  `L_(fK)g=0` forces `f` constant, and Killing transport/one-jet uniqueness extends the result over
  connected `R x S3` without assuming analyticity or geodesic completeness.
- The global polynomial profile, coefficient bound, strict slice inequality, nonconstant norm, and
  nonzero same-branch twist are valid.
- All K01–K12 rows now have honest outcomes: K08 and K12 remain open, K09 is only excluded from the
  regular witness, and no outcome pretends exhaustive family closure.

## Adversarial correction incorporated

The symbolic-`lambda` result originally used a Boolean meaning “the determinant polynomial is not
identically zero,” which could be misread as “nonzero at every real `lambda`.” The reviewer found
isolated real roots. The generator and result schema now separate:

```text
determinant_polynomial_not_identically_zero = true
invariant_gradient_determinant_nonzero = null
open_set_rank_three = null
```

for symbolic `lambda`. The roots are recorded only as places where this certificate is inconclusive;
they are not classified as extra symmetries.

## Caveats retained

- The exact existence witness is certified; the complete function/parameter space is not.
- “Complete” means global `S3` coframe/spatial completion, not Lorentzian geodesic completeness.
- No physical profile, stationary branch, action, or bootstrap law is selected.
