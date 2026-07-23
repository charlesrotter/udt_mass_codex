# Holonomy-Ledger Verifier Correction

Date: 2026-07-22

## Trigger

After the final full independent temporal recomputation passed its path, signature, complement,
threshold-conflict, and chart controls, the verifier stopped on an overbroad holonomy-ledger check.
It required every row of `BUNDLE_HOLONOMY_ATLAS.tsv` to use the completion-family phrase
`PROFILE_DEPENDENT_NOT_COMPUTED_WITHOUT_COMPLETE_METRIC`. The ledger also contains eight explicit
`FC07::M_*` monodromy controls whose correct phrase is `NOT_FIXED_BY_LATTICE_MONODROMY`.

This is a verifier schema mistake. Both row types retain Levi-Civita holonomy as open.

## Frozen correction

Before editing the verifier:

1. Require exactly twelve base completion rows `FC01` through `FC12`, each with
   `PROFILE_DEPENDENT_NOT_COMPUTED_WITHOUT_COMPLETE_METRIC`.
2. Require exactly eight `FC07::M_*` monodromy-control rows, each with
   `NOT_FIXED_BY_LATTICE_MONODROMY`.
3. Require twenty rows total and reject every other Levi-Civita holonomy status.
4. Do not change any scientific table, temporal classification, threshold, or maximum conclusion.
5. Preserve the failed transcript.
