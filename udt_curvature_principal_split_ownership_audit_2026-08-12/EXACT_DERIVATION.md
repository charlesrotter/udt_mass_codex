# Exact and numerical derivation notes

## Analytic spherical anchor

For

```text
g = diag(-f c_E^2, f^-1, r^2, r^2 sin^2 theta),
f = exp(-2 phi),
```

direct Cartan/coordinate curvature gives

```text
R = -(r^2 f'' + 4 r f' + 2 f - 2)/r^2.
```

In the static orthonormal frame the magnetic Weyl part is zero, and the electric part is

```text
diag(w, -w/2, -w/2),
w = (r^2 f'' - 2 r f' + 2 f - 2)/(6 r^2).
```

The self-dual Weyl operator therefore has one simple and one repeated eigenvalue when `w != 0`:
Petrov D, with the simple principal bivector defining the temporal-radial plane and its angular
orthogonal complement. When `w=0`, Euler's equation integrates locally to

```text
f = 1 + a r + b r^2,
```

and the Weyl operator is zero: Petrov O.

The mixed Ricci endomorphism has repeated pair and screen eigenvalues

```text
rho_pair   = -(r f'' + 2 f')/(2r),
rho_screen = -(r f' + f - 1)/r^2,
```

with gap

```text
rho_pair-rho_screen = -(r^2 f'' - 2 f + 2)/(2r^2).
```

Substitution of `f=1+a r+b r^2` gives `a/r`. Thus Weyl and Ricci degeneracies are distinct gates.

## Production route

`derive_curvature_split_atlas.py` reconstructs each complete G63/G85 metric from its source-owned
coframe or constructive witness. Torch automatic differentiation supplies first and second metric
derivatives. The script constructs Christoffels, Riemann, Ricci, scalar curvature, and Weyl in the
coordinate frame, transforms to the registered orthonormal frame, and builds the full complex
self-dual Weyl bivector operator.

The Petrov classifier uses eigenvalue multiplicity plus matrix-rank/Jordan or nilpotency tests. The
discriminant is diagnostic only. Registered-split recovery is tested directly by the self-dual
pair-bivector residual and its recovered projector. Ricci ownership separately requires block
invariance and a pair/screen spectral gap.

## Independent route

`verify_curvature_split_independent.py` is separately coded in NumPy. It uses fourth-order centered
finite differences for metric and connection derivatives on the frozen ladder

```text
8e-4, 4e-4, 2e-4.
```

The middle ladder value is compared with production. All 1,806 provenance rows agree in Petrov and
owner class, representing 1,221 unique local metric jets. The outer-ladder convergence defects are
below `2.7e-8` for Weyl and `2.0e-8` for Ricci.

## Scope boundary

This is a second-jet, pointwise-curvature result. It does not classify global eigenbundle
continuation, crossings, curvature derivatives, nonlocal holonomy, field equations, or the physical
subset of supplied metrics. A failure of pointwise curvature ownership is therefore not a proof
that no metric-native split owner exists at a higher differential or global level.

