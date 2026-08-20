# G194 implementation repair note

Date: 2026-08-20

The first hostile-catch run completed the symbolic catch calculations but failed while serializing
the result because one SymPy `BooleanTrue` object was not JSON serializable.  The repair converted
the already computed catch values to Python booleans only at the JSON boundary.  No formula,
mutation, tolerance, profile, outcome class, or scientific assertion changed.  The rerun passed
22 of 22 preregistered catches.
