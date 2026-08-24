# G243 audit — reciprocal SNe radial spline representation

Date: 2026-08-24

Status: `EXTERNALLY_ACCEPTED_NO_FREEZE__LOCAL_TURNING_CANDIDATE_RETAINED`

## Landing

```text
CROSS_ROUTE_OR_FULL_COVARIANCE_FAILURE__NO_FREEZE
```

## What was learned

SNe redshift enters directly through reciprocal depth,

\[
\phi=\log(1+z),
\]

without an angular orchestra term. Using only the two processed, de-overlapped SNe releases and
their full retained covariances, two independent numerical routes choose the same interior smooth
radial candidate (`K=48`, `alpha=0.1`). Its coefficients agree to `1.33e-12`.

The radial values are comparatively insensitive near the selected resolution, but their
derivatives are not. The local candidate has four increasing intervals and several small turning
regions. G243 retains those turns rather than imposing monotonicity.

## Why it is not frozen

The preregistration required every one of 485 candidates to agree across routes within absolute
`1e-7` in raw chi-square and GCV. After an exact three-mode nullspace repair, all GCV rows pass,
the selected curve passes very tightly, but 29 extreme smoothing rows still miss the raw
chi-square threshold. The worst miss is `9.17e-6`.

The original gate therefore forces `NO_FREEZE`. This is a numerical certification ceiling, not a
claim that reciprocal redshift failed or that no physical radial history exists.

## Safeguards that passed

- all eight source hashes are frozen;
- the exact 768 Pantheon and 1,623 DES rows are retained;
- full covariance is load-bearing;
- the two release offsets are live and cannot be collapsed;
- the alpha and basis census remained fixed;
- no monotonicity condition was imposed;
- no angular, BOSS/BAO, CMB, `X_max`, P1, G116, G189, Lambda-CDM distance, or protected package
  entered the construction;
- production and independent implementations use different covariance assemblies and different
  positive-block eigensolvers.

## What remains open

- a certified smooth radial representation suitable for global inversion;
- whether the observed turns are processed-data noise, residual release systematics, the temporary
  transfer interface, or real structure;
- a native UDT radiative-transfer law;
- any angular response, physical history, `X_max`, BAO, or CMB conclusion.

## Maximum conclusion

G243 establishes that reciprocal \(\phi\) supplies SNe redshift directly and identifies one
strongly reproduced SNe-only local radial candidate. It does not freeze that candidate as a
physical or globally invertible UDT history.

## External review

Fresh external Codex `gpt-5.4` review accepted the bounded landing without requesting repairs:

```text
G243_NO_FREEZE_ACCEPTED__LOCAL_TURNING_CANDIDATE_RETAINED
```

The reviewer independently recomputed the sealed manifest, reproduced the 29 controlling
raw-chi-square misses and worst row, confirmed the exact-nullspace repair, and retained the
`K=48`, `alpha=0.1` curve only as a local observational candidate. See `EXTERNAL_REVIEW.md` and
the exact response in `EXTERNAL_REVIEW_RAW.md`.
