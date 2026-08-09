# FD2 Phase-I refinement preregistration — continuum variational response

Date: 2026-08-09  
Registered after preserving the finite-element response failure and before inspecting any TT/SNe
inversion outcome.

## Why the method changes

The low-order FEM accurately certifies frequencies but not derivatives with respect to narrow
profile motifs. The pure correction is to compute the derivative of the continuum Sturm–Liouville
problem directly, not to weaken the failed threshold or select only favorable FEM rows.

For `m=0`, the exact radial equation is

```text
-(p R')' = lambda w R,
p = sqrt(A D),  w = r^2/p,  D = A r^2 + h^2,  lambda=omega^2.
```

For `A_c=A exp(cB)` at `c=0`, define

```text
L_B = (B/2) [1 + A r^2/D].
```

The fixed-endpoint variational derivative is

```text
d lambda/dc =
  integral [p L_B (R')^2 + lambda w L_B R^2] dr
  / integral w R^2 dr,
d omega/dc = (d lambda/dc)/(2 omega).
```

This is derived from the same metric operator and does not linearize the background equation; it
linearizes only the explicitly declared profile inversion at `c=0`.

## Independent continuum realization

Solve the baseline equation by flux shooting with `F=pR'` in `y=-log(1-r)`:

```text
dR/dy = (1-r) F/p,
dF/dy = -(1-r) lambda w R.
```

Use center-regular Bessel-series initial data, DOP853 with `rtol=1e-11`, `atol=1e-13`, and bracket
each root from the frozen FD1 mode sequence. Propagate the registered asymptotic tail analytically;
the profile motifs vanish before that tail. Evaluate the variational integrals on independently
refined `y` meshes and include the analytic tail in the normalization.

Certification gates, frozen here:

- all 28 baseline roots (four backgrounds x seven modes) found, positive, and ordered;
- maximum shooting boundary residual `<1e-8`;
- maximum relative drift from FD1 grid-240 frequencies `<1%`;
- compute every one of the same 320 registered motif rows—no row removed;
- response vectors agree to 2% between 8,001- and 16,001-point quadratures, using the same relative
  norm convention; a response norm below `1e-10` is reported as numerically zero and compared by
  absolute norm `<1e-10`;
- a direct nonlinear central difference at `c=+/-0.01` independently checks 16 fixed rows: for each
  background, the first BUMP and first DIPOLE in lexicographic motif order plus the last BUMP and
  last DIPOLE. Maximum relative response disagreement `<2%` where the variational response norm is
  above `1e-8`; otherwise absolute disagreement `<1e-8`.

The old FEM response atlases remain failed evidence. If the continuum gates pass, the continuum
surface—not the FEM derivative—is frozen before Phase II. If they fail, FD2 stops as numerically
open. The profile census, Phase-II plan, premise ledger, and maximum conclusion do not change.
