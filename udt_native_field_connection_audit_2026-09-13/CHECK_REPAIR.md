# NFCA1 bounded implementation diagnostic and repair

Initial connection capture exited1 before producing a result file. The trace
identifies the equality helper at the integer-valued pair-rank check: a Python
int difference has no SymPy rewrite method. The first expression had been
evaluated in memory, but no completed check total or saved result is claimed.
Original script, freeze, stdout/stderr and failed capture are preserved.

Finite diagnosis before rerun: distinguish ordinary exact Python integers from
SymPy expression objects in the helper. Normalize the exact difference with
sympify before rewrite; this changes representation only. Check zero and nonzero
integer differences and an unequal-shape comparison as explicit controls, then
run the original frozen witness checks from the separately repaired script.
No parameter, formula, tolerance, source premise or scientific claim changes.
CPU one thread/process180s2048MiB, same work-order stop. If the original matrix
or kernel claims fail, preserve the result and return a scientific objection.
