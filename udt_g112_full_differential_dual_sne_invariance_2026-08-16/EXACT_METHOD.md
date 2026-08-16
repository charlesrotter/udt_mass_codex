# G112 exact method

## Type correction under test

G110/G111 replaces a false identification of two `2x2` objects with one observer exponential whose
full differential contains distinct pair and sky blocks. The SNe replay therefore keeps

```text
Phi=log(1+z)
```

in the pair block and represents the already registered SNe-visible area by the separate screen
map

```text
D_sky=lambda_A I2,
lambda_A=n[1-(1+z)^(-2/n)].
```

This isotropic map is a conditional representative. It is not the unique screen history selected
by G110/G111.

The inherited conditional luminosity transfer gives

```text
dL=sqrt(det D_sky) exp(2 Phi)
  =n(1+z)^2[1-(1+z)^(-2/n)].
```

Thus the retyped and legacy P1 predictions are algebraically identical while their internal object
types are no longer conflated.

## Likelihoods

For either survey, with observed magnitude vector `m`, model vector `f`, covariance `C`, and one
additive calibration `B`,

```text
B* = [1^T C^-1(m-f)]/[1^T C^-1 1],
chi2 = (m-f-B*1)^T C^-1(m-f-B*1).
```

`n` is held bit-identical to G99. Production uses covariance-domain Cholesky whitening. The
independent route uses precision-domain profiling; for DES it constructs the marginal precision
by the Schur complement. No shape optimizer runs.

## Scope

The screen representative and flux rule are conditional interfaces. Numerical invariance can show
that the G110/G111 type correction did not make the frozen P1 anchor inconsistent. It cannot show
that P1 or this screen map is the physical complete metric history.
