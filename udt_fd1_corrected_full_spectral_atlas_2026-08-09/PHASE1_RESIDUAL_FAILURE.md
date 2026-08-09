# Phase-I first production return — residual gate failure preserved

Date: 2026-08-09  
Status: `NUMERICAL_CERTIFICATION_FAILURE`; no scientific atlas verdict

The complete 462-row blind census ran, but the preregistered normalized-wall-residual gate failed.
The output is preserved unchanged as `corrected_full_atlas.json` with SHA-256
`59842d806439827cfd385fb46ea3cfee757b7d24a822674c6fc872a1b2eb160f`.

Passed aggregate gates:

- 462 exact rows: 420 nonzero-mixing spectra plus 42 zero-limit controls;
- eight positive, strictly ordered roots in each carried channel;
- exact q=0 splitting, maximum error `3.456079866737127e-11`;
- exact Neumann m=0 zero-mode bookkeeping;
- no observational peak/trough data loaded.

Failed gate:

- maximum normalized wall residual `4.4994475719329153e-05`, versus `<2e-8` required;
- 54 of 1,260 row/channel maxima failed;
- every failure is Dirichlet at `q/qcrit=0.95`, concentrated at small hbar and frequencies as low
  as order `1e-4`.

The frozen Brent absolute tolerance was `1e-11`.  A diagnostic reroot of the worst first frequency,
using the same equation, endpoint chart, integration tolerances, and original sign bracket but a
stricter root tolerance, changed

```text
omega: 0.0002468540967554231 -> 0.0002468540985009238
delta omega: 1.746e-12
normalized residual: 4.499e-05 -> 6.606e-13
```

Thus the observed failure is consistent with absolute root-refinement precision amplified by the
very long near-critical optical interval.  This diagnosis does not certify the other roots and does
not authorize silently replacing the failed artifact.  The next action, if preregistered, is a
strict-tolerance reroot/replay retaining the same physical census and the original `<2e-8` gate.
