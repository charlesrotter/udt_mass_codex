# G112 audit report — full-differential dual-SNe invariance

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_CAVEATS`

## Result

Retyping the frozen P1 relation as distinct pair-depth and sky-area blocks changes neither SNe
prediction at measurable precision.

```text
Pantheon+ maximum pointwise magnitude change: 4.44e-15
DES maximum pointwise magnitude change:        1.78e-15
```

With `n=1.0559332414320268` frozen and no shape optimization:

```text
Pantheon+: chi2=1260.8480887274916 for nominal dof=1366
            upper-tail p=0.9799634, lower-tail p=0.0200366

DES:       chi2=1444.1864417504896 for nominal dof=1622
            upper-tail p=0.9993856, lower-tail p=0.0006144
```

Pantheon+ is compatible under the declared nominal likelihood. DES exactly retains G100's
`LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING`; this is not promoted into unusually strong support.

Pantheon+'s `dof=1366` is the correct current count because G112 fixes `n` and profiles only one
offset. G99 fitted `n` on the same calibration data and therefore records `ndof=1365`. Pantheon+
is not an independent holdout; DES is the cross-reduction holdout.

The implementation-distinct precision-domain replay agrees with production to `2.27e-12` in DES
chi-square and exactly at displayed precision for Pantheon+. It shares NumPy/SciPy and the source
data, so it is not end-to-end independent software or provenance. The executable mutations and
semantic regression guards pass; string/fixed-property guards are not promoted into strong
mutation proof.

## Meaning

This is a useful non-regression result. The corrected full observer relation can house the frozen
middle-regime SNe curve without bolting a post-processing orchestra correction onto it. It does not
derive the chosen isotropic screen representative, the P1 history, or the flux law. The complete
metric history remains open.

Fresh zero-context review returned `VERIFIED_WITH_CAVEATS` and accepted this bounded conclusion.
