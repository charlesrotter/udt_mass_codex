# Independent-verification profile registration

This registration is committed after the exact primary symbolic derivation but before the separate
Torch coordinate-tensor and direct Bach implementation is run. These profiles are verification
witnesses only and cannot change the frozen outcome classes.

All coefficients are exact rationals in the definitions; float64 evaluation is category-A.

## Profiles

Profile A:

```text
p(r) = r/3 + r^2/5 - r^3/7
u(r) = 2r/5 - r^2/4 + r^3/6 + r^4/9
points = [-1/3, 1/5, 2/3]
```

Profile B:

```text
p(r) = -r/4 + 2r^2/7 + r^4/13
u(r) = 1/7 + r/2 - r^3/5 + r^5/11
points = [-2/5, 1/7, 3/5]
```

Control profiles:

```text
flat-p: p(r)=1/6, u(r)=r^2/3+r^4/8, points=[-1/2,1/4]
constant-u: p(r)=r/3+r^2/5, u(r)=2/7, points=[-1/3,1/3]
```

## Frozen comparisons

1. Independently constructed `0.5*d^2/d epsilon^2 [sqrt(-g) C2]` versus the primary quadratic
   density: relative tolerance `1e-8`, absolute floor `1e-10`.
2. Direct linearized Bach `xy` component versus the action-derived Jacobi operator, allowing only
   the single convention/variation normalization derived once from the first nonzero witness and
   then frozen for every remaining point: relative spread `1e-7`.
3. The constant-`u` density coefficient, Jacobi operator, and linearized Bach component must all be
   at most `1e-9` in absolute value.
4. Reversing `u` must preserve the quadratic density and reverse the Jacobi/Bach linear response.
5. A metric constructor omitting the `epsilon^2 u^2` term in `g_xx` must fail at least one registered
   density comparison by more than `1e-6` relative/absolute combined tolerance.
6. Euclidean time substitution must fail at least one registered Lorentzian comparison by more than
   `1e-6` unless the exact coefficient is signature-independent; if it is exactly independent, that
   fact must be reported rather than forcing a catch.

No point or profile will be removed for small values, sign changes, disagreement, or an unattractive
result.
