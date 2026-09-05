# G349 audit report — finite null-wavefront patch area

Date: 2026-09-04
Grade: `PREREGISTERED_LOCALLY_REPAIRED_PENDING_EXTERNAL_FOLLOWUP`

## Finding

Preregistered alternative `A` closes locally with `T1`, `J1`, `M1`, `U1`, `E1`, `C1`, `S1`,
`O1`, `L1`, and `P1`. For any supplied smooth time-oriented four-dimensional Lorentzian metric,
source event, finite timelike source observer, compact celestial patch, smooth regular null family,
positive smooth affine cut, and retained path labels, the G348 infinitesimal density is exactly the
metric two-Jacobian of the finite null wavefront map.

Its integral is the area of all spacelike regular image sheets counted with transverse preimage
multiplicity. The area of the geometric union is a distinct global quantity. Transverse rank-one
and rank-zero points remain in the map with zero local two-Jacobian. Ordinary rank can exceed
transverse screen rank when a variable cut restores a null generator direction; such null sheets
also have zero Lorentzian metric two-area.

## Critical distinctions

- `A_mult = integral_U J_gF dOmega` counts every spacelike regular preimage sheet.
- `A_union = integral 1_(N_s>0) dA_g` counts each spacelike regular image point once.
- `A_mult = A_union` exactly when `N_s` is one almost everywhere; strict injectivity is
  not necessary because isolated crossings carry zero two-area.
- Signed sheet integration requires orientations and can cancel across folds. It is neither of the
  two nonnegative areas above.
- A rank-one point is not automatically a fold; a cusp is an explicit counterexample.
- Ordinary endpoint-map rank two need not mean positive metric area; transverse screen rank two
  is the correct classifier.

## Evidence

- Outcome-unseen preregistration committed and pushed at `84cb5264`.
- Production passed `44321/44321`; largest coordinate-invariant Jacobian error was
  `7.285283487590277e-13`.
- Implementation-distinct verification passed `14321/14321`; largest finite-difference cut error
  was `6.64484023360501e-11`. Rank-zero quadrature error decreased by factors greater than three
  through the registered `16`, `32`, and `64` meshes.
- The first hostile run returned `20/21` because a wording hook did not recognize the cusp claim.
  The failure was recorded before repair. The repaired behavioral cusp guard was committed and
  pushed at `134ecd4a`; it then caught `21/21` mutations.
- The fresh external review returned `ACCEPT_WITH_CAVEATS_G349_FINITE_NULL_PATCH_AREA`. It supplied
  a valid mixed screen-rank-one/ordinary-rank-two null counterexample. Repair R1--R4 was frozen at
  `c2967132` before the scientific documents and scripts changed.
- The repaired production and independent routes each contain a separate mixed-stratum check, and
  the repaired hostile route catches `22/22` mutations.
- Repaired aggregate no-write verification passed `21/21` with byte stability. The fresh full
  repository passed `221` tests with one registered expected failure; the full premise verifier
  passed all `331` rows and `754` historical dispositions. External repair-only follow-up remains
  required before banking.
- Before repair, aggregate no-write verification passed `18/18`; the full repository suite passed `221` tests
  with one registered expected failure, and the 331-row scientific-premise registry plus all 754
  historical dispositions passed after the startup compactness repair at `b0393099`.

## Native/import audit

The geometric construction uses only a supplied metric, its Levi-Civita null geodesics, the G348
metric quotient-screen Jacobian, and the complete supplied finite map. The standard smooth-map area
formula, auxiliary Riemannian measure used inside its proof, quadrature, finite differences, and
root counting are category-A mathematical methods. The auxiliary measure cancels and is not a
physical ingredient.

No optical reciprocity theorem, Maxwell/QED field, radiative stress tensor, emission law, transfer
law, brightness, flux, luminosity, detector, observational distance, field equation, action,
source, matter model, fitted profile, or `X_max` is imported. The theorem is general Lorentzian
geometry and is therefore native to a supplied UDT metric but not uniquely diagnostic of UDT.

## Scope audit

The bounded map domain retains caustics, folds, cusps, repeated sheets, ordinary and transverse
rank strata (including ordinary-rank-two null sheets), optional orientations, finite
source-observer changes, and path labels. It does not select
the supplied metric, source, patch, cut, rays, observers, endpoints, orientations, labels, or any
physical population or weighting.

No light, transfer, distance, history, occupancy, topology, stability, matter/mass, scale,
`X_max`, or canon follows. Repair execution is not external follow-up acceptance.
