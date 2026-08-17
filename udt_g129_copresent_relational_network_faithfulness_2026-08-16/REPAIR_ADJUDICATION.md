# G129 adversarial repair adjudication

Date: 2026-08-16

The first fresh adversarial review returned `PASS_BOUNDED`. The second code-level review returned
`PASS_WITH_REPAIRS` and identified three evidence-quality defects. All are implemented:

1. The independent verifier now reconstructs the Ricci tensor from the exact second metric jet at
   the registered event before contracting `Ricci^2=18/25` for `a=3/5`.
2. The all-orders smooth-bump claim is explicitly an analytic proof using
   `u^-n exp(-1/u)->0`; production and independent executables are labelled sampled support/interior
   regressions only.
3. Both production and independent overlap witnesses now perturb one local metric and verify that
   pullback descent fails, preventing the positive witness from serving as a vacuous catch.

The terminal-depth counterexample was also strengthened to retain the same `h00=-1` clock
normalization in both distinct pair metrics.

Fresh production, independent, and isolated package replay pass. The bounded follow-up returned
`FOLLOWUP_PASS` and verified all three repairs plus the strengthened terminal counterexample.
The result remains bounded to regular rank-complete reconstruction and regular overlap descent.
Physical network values, a global solution, and every downstream physical claim remain open.
