# G278 map — Cepheid scale attachment and DES holdout

Date: 2026-08-27

## Whole question

Can the already frozen, P1-free Pantheon+ relative areal state from G236 acquire the single positive
homothety scale left open by G275/G276 from the Pantheon+ Cepheid-host rows, and then survive a
no-retuning DES-Dovekie check?

This is an observational calibration of one remaining constant under the imported transparent
radiative-transfer bridge. It is not a derivation of a metric history, a fit of the reciprocal
kernel, an angular/orchestra fit, or an inference of `X_max`.

## Frozen dependency chain

```text
metric-native completed pair state
    -> phi = log(1+z)
    -> conditional d_A = R and d_L = (1+z)^2 R
    -> G236 Pantheon+-only relative S(phi)=5 log10 R(phi)
    -> Pantheon+ Cepheid-host absolute-magnitude rung
    -> one scale ell
    -> frozen DES-Dovekie no-retuning query
```

## Bounded regime

- central, static, spherical SNe projection only;
- Pantheon+ flow support exactly frozen by G236: `0.07334 <= z <= 1.14418` after its survey and
  calibrator exclusions;
- all 77 Pantheon+ rows marked `IS_CALIBRATOR == 1` for the Cepheid rung;
- DES-Dovekie `IDSURVEY == 10` held-out rows already frozen by G236;
- numerical state resolutions `K = 8, 12, 16, 24`, with `K=12` primary;
- no extrapolation of the relative state.

## What is pinned and what is supplied

- `pinned-by-THEORY`: completed-pair projective state, direct reciprocal redshift
  `phi=log(1+z)`, and one remaining positive homothety freedom;
- `pinned-by-PREREGISTERED_EVIDENCE`: G236 sample cuts, knot family, Pantheon+-only relative state
  reconstruction, and DES held-out vector;
- `OBSERVED`: Pantheon+ Cepheid-host distance moduli and full released covariance;
- `CONDITIONAL`: transparent radiative transfer and the identification of the Cepheid photometric
  distance with the same distance channel used by the UDT SNe interface;
- `OPEN_AND_NOT_USED`: UDT light theory, complete evolving history, `X_max`, CMB source history,
  angular/bootstrap amplitudes, and nonspherical/time-live completion.

## Proposed bounded action

Preregister the exact two-rung generalized least-squares calculation, commit and push it before
computing a numerical scale, then run the primary result, implementation-distinct verification,
hostile controls, and a fresh external adversarial review.
