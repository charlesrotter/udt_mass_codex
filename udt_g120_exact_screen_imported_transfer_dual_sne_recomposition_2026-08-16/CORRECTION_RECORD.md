# G120 correction record

## Pre-output JSON repair

The first execution completed the numerical calculations but stopped before writing a result
because one NumPy boolean was not JSON serializable. All check values were converted to ordinary
Python booleans. No equation, input, tolerance, or likelihood calculation changed.

## Algebraic gate repair

The next execution returned `G120_GATE_FAILURE` only because the exact identity

```text
sqrt[Z^3 R^2/(1/Z)] = Z^2 R,  Z>0, R>0
```

was tested by an unregistered absolute floating-point threshold at a diagnostic point as large as
`Z=1000`. Its absolute residual was `1.1641532182693481e-10`, about machine-relative precision at
the resulting scale, versus an implementation-added `1e-10` threshold. The preregistration called
for an *algebraic* verification and registered no floating tolerance for this identity.

The gate was therefore repaired to use exact SymPy simplification under `Z>0,R>0`. The floating
residual remains in the output as a diagnostic. No observational threshold, curve, likelihood,
parameter, or physical premise changed.

## Pre-review vacuous slope assertion repair

The first production implementation checked the origin-slope label with a tautological comparison
of `2 X_eff` to itself. Before adversarial review and banking, this was replaced by exact symbolic
differentiation of the registered radius expression. Exact derivative, origin-slope, and formal-
limit residuals are now all required to vanish. The numerical positive-derivative grid remains an
additional diagnostic. No result, parameter, or observational gate changed.

## Fresh adversarial review repairs

The first fresh read-only adversary returned `REPAIR_REQUIRED` while independently reproducing the
core algebra and both likelihoods. It required:

1. explicit restriction of the conditional P1 radius interpretation to `Z>=1`;
2. the nonvacuous symbolic slope/limit repair already implemented above; and
3. noncircular package replay against pre-run saved bytes in a temporary package copy.

All three are implemented. Its optional hardening was also adopted: method-description booleans in
the independent replay were moved out of the pass/fail checks, and Pantheon+'s calibration-sample
and 1365-versus-1366 degree-of-freedom provenance is explicit.
