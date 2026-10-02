# Direct review plan, after source-first seal

Exposed after SOURCE_FIRST_SEAL: frozen parent INITIAL_DERIVATION,
NUMERICAL_PLAN, check_candidates.py, output freeze metadata and parent_full summary.
No peer review read. Parent uses DOP853, dense-output eta inversion and nine-point
H differences; direct review will not import or call any parent function.

1. Verify every file in the parent candidate/output freeze by SHA-256, restricted
   to this authorized package. Correspondence does not certify science.
2. Reconstruct all 8 tight runs at saved grid32/64/128 from scale factor samples
   only. CubicSpline interpolates the scale factor; 16-node Gauss quadrature per
   cell integrates its reciprocal. Bracket actual arrivals in that cumulative
   integral and solve only inside the located saved cell. Parent eta is not used.
   Compare 24 first arrivals, echoes and endpoint ratios at finest grid to the
   parent's declared 1e-7 absolute+relative tolerance; retain all coarse errors.
3. Test finite proper emission interval delta=0.01 by arrival differences and
   integrate the instantaneous map slope independently over that interval.
   At emission0.5, a centered derivative with delta=1e-5 checks that both first
   and echo map derivatives equal the corresponding endpoint scale-factor ratios.
4. Reconstruct original E from saved scale factor using independent eleven-point
   derivatives through order4, avoiding parent H/R/P and RHS. This is a different
   metric-variable/stencil reconstruction, still float64 finite differences;
   check the parent1e-7 normalized residual threshold on the finest grid.
   Boundary-trimmed coverage is disclosed. Scalar residual zeros alone are not
   enough. Retain coarse residuals and roundoff behavior without inventing a
   new global error theorem.
5. Independently verify flat-event cubic Taylor coefficients by symbolic ODE
   differentiation, including the vanishing quartic term and fifth-order term.
   Report errors of the saved decreasing-distance p/q values against cubic terms.
   Verify actual contracting p,q<1 and stationary p q=1, without sign-based
   validity filtering. The extra finite interval queries do not add evolution
   cases or a third response candidate.

Resources: short CPU, 2GiB address space, one BLAS thread, existing TPS1 capture,
no elapsed/CPU timeout or GPU. If reconstruction fails, preserve it as a review
diagnostic and report whether representation/roundoff or candidate defect is known.
No change to parent candidate, original outputs, science, or thresholds authorized
by this plan. This is same-library/different-implementation review, not independent
general-data evolution, interval certification or physical-response admission.
