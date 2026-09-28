# Conditional shape/derivative comparison, before numerical BAO targets

2026-09-28, parent construction. Public DESI paper summaries and product schemas
have been exposed; the mean/covariance files have not yet been opened. This is
an additional consistency check, not a pristine blind confirmation. No SNe
coefficients have been supplied to the geometry lane before its initial freeze.

Question: do the six frozen empirical SNe functions also agree with a shape/
derivative combination constrained by DESI DR2 BAO, under the following explicit
comparison assumptions? This does not test a selected native UDT universe.

Supplied comparison class: spatially flat homogeneous conformal geometry with
comoving source/observer congruence, conventional optical distance relation and
conventional common comoving ruler/template interpretation of compressed BAO.
These are `free-and-explored` controls and declared external interfaces, not
adopted UDT dynamics or derived ruler physics. No Einstein equation, calibrated
sound-horizon size, Hubble-rate value or matter density is inserted.

Let x=ln(1+z), F(x)=H0 D_M/c_E, E=H/H0. Conditional null incidence gives
F'=exp(x)/E, hence F_AP=D_M/D_H=exp(x)F/F'. The geometry lane must independently
verify this relation and hypotheses before its numerical use. F and F' must be
positive on the compared interval. The normalization cancels. A spectral clock
ratio does not by itself identify a physical distance or prove this comparison
class is UDT's selected geometry.

Source: official DESI DR2 products link to
https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2 . Pin the
repository commit and exact files before parsing them. Use the combined mean
and covariance; retain anisotropic D_M/r_d and D_H/r_d pairs. Do not turn the
isotropic BGS D_V datum into a ratio. Compare within the fitted SNe redshift
domain; any outside-domain point is shown separately as extrapolation and is
excluded from the headline comparison statistic.

No new function family or fitting to BAO is authorized in this comparison.
Take each frozen SNe fit as supplied, with its coefficient covariance. Derive
the BAO ratio covariance by the explicit ratio Jacobian acting on the full
published covariance. Check this delta approximation with 100000 correlated
Gaussian draws, fixed seed 9282026, recording denominator positivity, mean bias
and variance differences. It is an approximation to a published Gaussian
likelihood, not a reconstruction of raw galaxy observations.

Propagate SNe coefficient covariance through the ratio's parameter Jacobian,
retaining correlations across redshift. Quote the residual quadratic form using
the sum of BAO and prediction covariance only under an explicit zero cross-probe
covariance assumption. Do not claim an exact chi-square sampling distribution
or calibrated discovery significance; record local Gaussian/linearization limits.
No threshold selects a new physics law. Pointwise curves may be shown even when
the covariance propagation is unreliable, with the statistic then withheld.

Implementation refinement before receiving SNe fit coefficients: use 20000
coefficient-Gaussian draws, seed 9282027, to diagnose nonlinear prediction
uncertainty. Require at least 99.9% of draws to have a positive denominator at
every included point, Monte Carlo marginal variances within 20% of the linear
approximation, and mean biases below 0.2 linear standard deviations. Treat a
zero-variance exact control separately. If these checks fail, withhold its
quadratic statistic rather than clipping draws or treating a heavy tail as
Gaussian. These are approximation diagnostics, not scientific acceptance cuts.
They were fixed after the BAO means were inspected, before SNe coefficients or
the resulting cross-probe residuals; this refinement is not outcome-blind.

Report all six families, failures, derivative-domain issues, extrapolation and
covariance approximation quality. Keep empirical/kinematic agreement separate
from native derivation, solar-system tests and asymptotic completion. Preserve
script, inputs, stdout/stderr, result/plot and checksums. CPU <=2 threads /2 GiB,
each subprocess <=600s; no additional light-curve or galaxy-processing pipeline.
