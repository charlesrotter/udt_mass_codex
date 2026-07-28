# P01 production attempt 01 — preserved numerical-gate failure

Status: `FAILED IMPLEMENTATION GATE; NO SCIENTIFIC VERDICT`

The first production launch stopped after writing the shell 0.03 checkpoint.
Every registered local invariant was finite, but the implementation calculated
the nonfinite fraction as `1 - finite_count / point_count`.  IEEE-754 division
made that expression `1.1102230246251565e-16`, rather than exact zero, for each
configuration.  The fail-closed `> 0` test therefore marked all 1,024 rows
unresolved and correctly stopped the run.

The correction changes only that expression to
`nonfinite_count / point_count`.  It does not change the coframe, curvature,
sampling, thresholds, or interpretation.  The failed checkpoint is preserved
without overwrite under `failed_production_attempt_01/`:

| file | SHA-256 |
|---|---|
| `ATLAS_shell_0030_N1024_T17_X33_MEXP64.npz` | `8ae5106079cd1abbb1faaed3fc7441fd1598f181f1ecef8b8d67272c449f2334` |
| `ATLAS_shell_0030_SUMMARY.json` | `4a122753ee3818be58ca685c48834bcb4acc83b72b37afe271456d1f0ee0ad09` |

This attempt is excluded from atlas counts and may not be cited as a metric
outcome.  Production restart must use new root-level checkpoint paths and must
again pass all registered controls and stop gates.
