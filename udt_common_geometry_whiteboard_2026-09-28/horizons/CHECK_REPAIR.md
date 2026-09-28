# Author check repair

The initial symbolic check failed one of 33 identities: SymPy 1.13.1 retained
`sinh(a*tau)-cosh(a*tau)+exp(-a*tau)` instead of reducing it to zero. The exact
hyperbolic definitions make this identically zero. Initial script, stdout,
stderr and result are preserved in initial_check_run/.

The residual simplifier now rewrites hyperbolic functions as exponentials
before simplification. No metric, equation, physical premise, candidate
formula, acceptance tolerance or check domain changed. The threshold remains
exact symbolic zero. This is an implementation representation repair, not a
failed physical candidate. The rerun is author regression, not independent review.
