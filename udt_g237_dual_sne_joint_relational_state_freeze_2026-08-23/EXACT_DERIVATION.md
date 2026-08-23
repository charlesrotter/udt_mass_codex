# G237 exact derivation — joint dual-SNe relational-state freeze

Date: 2026-08-23

## 1. Bounded question

G236 found that two de-overlapped, processed SNe releases support compatible finite-resolution
projections of one relative state on

\[
0.07077528204904217\leq\phi\leq0.7627571949083936.
\]

G237 asks only for the covariance-weighted common state implied by those two projections under the
same central-static query and imported transparent-transfer bridge. It does not fit, interpolate,
or derive a physical profile law.

The primary numerical resolution is the preregistered `K=12` grid. `K=8,16,24` are numerical
resolution controls, not alternative physical models or coefficients.

## 2. Conditional SNe state observable

The inherited conditional relation is

\[
y_c:=m_c-10\log_{10}(1+z)=5\log_{10}R(\phi)+B_c,
\qquad \phi=\log(1+z),
\]

where \(B_c\) is an independent additive zero point for release \(c\). Define the relative state
coordinate at the non-anchor knots by

\[
\theta_i=5\log_{10}\frac{R(\phi_i)}{R(\phi_0)},
\qquad \theta_0=0.
\]

The absolute ruler normalization remains open. The displayed relative ruler values are therefore

\[
\frac{R(\phi_i)}{R(\phi_0)}=10^{\theta_i/5}.
\]

This transformation is pointwise at the frozen knots. It supplies no physical interpolation
between them.

## 3. Joint estimator under the declared covariance approximation

Let the two G236 estimates at one resolution be

\[
\widehat\theta_P\sim(\theta,C_P),
\qquad
\widehat\theta_D\sim(\theta,C_D).
\]

After exact-CID de-overlap, G237 sets the unavailable cross-release covariance to zero. This is
`CHOSE_STATISTICAL_APPROXIMATION`, not a derivation of independence. Shared calibration and
processing systematics remain open.

With

\[
P_P=C_P^{-1},\qquad P_D=C_D^{-1},
\]

the common-state generalized least-squares estimator is

\[
\boxed{
C_J=(P_P+P_D)^{-1},
\qquad
\widehat\theta_J=C_J(P_P\widehat\theta_P+P_D\widehat\theta_D).
}
\]

The minimized disagreement quadratic is

\[
\boxed{
Q_J=
(\widehat\theta_P-\widehat\theta_J)^TP_P
(\widehat\theta_P-\widehat\theta_J)
+
(\widehat\theta_D-\widehat\theta_J)^TP_D
(\widehat\theta_D-\widehat\theta_J).
}
\]

Writing

\[
d=\widehat\theta_P-\widehat\theta_D,
\]

the standard GLS identity gives

\[
\boxed{
Q_J=d^T(C_P+C_D)^{-1}d.
}
\]

This equals the G236 shape-disagreement chi-square.

## 4. Direct raw-data formulation

The independent route does not read the G237 production result. For each release, let \(y_c\) be
the transformed raw released vector, \(W_c\) its retained precision, and \(A_c\) the fixed knot
basis. The simultaneous model is

\[
y_P=B_P\mathbf1+A_P\theta+\epsilon_P,
\qquad
y_D=B_D\mathbf1+A_D\theta+\epsilon_D.
\]

Writing \(b=(B_P,B_D,\theta)^T\), its normal equations are

\[
\left(X_P^TW_PX_P+X_D^TW_DX_D\right)b
=X_P^TW_Py_P+X_D^TW_Dy_D.
\]

Pantheon precision is obtained by solving its retained covariance. DES supplies a full precision;
the retained DES-only marginal precision is obtained by the omitted-block Schur complement

\[
W_{kk}^{\rm marg}=W_{kk}-W_{ko}W_{oo}^{-1}W_{ok}.
\]

The raw simultaneous estimator must equal the saved-estimate precision combination because the two
release estimates and covariances are sufficient GLS statistics under the declared block-diagonal
model. The two implementations use different data entry and linear-algebra routes.

## 5. Observed results

| K | joint raw chi-square | dof | preregistered ceiling | G236 disagreement quadratic |
|---:|---:|---:|---:|---:|
| 8 | 2188.449488 | 2382 | 2727.108679 | 11.539289 |
| 12 | 2145.854791 | 2378 | 2722.818793 | 14.409356 |
| 16 | 2135.070389 | 2374 | 2718.528664 | 18.118818 |
| 24 | 2124.469339 | 2366 | 2709.947670 | 25.679847 |

All four raw-residual gates pass.

For the frozen primary `K=12` state, the eleven non-anchor relative-state coordinates are

```text
1.2171865663  1.9217624436  2.4313539739  2.7636044410
3.0495915484  3.2348809434  3.4199890232  3.5293544916
3.5954981885  3.6997723876  3.6704314004
```

and the corresponding knotwise relative ruler display is

```text
1.7516095859  2.4229948370  3.0638732491  3.5704330028
4.0730365722  4.4358432260  4.8305636017  5.0800840566
5.2372057702  5.4948327433  5.4210857892
```

The last-bin downturn is retained exactly as observed. No monotonicity or smoothing is imposed.

## 6. Independent and hostile certification

The direct raw-data solution and saved-estimate solution agree at all four resolutions. Maximum
absolute discrepancies are:

| quantity | discrepancy | tolerance |
|---|---:|---:|
| state coordinate | `6.3994e-13` | `1e-8` |
| covariance entry | `2.7756e-17` | `1e-8` |
| joint raw chi-square | `2.4693e-10` | `1e-7` |
| raw-chi-square identity | `0` | `1e-7` |

Duplicate-input, release-swap, and weak-catalog limits pass. Five package mutations are caught:
primary resolution, row count, covariance-premise label, verification status, and cross-route
tolerance.

## 7. Exact epistemic ceiling

The result is a frozen, processed, finite-resolution observational state under:

- one bounded central-static query;
- an imported transparent-transfer relation;
- release-provided standardization and bias corrections;
- an explicitly chosen zero cross-release covariance after known-object de-overlap.

It does not derive `R(phi)`, native transfer, a complete metric history, an absolute distance scale,
`X_max`, P1, a source model, or agreement with a held-out channel. The exact maximum landing is

```text
JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS
__BLOCK_DIAGONAL_CROSS_RELEASE_COVARIANCE_CHOSEN
__NO_PROFILE_LAW_PREDICTION_OR_HELDOUT_VALIDATION
```
