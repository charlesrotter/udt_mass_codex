# G68 epsilon-limit preregistration

Date: 2026-08-11

Parent verification-selection commit: `76938822`

Before any trajectory inspection, freeze the numerical `epsilon -> 0` checks required by the main
preregistration. For every one of the `3` lapse profiles and `3` nonzero mixing shapes, integrate
two auxiliary controls at

```text
epsilon = 1e-2 and 5e-3.
```

Compare each endpoint Jacobi map with the matched zero-mixing F01 map. Record both errors and their
ratio. Require the smaller-amplitude error not to increase, except when both errors are below
`1e-10` absolute and therefore numerically indistinguishable. The local quadratic result may be
used as a comparison, but no finite-path convergence exponent is imposed or fitted.

These `18` auxiliary runs are limit checks, not additional profile-atlas rows or candidate physical
profiles. All other rules and maximum conclusions remain unchanged.
