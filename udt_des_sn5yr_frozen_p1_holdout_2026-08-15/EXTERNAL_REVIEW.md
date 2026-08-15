# Fresh sealed adversarial review

Reviewer: external Codex `gpt-5.4`
Mode: cold, read-only, no internet
Intake: `/tmp/udt_g100_des_review_20260815`
Scope SHA-256: `ef696389f5ea83d8b1c9e78073d848dd039ff966104c546d1f5fffc9b1d4c32b`

## Landing

```text
PASS_WITH_CAVEATS
```

## Load-bearing numbers independently reconstructed

- `N_all = 1820`
- `N_DES = 1623`
- `n_G99 = 1.0559332414320268`
- primary `chi2 = 1444.1864417493343`
- primary `dof = 1622`
- reduced `chi2 = 0.8903738851722159`
- `offset_B = 41.70895660296955`
- upper-tail `p = 0.9993855958364408`
- lower-tail `p = 0.0006144041635591934`

The reviewer independently reconstructed the DES marginal covariance in two ways. Taking
`C_DES=(W^-1)_KK` and using the precision Schur complement
`W_KK-W_KD(W_DD)^-1W_DK` agreed to `7.45e-9` in `chi2`. The incorrect shortcut `W_KK` gave
`chi2=1451.0553337559104`, a shift of `+6.868892006576061`.

The secondary shape result also reconstructed:

```text
n_DES approximately 1.0152458
Delta-chi2=1 interval [0.9916910, 1.0397635]
chi2_best approximately 1441.5037433
Delta chi2(frozen-best) approximately 2.6826985
one-dof p approximately 0.10144
```

The reviewer accepted “modest shift, no significant tension” only for this secondary diagnostic.
The full-1820, DES-stat-only, and DES-`zHEL` secondary chi-squares also reconstructed.

## Required caveats

1. The literal `chi2_(N-1)` reference is approximate rather than exact for the released,
   collaboration-produced Hubble diagram. The vector inherits fitted global nuisance structure,
   bias corrections, and BEAMS-renormalized uncertainties. The low-chi-square result must remain a
   warning; it cannot be promoted to a clean confirmation.
2. No model outcome was visible before the disclosed `1635 -> 1623` dry-gate correction. Five raw
   public table rows had been displayed, so limited raw-data exposure preceded the final typed
   preregistration. The correction changed only source typing and the expected count.
3. “No Lambda-CDM distance import” is valid only in the direct-use sense. G100 did not calculate or
   read a Lambda-CDM distance, chains, `MUMODEL`, `MURES`, or `MUPULL`; the released `MU` still
   inherits SALT3, host, selection, BEAMS, and bias-correction processing.
4. The first sealed bundle contained local data copies, but its replay scripts still defaulted to
   the repository scratch-disk path. This was an operational portability defect, not a numerical or
   scientific blocker. The reviewer therefore performed its own intake-local replay.

No silent primary fitting freedom, secondary repair of the primary, covariance double counting,
row-order misuse, or numerical/type blocker was found.

## Maximum accepted conclusion

One frozen conditional G99 P1 curve survives this DES-SN5YR/Dovekie release without a
large-residual rejection when evaluated with the correct DES marginal covariance. The primary
goodness-of-fit lies in a low-chi-square warning regime under only approximate `chi2_(1622)`
semantics. P1, the complete history, native transfer, absolute scale, `X_max`, and UDT generally
remain unproved.
