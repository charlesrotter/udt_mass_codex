# G116 audit report — calibrated frequency / terminal-pair junction

Date: 2026-08-16

Preregistration: `4497ace9`

Status: `BLIND_VERIFIED_WITH_CAVEATS__SCOPE_REPAIRS_IMPLEMENTED`

## Result

On the complete G115 regular central spherical time-live metric/query two-jet,

\[
\boxed{
\log\frac{\omega_s}{\omega_o}
=\phi_{\rm pair}^{\rm quotient}
+(b-q)R
+\left[(\dot b-\dot q)-\frac14(2\ell+2n+\dot b)\right]R^2
+O(R^3)
}.
\]

Every coefficient is an already-derived residual-slicing invariant. Equivalently,

\[
\log\frac{\omega_s}{\omega_o}
=-\frac12\log\frac{c_{\rm eff}^{\rm(pair)}}{c_E}
+v_{\rm rel}R
+\left(\dot v_{\rm rel}-\frac{\mathcal A}{4}\right)R^2
+O(R^3).
\]

The relation adds no fit coefficient or external angular correction. The same optical invariant
`A` already controls affine and sky-Jacobi propagation.

For the active fixed-label terminal readout, the complete-pullback sky term is retained in
`phi_pair_fixed` and exactly subtracted once inside the junction. Passive sky relabeling is gauge.

## Pure reciprocal control

For `n=-p`, `ell=p`, `b=q=0`, the relative drift and optical term vanish:

\[
\zeta=\phi_{\rm pair}=pR^2,
\qquad c_{\rm eff}^{\rm(pair)}/c_E=e^{-2\zeta}.
\]

Thus the old `1+z=e^{phi_pair}` interface is exact on the stationary pure reciprocal reduction, but
not on a generic live source query unless the derived correction vanishes.

## Type and uniqueness result

- A supplied source clock, observer clock, ray covector, and declared direct frequency-ratio query
  canonically give `Z=[-g(k,U_s)]/[-g(k,U_o)]` with its normalization and group law.
- A supplied regular calibrated pair metric uniquely gives terminal `phi_pair`.
- These are connected outputs of one query, not universally identical definitions.
- On the full abstract two-channel group—or a realized channel image spanning it—founding
  composition, reversal, neutrality, and pure normalization permit the full family
  `delta_alpha=alpha zeta+(1-alpha)phi_pair`. No `alpha` is selected.

The family statement is complete only among continuous homomorphisms on that full two-channel
group. Co-descent on an arbitrary lower-dimensional relation family is insufficient. This is not a
classification of arbitrary curvature-, endpoint-, path-, or global-data cocycles.

The correct bounded landing is therefore both positive and limiting:

```text
COEFFICIENT_FREE_METRIC_QUERY_JUNCTION_DERIVED_CONDITIONALLY
__FOUNDING_ONLY_UNIVERSAL_SCALAR_SELECTION_REMAINS_NONUNIQUE
```

The metric has made the local architecture more connected. It has not selected the physical
history or licensed a fitted mixture.

## Frozen low-distance series

For a later explicitly declared frequency-ratio observation `Z=e^zeta`,

\[
Z-1
=v_{\rm rel}R
+\left(p_2-\frac{\mathcal A}{4}+\dot v_{\rm rel}+\frac12v_{\rm rel}^2\right)R^2
+O(R^3).
\]

The linear, quadratic-leading, and higher-order-or-identically-zero strata are kept separately.
G116 assigns no values to their invariant history/query coefficients and opens no dataset.

## Evidence

- exact SymPy checks: 22/22, including raw metric reconstruction of quotient/fixed terminal,
  frequency, and optical channels;
- independent standard-library `Fraction` trials: 256/256 with zero residual numerator;
- hostile mutations: 7/7 caught;
- eight source hashes frozen at preregistration;
- observational outcomes remain sealed.

Fresh blind review independently reproduced the load-bearing equations and returned
`VERIFIED_WITH_CAVEATS`; its scope repairs are registered in `CORRECTION_RECORD.md`. The 103-row
premise verifier and full repository suite pass. Final package replay is recorded separately.

## Maximum conclusion

No physical history, universal observed-redshift protocol, SNe/BAO/CMB result, `X_max`, action,
bootstrap, source dynamics, matter, mass, or signalling conclusion follows.
