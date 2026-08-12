# G80 exact derivation — reverse ordered-pair reciprocity on the G79 control

Date: 2026-08-11

Status before fresh external review:
`PROVISIONAL_INTERNALLY_VERIFIED__FRESH_ADVERSARIAL_REVIEW_REQUIRED`

## 1. The correctly typed reversal

G79 supplies one complete null branch from the receiver control at `x=1/4` to the source control at
`x=1`, normalized to unit receiver frequency. Let its tangent at the source be `k_s`, and let

```text
Z = 1+z = omega_s/omega_r = sqrt(21)/4.
```

The reverse of that **same affine curve** is not obtained by changing only the radial component.
It is

```text
k_rev = -k_s/Z.
```

The minus sign reverses the whole affine tangent. Division by `Z` gives unit source-frequency
magnitude. The resulting branch is past-directed in the original time orientation; it is a
mathematical ordered-pair reversal, not a future material signal.

## 2. Endpoint depth reverses exactly

The stationary Killing energy is conserved. The reversed source frequency has signed value `-1`,
while its receiver value is `-1/Z`. Therefore the magnitudes obey

```text
Z_rev = omega_r^(rev)/omega_s^(rev) = 1/Z = 4/sqrt(21),
phi_rev = log Z_rev = -log Z = -phi_forward.
```

The numerical replay gives

```text
Z                         = 1.1456439237389628
Z_rev                     = 0.8728715609439718
|Z Z_rev - 1|             = 5.10702591327572e-15
|phi_forward+phi_reverse| = 5.051514762044462e-15.
```

## 3. Complete screen-map reciprocity

The screen Jacobi equation is a self-adjoint second-order system because its optical tidal matrix
is symmetric. The conserved matrix Wronskian relates the two endpoint-normalized fundamental
solutions. With the parallel screen at the G79 source used as the initial reverse screen, the
unscaled reversed solution is the transpose of the forward map. Source-frequency normalization
rescales the reverse affine parameter and Jacobi map by `Z`. Hence

```text
D_reverse = Z transpose(D_forward).
```

Consequently,

```text
d_A_reverse/R = Z (d_A_forward/R).
```

At the `4096` control,

```text
D_forward = [[0.7559967070430084, -1.0146339127533358e-22],
             [-1.0146395760930269e-22, 0.7559733363044177]]

D_reverse = [[0.8661030337904897, -1.1624156651358940e-22],
             [-1.1624091769652467e-22, 0.8660762592458356]]

d_A_forward/R = 0.7559850215834019
d_A_reverse/R = 0.8660896464146981
```

The full-matrix reciprocity residual is `6.885259158085081e-15`; the area-ratio residual is
`6.661338147750939e-15`. The reverse curve returns to the original event, tangent, and screen at
roughly `1e-15` relative/absolute scale. All `1024/2048/4096` controls agree without retuning.

## 4. Independent equation route

`verify_reverse_pair_independent.py` rebuilds the metric Christoffels directly and uses finite
differences of neighboring null rays in both directions. It imports neither the production Riemann
tensor nor its Jacobi equation. The independent results are

```text
forward vs production D          = 4.381542485329791e-11 relative
reverse vs production D          = 1.4161064164681488e-08 relative
independent reciprocity residual = 1.4204869936356233e-08 relative
independent area-ratio residual  = 1.627372281376438e-08
maximum null residual            = 3.321158061195084e-14.
```

This satisfies the preregistered `2e-4` independent gate. It remains method-independent only in
the bounded G79 sense: the metric, query, screen endpoints, and DOP853 family are shared.

## 5. Exact landing

```text
DERIVED_CONDITIONAL_RECIPROCITY_ON_ONE_FROZEN_GEOMETRY_AND_ONE_ORDERED_PAIR
```

This closes the orientation/normalization consistency of the one G79 control. It does not select a
physical profile, endpoint, `R`, `X_max`, source state, SNe fit, luminosity law, `cmb_temp`, CMB
spectrum, action, matter source, bootstrap rule, or signalling law.
