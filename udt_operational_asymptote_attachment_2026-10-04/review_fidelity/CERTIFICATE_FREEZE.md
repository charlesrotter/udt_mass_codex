# Exact counterexample-certificate review freeze

After explicit exposure, inspect the new ceiling counterexample and its rational
certificate. Independently recompute each saved rational endpoint w² and verify
q²w²<=1, strict source conditions, subinterval continuity/coverage, and final
positive B lower bound using fractions.Fraction. Reconstruct the sum from saved
certificate rows, without importing parent's generator or integer square-root
implementation. As a catch control, double the first q and require its exact
bound to fail. Two exact certificate cases, conservatively cumulative73 including
all earlier finite attempts. CPU2GiB/one-thread/no timeout. No new float solve.

Analytic hypotheses checked before execution: d(w²)/dr=2b²(r-3m)/(S²r^4)>0
on r>=a>3m; w²>0 at a from strict source bound; w²<1 for r>2m. This makes
right-endpoint q a lower integrand bound, with a strictly positive omitted
tail. S>14/5 and positive J_lower give B>J_lower/H-E/(H²*(14/5)). The test
validates this exact certificate, not physical source/stability/native status.
