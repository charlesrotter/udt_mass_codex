# Author-check repair before candidate freeze

author_01 exited 1 at the embedded-surface Gauss check. The returned discrepancy
was `(sinh(2t)tanh(t)-cosh(2t)+1)/(2cosh(t)^2)`. Hand reduction gives zero:
sinh(2t)tanh(t)=2sinh(t)^2 and cosh(2t)-1=2sinh(t)^2. The original script
and full failure output remain in initial_check/ and checks/author_01.*.

Finite diagnostic: exact exponential rewriting for remaining hyperbolic/trig
expressions, then algebraic simplification; no numerical tolerance, field
equation change, branch restriction or physical repair. Keep nonzero wrong-
formula rejection tests, so rewriting must not turn all expressions into passes.
Rerun the full bounded author script once. If a genuine discrepancy remains,
retain and diagnose it rather than suppress the assertion. This is a symbolic
normal-form issue, not an observational mismatch or a new mechanism.
