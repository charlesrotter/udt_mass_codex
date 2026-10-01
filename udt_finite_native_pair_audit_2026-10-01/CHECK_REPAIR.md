# Parent symbolic check repair before candidate review

The original check_pair.py and pair_initial capture remain fixed. Its final
static-chart assertion compared symbolic 1-kappa*m² to2-p² without substituting
the already declared kappa=(p²-1)/m². It failed with the explicit residual
-kappa*m²+p²-1. This is a missing symbolic substitution, not a mathematical
counterexample or a changed curvature premise. No successful overall check was
claimed for the failed run. check_pair_repaired.py differs only by applying that
substitution in the assertion. The proof and earlier original code stay fixed.

The corrected exact check remains2GiB/no timeout, noGPU, and the same finite
identity scope. Its captured result is checks/pair_repaired. Candidate review
will inspect both editions and the explanation. No source or physical premise
is repaired or imported by this implementation correction.
