# External review adjudication

Date: 2026-08-16
Review landing: `DERIVATION_VALID_CONDITIONALLY__TYPE_TIE_EXPLICIT`
Current status: `REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS`

## Accepted result

The reviewer independently re-derived the determinant/Gram identity, logarithmic area rate,
Jacobi/Riccati and depth-reparameterization equations, and the constant-family reduction. It found
no factor, sign, unit, or numerical defect on the declared regular stratum.

The strongest accepted statement is conditional: when a supplied query identifies the complete
pair-screen block `W=Q(SY+Z)` with the physical Jacobi screen map, its effective reciprocal-depth
screen-volume rate is derived. The metric history, query, branch, initial data, and depth map remain
supplied rather than selected.

## Accepted repairs

1. The original sealed intake omitted `build_review_intake.py` even though the package verifier
   required it. The builder now includes itself, so the corrected scope makes the required-file
   claim auditable.
2. The audit and landing language now state explicitly that `Q(SY+Z)` becomes the Jacobi map only
   when the supplied query makes that identification.
3. The exact derivation now states the full-family criterion
   `K=W_,delta W^-1=aI+b epsilon` in an oriented orthonormal screen frame. Constant determinant rate
   alone recovers only the scalar character, not the complete G107 matrix family.

These are evidence/type-precision repairs. They do not alter the bounded mathematical conclusion.

## Frozen-preregistration clarification

The preregistered falsification ledger is preserved unchanged. Its phrase “constant G107 a occurs
iff propagated log-area is affine” is now read as the determinant-character condition. Recovery of
the full matrix family additionally requires the no-shear/constant-rotation criterion above.

## Follow-up result

The corrected 31-file sealed intake was reviewed in a fresh read-only context restricted to the
registered repairs and original bounded landing. It returned
`REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS` and reported no remaining defect. The accepted
conditional result and all ownership boundaries therefore stand unchanged.
