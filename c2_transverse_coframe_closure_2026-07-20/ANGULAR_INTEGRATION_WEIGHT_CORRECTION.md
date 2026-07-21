# Angular-integration weight correction

The first successful background harness output divided the complete action density by `F(theta)`
before varying the general transverse leg profiles. That operation reproduces the product control,
where `F` is an overall volume factor, but is invalid for nonconstant `b(r),c(r)`.

The exact general density contains independent angular weights proportional to both

```text
F(theta)
```

and

```text
F_first(theta)^2 / F(theta).
```

Consequently there is no unique radial action “per `F`” until the angular domain, cap regularity,
and integration data are supplied. The script is corrected to vary the complete action density.
Its general Euler and endpoint objects are density projections that must be integrated over a
selected angular completion; the package supplies no such selection. Division by `F` is retained
only after imposing the exact product control `b=c=1`, where it is algebraically valid.

This correction changes no metric, witness, tolerance, action premise, or registered outcome. It
prevents an unresolved angular boundary choice from entering the local equations silently. The
uncommitted superseded JSON output supplies no scientific result.
