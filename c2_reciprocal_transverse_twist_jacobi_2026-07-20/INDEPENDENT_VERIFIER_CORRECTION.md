# Independent-verifier differentiation correction

The first independent-verifier invocation failed the exact constant-twist coordinate zero mode and
the density comparison. Direct evaluation at finite `epsilon` showed the scalar curvature,
Weyl-squared density, and determinant were in fact invariant to machine precision for the constant
shear. The false derivative came from nesting forward-mode `jacfwd` with respect to `epsilon`
through the already nested radial connection/curvature derivative graph; cancellation that was exact
in function values produced a spurious second parameter derivative.

Before banking any verdict, parameter differentiation was changed to a frozen symmetric Richardson
calculation with initial step `2e-3`:

- the even quadratic coefficient uses `(f(h)+f(-h)-2f(0))/(2h^2)` at `h` and `h/2`;
- the odd linearized Bach coefficient uses `(B(h)-B(-h))/(2h)` at `h` and `h/2`;
- the two estimates are combined as `(4*fine-coarse)/3`.

Radial derivatives inside the coordinate connection, curvature, Weyl divergence, and Bach tensor
remain forward automatic differentiation. The registered profiles, points, metric, action,
outcomes, and comparison tolerances are unchanged. The failed invocation supplies no scientific
result.
