# G278 preregistration — Cepheid scale attachment and DES holdout

Date: 2026-08-27

## Frozen question

Conditional on the G236 central-static SNe projection and temporary transparent-transfer bridge,
does the Pantheon+ Cepheid-host rung identify the one positive scale multiplying the already frozen
Pantheon+-only relative state, and does the resulting absolute curve agree with the held-out
DES-Dovekie release without any DES, state, kernel, or angular retuning?

No calibrator-derived scale or DES residual may be evaluated before this preregistration is committed
and pushed.

## Exact frozen interface

Let

\[
Z=1+z=e^\phi,\qquad d_A=R,\qquad d_L=Z^2R
\]

under the explicitly imported temporary transparent-transfer bridge. At G236 resolution `K`, write

\[
5\log_{10}\!\left(\frac{R(\phi)}{\mathrm{Mpc}}\right)
=a+S_K(\phi),
\qquad
a=5\log_{10}\!\left(\frac{\ell}{\mathrm{Mpc}}\right),
\]

where the first G236 knot fixes `S_K(phi_min)=0`. The standardized SNe relations are then

\[
m_i=\mu_i^{\rm Cepheid}+M
\]

on Cepheid-host rows, and

\[
m_i=10\log_{10}Z_i+S_K(\phi_i)+a+25+M
\]

on G236 Pantheon+ flow rows. Only `M` and `a` are dimensional-calibration unknowns. `S_K`, the
kernel, the redshift law, and every angular channel are frozen.

## Exact data and selections

### Pantheon+ relative-state rung

Reproduce G236 exactly:

- `zCMB > 0.023`;
- `IS_CALIBRATOR == 0`;
- `IDSURVEY != 10`;
- restrict to the DES-only G236 depth support;
- expected count: 768;
- state basis: continuous piecewise-linear hats on the frozen uniform knot grids
  `K=8,12,16,24`;
- first knot fixed to zero; one flow offset retained;
- primary covariance serialization: symmetric mean of the released matrix.

### Cepheid rung

- retain every row with `IS_CALIBRATOR == 1`;
- expected count: 77 rows and 43 unique `CID` values;
- use `c_i=m_b_corr_i-CEPH_DIST_i`;
- use the full calibrator block and its full cross-covariance with the 768 flow rows;
- never use calibrator redshift to assign its distance.

### DES holdout

- use the exact 1,623 DES-Dovekie `IDSURVEY == 10` rows frozen by G236;
- use `zHD`, `MU`, and the full covariance obtained from the released inverse covariance exactly as
  in G236;
- no DES offset, scale, state coefficient, knot value, kernel coefficient, or angular coefficient
  may be estimated;
- the strict check is conditional on the release's published `MU` normalization (including its
  stated `H0=70` convention), which is catalog cargo rather than a UDT scale derivation.

## Two-stage estimator with exact shared-data covariance

For each `K`, the G236 flow fit is

\[
y_f=m_f-10\log_{10}Z_f=X_K\beta_K+\epsilon_f,
\qquad
\beta_K=(B_K,\theta_K)^T,
\]

with `X_K=[1,A_K[:,1:]]`. Recompute the linear GLS operator

\[
L_K=(X_K^TC_{ff}^{-1}X_K)^{-1}X_K^TC_{ff}^{-1}
\]

and freeze the G236 state `theta_K`. The scale calculation uses only the fitted flow intercept
`B_K`, not a refit of `theta_K`.

Form the reduced observation vector

\[
q_K=(c_1,\ldots,c_{77},B_K)^T
\]

with covariance derived from the full released Pantheon+ covariance,

\[
\operatorname{Cov}(c)=C_{cc},\quad
\operatorname{Cov}(c,B_K)=C_{cf}L_{K,B}^T,\quad
\operatorname{Var}(B_K)=L_{K,B}C_{ff}L_{K,B}^T.
\]

Fit exactly two columns:

\[
q_K=
\begin{pmatrix}
1&0\\
\vdots&\vdots\\
1&0\\
1&1
\end{pmatrix}
\binom{M}{a+25}+\epsilon.
\]

Equivalently, report `a=B_K-25-M` and `ell=10^(a/5) Mpc`. This reduction retains the exact
calibrator/flow cross-covariance while preventing the calibrator rows from changing the frozen
relative state.

