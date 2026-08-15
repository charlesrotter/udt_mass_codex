# Preregistration — DES-SN5YR/Dovekie frozen-P1 robustness holdout

Date: 2026-08-15

Program label: `G100`

Mode: observational robustness holdout; no complete-history claim

## Whole question

Does the exact P1 luminosity-relation shape frozen from Pantheon+ in G99 remain compatible with the
current DES-SN5YR/Dovekie standardized supernova Hubble diagram under a substantially different
survey and reduction, without refitting P1, importing a Lambda-CDM distance, or activating any
complete-history, orchestra, BAO, CMB, endpoint, or `X_max` freedom?

This is a data-led compatibility test of one `OBSERVED/CONDITIONAL` relation. It is not a metric
solution, a cosmological-parameter fit, or a test of every UDT history.

## Frozen model

Let

```text
n_G99 = 1.0559332414320268,
Z = 1+z,
dL_shape(z) = n_G99 Z^2 [1-Z^(-2/n_G99)].
```

The factor `X_eff` is omitted because it is exactly degenerate with the supernova brightness zero
point. The predicted shape in magnitudes is

```text
mu_shape(z) = 5 log10(dL_shape(z)).
```

One additive constant `B` is profiled analytically. This is the only fitted quantity in the primary
holdout. Neither `n_G99` nor a complete-geometry parameter may move.

## Frozen data release

Official source: `https://github.com/des-science/DES-SN5YR.git`

Frozen upstream commit: `c9a4fcafc4cbd19bd750dee47fc76194a45c181f`

Local acquisition root:

```text
/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15
```

Only `4_DISTANCES_COVMAT/` was materialized. Cosmology chains and author parameter fits are outside
the source universe.

## Primary test

1. Read `DES-Dovekie_HD.csv` in its released order.
2. Select exactly the rows with `IDSURVEY == 10` (`DES`), expected count `1623` in the frozen
   Dovekie Hubble diagram. The originally preregistered `1635` belonged to the documented upstream
   DES quality-cut sample, not this later 1820-row Dovekie vector; see `DRY_GATE_REPAIR.md`.
3. Use `zHD` as the primary redshift because it is the release's CMB-frame/VPEC-corrected Hubble-
   diagram coordinate and is the closest typed analogue of G99's primary `zCMB` coordinate.
4. Use the released `MU` vector only as a standardized observational brightness relation.
5. Reconstruct the full `1820 x 1820` precision matrix from `STAT+SYS.npz`, invert it to the full
   covariance, take the DES marginal covariance block, and factor that block without explicitly
   inverting it inside the primary chi-square evaluation.
6. Profile the one additive offset exactly:

```text
r0 = MU - mu_shape,
B* = (1^T C^-1 r0)/(1^T C^-1 1),
chi2_fixed = (r0-B*1)^T C^-1 (r0-B*1),
dof = N_DES-1.
```

The official marginal-likelihood normalization term is recorded separately if reproduced; it is
not added to the goodness-of-fit chi-square compared with `dof`.

## Preregistered result classes

The primary upper-tail probability is computed from a chi-square distribution with `N_DES-1`
degrees of freedom.

- `FIXED_P1_DES_COMPATIBLE`: upper-tail `p >= 0.01` and all data/covariance gates pass.
- `FIXED_P1_DES_TENSION`: upper-tail `p < 0.01` and all data/covariance gates pass.
- `LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING`: lower-tail `p < 0.01`; this is not called a P1
  success without further covariance/effective-sample analysis.
- `DATA_OR_COVARIANCE_TYPE_FAILURE`: hashes, row count, ordering, matrix shape, symmetry, positive
  definiteness, or released schema fail.

Compatibility means only that this frozen conditional curve survives this release. Tension means
only that this frozen Pantheon+-derived curve and the DES release are incompatible under the
declared reduction and covariance.

## Secondary diagnostics — never allowed to repair the primary return

After the primary result is written:

1. full `1820`-row Dovekie sample with `STAT+SYS`;
2. DES-only sample with `STATONLY`;
3. DES-only sample with `zHEL` substituted for `zHD` in the same P1 formula;
4. one DES-only profile diagnostic in which `s=1/n` alone is estimated with the additive offset
   profiled, reporting `n_DES`, its `Delta chi2=1` interval, and
   `Delta chi2 = chi2(n_G99)-chi2(n_DES)`;
5. residual characterization versus redshift using only preregistered equal-count bins, reported as
   descriptive evidence rather than an acceptance filter.

The overlap with Pantheon+ is not claimed to be zero. G100 tests a substantially different survey
and reduction. A truly event-disjoint test requires a separately preregistered identifier/crossmatch
audit before any overlap-pruned likelihood is run.

## Lambda-CDM exclusion

G100 must not read or use:

- the release's cosmological chains or fitted Lambda-CDM/wCDM parameters;
- a Lambda-CDM luminosity-distance or angular-distance calculation;
- a standard expansion history, standard ruler, sound horizon, or BAO/CMB prior;
- the metadata columns `MUMODEL`, `MURES`, or `MUPULL`.

The released `MU` values remain standardized and bias-corrected observational products. Their SALT3,
BEAMS, host, selection, and bias-correction processing is inherited as an `OBSERVED/CONDITIONAL`
data-reduction premise, not rebranded as raw photons or a UDT derivation. The nominal `H0=70`
normalization is removed by profiling `B` and is not interpreted physically.

## Scope not covered

G100 does not test or derive:

- a complete `B,Q,S,Y,Z` history or physical pair realization;
- the native carrier/flux/source law;
- angular or mixing attribution inside the terminal relation;
- time-live continuation or loud-quiet-loud selection;
- absolute `X_eff`, `X_max`, BAO, CMB, bootstrap, action, matter, mass, or signalling;
- raw-light-curve reduction independence;
- complete event-level independence from Pantheon+.

## Certification contract

1. Commit this preregistration before reading any DES `MU` value or executing a likelihood.
2. Verify all registered source hashes and the frozen upstream commit.
3. Run a schema-only dry check before exposing `MU`; it may inspect row counts, identifiers,
   redshift ranges, matrix dimensions, symmetry, and definiteness, but not residuals.
4. Production and independent implementations must reconstruct the compact precision independently.
5. The independent implementation must evaluate the profiled chi-square by a distinct algebraic
   route and agree to `max(1e-8, 1e-10*chi2)`.
6. Catch proofs must reject movement of `n_G99`, use of any forbidden cosmology column/product,
   subsetting the released precision instead of marginal covariance, dropping systematics in the
   primary result, or reporting a secondary result as the primary verdict.
7. Run the current premise verifier and repository tests before banking the result.

## Maximum conclusion

At most G100 may determine whether the frozen G99 P1 shape is compatible with the declared
DES-SN5YR/Dovekie observational reduction and quantify the DES-preferred shape as a strictly
secondary diagnostic. It cannot select a spacetime history, derive P1, validate UDT generally, or
infer `X_max`.
