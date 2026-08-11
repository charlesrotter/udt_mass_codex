# Complete CMB observation-query map — preregistration

Date: 2026-08-11  
Branch: `grok`  
Mode: `MAP -> OBSERVE`; CPU-only; no eigensolve or fit

## Whole question

What mathematical query is actually made by the banked CMB TT peak-position and angular-power
comparisons, which complete-metric channels must a regular realization supply, and which of the
already registered CMB geometry families own those channels?

This is metric-led classification. It is not a search for a branch that resembles the observed
sky. The observed Planck TT locations may be retained only as the already attributed readout that
defines what the historical comparison called a peak. They may not select, rank, or repair a
geometry family.

## Frozen source universe

The exact sixteen sources and their pre-result SHA-256 values are frozen in
`SOURCE_MANIFEST.tsv`. No later-generated file may change candidate selection.

The complete registered geometry universe is the eighteen rows `F00` through `F17` in the frozen
`FAMILY_UNIVERSE.tsv`. Every family receives exactly one row in the realization atlas. Degenerate,
symmetry-enhanced, slice-only, conditional, and no-solve controls remain visible.

## Query layers to classify

The audit will type these layers separately:

1. observer endpoint and celestial-screen query;
2. terminal pair geometry (`kappa_pair`, `phi_pair`, `beta_pair`);
3. angular/Jacobi/ambient/normal transport needed to relate a remote pattern to the observer's sky;
4. conditional spectral/operator and boundary data that define candidate modes;
5. source/state covariance or population data that turn modes into nonzero angular power;
6. the attributed observational readout (TT peak locations, heights/power, polarization).

No layer may inherit ownership merely because another layer is present.

## Physical choices and premise stamps

- `c_E`: `OBSERVED`, local clock/ruler calibration; not a material propagation speed or path
  selector.
- `c_eff^(pair)/c_E=exp(-2 phi_pair)`: `CONDITIONAL`, terminal inter-observer pair-cone readout.
- co-presence: `POSIT` interpretive frame; it is not a signalling rule.
- `X_max`: `WORKING`, observer-pair positional-dilation asymptote; guard only, not a centered wall,
  boundary condition, or branch selector.
- complete query architecture: `DERIVED` conditionally once a typed query/realization is supplied;
  the physical CMB query owner remains `OPEN`.
- stationary scalar `Box_g`, C0/C1/general-screen envelopes, D/N wall representatives, and
  harmonic truncations: `CHOSE` controls in their cited scopes.
- P1 SNe profile: `CONDITIONAL` low-redshift observer-pair compatibility anchor; forbidden as a
  centered CMB lapse.
- mode populations, source covariance, peak heights, overall amplitude, polarization source, and
  native response law: `OPEN`.
- bootstrap, action, source, local matter physics, carrier, and new coefficients: inactive.

All values in this audit are either source identifiers/counts (`pinned-by-THEORY` to the frozen
ledger) or classifications (`free-and-explored` across all eighteen rows). There is no
`pinned-by-HABIT` physical value.

## Falsification and certification contract

The result fails if any of the following occurs:

1. a frozen source hash changes;
2. any `F00`--`F17` family is missing or duplicated;
3. a conditional scalar probe, wall datum, screen, or S3 control is relabelled native/selected;
4. TT peak position is treated as identical to a radial eigenvalue without an explicit projection;
5. nonzero TT power is inferred from eigenvalue existence without a source/state covariance;
6. a pure screen-frame rotation is said to change scalar TT temperature without an additional
   orientation-sensitive observable;
7. the SNe P1 pair profile is copied into the centered CMB lapse;
8. `X_max` is treated as a local edge or a branch selector;
9. local physics or local signal propagation is inferred from the observer-pair relation;
10. a generated record influences the frozen universe or an observational residual ranks families.

Certification requires a deterministic production table, a separate standard-library verifier
that reconstructs every key universe and source hash, exercised mutations for all ten failures,
the repository test baseline, six frozen-manifest replay, link/frontier checks, and confirmation
that unrelated untracked paths remain metadata-identical and unread.

## Maximum allowed conclusion

At most: a verified, premise-scoped architecture stating which parts of the historical CMB
calculation are already owned, which registered geometry families can conditionally realize which
query channels, and the smallest next calculation that does not fit or invent physics.

Forbidden conclusions include a CMB prediction, a selected screen/background, an FD2 restart, a
mode-population law, a polarization law, an `X_max` value, a bootstrap result, local signalling, or
native dynamics.

