# G274 preregistration execution note

The first production execution completed every preregistered algebraic assertion but failed while
serializing SymPy `BooleanTrue` objects to JSON. The repair converts already-evaluated symbolic
booleans to Python `bool` immediately before the assertion and serialization gates.

This was a mechanical output-type repair. It changed no formula, alternative, sample, tolerance,
scope, or scientific landing. The repaired production run passed all 26 exact checks.
