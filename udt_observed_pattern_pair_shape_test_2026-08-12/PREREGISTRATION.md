# Preregistration — complete-pair observed-pattern shape operator and frozen controls

Date: 2026-08-12  
Mode: `MAP -> DERIVE -> OBSERVE`  
Question type: metric-led operator derivation plus bounded six-bin compatibility test  
Outcome status at registration: **NOT YET EVALUATED**

## 1. Whole question

Does one supplied complete UDT observer-pair history define the same dimensionless transverse/radial
pattern-shape quantity carried by the six anisotropic official DR2 measurements, and how do two
already frozen scalar controls compare before any complete-orchestra history is selected?

This is not an acoustic-scale, standard-ruler, yardstick, Lambda-CDM, expansion-history, or
feature-origin test. The public data are an observed correlation pattern compressed through a
declared fiducial/template readout. No conventional mechanism enters the UDT prediction.

## 2. Exact complete-pair operator to derive

Let a supplied regular calibrated pair immersion have pair metric

```text
h=-T_pair^2(dy0+beta_pair dlambda)^2+L_pair^2 dlambda^2,
```

terminal depth and redshift coordinate

```text
1+z=exp(phi_pair),
```

and complete screen Jacobi area distance

```text
d_A=sqrt(abs(det D)).
```

The horizontal pair-ruler direction obeys `dy0+beta_pair dlambda=0`, so its source-calibrated
physical length is `d ell_parallel=L_pair dlambda`. The publication-coordinate conversion multiplies
both transverse and radial source lengths by the same endpoint factor `1+z`; that factor cancels in
their ratio. The candidate complete-pair shape operator is therefore

```text
F_pair
 = D_transverse/D_radial
 = d_A (dz/dlambda)/L_pair
 = exp(phi_pair) d_A (d phi_pair/dlambda)/L_pair.       (1)
```

Equation (1) must be proved invariant under every orientation-preserving reparameterization of
`lambda`. Reversal is tested separately with the appropriate absolute/orientation convention; no
future-signal interpretation is allowed.

The operator is evaluated only where `L_pair>0`, `d_A>0`, and `dz/dlambda` is finite and nonzero.
Turning, caustic, degenerate, and nonmonotone strata must be reported rather than discarded.

## 3. Frozen scalar controls

Neither control is the full UDT prediction.

### C0 — exact reciprocal-L control

Freeze the scalar pair relations

```text
phi_pair=log(1+z),
d_A=r(z),
L_pair=exp(phi_pair),
r(z)=X[1-(1+z)^(-2)].
```

Equation (1) must reduce exactly to

```text
F_C0(z)=z+z^2/2.
```

### C1 — independently frozen SNe-P1 shape control

Freeze the same scalar relation with

```text
r(z)=(R_w/n)[1-(1+z)^(-2/n)],
n=1.0559332414320268,
```

where `n` is the already banked primary SNe value. No refit or uncertainty optimization is allowed.
Equation (1) must reduce exactly to

```text
F_C1(z)=(n/2)[(1+z)^(2/n)-1].
```

`X`, `R_w`, `c_E`, and the publication normalization cancel. C1 tests only the scalar middle-regime
control inherited from the conditional SNe readout. A mismatch does not reject the complete pair
operator; it measures where that frozen scalar control is insufficient.

## 4. Frozen observed-pattern likelihood

Use exactly the six paired `(D_M/r_d,D_H/r_d)` blocks at

```text
z = 0.510, 0.706, 0.934, 1.321, 1.484, 2.330
```

from `CobayaSampler/bao_data v2.6`, commit
`b7b8a36e9bccb063081f811f323cada21ab5fbdd`, with the released 13x13 covariance. The `z=0.295`
isotropic-only entry is excluded from the ratio test by type, before residual evaluation.

For predicted shape `F_i`, define `v_i=(F_i,1)`. In each released two-dimensional block, profile only
the algebraic publication amplitude

