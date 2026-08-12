# G81 independent-method registration

This method layer was fixed after the production outcome but before any independent neighboring-ray
outcome was computed. It cannot alter the preregistered two-control universe or conclusion ceiling.

- Rebuild the supplied G79 metric and its first coordinate derivatives locally.
- Assemble the full Christoffel tensor directly; import no production Riemann or Jacobi equation.
- Integrate central and neighboring null geodesics with SciPy DOP853, `rtol=2e-12`, `atol=2e-14`,
  and `max_step=1/800`.
- Use centered angular perturbations `1e-4` and `5e-5` radians for both screen columns.
- Evaluate neighboring endpoints at the central ray's fixed affine endpoint.
- For the rotated test, seed the reverse neighboring rays in `A E_source` and project at the
  receiver on `B E_receiver`.
- Require each independent production-map and covariance residual to be below the preregistered
  `2e-4` relative tolerance. No method parameter may be changed after inspection.

Maximum conclusion remains the preregistered control-scoped covariance statement.
