# G174 preregistration — native calibrated pair-germ chart ownership

Date: 2026-08-19
Mode: metric-led exact type and covariance classification
Frozen source commit: `9e40a840`

## Question

For the G173 turning family, does a fully calibrated pair germ leave multiple terminal reciprocal
scalars, or does it uniquely determine the line density needed to express the one metric-owned
readout in an arbitrary auxiliary chart?

## Frozen inputs

Only the 12 files in `SOURCE_MANIFEST.tsv` may control the derivation. Protected local work,
G142--G160 scaffolds, observational outcomes, `X_max`, and global-completion proposals are
excluded.

## Preregistered primary landings

Exactly one will be selected:

1. `CALIBRATED_GERM_OWNS_UNIQUE_SCALAR__UNCALIBRATED_LINE_RETAINS_ATLAS`: one supplied calibrated
   ruler coordinate/vector uniquely fixes the G173 density and scalar; distinct positive densities
   are distinct calibrated germs/tapes on the same unparameterized line, not multiple scalar
   outputs for one input. Physical ownership of the calibration remains open.
2. `FULLY_CALIBRATED_GERM_RETAINS_SCALAR_NONUNIQUENESS`: two inequivalent terminal scalars survive
   for the same metric, same pair image, same clock calibration, and same calibrated ruler vector.
3. `PAIR_GERM_TYPE_INSUFFICIENT`: the current source record does not type the germ strongly enough
   to distinguish a calibrated vector from an unscaled line, so no classification follows.
4. `TYPE_OR_REGULARITY_FAILURE`: the proposed ruler-density reconstruction is not lawful on the
   stated turning stratum.

## Exact derivation contract

1. Begin with the G173 pullback

   ```text
   h_sigma=diag(-exp(-2 phi),H),
   H=exp(2 phi)v^2+r^2 b2.
   ```

2. Introduce a physical ruler coordinate `s` by the positive density

   ```text
   ds=m(sigma) dsigma.
   ```

   Derive the pair metric in `(x0,s)` and prove that its terminal scalar is exactly `Phi_m`.
3. Under every auxiliary reparameterization, transform both the tangent and `m`; prove that `ds`,
   the calibrated tangent `F_* partial_s`, the pair tensor in calibrated coordinates, and the
   terminal scalar are unchanged.
4. Prove uniqueness: for a fixed oriented auxiliary tangent and a fixed calibrated ruler vector on
   the same line, there is exactly one positive proportionality density `m`.
5. Classify the weaker inputs separately:
   - an unparameterized line/plane does not fix `m`;
   - a calibrated nonzero vector or ruler one-form does;
   - a fixed calibrated coordinate is preserved only by unit-slope translations and reversal, not
     arbitrary rescalings that alter the ruler unit.
6. Reinterpret the G173 witnesses `m_A` and `m_P` without selecting either. Test whether they define
   distinct calibrated tangent vectors whenever they differ.
7. Preserve the G173 tensor regularity and rank theorem unchanged.
8. Test same-calibration endpoint reversal/telescoping only. Do not invent cross-calibration carry.

## Values, charts, and omitted sectors

- `phi(r)`, `r(sigma)`, `gamma(sigma)`, and positive `m(sigma)`:
  `FREE_AND_CHARACTERIZED` under stated smoothness and regularity;
- orientation of `sigma`: free, with absolute density weight;
- static time-orthogonal spherical class and `r>0`: `CHOSE_BOUNDED_CLASS`;
- no numerical coefficients, profiles, boundary values, sources, or observational anchors;
- omitted: pair shift, ambient time dependence, nonspherical/micro metric, connection/Jacobi/
  holonomy channels, center/null/cut/focal/topology strata, and global realization.

## Certification and falsification contract

- exact symbolic derivation of coordinate/density transformations and uniqueness;
- independent standard-library rational replay over at least 10,000 regular samples, including at
  least 1,000 exact turns and explicit `m_A != m_P` witnesses;
- at least 12 mutation/semantic catches, including confusing a line with a calibrated vector,
  holding `m` fixed under reparameterization, selecting `m_A` or `m_P`, and widening to physical or
  global ownership;
- all 12 source hashes verified against commit `9e40a840`;
- repository premise verifier and full regression suite pass;
- fresh adversarial review before any final `VERIFIED` grade.

Landing 1 is falsified by one exact witness in which the same fully calibrated spatial vector
admits two distinct positive densities relative to the same oriented auxiliary tangent. Landing 2
is falsified if proportionality uniquely fixes the density and every apparent alternative changes
the calibrated vector or ruler coordinate.

## Maximum conclusion

At most G174 may distinguish coordinate-chart freedom, uncalibrated line freedom, and a supplied
calibrated pair germ in the bounded G173 family. It cannot derive which calibration is physical,
select a pair family, add a path or carry law, globalize the metric, or infer `X_max`, observations,
dynamics, action, source, matter, bootstrap, signalling, or canon.
