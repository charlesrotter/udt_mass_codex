# Post-Outcome Numerical-Margin Escalation

Date: 2026-07-21

Status: `POST_OUTCOME_TARGET_SET_PREREGISTERED_BEFORE_REPLAY`

The outcome-blind 384-configuration verifier passed 35,712 classifications but its hash-selected set
contained no production rows marked uncertain. This escalation is not blind coverage. Its target is
mechanically frozen as every unique `(configuration_id, family_id)` appearing in the complete
162-row `NUMERIC_MARGIN_LEDGER.tsv`, regardless of probe, motif, family, or expected result.

For every target identity, the independent verifier implementation must recompute the original and
both nonlinear classifications and compare all registered motif fields and saved status/accounting
rows. No tolerance changes are allowed. Any disagreement remains an implementation discordance and
lowers the package grade; no identity may be omitted.

Pinned input hashes:

- `NUMERIC_MARGIN_LEDGER.tsv`: `9eb973bbfcb56502c451f89464b51229b3dab4a0d55ba8e201d44b9a39007971`
- `FAMILY_MOTIF_ATLAS.tsv.gz`: `af8f4f68deb95fd7136f605d0a70989cad6b6a589695117086fc617942332926`
- `NONLINEAR_FAMILY_COMPARISON.tsv.gz`: `fa27912f151d06f32ed376fceb2c3df9d4fb14ddeaad2668bbce5077c5e25b17`

