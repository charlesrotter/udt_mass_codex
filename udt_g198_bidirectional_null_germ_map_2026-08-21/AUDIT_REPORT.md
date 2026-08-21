# G198 audit report — bidirectional null-germ map

Date: 2026-08-21

## Landing

```text
OPPOSITE_GERM_NULL_CONTROL__ASYMMETRY_IS_METRIC_ENCODED
```

Current grade:

```text
INDEPENDENTLY_VERIFIED_WITH_CAVEATS
```

## What was tested

G198 kept the exact full nonlinear G196 metric and central calibrated pair, then supplied the
opposite future null germ. It asked whether the full curvature retained hidden `M` dependence even
though the displayed screen one-form contracts to zero on that tangent.

## Result

The metric itself makes the two germs hear different channels:

| output | outgoing `k+` | incoming `k-` |
|---|---|---|
| frequency | `a^-1` | `a^-1` |
| screen connection in `s` | `2 Omega` | `0` |
| tide | `tau0 I + a^-4(2 D+ S - 4 S^2 - 4[S,Omega])` | `tau0 I` |
| coordinate Jacobi law | `(D+ - 2M^T)(D+ + 2M)Y=0` | `D-^2 Y=0` |

In null coordinate `u`, the incoming physical Jacobi map is `D_-(u)=a(u)uI`, so
`det D_-=a(u)^2u^2>0` at every nonvertex point of a connected regular interval. The affine tangent
is `a^-2D_-`; `u` is not mislabeled as affine parameter.

This is not an imposed on/off switch. It follows because the chosen metric family contains only
the `deta+dz` screen coupling. An independent `deta-dz` metric component would be a different,
less-frozen family and remains mapped but inactive.

## Evidence

### Exact production

- 23/23 symbolic assertions passed, including exact tangent/screen closure of both Jacobi laws.
- Full metric, inverse, Christoffels, Riemann tensor, screen connection, tide, and coordinate
  Jacobi residual were directly reconstructed for both germs.
- The outgoing branch exactly reproduced G196.
- The incoming branch exactly reduced to the common-scale control.

### Independent metric-jet implementation

The verifier imports neither production code nor its artifact. It separately constructs the
coframe in Torch `float64`, obtains automatic first and second metric jets, reconstructs
Christoffels and Riemann by index contraction, and tests direct coordinate Jacobi residuals on
arbitrary screen-vector jets.

| gate | result | ceiling |
|---|---:|---:|
| histories | 68 | 4 named + 64 seeded random |
| points | 204 | 3 per history |
| assertions | 1,838 | frozen count |
| direct base-residual evaluations | 816 | both germs; nonvacuous screen-closure gate |
| incoming connection error | `4.1324542558998963e-17` | `8e-8` |
| incoming tide versus same-`a` zero-mixing control | `2.1510571102112408e-16` | `8e-8` |
| incoming coordinate-operator error | `2.220446049250313e-16` | `8e-8` |
| outgoing coordinate-operator regression | `5.551115123125783e-16` | `8e-8` |

### Hostile controls

All 9/9 preregistered mutations were caught, including replacing `k-` with `k+`, imposing a mirror,
zeroing the common tide, inserting the wrong directional operator, equating the Jacobi maps,
claiming two-ray reconstruction, activating an unregistered second null component, and using
finite determinant samples as a proof.

## Premise audit

| input | status |
|---|---|
| measured `c_E`, set to one in control units | `OBSERVED` calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` |
| displayed `a(eta),M(eta,z)` coframe | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` |
| central pair and two future null germs | `CHOSE_QUERY` |
| connection, curvature, Jacobi, and sign results | `DERIVED_CONDITIONAL` |
| independent `C_eta,C_z` family | `MAPPED_NOT_ACTIVE` |
| physical functions, germs, population, and global realization | `OPEN` |
| P1, G116, G189, fits, transfer, source, observations, `Xmax` | `OMITTED` |

## Interpretation

G198 is a real simplification: the quiet channel does not require a hand-tuned regime coefficient.
It emerges from which null component this metric family actually contains. But it also exposes the
next honest question. Is the absent second null component excluded by the intended primary metric,
or was it merely frozen by the G196 family choice? G198 does not answer that by itself.

## Maximum conclusion

G198 classifies both central future null germs of one displayed complete-coframe family. It proves
metric-encoded directional asymmetry and an exact incoming no-nonvertex-caustic control. It does
not establish arbitrary-direction closure, select physical observers or functions, reconstruct the
off-ray field, authorize a second null coupling, or supply downstream observational physics.
