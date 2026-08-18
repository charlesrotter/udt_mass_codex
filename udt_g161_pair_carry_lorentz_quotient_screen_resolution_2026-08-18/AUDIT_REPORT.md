# G161 audit report

Date: 2026-08-18

## Primary result

G161 lands in preregistered outcome class 4:

`LORENTZ_QUOTIENT_AND_UNIQUE_BPLUS2_SECTION_DERIVED__SWEEP_FIXES_QUOTIENT_NOT_VERTICAL_RAPIDITY__NORMAL_TRANSPORT_INDEPENDENT__EXTRINSIC_SIMPLE_SPECTRUM_CONDITIONALLY_FIXES_FLAG`

The apparent four-carry-versus-three-pair mismatch is now classified exactly. Let
`D_h={M in GL+(2): M e_0 is future timelike}`. On the oriented, future-clock stratum, the pair
metric identifies the left quotient `SO+(h)\D_h` with Lorentzian pair metrics having a timelike
calibrated clock column. Only after choosing `h=eta` may this be written `SO+(1,1)\D_eta`. Its three
terminal quantities are complete coordinates on that quotient. The omitted fourth carry coordinate
is precisely a Lorentz rapidity.

## Answer to the motivating question

The ambiguity is **not** confined to one static radius. A smooth changing-distance sweep fixes the
entire quotient trajectory `(T(lambda), beta(lambda), L(lambda))`, including its first jet, while a
smooth Lorentz rapidity `theta(lambda)` remains invisible. So changing ratios strongly constrain
the metric-visible chord but do not, by themselves, reconstruct which boosted coframe played it.

If one artificially requires the same fixed boost at every distance, a rich sweep can shrink or
remove that restricted ambiguity. G161 does not impose that restriction: the exact live coframe
covariance permits distance-dependent boosts.

## Major simplification

The positive upper-triangular carry used repeatedly in the UDT pair work is no longer best viewed
as a physical ansatz. Conditional on a supplied target orthonormal pair frame and orientations, it
is the unique Lorentzian-QR representative of each quotient orbit. This removes one layer of
scaffolding without selecting a physical carry.

## Complete-geometry boundary

The screen metric, normal connection, and normal holonomy do not universally determine tangent
rapidity. A flat totally geodesic product supplies an exact countermodel.

Extrinsic geometry can do more. On a supplied pair immersion, the normal-frame-independent tensor

\[
\mathcal C_{II}=\sum_A A_A^2
\]

selects a canonical timelike/spacelike eigenflag wherever its spectrum is distinct and real. This
conditionally removes the continuous boost. Umbilic, totally geodesic, null/Jordan, complex, and
eigen-crossing strata remain unresolved.

## Evidence

- 10-source frozen manifest verified from committed bytes and SHA-256 values;
- 11 exact symbolic checks;
- 700 raw-admissible exact `Fraction` reconstruction trials generated directly in matrix
  coordinates, plus 700 exact factorized/live first-jet and normal-rotation regression trials;
- explicit simple, umbilic, Jordan, and complex extrinsic witnesses;
- 12 mutation/semantic catches;
- fresh adversarial repair and exact follow-up PASS.

## Honest ceiling

This is a structural quotient theorem and a conditional flag construction. It does not derive the
physical history or observer query, identify vertical rapidity as physical, choose a global lift,
or close null and global strata.
