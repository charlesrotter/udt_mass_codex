# Presolve self-check correction

The first post-implementation invocation stopped before writing a result because the
`no_undifferentiated_u` check used SymPy's structural `quadratic.has(u)`. That query is true even
when `u(r)` appears only inside `Derivative(u(r),r)`, so it was not the registered physical test.

Before an official result was banked, the check was corrected to the exact partial derivative of
the jet expression with respect to undifferentiated `u(r)`. The diagnostic reconstruction gave

```text
diff(quadratic_density, u(r)) = 0
quadratic_density[u(r)+constant] - quadratic_density[u(r)] = 0.
```

No metric, action, expansion, tolerance, profile, or outcome class changed. The failed invocation
is a harness correction layer and supplies no scientific result.
