# G117 audit report — operational frequency regrade and dual-SNe regression

Date: 2026-08-16

Preregistration commit: `a7890d9f`

Status: `BLIND_VERIFIED_WITH_CAVEATS__SCOPE_AND_EVIDENCE_REPAIRS_IMPLEMENTED`

## Result

The more native G116 typing preserves the frozen SNe anchor without refitting. The active
observational interface is

```text
Z_release=1+z_release,
zeta_release=log Z_release,
dL_shape=exp(2 zeta_release) sqrt(det D_sky).
```

For the frozen conditional P1 screen chord this is exactly

```text
dL_shape=n Z_obs^2 [1-Z_obs^(-2/n)].
```

Here `zCMB` and `zHD` are processed release coordinates conditionally adopted for G94's frequency
slot—not raw one-ray ratios, UDT distances, or G116-derived global coordinates. The numerical curve
is unchanged, but its type is cleaner. SNe does not universally identify
`phi_pair=zeta_obs`; G116 places terminal depth, relative source/tape drift, and optical focusing
inside one coefficient-free junction. `phi_pair=zeta_obs` and `c_eff/c_E=Z_obs^-2` remain exact on
the pure stationary reciprocal reduction only.

## Observational replay

- Pantheon+: `1260.8480887274925 / 1366` nominal dof; fixed-`n` calibration replay.
- DES-SN5YR/Dovekie: `1444.1864417504900 / 1622` nominal dof; no large-residual rejection with the
  existing low-chi-square covariance/effective-dof warning.
- Maximum retyped/legacy magnitude difference: `1.07e-14` Pantheon+, `3.11e-15` DES.
- `n` remained bit-identical; no shape or history optimizer ran.

## Limiting result

Two inequivalent terminal-depth decompositions give the same formal local frequency coordinate and
SNe curve in an exact rational G116 two-jet witness. This witness rejects universal
`phi_pair=zeta`; it is never extrapolated across the SNe range. Therefore the current interface preserves the
macro anchor but cannot determine whether the realized local history is linear-live,
quadratic-leading, higher-order, or pure reciprocal. That requires a physical history, an
independently derived screen response, or another independent observable.

This structural non-identifiability is scoped to the current conditional P1 interface, whose
likelihood omits terminal `phi_pair` and G116 coefficients by construction. It does not establish
two global physical histories sharing one metric-derived screen. It exposes only that the old SNe
fit never independently measured terminal depth.

## Evidence

- all 18 preregistered source hashes pass;
- full retained Pantheon+ and DES rows evaluated with frozen covariances;
- the closely related production and precision-domain implementations provide regression evidence;
- a fresh blind raw-data replay independently reproduces the likelihoods and algebra;
- exact local non-identifiability witness passes;
- 5/5 executable mutations and 3/3 semantic guards pass; the latter are not catch proofs;
- the 104-row premise/startup verifier and repository suite (`90 passed, 1 xfailed`) pass;
- observational and protected downstream packages were not modified.

## Maximum conclusion

```text
VERIFIED_WITH_CAVEATS
__FROZEN_P1_DUAL_SNE_NUMERICS_PRESERVED_UNDER_CONDITIONAL_RELEASE_COORDINATE_RETYPING
__TERMINAL_DECOMPOSITION_STRUCTURALLY_UNIDENTIFIED_ONLY_IN_CURRENT_INTERFACE
__NO_GLOBAL_G116_HISTORY_TRANSFER_OR_DOWNSTREAM_PHYSICS_SELECTED
```

No selected complete history, loud-quiet-loud theorem, `X_max`, BAO/CMB result, action, bootstrap,
matter, mass, or signalling conclusion follows.
