# Finite pre-freeze parser diagnostic

The first baseline exited1 at19:39:02 UTC when SymPy converted the witness
string `1+lambda^2` into Python syntax. `lambda` is a Python keyword.
Earlier constant weights were executed, but no whole-baseline success is claimed.
Original script and exact stdout/stderr/exit are retained beside this note.

Relevant omitted sector: none; this occurs before evaluating that witness.
Numerical error: none (exact algebra). Frozen degree of freedom: none changed.
Coverage issue: the intended nonconstant witness must execute, not be discarded.
Finite diagnostic budget: one notation-only parser change and one60-second
baseline replay; if it fails again, preserve that outcome before further work.
Change only the parsing alias lambda->ell, mapping ell back to the same real
SymPy coordinate. Keep the saved mathematical witness, equations, assertions,
both nonzero alternatives and zero control unchanged. Maximum disposition:
implementation syntax defect, not scientific incompatibility or new physics.
