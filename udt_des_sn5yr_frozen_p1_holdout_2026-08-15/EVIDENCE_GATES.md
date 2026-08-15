# Evidence gates

1. **Preregistered — PASS WITH DISCLOSED SCHEMA REPAIR.** Commits `fbc1c9e0` and `fc2d14c6`
   froze the model, statistic, source, thresholds, secondary diagnostics, and parser before any
   likelihood. The dry gate then found the current Dovekie vector contains 1623 rather than 1635 DES
   rows. Commit `b9dbac48` changed only that count before any residual was evaluated.
2. **Full or bounded — PASS FOR THE DECLARED BOUND.** The primary covers every `IDSURVEY==10` row
   in the exact frozen 1820-row release and its full released covariance. It does not cover raw-
   light-curve reduction, event-disjoint data, every SNe catalogue, complete histories, or native
   transfer.
3. **Independently verified — PASS WITH CAVEATS.** A separate parser, precision Schur complement,
   direct-power curve, and independent shape minimizer reproduce the load-bearing numbers. A fresh
   sealed `gpt-5.4` adversary independently reconstructed the statistic from the intake-local data
   and returned `PASS_WITH_CAVEATS`; the literal `chi2_(N-1)` reference is approximate.
4. **Premises audited — PASS.** P1 choice, redshift, standardization, bias correction, covariance,
   nuisance offset, event overlap, complete orchestra, transfer, Lambda-CDM exclusion, BAO/CMB,
   `X_max`, bootstrap, action, source, matter, and mass roles are explicit.

Maximum bankable status after fresh external review:

```text
VERIFIED_WITH_CAVEATS
__FROZEN_G99_P1_NOT_REJECTED_BY_DES_DOVEKIE
__LOW_CHI2_REFERENCE_WARNING
```
