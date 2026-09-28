# Correction to the sealed source-first note

2026-09-28, identified immediately after the source-first seal, before candidate
proof, producer-code or result exposure. SOURCE_FIRST.md remains unchanged to
preserve the error and chronology.

Defective sentence in section B: the R-squared Euler derivative “has zero
linearized response around flat space.” This is false. The derivative terms in
the very formula displayed above that sentence give

    E2_ab^(1) = 2(eta_ab Box - partial_a partial_b) R^(1),

which generally is nonzero and fourth order in a metric perturbation. Only the
algebraic curvature-square terms have vanishing first variation at flat.
Conflating these with the full variational response was the defect.

The corrected claim is: R-squared does not have EH's nondegenerate second-order
full-metric quiet principal response. Its flat linearization is a fourth-order
scalar-curvature response, and it vanishes on the linearized scalar-free sector.
The exact R=0 but Ric!=0 metric witness, homothety weight -2, generic fourth
order and failure of the G301 response-class gates are unchanged.

Smallest repair: replace the defective sentence in any downstream synthesis by
the corrected statement above. Do not cite the uncorrected line as evidence.
Parent was notified immediately by message before any direct candidate review.
