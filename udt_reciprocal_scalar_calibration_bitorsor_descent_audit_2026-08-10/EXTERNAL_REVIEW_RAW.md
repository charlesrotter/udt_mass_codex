`ACCEPT_SCOPED_DESCENT_AND_OPEN_CALIBRATION_OWNER`

Load-bearing corrections:

1. In `EXACT_DERIVATION.md`, the equality “terminal determinant bracket = `Q`” needs its
normalization written explicitly. For a regular source flag `F=(u,r)` and

```text
h=F^T A^T g_q A F,
rho_1=|g_q(Au,Au)|/|g_p(u,u)|,
rho_2=|det Gram_q(Au,Ar)|/|det Gram_p(u,r)|,
```

the exact identity is

```text
(-det h)/h_00^2
  = (rho_2/rho_1^2) * |det Gram_p(u,r)|/|g_p(u,u)|^2.
```

Hence `(-det h)/h_00^2 = Q` only after the normalized source-calibration hypothesis
`|det Gram_p(u,r)|=|g_p(u,u)|^2`, which holds for the audit witness
`Gram_p(F)=diag(-1,1)`. With that factor stated, the claimed `phi_pair=delta_RF` is correct.

2. `DESCENT_ATLAS.tsv` and `derive_descent.py` contain an inverted status string:
`NO_ISOMETRIC_ALIGNMENT_HAS_ZERO_LOG_DENSITIES`. The proved algebra is the opposite:

```text
M in SO^+(V,g) => rho_1(M,F)=rho_2(M,F)=Q(M,F)=1, delta_RF(M,F)=0.
```

The row should therefore read either `ALL_ISOMETRIC_ALIGNMENTS_HAVE_ZERO_LOG_DENSITIES` or
`NO_ISOMETRIC_ALIGNMENT_HAS_NONZERO_LOG_DENSITIES`.

Subject to those corrections, the scoped landing stands: independent left/right screen actions do
not change `rho_1`, `rho_2`, `delta_RF`, the normalized terminal pair readout, or the conditional
R17 exponent; balanced middle-gauge composition preserves telescoping; `lambda=+-1` cause no
full-projector failure; null/degenerate strata remain excluded; and no physical calibration owner
or universal `c_eff` is derived.
