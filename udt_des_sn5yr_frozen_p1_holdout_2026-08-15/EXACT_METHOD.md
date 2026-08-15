# Exact statistic and covariance ownership

## Frozen curve

For `n=n_G99` and `Z=1+z`, G100 uses

```text
d_shape(z) = n Z^2 [1-Z^(-2/n)],
mu_shape(z) = 5 log10 d_shape(z).
```

The production evaluation is the equivalent cancellation-safe expression

```text
log d_shape = log n + 2 log1p(z) + log[-expm1(-2 log1p(z)/n)].
```

The independent replay evaluates the direct powers. `X_eff`, the nominal `H0`, and absolute
supernova luminosity all enter only as one additive magnitude constant and are not inferred.

## Profiled zero point

For observed standardized magnitudes `y`, covariance `C`, model vector `m`, residual `r0=y-m`, and
all-ones vector `1`,

```text
B* = (1^T C^-1 r0)/(1^T C^-1 1),
chi2 = (r0-B*1)^T C^-1 (r0-B*1).
```

The primary degrees of freedom are `1623-1=1622`. The normalization term used in a marginalized
Bayesian likelihood is not part of this goodness-of-fit chi-square.

## Correct DES-only covariance

The release stores the full `1820 x 1820` precision matrix `W=C_full^-1` in packed upper-triangular
form. Simply selecting `W_KK` would condition on the excluded low-redshift measurements. G100 needs
the marginal covariance of the retained DES rows:

```text
C_DES = (W^-1)_KK.
```

Production factors `W`, solves for `W^-1`, selects `C_DES`, and factors that block. The independent
route partitions retained rows `K` and dropped rows `D` and constructs the equivalent Schur
complement precision

```text
W_DES = W_KK - W_KD (W_DD)^-1 W_DK.
```

The two routes agree on the primary chi-square to `1.16e-9`. The naive wrong operation
`W_DES=W_KK` gives `chi2=1451.0553337559104`, and the catch proof rejects it.

## Result typing

The primary full-covariance statistic is a compatibility test of the frozen G99 terminal curve.
The DES shape profile, alternate redshift, statistical-only covariance, full sample, and residual
bins are secondary characterization. None is permitted to replace the primary result.

No Lambda-CDM distance, expansion history, standard ruler, BAO/CMB prior, or author cosmology chain
enters any displayed equation.
