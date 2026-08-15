# Exact derivation and typing of the frozen middle-regime calibration

## 1. What was calibrated

Let `Z=1+z`. G65 conditionally identifies the supplied-pair terminal coordinate as

```text
phi_pair = log Z,
c_eff^(pair)/c_E = exp(-2 phi_pair) = Z^(-2).
```

Pantheon+ does not directly return a complete coframe or pair immersion. Under the frozen SNe
readout, it constrains the effective luminosity relation

```text
dL_cal(z) = n X_eff Z^2 [1-Z^(-2/n)].
```

The historical factorization

```text
r_cal = n X_eff [1-Z^(-2/n)],
d_A = r_cal,
d_L = Z^2 d_A
```

is conditional. The same SNe magnitudes cannot independently determine the screen area, source
transfer, and radial factor. In G94 notation, the displayed `Z^2` relation is compatible with
`eta*epsilon=1/Z`; G99 does not derive that product.

## 2. Frozen central relation

G99 does not refit the data. It adopts the already externally verified G65 fields:

```text
inv_n = 0.9470295666076658
n = 1.0559332414320268
X_eff = 2085.9586748597476 Mpc
R_w = n X_eff = 2202.6331050379085 Mpc  [joint best point only]
chi2/dof = 1260.8480887040496 / 1365
```

The absolute scale carries the external `M_B=-19.253 +/- 0.027` premise. The primary shape is
anchor-free; `X_eff` is not.

## 3. Exact shape properties

For positive `n`, positive `X_eff`, and `Z=1+z>0`,

```text
r_cal(z)=n X_eff [1-Z^(-2/n)].
```

At coincidence,

```text
r_cal(0)=0,
dL_cal(0)=0.
```

The radial slope is

```text
dr_cal/dz = 2 X_eff Z^(-1-2/n),
```

so

```text
dr_cal/dz at z=0 = 2 X_eff > 0.
```

The luminosity derivative can be written as a sum of positive terms for `z>0`:

```text
d(dL_cal)/dz
 = n X_eff [2 Z (1-Z^(-2/n)) + (2/n) Z^(1-2/n)] > 0.
```

Thus the frozen central curve is positive and strictly increasing over the registered SNe domain.
This is a property of the chosen P1 calibration, not a native selection theorem.

## 4. What the numbers do not identify

The same terminal `dL_cal` can be produced by many complete `E,J` histories. G98's exact
factorization remains load-bearing: supplied regular `E` and target pair coframe `V_*` admit
`J=E^-1 V_*`. Therefore G99 fixes one observed terminal chord; it does not assign the contribution
of `B,Q,S,Y,Z` or select a time-live continuation.

The banked result also lacks the full joint covariance of `(n,X_eff)`. Separate profile intervals
are retained, but they cannot be treated as independent rectangle bounds. No marginal `R_w`
interval or rigorous joint calibration band is claimed.

## 5. Domain boundary

The frozen primary sample contains 1,367 noncalibrators with

```text
0.02307 <= zCMB <= 2.2613
```

after the historical `zCMB>0.023` cut. The algebra is defined outside that interval, but empirical
calibration is not. In particular, the upper SNe redshift is not an `X_max`, wall, seam, CMB
endpoint, or global universe scale.

## 6. Maximum result

```text
OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN.
```

This is an explicit observational premise for forward development. It is not a metric derivation
of the physical history, transfer law, or cross-regime continuation.
