# Branch-check canonicalization correction

The first invocation of `analyze_background_branches.py` stopped before writing an outcome because
its cubic constraint check used Python structural equality. SymPy returned

```text
-4*(3*A*C - B**2)
```

while the registered expected expression was

```text
4*(B**2 - 3*A*C).
```

Their simplified difference is exactly zero. The check was corrected to test that exact simplified
difference rather than expression-tree identity. No equation, profile, branch, tolerance, or outcome
class changed. The failed pre-solve invocation supplies no scientific result.

The next invocation passed all branch checks but stopped while serializing their results because one
resolved SymPy relational remained a `BooleanTrue` object rather than a Python `bool`. The harness
now converts every already-resolved check to a built-in boolean before JSON serialization. This
second pre-bank failure also changed no equation, profile, branch, tolerance, or outcome and supplies
no scientific result.
