# G129 bounded adversarial follow-up

`FOLLOWUP_PASS`

All repairs are verified:

1. The independent `Fraction` route reconstructs Ricci from the metric second jet, obtaining
   `R12=R21=-a` and `Ricci^2=18/25` for `a=3/5`; it no longer assumes the result.
2. The all-orders bump smoothness is correctly proved analytically via
   `u^-n exp(-1/u)->0`. Executable checks are honestly named sampled regressions.
3. Production and independent overlap catches perturb `h2,00` by `1/7`; the resulting invertible
   pullback residual is necessarily nonzero, so both catches are non-vacuous.
4. The terminal counterexample keeps `h00=-1` in both distinct regular metrics while preserving
   `phi_pair=0`.

Fresh isolated replays pass production 18/18, independent 12/12, and package verification. All
generated artifacts are byte-identical. No files were edited by the reviewer.
