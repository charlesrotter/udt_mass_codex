# G68 verification-selection preregistration

Date: 2026-08-11

Parent preregistration commit: `05654f24`

This closes two intentionally unspecified verification subsets before any trajectory is run.

## Independent geodesic-bundle universe

Run the null geodesic-bundle reconstruction on all `21/21` registered profile rows and both initial
screen directions. Use symmetric angular perturbations at `delta=1e-4` and `delta=5e-5`, with

```text
k_delta = u+n*cos(delta)+E_B*sin(delta).
```

Compare the central finite difference at the central geodesic's endpoint affine parameter with the
integrated Jacobi column. Record both delta levels and their convergence. No row may be selected or
dropped after seeing production behavior.

## Mixing-sign reflection universe

For all `18/18` F02 rows, rerun the complete finite-path system with `h -> -h` while retaining the
same positive-coordinate screen convention. Compare against the exact coordinate reflection
`psi -> -psi` with the screen/source conjugation `S=diag(1,-1)`:

```text
D_minus = S D_plus S.
```

Endpoint `t,r,theta` must agree and endpoint `psi` must reverse sign modulo ordinary numerical
tolerance. This is a metric-coordinate reflection check, not an additional physical profile.

All tolerances and allowed conclusions remain those frozen in `PREREGISTRATION.md`.