## Pantheon+ calibration gates

For each resolution require:

1. the reduced covariance is symmetric positive definite;
2. the whitened two-column design has rank two;
3. `ell` is finite and positive;
4. the calibrator common-`M` residual satisfies

   \[
   \chi^2_{\rm cal}\le \nu+5\sqrt{2\nu},\qquad \nu=77-1;
   \]

5. the reconstructed `theta_K` and `B_K` reproduce G236 to `1e-10` absolute tolerance on the
   primary symmetric-mean route.

Failure of items 1--4 blocks scale attachment. Failure of item 5 is a regression failure.

## Resolution and calibrator-subset controls

### Resolution control

Use `K=12` as primary and `K=8,16,24` as frozen controls. From the exact common-data linear weight
vectors, form

\[
d=(a_8-a_{12},a_{16}-a_{12},a_{24}-a_{12})
\]

and its full covariance. Call the scale resolution-stable only if this covariance has its expected
rank and

\[
d^TV_d^+d\le 3+5\sqrt6.
\]

### Calibrator-subset controls

On the primary `K=12` symmetric-mean route, preregister:

- all 43 unique calibrator CIDs (primary);
- the even and odd members of the lexicographically sorted unique-CID list;
- 43 leave-one-CID-out deletions, removing every light-curve row of that CID.

Using exact common-data covariance of the resulting linear scale estimators, require every
even/odd and leave-one-CID-out difference from the all-CID result to be within five of its own
standard deviations. These are robustness controls, not alternative physical scales.

### Covariance-serialization control

Retain the raw Pantheon+ asymmetry already documented by G277. In addition to the primary symmetric
mean, repeat with the reflected lower and reflected upper triangle. Require every resulting `a_K`
to differ from the primary route by at most `1e-4` magnitude. A larger difference is a
serialization-sensitive landing.

## Frozen DES prediction and score

For each resolution,

\[
\mu_{\rm pred}(z)=25+a_K+10\log_{10}(1+z)+S_K(\log(1+z)).
\]

Propagate the full Pantheon+-derived covariance of `(a_K,theta_K)`, including their correlation,
into the DES prediction and add it to the G236 DES covariance. No DES parameter is fitted. Record

\[
\chi^2_{\rm DES}=r^TC_{\rm total}^{-1}r,
\qquad \nu_{\rm DES}=1623,
\]

and call the strict published-normalization check adequate only if

\[
\chi^2_{\rm DES}\le1623+5\sqrt{2\cdot1623}.
\]

Because DES `MU` carries a published `H0=70` convention, failure is a scoped absolute-normalization
or transfer mismatch, not a rejection of the metric-native reciprocal kernel. G236 remains the
separate relative-shape check.

## Preregistered landings

1. `CONDITIONAL_ONE_SCALE_ATTACHED__DES_NO_RETUNING_CHECK_ADEQUATE` if all primary calibration,
   resolution, subset, serialization, and primary DES gates pass.
2. `CONDITIONAL_ONE_SCALE_ATTACHED__DES_PUBLISHED_NORMALIZATION_MISMATCH` if the scale gates pass
   but the primary DES gate fails.
3. `SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE` if the primary scale exists but a frozen
   resolution, subset, or serialization gate fails.
4. `PANTHEONPLUS_CEPHEID_SCALE_ATTACHMENT_INADEQUATE` if a primary calibration gate fails.
5. `REGRESSION_OR_IMPLEMENTATION_FAILURE` if frozen G236 values or source hashes are not reproduced.

## Maximum conclusion

At most, G278 may report one conditional empirical homothety scale for the frozen G236 state and a
held-out DES consistency or mismatch under the release normalization. It may not claim a derived
UDT history, native radiative transfer, a fitted kernel, angular physics, `X_max`, CMB closure, or
canonization.

## CMB-temperature note, not used by G278

The user's proposed later thermal anchor is retained as the transparent conditional relation

\[
1+z_T=\frac{T_{\rm source}}{T_{\rm obs}},
\qquad
T_{\rm source}=3000\,\mathrm K,
\qquad
T_{\rm obs}=2.725\,\mathrm K,
\]

so `1+z_T ~= 1100.9` and `phi_T ~= 7.00`. It does not participate in the G278 scale estimate.
