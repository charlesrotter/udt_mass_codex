# G280 audit report — projective position / optical area bridge

Date: 2026-08-27

## Bounded landing

```text
SAME_COMPLETE_PROJECTIVE_PAIR_STATE_ADMITS_DIFFERENT_NATIVE_JACOBI_AREA
__OPTICAL_AREA_IS_NOT_A_FUNCTION_OF_PHI_OR_W5_STATE_ALONE
__PRIMARY_SPHERICAL_SAME_DEPTH_PROFILES_REACH_DIFFERENT_AREAL_RADII
__DIRECT_ONE_SCALE_SNE_CURVE_REQUIRES_ADDITIONAL_AREAL_IDENTIFICATION_OR_COMPLETE_HISTORY
```

## What was learned

W5 projective position and optical Jacobi area are both metric-native, but they are not the same
metric datum. W5 reads the transported endpoint clock column. Optical area integrates transverse
curvature along a null bundle.

Two exact complete metrics were constructed with the same metric and first jet on one central null
branch, the same full transported endpoint arrow, arbitrary common reciprocal depth, the same
redshift, and the same W5 state. Their transverse curvature and native regular Jacobi areas differ.

The separation also survives inside the primary static-spherical class. The smooth-centered
profiles `phi_A(s)=s^2` and `phi_B(s)=s^2+s^4` reach the same reciprocal depth at different areal
radii. Thus `phi` plus one scale does not determine `R(phi)`.

Declaring `R=ell tanh(phi)` would be an additional areal/projective law. Applied globally from a
regular center, it forces `phi=artanh(R/ell)` and violates the smooth-center zero-slope condition.

## Evidence

- preregistration committed and pushed at `d20398a9` before the outcome calculation;
- symbolic inverse-metric, connection, curvature, and Jacobi derivation;
- 4,096 arbitrary finite projective/redshift cases;
- 4,096 regular pre-caustic complete-screen cases;
- 4,096 primary static-spherical same-depth cases;
- 36,883 production assertions;
- independent direct neighboring-ray RK4 method: 4,096 cases and 40,960 assertions;
- maximum independent screen integration error `2.55e-12`;
- four executable mathematical mutation/counterchecks and four premise-ledger provenance guards;
- ten repair-specific fail-closed mutations catch wrong labels or altered center derivatives;
- zero fitted coefficients and no observational values used.

Fresh external `gpt-5.4` review independently reproduced the geometry and all eight registered
replays, retained alternative B, and returned `ACCEPT_WITH_REPAIRS`. Its only defect was the prior
overstatement of all eight checks as hostile mutations and the epsilon-only center probe. Repairs
R1--R3 now classify the checks honestly and use the exact center derivatives. The sealed
repair-only external follow-up verified all 38 payloads, reproduced all four durable outputs
byte-for-byte, accepted R1--R3, retained the bounded scientific landing, and reported no remaining
scoped defect.

## Scientific meaning

The direct reciprocal redshift law is intact. W5 is intact. The complete angular/screen orchestra
is intact. The result says that the orchestra contains real tidal-history information not encoded
in one endpoint depth or projective clock-column state.

Pantheon+, Cepheids, and the imported luminosity rule can reconstruct and calibrate an optical
curve. Without a complete history or separately adopted areal/projective identification, that is
an empirical reconstruction rather than a parameter calibration of a native predicted curve.

## Maximum conclusion

Source-bounded metric geometry only. G280 does not select a physical history, reject an empirical
SNe reconstruction, derive native radiative transfer, determine a scale or `X_max`, or say the
quiet-regime screen correction is observationally large.

Current grade:
`EXTERNAL_REPAIR_ACCEPTED__BOUNDED_LANDING_UNCHANGED`.
