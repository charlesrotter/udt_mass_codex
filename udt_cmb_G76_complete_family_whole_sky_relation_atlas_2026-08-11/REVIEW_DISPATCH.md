# Cold adversarial review dispatch — G76 complete-family whole-sky relation atlas

Review only the files listed in `REVIEW_MANIFEST.tsv`. Do not edit the repository or continue the
research. Do not inspect the protected stopped native-on-shell draft.

## Central question

Does G76 correctly and completely classify the sampled whole-sky endpoint relation of all 591 frozen
G75 stationary axial profiles under the supplied G74 query, while keeping the four numerical
exceptions and every ownership limitation honest?

## Required audits

1. Reconstruct the Cartesian metric inverse and variable-`q` Hamiltonian. Check every `q_s` term and
   the initial metric-orthonormal null directions.
2. Audit the independent Christoffel implementation, including metric derivatives, index order,
   initial data, first-crossing interpolation, null residual, the eight-stratum panel, and the
   preserved verifier-development failure.
3. Recompute from the saved TSV/NPZ evidence:
   - 591 unique profiles and 49 shapes;
   - 2,364 mesh trials;
   - 587 resolved orientation-preserving rows and four exact unresolved identities;
   - zero missing/nonfinite rays, negative faces, negative intrinsic maps, and near-`1e-2` areas;
   - degree, area, singular-value, shear, Hamiltonian, reflection, and G74 replay extrema.
4. Determine whether the signed-area and intrinsic tangent-map code legitimately supports the
   sampled orientation/fold statements. Look for mesh-ordering, spherical-log, interpolation,
   branch, or local-Jacobian false positives.
5. Challenge the classification of the four exceptions. They may not be promoted, removed, or
   called geometric failures solely because their frozen time-refinement threshold fails.
6. Audit type and ownership. In particular, do not allow the endpoint tangent map to become
   polarization transport; do not select a profile, source, endpoint, `R`, `X_max`, action, matter,
   bootstrap state, or CMB spectrum.
7. Run the supplied scripts where useful and independently test at least one load-bearing claim by a
   method that does not merely compare a file with itself.

## Required landing

Return one primary grade:

- `VERIFIED_WITH_CAVEATS`;
- `INTERNALLY_VERIFIED_LEAD_ONLY`;
- `NUMERICALLY_UNRESOLVED_FAMILY`;
- `TYPE_OR_IMPLEMENTATION_FAILURE`; or
- a more precise explicitly defined grade.

State the strongest allowed conclusion, every repair required before banking, and the smallest
justified next calculation. Do not derive source physics or fit CMB observations.
