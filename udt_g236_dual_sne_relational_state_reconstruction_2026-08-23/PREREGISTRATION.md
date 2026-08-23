# G236 preregistration — dual-SNe relational-state reconstruction

Date: 2026-08-23

## Whole question

On the bounded regular central-static-spherical SNe query, and conditional on the already declared
temporary transparent-transfer bridge, do two release-defined SNe samples reconstruct the same
relative areal-state shape

\[
S(\phi)=5\log_{10}R(\phi)
\]

over their common observed depth interval?

This is an observational inverse reconstruction of one supplied state projection. It is not a fit
of a physical profile, a derivation of a history law, or a prediction of the SNe data.

## Exact metric-to-observable transformation

The pinned conditional interface is

\[
Z=1+z=e^{\phi_s-\phi_o},\qquad d_A=R,
\qquad d_L=Z^2R,
\]

where the last equality uses the imported temporary transfer bridge
`eta=1, epsilon=1/Z`. Therefore each release magnitude-like observable obeys

\[
y_i:=m_i-10\log_{10}Z_i=S(\phi_i)+B_c+\epsilon_i,
\qquad \phi_i=\log Z_i,
\]

with one additive catalog calibration `B_c`. Pantheon+ uses `m_b_corr,zCMB`; DES-Dovekie uses
`MU,zHD`. No Lambda-CDM luminosity-distance function enters this transformation.

## Frozen sample definitions

### Pantheon+

- release table: `Data/Pantheon+SH0ES.dat`;
- release covariance: `Data/Pantheon+SH0ES_STAT+SYS.cov`;
- retain `zCMB > 0.023` and `IS_CALIBRATOR == 0`, matching the frozen interface;
- remove every `IDSURVEY == 10` row before cross-release comparison;
- restrict to the DES-only depth support.

The resulting expected count is 768 rows on the common support.

### DES-Dovekie

- release table: logical path `external_data/DES-Dovekie_HD.csv`, resolved only through the
  declared `G236_DES_ROOT`;
- release inverse covariance: logical path `external_data/STAT+SYS.npz`, resolved through the same
  root;
- retain `IDSURVEY == 10` only;
- use `zHD` and `MU`;
- retain the full resulting support.

The resulting expected count is 1,623 rows. Exact CID comparison has found 148 overlaps between
the DES-only release and Pantheon+ `IDSURVEY == 10`; excluding all 203 Pantheon+ survey-10 rows is
the preregistered conservative de-overlap rule. Unknown cross-release calibration systematics are
not thereby proved absent.

The common support is fixed from the release cuts, not from the reconstructed state:

\[
0.07334\le z\le1.14418,
\qquad
0.07077528204904217\le\phi\le0.7627571949083936.
\]

## Numerical reconstruction family

This is a numerical readout family, not a physical ansatz.

For each `K` in

```text
K = 8, 12, 16, 24
```

place `K` knots uniformly in the frozen common `phi` interval and use continuous piecewise-linear
hat functions. For each catalog fit, by generalized least squares with its full retained
covariance,

```text
y = B_catalog * 1 + A(phi) * theta + residual,
```

with the first knot value fixed to zero. The fitted `theta[1:]` are therefore relative shape
values; `B_catalog` absorbs the arbitrary additive magnitude/radius normalization.

The primary resolution is `K=12`. The others are preregistered resolution controls. No smoothing
penalty, prior, monotonicity condition, center expansion, P1 value, `X_max`, optimizer-selected knot
count, or physical shape constraint may be used.

## Adequacy and concordance statistics

For catalog `c`, record the raw generalized least-squares residual

\[
\chi_c^2=r_c^TC_c^{-1}r_c
\]

with `N_c-K` residual degrees of freedom. A resolution is called `ADEQUATE_AT_DECLARED_CEILING`
only if

\[
\chi_c^2\le (N_c-K)+5\sqrt{2(N_c-K)}
\]

for both catalogs. Failure is reported as a resolution limitation, not as rejection of either
release or UDT.

For each adequate resolution, compare the independently estimated relative shapes:

