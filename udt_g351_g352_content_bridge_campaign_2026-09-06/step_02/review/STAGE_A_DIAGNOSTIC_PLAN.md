# Pre-freeze reviewer checker diagnostic

The first independent child exited 1 at `wrong_v_scaling_detected`, after the
full isometry and correct homothety identities passed. Suspected issue:
structural SymPy equality compares `h*(h-1)` to `h*h-h` without expanding.
Before editing, print the exact expressions, their symbolic difference and the
residual at h=2. Stop after this finite check. If the difference is zero, repair
only the structural assertion by simplifying the difference; preserve original
script/runner/raw stdout/stderr. If the difference is nonzero, retain an actual
algebraic objection. Same 512 MiB / 60-second CPU-child limit; no new physics,
domain, metric, approximation or broader search. Maximum result: implementation
diagnosis, not scientific repair.
