# Independent-verifier correction note

Before banking, the first independent run failed one comparison:

```text
controller torsion count: 4
independent torsion count: 14
```

Cause: the controller iterated over top-level `NDimArray` slices when
counting nonzero entries. The tensor itself and every algebraic identity
were correct.

Correction: count explicit `(c,a,b)` components. The corrected
controller and independent standard-library implementation both return:

```text
14 nonzero torsion components
```

for each preregistered generic causal-sign witness.

No rank, existence condition, counterfamily, interface ruling, or
scientific conclusion changed.
