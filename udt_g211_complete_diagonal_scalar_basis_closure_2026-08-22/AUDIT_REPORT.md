# G211 audit report — complete diagonal-scalar basis closure

Date: 2026-08-22

## Landing

```text
COMPLETE_LOCAL_DIAGONAL_SCALAR_SECTOR_HAS_RANK_TWO_AFTER_SUPPLIED_1PLUS3_REFERENCE
__COMMON_SCALE_AND_RELATIVE_SPATIAL_VOLUME_FORM_AN_EXACT_BASIS
__LAPSE_ONLY_IS_NOT_A_THIRD_TILE
__CAUSAL_CONES_DEPEND_ONLY_ON_RELATIVE_MODE_WHILE_NULL_AFFINE_AND_COMPLETED_DEPTH_HEAR_COMMON_SCALE
__NO_PHYSICAL_SCALAR_HISTORY_OR_XMAX_SELECTION
```

## Result

After a calibrated `1+3` split, positive reference lapse, and positive spatial reference are
supplied, the complete local diagonal scalar sector has exactly two coordinates. Lapse scale
`ell` and spatial-volume scale `sigma` are equivalent to common conformal scale `Omega=ell` and
relative mode `q=sigma-ell`. The transformation has rank two. A lapse-only deformation is the line
`Omega=ell,q=-ell`; it is not a third scalar tile.

The square-root four-volume ratio is `exp(ell+3 sigma)`. Every causal width scales by
`exp(ell-sigma)=exp(-q)`, while the shift center remains fixed. Common scale cancels from causal
curves but weights null affine parameter by `exp(2 Omega)` and shifts completed pair depth by
`-Omega`. Generic spatially bearing clocks hear both modes; exact static/Eulerian strata are blind
to `q` but not `Omega`.

G205 controls prove equal causal cones can have different radial affine reach, and a common factor
can compensate the relative mode's radial affine compression without changing those cones.

## Status

This is a complete local basis theorem conditional on a supplied calibrated split. It is not a
foliation theorem, field equation, scalar-profile selection, physical history, or `X_max` law.
Global causal transfer and null-affine criteria are analytic; finite scripts certify algebra and
radial anchors only.

## Evidence gates

- Preregistered: **PASS** (`7220e71f`, pushed before outcomes).
- Full space or bounded scope: **PASS WITH CAVEATS** (whole local diagonal scalar plane; bounded
  G205 radial controls).
- Independent finite-dimensional verification: **PASS** (10,000 distinct exact cases and 280,003
  assertions; no production import).
- High-precision radial controls: **PASS** (four profiles at 120 digits).
- Premise audit: **PASS** (194-row registry before solve).
- Hostile catches: **PASS** (31 preregistered mutation catches).
- Fresh external adversarial review: **PASS WITH CAVEATS**. External `gpt-5.4` verified all 34
  payload hashes, passed the registered no-write replay, retained the two-mode theorem, found no
  refuting defect, and required no repair. The universal global claims remain analytic rather than
  independently mechanized end to end.
