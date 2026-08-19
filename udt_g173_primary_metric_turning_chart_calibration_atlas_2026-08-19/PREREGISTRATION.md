# G173 preregistration — non-areal turning-chart classification

Date: 2026-08-19
Mode: metric-led exact classification; no fitted profile, physical-family selection, or preferred calibration
Frozen source commit: `d1f2e6f5`

## Question

For

\[
F(x^0,\sigma)=(x^0,r(\sigma),\gamma(\sigma)),
\]

does the G172 primary-metric pair surface remain regular at \(dr/d\sigma=0\)? If it does, does the
metric uniquely extend the G172 scalar calibration, or only supply a lawful calibration atlas?

## Frozen inputs

Only the 11 files in `SOURCE_MANIFEST.tsv` may control the derivation. Protected work,
G142--G160, observational outcomes, `X_max`, and global-completion proposals are excluded.

## Preregistered primary landings

Exactly one will be selected:

1. `UNIQUE_METRIC_NATIVE_TURNING_CALIBRATION`: the declared metric and supplied family uniquely
   determine a smooth non-areal scalar calibration that agrees with G172 on every monotone overlap.
2. `PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE`: the tensor extends through a regular turn, but
   two or more inequivalent lawful metric-built scalar calibrations survive; G172 is connected to
   them by exact transition laws rather than a unique finite scalar continuation.
3. `TURNING_IS_TRUE_RANK_FAILURE`: every `dr/dsigma=0` point makes the pair pullback degenerate even
   when angular motion is nonzero.
4. `TYPE_OR_REGULARITY_FAILURE`: the proposed non-areal construction is not a lawful pullback/chart
   problem in the declared arena.

## Exact derivation contract

1. Derive the full pullback from

   \[
   g=-e^{-2\phi}(dx^0)^2+e^{2\phi}dr^2+r^2\gamma_{S^2}
   \]

   without dropping either radial or angular tangent data.
2. With

   \[
   v=dr/d\sigma,\qquad
   b^2=\gamma_{S^2}(d\gamma/d\sigma,d\gamma/d\sigma),
   \]

   classify `det(h)` and immersion rank at radial turns, pure-angular segments, and simultaneous
   `v=b=0`.
3. Derive the exact transformation of the raw component readout under every regular
   reparameterization of `sigma`.
4. Type a scalar calibration as a positive weight-one line density `m` and derive the invariant
   readout `Phi_m` and transition between any two such calibrations.
5. Recover the G172 areal calibration `m_r=abs(v)` wherever `v!=0`.
6. Audit, without privileging, at least these metric-built non-areal candidates:

   \[
   m_A^2=v^2+r^2b^2,
   \qquad
   m_P^2=v^2+e^{-2\phi}r^2b^2.
   \]

   Both must be tested for smoothness, reparameterization covariance, radial recovery, and turning
   behavior. Their inequivalence, if any, must be reported rather than resolved by preference.
7. Prove or disprove the existence of a positive continuous calibration that is numerically equal
   to the G172 areal calibration on every punctured monotone neighborhood and remains nonzero at a
   genuine radial turn.
8. Test scalar reversal/telescoping only inside one fixed calibration family. Do not promote it to
   cross-calibration or non-scalar carry.

## Values, charts, and omitted sectors

- `phi(r)`, `r(sigma)`, and `gamma(sigma)`: `FREE_AND_CHARACTERIZED` subject only to stated
  smoothness and local regularity;
- sign/orientation of `sigma`: free; formulas must use the appropriate absolute density weight;
- time-orthogonal static chart: `CHOSE_BOUNDED_CLASS`;
- `r>0`: `CHOSE_BOUNDED_DOMAIN` because the center is separately singular as a spherical chart;
- no numerical coefficient, boundary condition, angular curve, profile, or observational anchor;
- omitted: pair shift, ambient time dependence, nonspherical/micro metric, connection/Jacobi/
  holonomy channels, cut/focal/topology strata, center completion, global relation ownership.

## Certification and falsification contract

- exact symbolic derivation with explicit chart-transition identities;
- independent standard-library rational/numerical replay over at least 10,000 regular samples,
  including at least 1,000 exact radial-turn samples;
- at least 12 mutation/semantic catches, including false turning degeneracy, dropped angular Gram,
  raw-readout invariance, hidden calibration selection, and widening to physical/global closure;
- all 11 frozen source hashes verified against commit `d1f2e6f5`;
- repository premise verifier and full regression suite pass;
- fresh adversarial review before any `VERIFIED` grade.

The unique-calibration landing is falsified by two inequivalent positive metric-built calibration
densities satisfying the registered covariance, radial-recovery, regularity, and bounded-scope
gates. The rank-failure landing is falsified by one exact `v=0`, `b>0`, `det(h)<0` witness.

## Maximum conclusion

At most G173 may classify the local static time-orthogonal turning-chart tensor, its calibration
atlas, and its first true rank boundary. It cannot select the physical ruler or family, alter the
primary metric, derive distance globally, close transport, or infer `X_max`, dynamics,
observations, action, source, matter, bootstrap, signalling, or canon.
