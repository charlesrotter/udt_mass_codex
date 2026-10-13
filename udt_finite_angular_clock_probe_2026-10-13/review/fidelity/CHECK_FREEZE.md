# Fidelity direct-check freeze

Question: do the frozen directional polynomials integrate to the claimed exact
spherical coefficients, do source-qualified Kerr exterior parameters give the
claimed sign, and do raw saved endpoint records independently reproduce B's
reported actual-clock means? This is arithmetic/artifact checking plus source
review, not independent symbolic derivation of the directional polynomials,
a new Kerr ray integration, or certified numerical enclosures.

Exposure: A/B candidates and author plane-wave and Kerr check implementations
have been read, as has B's analyze_saved.py. No author module will be imported
or rerun. The reviewer code uses standard-library Fraction/math and the saved
JSON only. Sibling mathematical review files/verdicts remain unread. Exact
primary references for normal-coordinate jets and Kerr have been browsed.

Test controls fixed before execution: exact rational equality of Kasner sphere
means to 4/1215, plane-wave means to 1/720, and resulting invariant coefficients
to 1/90 and -1/120; exact Kerr exterior/ergosphere arithmetic and negative sign;
independent endpoint-frequency reconstruction from each saved angular record,
maximum directional log discrepancy <=5e-14; weight sum error <=1e-14; independent
weighted-mean versus stored-mean discrepancy <=1e-14. These are consistency
tolerances, not error bounds on the true physical mean. Print actual errors and
means rather than treating passing as a precision certificate. A negative
deformation's separated forward/reverse signs are explicitly retained.

Resources: one CPU process, standard-library float64 and exact rational
arithmetic, 2GiB virtual memory, one thread, no killing wall/CPU timeout, expected
under ten seconds. Coordinator approved the available CPU slot before this
freeze. Use TPS1 capture with unique prefix `checks/direct_01`; preserve failure
if any. Output under 1MiB. No scientific hypothesis, empirical threshold, metric
selection or physical positivity law is adopted.
