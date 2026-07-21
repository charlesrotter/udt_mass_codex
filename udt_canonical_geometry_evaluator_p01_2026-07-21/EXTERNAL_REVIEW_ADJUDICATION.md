# External-review adjudication

Date: 2026-07-21

## Historical first return

`EXTERNAL_ADVERSARIAL_REVIEW.md` is retained unchanged. Its blocking provenance finding was caused
by the reviewer's mandatory startup checkout returning the read-only review process to base commit
`7476fe3`, before P01's preregistration commit. From that wrong tree state it could not see
`PREREGISTRATION.md` and reported source-lineage row `S15` as missing.

The first return nevertheless confirmed the tensor algebra and identified useful coverage gaps:
generic off-diagonal metric jets, coordinate-dependent local Lorentz jets, and full constant linear
coordinate transformations. Those gaps were treated as real review advice rather than discarded.

## Correction

The implementation and verifier were strengthened before final adjudication:

- a generic off-diagonal metric two-jet has an independently written direct tensor reference;
- the conditional `2+2` slot map has exact symbolic first- and second-derivative comparison;
- a coordinate-dependent Lorentz two-jet checks metric-jet invariance, the inhomogeneous spin
  connection gauge law, and Cartan-curvature covariance; and
- a general constant linear coordinate map checks metric value, first and second jets, connection,
  curvature, and the coframe round trip.

The correction review ran from preregistration commit `c2264f9` with the complete untracked result
package visible. `EXTERNAL_ADVERSARIAL_REVIEW_FINAL.md` reports `PASS`, no blocking defect, and no
material coverage caveat. It also supplied a fresh noncommuting Lorentz-jet stress test with maximum
reported residual `5.56e-17`.

## Ruling

The initial `FAIL_BLOCKING` is preserved as historical evidence and superseded only for its stated
wrong-tree provenance defect. The substantive review advice was incorporated. The corrected fresh
review is the controlling external return.

Final review status: `PASS`.

Maximum supported conclusion:
`GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED`.