\[
d=\theta_P-\theta_D,
\qquad
V_d=V_P+V_D,
\qquad
\chi_{\rm shape}^2=d^TV_d^{-1}d,
\]

with `K-1` degrees of freedom. The covariance sum is conditional on treating the de-overlapped
release vectors as independent; unregistered shared systematics remain an explicit caveat.

Classify each adequate resolution using the frozen conservative ceiling

\[
C_K=(K-1)+5\sqrt{2(K-1)}.
\]

- `PROCESSED_RELEASE_SHAPES_CONCORDANT_AT_RESOLUTION_K` if
  `chi2_shape <= C_K`;
- `PROCESSED_RELEASE_SHAPES_IN_TENSION_AT_RESOLUTION_K` otherwise.

The package-level result is:

1. `DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD` only if all adequate registered resolutions are
   concordant and `K=12` is adequate;
2. `RESOLUTION_SENSITIVE_OR_INCONCLUSIVE` if adequacy or concordance changes across the registered
   family;
3. `DUAL_SNE_PROCESSED_STATE_TENSION` if every adequate resolution, including `K=12`, is in tension;
4. `REGISTERED_RECONSTRUCTION_RESOLUTION_INADEQUATE` if `K=12` and `K=24` both fail adequacy for
   either catalog.

These are observational-interface classifications only.

## Certification and hostile controls

- freeze all repository and external-data SHA-256 values before evaluation;
- preserve the full Pantheon covariance and correctly marginalize the DES inverse covariance;
- production implementation: Cholesky-whitened generalized least squares;
- independent implementation: direct normal equations from a Pantheon precision solve and a DES
  Schur-complement marginal precision, without reading production output;
- require coefficient, covariance, residual-chi-square, and shape-contrast agreement at declared
  floating-point tolerances;
- duplicate-catalog null control must give `chi2_shape <= 1e-10`;
- at `K=12`, add the explicitly nonphysical test mutation
  `0.5*(phi-phi_min)/(phi_max-phi_min)` magnitudes to one synthetic catalog copy and require
  `chi2_shape > C_12`;
- at `K=12`, sort one catalog and its covariance by redshift, then cyclically roll only the sorted
  redshift vector by `floor(N/2)` while retaining the observed-vector/covariance ordering; require
  raw residual `chi2` to exceed twice the unmutated value;
- including the Pantheon survey-10 overlap is diagnostic only and cannot enter the primary result;
- assert that P1, `X_max`, Lambda-CDM distance functions, a physical profile optimizer, and
  post-readout angular corrections are absent;
- production and independent shape values must agree within `1e-8` absolute, covariance entries
  within `1e-8` absolute, and every reported chi-square within `1e-7` absolute;
- rerun `verify_current_scientific_premises.py` and the repository purity suite before banking;
- obtain a fresh zero-context adversarial review before any scientific landing is committed.

## Observational-processing caveat

Neither release vector is raw photon data or model-independent geometry. Both contain light-curve
standardization and survey corrections. The DES release explicitly includes a bias correction
constructed using an approximate reference cosmology; Pantheon+ likewise applies bias corrections.
The DES collaboration reports tests of reference-model sensitivity, but those tests do not make the
released vector a UDT-native observable. The exact grade is therefore
`OBSERVED_PROCESSED_CONDITIONAL`, and any positive result is only a release-level state-concordance
lead.

## Omitted scope

Native radiative transfer, raw-light-curve reprocessing, source-population evolution, unknown
cross-release systematics, displaced and nonspherical queries, time-live frequency history,
multiple imaging, caustics, BAO, CMB, `X_max`, action, source, matter, bootstrap, mass, and
signalling are omitted.

## Maximum conclusion

At most G236 can determine whether the two de-overlapped processed SNe releases support one common
relative `R(phi)` state projection under the frozen static query and imported transfer, at the
registered finite resolutions. Concordance would authorize a joint observational state estimate
for later held-out channel tests. It would not derive `R(phi)`, canonize the transfer bridge, prove
UDT, or turn observational reconstruction into a physical law.
