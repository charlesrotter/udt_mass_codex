# Exact-check implementation repair

The first run ticks.json exited1 at the density-Jacobian assertion. SymPy's
plain simplify left (2*x+1)/sqrt(4*x*x+4*x+1) unevaluated despite x>=0. The
identity is valid: radicand=(2*x+1)^2 and2*x+1>0. Repaired code checks this
factorization separately and evaluates the same Jacobian using the positive
branch. No expected scientific value or tolerance changes.

Code inspection also found that the later atom-count sum would add SymPy
Boolean objects. The repaired copy converts each exact finite comparison to a
Python bool/integer before summing. That prospective type problem was not the
observed first failure and is not claimed as a second executed failure.

Original code, candidate, plan, freeze and failed receipt/stdout/stderr remain
unchanged. This is an implementation repair, not a new physical assumption or
candidate mathematics revision. The repaired exact run uses the same limits.
