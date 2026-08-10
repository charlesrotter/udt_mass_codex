# Audit report — reciprocal scalar/calibration bitorsor descent

Date: 2026-08-10

Status: **VERIFIED-WITH-CAVEATS**

## Result

Across all six retained regular C01--C06 full-projector strata, independent source and target
screen rotations leave the supplied clock-line density, clock/ruler-plane density, conditional
`delta_RF`, terminal supplied pair-metric log imbalance, and conditional R17 reciprocal exponent
unchanged. Balanced composition preserves the density telescoping law exactly while path labels and
holonomy remain intact.

Primary landing:

```text
RECIPROCAL_READOUT_DESCENT_DERIVED__CALIBRATION_MAGNITUDE_NOT_GENERATED
```

Every projector alignment is isometric and has density ratios `(1,1)` and reciprocal argument `1`.
It therefore transports an already supplied calibration magnitude but cannot generate a nonzero
one. The arbitrary screen phase is not the missing scalar physics; the non-isometric calibration
owner remains open.

## Exact gates

- arbitrary continuous independent source/target `SO(2)` rotations proved symbolically;
- complete mixed-arrow witness retains clock-to-screen mixing and gives exact
  `(rho_1,rho_2,Q)=(3/16,3/4,64/3)`;
- terminal pair readout equals `delta_RF=log(64/3)/4` on that supplied, normalized witness; the
  exact source-normalization factor is exposed and independently checked with an unnormalized
  `9/4` witness;
- all six `lambda` rows retain R17 screen-gauge descent with no ownership promotion;
- exact balanced three-arrow composition and density telescoping pass;
- independent pure-Python `Fraction` verifier reproduces 36 independent rational source/target
  screen-gauge pairs, the mixed witness, zero alignment density, composition, 16 source hashes, and
  36 path-labelled loop rows.

## Interpretation boundary

This result removes one false blocker: no preferred angular screen phase is required for the
declared reciprocal scalars. It does not provide the non-isometric calibration amount, physical
pair arrow, pair surface, or scalar-law selection. It also does not identify different paths or
resolve null/degenerate strata.

No action, source, matter, mass, bootstrap, `X_max`, CMB, signalling, eigenvalue solve, or GPU work
is inferred.

## Four banking gates

1. **Preregistered:** yes, commit `2903a0da` before derivation.
2. **Full space or bounded scope:** complete for all six retained regular full-projector strata and
   the full continuous screen stabilizer; not universal over null/degenerate strata or all UDT
   metrics.
3. **Independently verified:** yes locally by a code-independent rational implementation and by a
   fresh isolated external adversarial review. The reviewer accepted the scoped landing after the
   source-normalization factor and one inverted atlas status string were corrected.
4. **Every premise audited:** yes for gauge action, conditional readout ownership, mixing, path
   labels, R17 status, and the generation-versus-descent distinction.

External verdict: `ACCEPT_SCOPED_DESCENT_AND_OPEN_CALIBRATION_OWNER`.
