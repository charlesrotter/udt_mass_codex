# Edge-Uncertainty Accounting Correction

Date: 2026-07-21

Status: `PREREGISTERED_BEFORE_CORRECTED_REPLAY`

The first complete 6,144-configuration return produced the exact registered coverage and zero
non-uncertain family discordances, but `ATLAS_RESULT.json` counted every transformed edge-label
difference in one field named `nonlinear_edge_discordances`. That aggregate included edges whose
source or destination family was explicitly `NUMERIC_UNCERTAIN`. It therefore did not implement the
preregistered distinction between a retained numerical margin and a certified chart discordance.

The first return is preserved as `PRE_EDGE_UNCERTAINTY_*`. Its load-bearing hashes before replay were:

| artifact | SHA-256 |
|---|---|
| `ATLAS_RESULT.json` | `2ede98076910422249b90260f0873c58a5a33c7008eba27f4775c667d8b33a01` |
| `NUMERIC_MARGIN_LEDGER.tsv` | `9eb973bbfcb56502c451f89464b51229b3dab4a0d55ba8e201d44b9a39007971` |
| `COVERAGE_LEDGER.tsv` | `1e8c06a7009aa739866407589c5b392b74901953125884211f1be91e67d2f1a6` |
| `CATCH_PROOFS.tsv` | `dcf238df7d22a207eecdf82de9cb5005562d9c01d5b1cfe18fc78463b4fc6580` |
| `FAMILY_MOTIF_ATLAS.tsv.gz` | `af8f4f68deb95fd7136f605d0a70989cad6b6a589695117086fc617942332926` |
| `EDGE_INTERACTION_ATLAS.tsv.gz` | `6014ca6bb750cec3920ed65895e8ff10f1fa40e3778b36ae286b75cbb87b28b4` |
| `NONLINEAR_FAMILY_COMPARISON.tsv.gz` | `fa27912f151d06f32ed376fceb2c3df9d4fb14ddeaad2668bbce5077c5e25b17` |

The corrected replay must keep the same 31-family registry, inputs, classification algorithms,
tolerances, and outputs while splitting edge comparisons into:

- `nonlinear_edge_nonuncertain_discordances`;
- `nonlinear_edge_uncertain_comparisons`;
- `nonlinear_edge_uncertain_discordances`;
- `nonlinear_edge_total_label_differences`.

An edge comparison is uncertain if any of its four participating family rows—original source,
original destination, transformed source, or transformed destination—is uncertain. Only the first
field can support or fail the registered covariance conclusion. Alignment comparisons receive the
same fail-closed distinction. No uncertain comparison may be discarded, retuned, or promoted.

