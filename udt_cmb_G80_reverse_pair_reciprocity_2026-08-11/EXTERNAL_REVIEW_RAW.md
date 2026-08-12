VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY

Manifest and payload are clean. All 30 rows in `REVIEW_MANIFEST.tsv` matched their SHA-256 values,
the exact 10-row source subset in `SOURCE_MANIFEST.tsv` matched, and the payload file
`REVERSE_PATH_EVIDENCE.npz` matched the recorded digest `845aca117275...` with the expected
`(501,)`, `(32,501)`, `(2,2)`, `(2,2)` contents.

The bounded claim is supported. The metric/query reconstruction is explicit in
`solve_finite_path.py` and `derive_reverse_pair_reciprocity.py`: `A(x)=1-x^2/4`, `h(x)=x^6/20`,
receiver at `x=1/4`, source control sphere at `x=1`, stationary observers, forward
unit-receiver-frequency normalization, and reverse tangent typed exactly as `k_rev=-k_s/Z` with
the forward endpoint screen reused as the reverse initial screen. The production replay gives
`Z=1.1456439237389628`, `1/Z=0.8728715609439718`, `|ZZ_rev-1|=5.11e-15`,
`|phi_f+phi_r|=5.05e-15`, `||D_r-ZD_f^T||rel=6.89e-15`, and area-ratio residual `6.66e-15`
with all gates passing. The direct-Christoffel neighboring-ray replay does not use the production
Riemann/Jacobi implementation and still recovers the same law to `1.42e-08` relative on `D` and
`1.63e-08` on area.

```text
unscaled affine reversal:   D_rev^(0) = D_fwd^T
source-unit renormalization rho = lambda/Z  =>  D_rev = Z D_rev^(0) = Z D_fwd^T
determinant scaling:        det(D_rev) = det(Z D_fwd^T) = Z^2 det(D_fwd)
                            d_A,rev = Z d_A,fwd   since Z>0
```

Binding caveats: this is a generic self-adjoint Jacobi/Wronskian reciprocity statement on one
fixed null geodesic, not a UDT-specific selector; no physical profile, endpoint, `R`, `X_max`, SNe
fit, luminosity law, `cmb_temp`, CMB field/spectrum, source law, action, matter law, bootstrap rule,
or future-signalling law follows. The direct check is independent only in the bounded sense it
claims: it rebuilds the metric first derivatives and Christoffels locally, but it still shares the
same metric/profile, endpoint pair, stationary frequency convention, reverse normalization,
transported endpoint screens, and DOP853-family integration. The matrix equality is also
screen-gauge conditional in general; with different endpoint screen bases or an orientation
reflection the generic statement is the conjugated form `D'_rev = Z S_r D_fwd^T S_s`. On this path
no hidden reflection is present because the returned screen overlap is numerically the identity.
No correction is required for the bounded claim. Smallest next calculation: replay the same theorem
on one less symmetric nonradial branch or under an explicitly rotated endpoint screen to confirm the
expected conjugated reciprocity law away from this near-diagonal control.
