# BAO data suitability reset — result

Date: 2026-08-12  
Mode: `MAP -> OBSERVE`; no UDT fit  
Primary landing: `OFFICIAL_PRODUCT_READY_ONLY_WITH_DECLARED_FIDUCIAL_OR_RULER_NUISANCE`

## Ontology correction carried into the landing

The preregistered word `ruler` is retained only to preserve the frozen contract. Its operational
meaning is:

```text
FULL_PATTERN_VECTOR_READY_ONLY_WITH_PUBLISHED_NORMALIZATION_NUISANCE
```

`BAO` is only the public release label. This audit assigns no acoustic origin, standard ruler,
yardstick, sound horizon, Lambda-CDM dynamics, or early-universe mechanism to the observed
correlation pattern. The release's symbol `r_d` is only a common packaging normalization.

## What passed

The official DESI DR2 Gaussian product distributed by `CobayaSampler/bao_data` release `v2.6`
contains a 13-component vector and a 13x13 covariance:

- one isotropic `D_V/r_d` entry at `z=0.295`;
- six paired `D_M/r_d`, `D_H/r_d` entries from `z=0.510` through `z=2.330`;
- an exactly symmetric, full-rank, positive-Cholesky covariance;
- a released Gaussian quadratic form reproduced both by pinned Cobaya `v3.6.2` and by an
  independent standard-library `Decimal` implementation.

On the fixed synthetic residual, the three log likelihood values are:

```text
released Cobaya:       -15.350004514927292
UDT NumPy replay:      -15.350004514927313
independent Decimal:   -15.3500045149273183333049967557...
```

The largest disagreement is `2.2e-14`.

The mean vector reproduces the primary paper's separately printed central values to below `0.001`.
The square roots of the public Gaussian covariance diagonal differ from the paper's separately
marginalized one-dimensional widths by as much as `0.0098`. That is a real representation caveat:
the public Gaussian is a released distance-basis approximation, not an exact reproduction of every
nonlinear marginalized one-dimensional posterior. It remains the internally consistent likelihood
product tested here.

## Clean UDT-facing channels

Two uses survive the ontology audit:

1. **Full released pattern vector.** A later UDT prediction may be compared to all 13 components
   with the full covariance, but the common publication normalization must remain a free
   `PUBLISHED_NORMALIZATION_NUISANCE` unless separately fixed by an observational anchor.
2. **Normalization-free two-leg shape.** In the six anisotropic bins, `D_M/D_H` cancels that common
   normalization. This is the cleanest current pattern-shape channel. The tabulated delta-method
   errors are characterization only; a scientific fit should transform or evaluate the original
   two-dimensional covariance blocks rather than treat those approximate errors as independent.

Neither use makes the product a raw observer-pair measurement. It was compressed through a declared
fiducial coordinate and template pipeline. That layer is a comparison/readout map, not a UDT premise.

## Lineage results

- `LOCAL_ANGULAR_M2_M3`: `CHARACTER_ONLY`. The catalog calculation is reproducible, but uses a
  diagonal jackknife covariance, the one-scale profile was variant-unstable, and the radial leg was
  never built. It cannot calibrate the complete pair relation or `X_max`.
- `LOCAL_LYA_SELF_FIT`: `UNSUITABLE_AS_FIT`, while its correlation and covariance products are
  `REPROCESSABLE` under a new preregistration. The local template failed its absolute-fit gate.
- authoritative published DR1/eBOSS two-leg summaries: `AP_READY_WITH_FIDUCIAL_MAP` as secondary
  cross-survey pattern checks. Simplified local DESI tables are not authority.
- `OFFICIAL_DR2_GAUSSIAN`: full vector ready only with a publication-normalization nuisance; six
  normalization-free two-leg shape bins are ready with the fiducial readout declared.
- DR1 full-shape/window products and raw DR1 catalogs: `REPROCESSABLE`, not presently pair-ready.

## Maximum justified conclusion

There is now a reproducible current dataset suitable for a later preregistered UDT pattern
comparison. This audit does **not** fit UDT, validate a pair history, derive a feature origin, select a
physical branch, or determine `X_max`.

The next lawful action is a separate preregistration for the one complete pair relation: first use the
normalization-free six-bin pattern shape, then—only if the metric owns the required normalization
map—use the full 13-vector with one declared packaging nuisance. SNe remains a separate low-resolution
middle-regime anchor; neither dataset may silently supply a UDT law.

## External review

A fresh sealed `gpt-5.4` review returned `SUSTAINED_VERIFIED_WITH_CAVEATS`. It reproduced the
load-bearing data/likelihood reasoning and sustained the ontology and lineage classifications. Its
two evidence-presentation repairs are implemented in `PREREGISTRATION_COMMIT_PROOF.md` and
`TABLE4_REPRESENTATION_NOTE.md`; neither changes any scientific or numerical result.
