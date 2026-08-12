# G80 external adversarial-review adjudication

Date: 2026-08-11

External model: `gpt-5.4`, fresh ephemeral context, high reasoning, web disabled

Sealed intake: `31` files total (`30` payload rows plus `REVIEW_MANIFEST.tsv`)

Sealed-manifest SHA-256:
`1bda2cbe5e8c04201d80736a1f1e2f24e1f5a150f3bf46d8bc781b1b5beeefa4`

## Final status

`VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY`

No correction is required for the bounded calculation. The external reviewer independently
reconstructed and replayed both numerical routes and accepted the exact conditional identities on
the one frozen metric, ordered endpoint pair, null curve, observer convention, affine
normalization, and carried screen gauge:

```text
Z_reverse = 1/Z_forward
phi_reverse = -phi_forward
D_reverse = Z_forward transpose(D_forward)
d_A_reverse = Z_forward d_A_forward
```

The scientific landing is therefore upgraded from provisional internal verification to externally
verified bounded geometric reciprocity. It is not promoted to a universal UDT selector or a new
physical law.

## Exact reproduced values

```text
profile                              = G75_AM_S01_E05
Z_forward                            = 1.1456439237389628
Z_reverse                            = 0.8728715609439718
|Z_forward Z_reverse - 1|            = 5.10702591327572e-15
|phi_forward + phi_reverse|          = 5.051514762044462e-15
production D reciprocity residual    = 6.885259158085081e-15
production area-ratio residual       = 6.661338147750939e-15
independent D reciprocity residual   = 1.4204869936356233e-08
independent area-ratio residual      = 1.627372281376438e-08
```

## Binding caveats

1. **Generic geometric theorem, not a selector.** The accepted relation is a generic consequence of
   the self-adjoint Jacobi equation and its Wronskian on the supplied fixed null curve. Its validity
   inside this UDT metric does not make it a UDT-specific branch, profile, endpoint, or query
   selector.
2. **Bounded independence.** The neighboring-ray replay replaces the production Riemann/Jacobi
   implementation with directly rebuilt Christoffels and finite-difference neighboring rays. It
   still shares the same metric/profile, endpoint pair, stationary observers, frequency convention,
   reverse normalization, endpoint screens, and integration-method family.
3. **Screen-gauge form.** The bare transpose identity is exact in the transported screen gauge used
   by G80. With independent endpoint screen changes the general relation is conjugated:
   `D'_reverse = Z S_r D_forward^T S_s`. The returned screen overlap is the identity to numerical
   precision, so no hidden reflection occurs in the tested path.
4. **Past-directed reversal only.** The reverse branch is the mathematical affine reversal of the
   same curve, normalized at the former source. It is not a future-directed signal.
5. **No downstream promotion.** No physical profile, endpoint, scale `R`, `X_max`, SNe fit,
   luminosity law, `cmb_temp`, CMB field or spectrum, source, action, matter law, bootstrap rule, or
   signalling law follows.

## Four evidence gates

1. **Preregistered:** yes, commit `76683fa1` and the sealed `REVIEW_DISPATCH.md`.
2. **Full or bounded:** complete only for one frozen geometry, one ordered pair, one null curve, and
   the declared screen/normalization conventions.
3. **Independently verified:** yes within that bounded scope, by a direct-Christoffel
   finite-difference neighboring-ray method and a fresh external replay.
4. **Premises audited:** yes; all profile, endpoint, observer, path, screen, affine, and conclusion
   restrictions remain explicit.

## Smallest next calculation

Test the covariant screen-gauge form on one less-symmetric nonradial branch or with an explicitly
rotated endpoint screen. This checks the theorem away from the near-diagonal control without opening
an endpoint/`X_max` family or claiming new physics.
