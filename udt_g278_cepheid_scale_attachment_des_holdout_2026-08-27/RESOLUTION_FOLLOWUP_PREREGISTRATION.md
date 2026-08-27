# G278 resolution follow-up preregistration

Date: 2026-08-27

Status: `OUTCOME_INFORMED_FOLLOWUP_PREREGISTRATION`

## Trigger already observed

The primary G278 calculation and implementation-distinct replay agree that all four Cepheid scale
attachments are individually regular and all four unretuned DES queries pass their declared
adequacy ceilings, but the exact correlated comparison of the first-knot scale coordinate fails the
preregistered resolution-stability gate.

No claim of outcome blindness is made for this follow-up. The original G278 landing cannot be
changed by it.

## Frozen diagnostic question

Does the observed resolution sensitivity primarily affect the boundary-normalized coordinate
`ell=R(phi_min)`, or does it persist in the reconstructed physical absolute-radius curve through
the common support?

## Exact diagnostics fixed before evaluation

For each `K=8,12,16,24`, form

\[
U_K(\phi)=a_K+S_K(\phi)
=5\log_{10}\!\left(\frac{R_K(\phi)}{\mathrm{Mpc}}\right).
\]

Evaluate it on exactly 4,097 uniformly spaced `phi` nodes over the frozen G236 common support. Use
`K=12` only as the registered comparison reference; do not optimize a reference or a pivot.

Record for `K=8,16,24`:

1. maximum and RMS raw magnitude difference `U_K-U_12` over all nodes;
2. maximum and RMS difference on the interior 90 percent of the support, obtained by dropping the
   first and last 5 percent of nodes;
3. the location of the maximum absolute difference;
4. the exact pointwise standard deviation of the difference from the common Pantheon+ covariance;
5. the corresponding maximum absolute standardized difference;
6. the same raw and standardized comparison at the fixed midpoint
   `phi_mid=(phi_min+phi_max)/2`.

Also record consecutive dense-grid RMS differences `(8,12)`, `(12,16)`, and `(16,24)`. No
monotone-convergence claim is preregistered; these are descriptive diagnostics.

## Allowed conclusions

- `BOUNDARY_COORDINATE_SENSITIVITY_DOMINATES` only as a descriptive lead if every interior-90%
  RMS difference is smaller than its corresponding full-support RMS and every maximum lies in one
  of the excluded 5% boundary bands.
- `PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS` otherwise.

Neither landing repairs, replaces, or weakens the original
`SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE` result. The follow-up may only choose the next
numerical representation audit. It may not select a preferred `K`, average scales, add a smoother,
fit a profile, retune DES, or change the metric/kernel.
