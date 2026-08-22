# G215 preregistration execution note

The first independent replay stopped before producing a result because its random witness generator
required every pair of different raw ruler inputs to yield different completed metrics. That
requirement is false: density normalization can make different auxiliary descriptions represent
the same completed tuple.

The witness generator was repaired to force the invariant ratio `beta/L_sigma` to differ. No
production equation, theorem statement, tolerance, source, or conclusion was changed. The complete
independent replay was then restarted and passed 10,000 cases with 190,000 exact assertions.

This is a verifier witness-design repair caught before outcome banking, not a theorem repair.
