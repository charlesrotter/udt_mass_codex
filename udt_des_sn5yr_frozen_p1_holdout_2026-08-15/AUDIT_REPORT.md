# Audit report — DES-SN5YR/Dovekie frozen-P1 robustness holdout

Date: 2026-08-15

Status:

```text
VERIFIED_WITH_CAVEATS
__FROZEN_G99_P1_NOT_REJECTED_BY_DES_DOVEKIE
__LOW_CHI2_REFERENCE_WARNING
__MODEST_SECONDARY_SHAPE_SHIFT
```

## Result

The exact P1 shape frozen from Pantheon+ in G99 was exposed unchanged to the current official
DES-SN5YR/Dovekie Hubble diagram. The primary test used all 1623 rows with `IDSURVEY == 10`, the
released full statistical-plus-systematic covariance marginalized from the complete 1820-object
vector, `zHD`, and exactly one analytically profiled brightness zero point.

```text
n_G99 = 1.0559332414320268  [fixed]
chi2 = 1444.1864417493343
dof = 1622
reduced chi2 = 0.8903738851722159
upper-tail p = 0.9993855958364408
lower-tail p = 0.0006144041635591934
```

The preregistered landing is therefore
`LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING`. P1 is not rejected by a large residual, but the
chi-square is too low for a clean compatibility claim under a literal 1622-degree chi-square
interpretation. Fresh external review further established that this reference distribution is only
approximate for the released, processed Hubble diagram. The release's probabilistic BEAMS treatment,
renormalized errors, correlations, global nuisance fitting, or effective degrees of freedom may
matter; G100 does not choose among those explanations or invent an effective degree count.

## Secondary diagnostics

None of these may repair or replace the primary return.

| Diagnostic | chi2/dof | reduced chi2 | Result |
|---|---:|---:|---|
| Full 1820, STAT+SYS | 1654.5303/1819 | 0.90958 | same low-chi2 warning |
| DES-only, STATONLY | 1482.5694/1622 | 0.91404 | same low-chi2 warning |
| DES-only, zHEL, STAT+SYS | 1443.4739/1622 | 0.88993 | essentially unchanged |

The preregistered DES-only shape diagnostic gives

```text
n_DES = 1.0152457866699016
Delta-chi2=1 interval: [0.9916910134637913, 1.0397634826261326]
Delta chi2(frozen G99 - DES best) = 2.6826984956860542
one-parameter upper-tail p = 0.10144369696694312
equivalent |normal sigma| = 1.6378945313072066
```

Thus DES prefers a slightly flatter P1 shape closer to `n=1`, but the frozen Pantheon+ value is not
in significant tension in this one-parameter diagnostic. Ten descriptive equal-count residual bins
show a broad downward drift in arithmetic mean residual toward the highest-redshift bin; those bins
ignore the full covariance in their displayed means and carry no separate verdict.

## What this means

This is useful robustness evidence against the worry that P1 merely memorized Pantheon+. A
substantially different survey and reduction does not demand a radically different P1 shape.
However, this is not a clean independent confirmation because:

1. the primary chi-square is anomalously low;
2. the DES vector is standardized, BEAMS-weighted, and bias-corrected rather than raw photometry;
3. the DES and Pantheon+ event sets are not proven disjoint;
4. P1 remains a chosen historical family, not a metric-derived complete history.

## No Lambda-CDM distance import

G100 used only the released `zHD`, `zHEL`, `MU`, survey identifier, and compact covariance products.
It did not read the release cosmology chains, `MUMODEL`, `MURES`, `MUPULL`, fitted cosmological
parameters, or any Lambda-CDM distance calculation. The nominal `H0=70` magnitude normalization was
removed by the free additive offset and was not interpreted physically.

The released `MU` nevertheless inherits the collaboration's SALT3, host, selection, BEAMS, and bias-
correction pipeline. That observational processing is a declared conditional premise.

## Evidence

- preregistration committed and pushed before any DES magnitude likelihood;
- one disclosed dry-gate count correction changed only `1635 -> 1623` before any residual;
- all eight registered source hashes pass;
- schema and full-precision Cholesky dry gate passes;
- production uses full-precision inversion then a DES covariance block;
- independent replay uses a precision Schur complement, independent table parser, and direct-power
  P1 formula;
- independent primary chi-square disagreement is `1.16e-9`;
- all registered fixed and secondary chi-squares reproduce within the frozen tolerance;
- 14/14 hostile mutations are rejected;
- package verification passes 35/35 checks;
- the current premise verifier passes 99 guards on 87 rows;
- repository tests pass `90 passed, 1 xfailed`.

Fresh sealed external review independently reconstructed the load-bearing numbers and returned
`PASS_WITH_CAVEATS`. It found no scientific numerical/type blocker, confirmed the covariance
marginalization, and accepted the maximum conclusion. It required the approximate-chi-square,
processed-data, direct-use-only Lambda-CDM exclusion, and limited preregistration-exposure caveats.
The intake-local replay portability defect is repaired for future sealed reviews without changing
the computation. Repository and premise tests pass as recorded.

## Scope ceiling

G100 tests one frozen `OBSERVED/CONDITIONAL` terminal luminosity relation against one released
standardized supernova reduction. It does not derive P1, select a complete `B,Q,S,Y,Z` history,
establish the native flux/source law, determine absolute `X_eff` or `X_max`, validate UDT generally,
or authorize BAO/CMB retuning.
