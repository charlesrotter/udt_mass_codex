# Fixed-history arrival-derivative check freeze

After the numerical discoveries recorded in EXPOSURE_AND_NEXT_PROBE, check the
observable definition independently of endpoint frequency contraction. This is
an independent numerical arrangement using the same preparation and library,
not a second metric integrator or independent analytic proof.

For vacuum at L=.06 and epsilon=-1e-5 at L=.04, use directions
mu=.13,.57,.91. Hold each prepared A and B worldline fixed, vary emission
coordinate time around A(t=1) or B(t=T), and re-solve both full spatial incidence
equations. Convert reception and emission increments using the actual proper
time factors N for A and N/gamma for B. Use a symmetric fourth-order derivative
at steps h=2e-4 and1e-4. Compare the resulting actual arrival derivative with the
endpoint-frequency ratio. Require absolute mismatch<2e-8 and save both step
results and original incidence residuals. This tolerance checks implementation
and derivative semantics, not the tiny angular mean's absolute error.

Repeat both negative conformal grids with baseline angular/time/ODE controls.
Compare against their saved fine results before reporting finite signs. Numerical
sign separation keeps the original50-times-refinement rule and is not a certified
interval bound. No grid or tolerance is chosen to force a mean sign.
