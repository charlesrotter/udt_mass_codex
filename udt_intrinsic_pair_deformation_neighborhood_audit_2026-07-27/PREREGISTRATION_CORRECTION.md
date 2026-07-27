# Preregistration correction — restored positive coframe scale in the slice gate

Date: 2026-07-27

Parent preregistration: `1eb609b`

Status: **CORRECTION BEFORE FINAL OUTCOME BANKING**.

The original preregistration declared positive coframe scale `R` as a deformation axis but displayed
the unit-slice inequality without restoring `R`. For

```text
theta_1 = R exp(phi) sigma_3,
theta_0 = exp(-phi)(dt+a sigma_3),
```

the coefficient of `sigma_3^2` on `t=constant` is

```text
R^2 exp(2phi) - a^2 exp(-2phi),
```

so the correct slice gate throughout the full declared product space is

```text
min_S3 [R^2 exp(4phi)-a^2] > 0.
```

The six frozen centers all have the already registered unit convention `R=1`. Their exact lower
bound remains

```text
1/81 - 1/4096 = 4015/331776 > 0.
```

The corrected map is continuous in `C0(S3) x R_a x R_positive`, so restoring `R` changes neither the
candidate universe nor the preregistered maximum conclusion. It only repairs the declared
neighborhood dependence. Production output and verification must use this corrected formula.

The original `PREREGISTRATION.md` remains unchanged as historical evidence.
