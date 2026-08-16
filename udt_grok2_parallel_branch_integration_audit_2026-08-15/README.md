# `grok2` parallel-branch integration audit

Date: 2026-08-15

Status:

```text
INTERNALLY_VERIFIED_WITH_CAVEATS
__PARTIAL_CONCEPTUAL_INTEGRATION_ONLY
__NO_BRANCH_MERGE
```

This package audits the four commits unique to `origin/grok2` at `13921e818c0f2` against the
current `grok` evidence ledger. It does not merge the branch or import its stale startup surface.

The retained contributions are:

1. an observer-centred correction to the future BAO query, sharpened here to one observer plus
   two source directions in a redshift selection;
2. a source-level megamaser local-slope lead near 4.06 Gpc, which is numerically consonant with
   the frozen G99 P1 origin slope near 4.17 Gpc.

The audit does **not** retain the `grok2` identification of that slope with `X_max`, the chosen
`tanh` profile as a derivation, the historical `Z^2` luminosity law as unconditional, the
one-screen August `mu_lock` as the complete mixing sector, or the 2.725 K starlight-screen posit as
active physics.

Read `AUDIT_REPORT.md` first.