```text
a_i=(v_i^T C_i^-1 y_i)/(v_i^T C_i^-1 v_i),
chi2_i=y_i^T C_i^-1 y_i-(v_i^T C_i^-1 y_i)^2/(v_i^T C_i^-1 v_i).   (2)
```

The six `a_i` values are data-coordinate projections, not UDT physical parameters, feature scales,
or fitted history coefficients. They isolate the normalization-free direction of each released
two-leg block. No delta-method ratio errors enter the load-bearing likelihood.

The primary diagnostics are:

- exact `chi2_total=sum_i chi2_i` for C0 and C1;
- six signed whitened orthogonal residuals for each control;
- per-bin observed direction `D_M/D_H` for visualization only;
- C1 minus C0 chi-square as a comparison of two frozen controls, not model selection over a menu.

## 5. Degrees of freedom and omissions

No UDT coefficient is fitted. Each frozen control has six orthogonal data constraints and zero fitted
UDT parameters. The six analytic amplitudes remove the unpredicted along-ray normalization in data
space and do not reduce the six orthogonal shape constraints.

Not covered:

- a physical complete history `B(lambda),P(lambda)`;
- a selected pair immersion or branch;
- complete time-live `d_A`, `L_pair`, or `phi_pair` profiles;
- caustic/turning branch aggregation;
- the isotropic-only data point;
- the full 13-vector normalization test;
- SNe refitting, CMB spectra, microphysics, bootstrap, action, source, matter, or `X_max`.

## 6. Preregistered gates

1. `G-OPERATOR`: derive (1) from the complete pair metric, endpoint depth, and Jacobi area without
   importing a conventional expansion law.
2. `G-REPARAM`: prove orientation-preserving parameterization invariance symbolically and by exact
   controls.
3. `G-SCALAR`: reproduce both frozen C0 and C1 formulas exactly.
4. `G-DATA`: exact release hashes and all six anisotropic blocks match the banked suitability audit.
5. `G-PROFILE`: production and independent implementations reproduce (2).
6. `G-NO-FIT`: `n`, data rows, covariance, and formulas remain frozen; no UDT parameter optimization.
7. `G-COMPLETE-BOUNDARY`: distinguish the generic complete operator from scalar controls in every
   conclusion.
8. `G-ONTOLOGY`: no acoustic/ruler/Lambda-CDM/feature-origin language enters the derivation.
9. `G-INDEPENDENCE`: independently recompute the load-bearing likelihood without importing the
   production residual routine.
10. `G-CATCH`: hostile controls must detect at least missing `L_pair`, missing `exp(phi_pair)`, using
    diagonal-only errors, replacing the exact profile by delta-method errors, fitting `n`, dropping a
    high-residual bin, and treating C1 as the complete history.

## 7. Result classes and maximum conclusion

The operator derivation returns one of:

- `COMPLETE_PAIR_SHAPE_OPERATOR_DERIVED`;
- `OPERATOR_DERIVED_WITH_STRATUM_FAILURES`;
- `TYPE_FAILURE`.

Each frozen control is classified independently as:

- `COMPATIBLE_ON_SIX_BIN_SHAPE_QUERY` if `chi2_total<=12.592` (95% for six constraints);
- `TENSION_ON_SIX_BIN_SHAPE_QUERY` if `12.592<chi2_total<=22.458` (between 95% and 99.9%);
- `INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY` if `chi2_total>22.458` (beyond 99.9%).

These thresholds are fixed before residual evaluation. They are descriptive gates for the released
Gaussian shape query, not proof probabilities for UDT.

Maximum possible conclusion:

> The complete metric defines a normalization-free pattern-shape operator on a supplied monotone
> regular pair history, and one or both frozen scalar controls are compatible, tense, or incompatible
> with the six-bin released shape query.

No outcome may select the physical complete history, derive a feature origin, validate all UDT,
determine `X_max`, or justify adding a fitted orchestra correction.
