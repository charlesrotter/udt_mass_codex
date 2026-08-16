# G117 preregistration — operational frequency ownership and dual-SNe regrade

Date: 2026-08-16

## Whole question

Does the coefficient-free G116 frequency/terminal junction preserve the frozen Pantheon+ P1
calibration and its no-refit DES-SN5YR/Dovekie replay after the release redshift coordinate is
correctly typed as an observational frequency-ratio protocol rather than universally identified
with terminal `phi_pair`?

This is a retyping and numerical-regression test. It is not a fit of a new history and is not a
test of the unowned G116 invariant coefficients.

## Frozen interface

For each retained catalog row adopt, explicitly and only for this observational protocol,

```text
Z_obs = 1 + z_release,
zeta_obs = log Z_obs.
```

`zCMB` for Pantheon+ and `zHD` for DES are `OBSERVED_RELEASE_REDSHIFT_COORDINATES`: processed
frame-aware catalog quantities rooted in spectroscopic redshift, not metric-derived UDT distances
and not asserted to be an untouched one-ray local frequency measurement.

Freeze the G99/G112 curve without modification:

```text
n = 1.0559332414320268,
lambda_A(zeta) = n [1-exp(-2 zeta/n)],
D_sky = lambda_A I2                         [conditional representative],
dL_shape = exp(2 zeta) sqrt(det D_sky)
         = n Z_obs^2 [1-Z_obs^(-2/n)]       [conditional transfer].
```

G116 is used internally, not appended:

```text
zeta = phi_pair + v_rel R + [dot(v_rel)-A_opt/4]R^2 + O(R^3).
```

Consequently `phi_pair=log Z_obs` and `c_eff/c_E=Z_obs^-2` are retained only on the pure stationary
reciprocal reduction, or another realized history where the correction vanishes. They are not
universal consequences of an SNe redshift column.

## Pins and omissions

- `pinned-by-THEORY`: G116 local junction and its pure reciprocal reduction; G94 regular-branch
  frequency/screen factorization; covariance likelihood algebra.
- `pinned-by-OBSERVATION/CONTRACT`: catalog rows and release redshift columns, full published
  covariance products, G99 `n`, Pantheon+ cut, DES survey subset, one profiled additive offset.
- `CHOSE_CONDITIONAL`: P1 observed screen chord and `d_L=Z^2 d_A` transfer closure.
- no free/fitted metric, orchestra, drift, optical, transfer, or regime coefficient.
- omitted: finite-radius completion of the G116 jet, physical history, independent `phi_pair`,
  source/carrier dynamics, global branches, BAO, CMB, `X_max`, bootstrap, action, matter, mass, and
  signalling.

## Preregistered checks

1. Verify every frozen source hash before data evaluation.
2. Reconstruct the retyped and legacy frozen P1 magnitude curves independently and require maximum
   pointwise disagreement at most `1e-12` on every retained row.
3. Hold `n` bit-identical; prohibit every shape/history optimizer.
4. Reproduce the banked Pantheon+ fixed-`n` replay within `3e-5` in chi-square and `3e-6` in offset.
5. Reproduce the banked DES primary within `2e-6` in chi-square and `2e-9` in offset, retaining the
   low-chi-square warning.
6. Provide an implementation-distinct precision-domain replay with the DES Schur complement.
7. Demonstrate at least two inequivalent G116 terminal-depth decompositions with identical
   `zeta_obs`, screen chord, and SNe likelihood. This is a non-identifiability check, not a fit.
8. Catch mutations that restore universal `phi_pair=log Z`, alter `n`, append a correction, use the
   DES precision subblock, or call a release redshift column a UDT distance.

## Registered returns

- `RETYPE_PRESERVES_DUAL_SNE_ANCHOR__JUNCTION_DECOMPOSITION_NOT_IDENTIFIED_BY_SNE`;
- `RETYPE_CHANGES_FROZEN_SNE_PREDICTION`;
- `DUAL_SNE_REPLAY_MISMATCH`;
- `SOURCE_OR_TYPE_FAILURE`.

## Maximum conclusion

At most G117 can show that the more native G116 typing leaves the frozen conditional SNe curve
numerically intact while removing the unsupported universal identification of catalog redshift with
terminal `phi_pair`. It cannot select a physical history, prove loud-quiet-loud evolution, determine
the G116 invariant coefficients, derive transfer, establish UDT, or infer any downstream physics.
