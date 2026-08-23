# G236 exact derivation — dual-SNe relational-state reconstruction

Date: 2026-08-23

## 1. Reframed task

The completed reciprocal pair kernel is a universal evaluator on supplied pair geometry. A fully
valued compatible relation network is the metric state rather than a second object waiting to be
selected. G236 therefore asks whether two observational releases measure a compatible projection
of that state. It does not ask the SNe data to derive a metric law.

The bounded domain is the regular central-static-spherical source/observer query, with the existing
temporary transparent-transfer bridge retained as `IMPORTED_CONDITIONAL`.

## 2. Direct transformed observable

On the declared branch,

\[
Z=1+z=e^{\phi_s-\phi_o},\qquad d_A=R,
\qquad d_L=Z^2R.
\]

For either release magnitude-like vector,

\[
m=5\log_{10}d_L+B_c
=10\log_{10}Z+5\log_{10}R(\phi)+B_c.
\]

Therefore

\[
\boxed{
y:=m-10\log_{10}(1+z)
=S(\phi)+B_c,
\qquad
S(\phi)=5\log_{10}R(\phi),
\quad
\phi=\log(1+z).
}
\]

This is an exact algebraic transformation conditional on the static query and imported transfer.
It contains no Lambda-CDM luminosity-distance function, P1 profile, `X_max`, or fitted physical
coefficient. One additive `B_c` per release removes absolute magnitude and distance normalization.

## 3. De-overlapped release samples

The frozen cuts give:

| sample | rule | rows |
|---|---|---:|
| Pantheon+ | `zCMB>0.023`, noncalibrator, `IDSURVEY!=10`, common support | 768 |
| DES-Dovekie | `IDSURVEY==10`, full DES-only support | 1,623 |

The DES-only depth support is

\[
0.07077528204904217\le\phi\le0.7627571949083936,
\]

equivalently

\[
0.07334\le z\le1.14418.
\]

Pantheon+ contains 203 otherwise eligible survey-10 rows. Exact CID comparison finds 148 of those
objects in the DES-only release. All 203 are excluded before comparison. This removes known object
reuse but cannot prove absence of cross-release calibration systematics.

## 4. Finite-resolution numerical readout

At each preregistered `K=8,12,16,24`, let `A_K(phi)` be the continuous piecewise-linear hat basis
on `K` uniform depth knots. The first knot value is fixed to zero and one release offset is free:

\[
y_c=B_c\mathbf 1+A_K\theta_c+\epsilon_c.
\]

Generalized least squares with the full retained covariance yields

\[
\widehat\beta_c
=(X_c^TC_c^{-1}X_c)^{-1}X_c^TC_c^{-1}y_c,
\]

and parameter covariance

\[
V_c=(X_c^TC_c^{-1}X_c)^{-1}.
\]

The relative state contrast is

\[
d=\widehat\theta_P-\widehat\theta_D,
\qquad
V_d=V_P+V_D,
\qquad
\chi^2_{\rm shape}=d^TV_d^{-1}d.
\]

The covariance sum is conditional on release independence after known object removal.

## 5. Observed reconstruction

Every registered resolution passes its raw-residual adequacy ceiling and its processed-release
shape-concordance ceiling:

| K | Pantheon raw chi-square / ceiling | DES raw chi-square / ceiling | shape chi-square / df / ceiling |
|---:|---:|---:|---:|
| 8 | 756.066095 / 954.935887 | 1420.844105 / 1899.165445 | 11.539289 / 7 / 25.708287 |
| 12 | 720.406473 / 950.422221 | 1411.038962 / 1894.813319 | 14.409356 / 11 / 34.452079 |
| 16 | 713.077825 / 945.907194 | 1403.873746 / 1890.460756 | 18.118818 / 15 / 42.386128 |
| 24 | 699.294454 / 936.873015 | 1399.495039 / 1881.754310 | 25.679847 / 23 / 56.911650 |

The preregistered classification is therefore

```text
DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD
```

The reconstructed knot values are retained in `STATE_RECONSTRUCTION.tsv`. They are observational
state estimates, not coefficients of a physical UDT profile.

## 6. Independent replay and hostile controls

The production route forms the marginal DES covariance by inverting the full released precision
matrix and performs Cholesky-whitened generalized least squares.

The independent route never reads the production artifact. It instead:

- solves the Pantheon covariance for its precision;
- constructs the DES marginal precision directly by the omitted-block Schur complement; and
- uses direct precision-domain normal equations.

Maximum production/independent discrepancies are:

| quantity | maximum absolute discrepancy | tolerance |
|---|---:|---:|
| relative state coefficient | `1.4261e-11` | `1e-8` |
| coefficient covariance entry | `1.8354e-15` | `1e-8` |
| raw residual chi-square | `1.2506e-11` | `1e-7` |
| shape chi-square | `1.7569e-10` | `1e-7` |

Registered hostile controls pass:

- duplicate-catalog shape contrast: exactly `0`;
- inserted half-magnitude depth ramp: shape chi-square `178.378826`, above `34.452079`;
- half-cycle redshift reassignment: raw chi-square ratio `5.904528`, above the required factor `2`;
- nine package-validator mutations are caught.

## 7. Observational provenance ceiling

The releases are not raw photon counts and are not model-independent UDT observables. Both contain
light-curve standardization and bias corrections. The DES release documentation explicitly places
an approximate reference cosmology inside the bias-correction simulations. The collaboration's
robustness tests constrain that dependence in tested neighborhoods but do not erase it.

The result must therefore remain

```text
OBSERVED_PROCESSED_CONDITIONAL
```

and not `DERIVED`, `PREDICTED`, or canon.

## 8. Exact landing and next gate

The two de-overlapped processed releases support a common finite-resolution relative `R(phi)` state
over their shared depth interval under the declared static query and imported transfer.

This authorizes, but does not yet perform, a joint state reconstruction for a held-out observable
channel. The next valid use is to freeze one common SNe-derived state estimate and ask whether a
separate BAO- or CMB-typed query agrees without refitting the state. Reusing SNe to choose a new
physical formula would undo the state/law reframe.
