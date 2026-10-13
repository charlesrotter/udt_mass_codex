# Exposed mathematics check plan

Parent authorized one short CPU slot after the source-first record was sealed.
Question: does B's exact special-conformal flat-limit construction satisfy its
full metric identity and retain the stated normalized, strictly increasing
inverse conformal factor? Regime: supplied smooth local Lorentz4 patch, positive
v and 1+at, a>0, all choices free-and-explored. No physical law is adopted.

Implementation difference: B differentiates a four-component F, forms its
Jacobian J and checks J.T*eta*J. This reviewer instead proves the pullback via
abstract bilinear invariants of X, a direction Y and the parameter vector b.
The square of dF is expanded as a polynomial in six independent inner products.
Vanishing of that polynomial proves the all-direction metric identity by
polarization, with no finite-point or vector sampling. A second direct
flat-conformal Ricci calculation checks the limiting inverse factor; no author
coordinate-curvature utility, author check or author result JSON is imported.
The shared SymPy library is not implementation/model independence.

Checks: bilinear directional identity, inverse map, normalization, Hessian and
gradient norm of v, all16 flat-conformal Ricci components, actual flat static
null incidence derivative and the distinct endpoint limit. A deliberately wrong
pullback weight and omitted gradient-norm Ricci term must produce nonzero
residuals. These catches concern this check, not empirical truth.

One process, one BLAS/OpenMP thread, 2GiB virtual address limit, existing TPS1
capture.py, unique math/check_01 prefix. Expected seconds, no wall/CPU killing
timeout; manual interruption remains available. Small symbolic output only,
no GPU, installation, production or finite tolerance. Preserve any failure.
Maximum conclusion: exact identities supporting the scoped analytic two-family
argument, not numerical validation of all family members or physical adoption.

Exact command from repository root:

    python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_positional_effect_assignment_2026-10-13/review/math/check_01 python3 udt_positional_effect_assignment_2026-10-13/review/math/check_independent.py
