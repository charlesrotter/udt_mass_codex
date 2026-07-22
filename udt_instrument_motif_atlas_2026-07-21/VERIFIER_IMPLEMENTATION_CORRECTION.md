# Independent-Verifier K09 Correction

Date: 2026-07-21

The first frozen independent-verifier run completed its blind computations but stopped because K09
did not reject its mutation. The mutation replaced the registered nonlinear chart with a fully
consistent linear chart having the same pointwise Jacobian. Curvature, Ricci, and the covariant phi
Hessian are tensors, so this different valid chart must reproduce the same pointwise objects. The
zero residual was mathematically correct and the catch was invalid.

The corrected K09 retains the complete nonlinear metric jets and scalar first derivative but omits
only the inhomogeneous scalar second-derivative chain-rule term `dphi_r K^r_ab`. That hybrid is not
the jet of the registered scalar transformation. K09 now measures the resulting covariant-Hessian
discrepancy and requires it to exceed `1e-9` on at least one blind anchor.

No production result, input, motif rule, tolerance, anchor, or conclusion changes. The failed
transcript is preserved in `PRE_OMITTED_JET_CATCH_VERIFICATION_TRANSCRIPT.txt`.
