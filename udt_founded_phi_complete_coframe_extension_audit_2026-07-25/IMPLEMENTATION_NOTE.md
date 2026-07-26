# Preserved implementation-count correction

The first post-preregistration execution failed only its terminal expected-
check-count assertions. All substantive checks had passed: the production
dictionary contained 27 checks rather than the hand-counted 25, and the
independent dictionary contained 18 rather than the hand-counted 17.

The assertions were corrected to 27 and 18. No formula, test predicate,
premise, expected scientific outcome, or saved source artifact changed. Both
implementations then passed, and the package verifier fixes those totals.
