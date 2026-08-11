# G69 exact derivation — profile, endpoint, and source identifiability

## Status

- screen-map reconstruction from each supplied saved metric/query state: `DERIVED`;
- three-channel finite-tile sensitivity rank: `OBSERVED`, coarse and control-scoped;
- unrestricted positive-definite source-covariance degeneracy: `DERIVED`;
- physical profile, endpoint, source/state, and observational coefficients: `OPEN`.

## 1. Saved complete-state readout

G68 stores the complete coordinate state along each already solved observer-sky path. At any
intermediate radius, the transported screen vectors `E_A`, Jacobi vectors `J_B`, and complete
metric give

```text
D_AB = E_A^mu g_mu_nu J_B^nu.
```

G69 reconstructs this object at fifteen declared surfaces `x=r/R=0.30,...,1.00`. No geodesic,
screen, or Jacobi equation is reintegrated. The production PCHIP and independent cubic-spline
reconstructions use different interpolation families and agree over all 315 cells to
`1.0141e-10` relative. At `x=1`, the reconstruction agrees with the official G68 endpoint maps to
`3.7445e-16` relative.

The registered geometric readout is

```text
y = ( log(det(D)/s_F01(a,x)^2),
      log(sigma_max(D)/sigma_min(D)),
      psi ).
```

The three components are respectively matched-F01 logarithmic area, logarithmic anisotropy, and
azimuthal carry. They are separate geometric channels; they are not automatically three observed
CMB quantities.

## 2. Coarse local sensitivity

For each shape, define the control parameters

```text
p = (x_endpoint, a, epsilon).
```

The preregistered finite differences form

```text
S_ij = Delta y_i / Delta p_j.
```

Endpoint and lapse columns are averaged over the two registered amplitudes. The amplitude column
is their secant. Each column is divided by its Euclidean norm before the numerical-rank test.

All `15/15` registered shape/endpoint matrices have nonzero determinant and normalized
`sigma_min/sigma_max` between `4.6381e-4` and `1.4965e-2`, above the preregistered `1e-6` full-rank
threshold. Thus the complete three-channel geometric instrument locally separates endpoint, lapse,
and mixing-amplitude directions inside this finite tile.

This separation is not well conditioned uniformly. The normalized condition numbers range from
`66.82` to `2156.08`. The result is therefore a real local distinction, but some parameter
combinations would be highly noise-sensitive. It is neither a global injectivity theorem nor a
license to fit three physical coefficients.

## 3. Exact source-covariance degeneracy

Let an invertible geometric screen transfer be `D`, a positive-definite source covariance be
`C_src`, and its transported covariance be

```text
C_obs = D C_src D^T.
```

For any positive-definite target `C_obs`, define

```text
C_src(D) = D^-1 C_obs D^-T.
```

Then directly

```text
D C_src(D) D^T = C_obs.
```

For every nonzero vector `v`,

```text
v^T C_src(D) v = (D^-T v)^T C_obs (D^-T v) > 0,
```

so the constructed source covariance remains positive definite. Therefore an unrestricted source
covariance can exactly absorb any invertible geometric map. This is a congruence identity, not a
numerical coincidence.

All 315 G69 maps are invertible; their minimum singular value is `0.0496135`. Across the three
registered covariance controls and all `945` reconstructions, the maximum relative backward error
is `2.8306e-16` and the minimum constructed source eigenvalue is `1.56159`.

## 4. Channel ownership consequence

The geometric rank uses area, anisotropy, **and** azimuthal carry. A scalar TT readout does not
directly read arbitrary screen orientation/carry. Projecting from three readout channels to two or
one can only reduce rank. More importantly, even a complete local covariance readout cannot select
`D` while `C_src` is unrestricted, by the exact identity above.

Consequently:

- the metric map contains genuine profile and endpoint information;
- that information does not by itself identify the physical profile or endpoint from a sky
  covariance;
- a typed source/state restriction, an independently owned endpoint/profile rule, or genuinely
  independent observational channels are required before coefficients can be estimated;
- an observational fit cannot be used to pretend that an unrestricted source has been derived.

This result concerns the declared `2 x 2` screen-covariance transfer only. It is not a theorem that
all full-sky TT/TE/EE/BB data are degenerate, and it supplies no population law.
