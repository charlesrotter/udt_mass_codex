# G168 execution note

The first production run stopped at `pair_gram_determinant` because the test used direct SymPy
structural equality on two algebraically equal rational expressions. The assertion was repaired to
test whether their simplified difference is zero. No scientific expression, input, premise,
landing, or tolerance changed. The independent standard-library Fraction replay had already passed
all 6,012 checks on that first attempt.

The first administrative package-verifier run then looked for the prose phrase `fresh external
review`, while the audit uses the exact machine grade `FRESH_EXTERNAL_REVIEW_OPEN`. The gate was
repaired to test the registered grade. No scientific evidence or conclusion changed.

After the external-review regrade, the first repair verifier looked for one scope-ceiling sentence
as a contiguous string even though the repaired prose wraps it across a line. The gate was changed
to require both substantive clauses separately: physical germ ownership is not derived, and the
event-pairing rule remains outside the conclusion. No scientific content changed.
