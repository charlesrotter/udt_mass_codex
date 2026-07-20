# Full metric-path Bach projection correction

The second independent-verifier invocation correctly reproduced the finite-value density behavior
but still failed because it compared the action Jacobi operator to the isolated covariant
linearized `B_xy` component. That comparison is incomplete on an off-shell background.

The coframe path has both

```text
g_xy = epsilon*u,
g_xx = 1 + epsilon^2*u^2.
```

For a non-Bach-flat background, a coordinate shear generates a nonzero component `B_xy` simply by
transforming the nonzero background Bach tensor. The action Hessian along the full metric path also
contains the background Euler contribution from the quadratic `g_xx` backreaction. In raised-index
form the required local combination is

```text
(d/d epsilon B^xy)|_0 + u*B^xx|_0.
```

At the diagnostic constant-`u` witness the two terms were

```text
0.03962458951729691
and
-0.03962458951729693,
```

canceling to float64 backward error. At a nonconstant witness, the action Jacobi divided by the
complete projected combination was `-7.999999999999986`, exposing the fixed action/Bach convention
normalization.

The verifier was corrected before banking to raise the Bach tensor, include the registered
quadratic metric backreaction, freeze the first nonzero ratio, and test that ratio at every other
point. The primary metric, action, profiles, outcomes, and tolerances remain unchanged. The second
failed invocation supplies no scientific result.
