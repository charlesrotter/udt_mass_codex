# Reviewer diagnostic frozen before correction rerun

Initial child exited 1 after 0.065 s: Python 3.10 rejects starred-expression
subscript `Rup[e,*k[1:]]`. No mathematical code ran and no formula failed.
Preserve initial code as stage_a_initial_syntax.py, original stdout/stderr and
runner metadata. Correct only tuple indexing to `Rup[(e,)+k[1:]]` and replay
all existing checks under the same 512 MiB/60 s limits.
No changed equation, degree of freedom, domain, omitted sector or tolerance.
This is reviewer pre-seal implementation repair, not an author repair cycle.

The syntax-corrected replay reached the cubic q guard, then failed structural
SymPy `==`. Freeze this code separately as stage_a_structural_equality.py.
Inspect the independently derived rational expression and expected expression,
their difference after cancellation, and a wrong-coefficient control. If and
only if the difference vanishes exactly, replace this equality with explicit
rational cancellation; do not change the formula or expected coefficient.

Diagnostic confirms factored `1/(4*(x**2+y**2))` versus expanded denominator
`1/(4*x**2+4*y**2)`: exact difference zero; doubling the expected coefficient
has nonzero difference. Only that guard's equality normalization was changed.
