# Independent-Verifier Anchor-Label Correction — Preregistration

Date: 2026-07-22

The first independent verifier run correctly selected and recomputed one anchor from each of
`FOUR_LINES`, `LINE_PLUS_THREE`, and `TWO_PLUS_TWO_LINES`. Its output row construction mistakenly
used the loop variable left after the selection loop, so all three result rows reported the final
label `TWO_PLUS_TWO_LINES`.

The original `VERIFICATION_RESULT.json` and `VERIFICATION_TRANSCRIPT.txt` will be preserved under
`PRE_VERIFIER_LABEL_CORRECTION_*` names before the code edit.

Allowed correction:

- replace the output field value `motif` with the selected row's own `row["motif"]`;
- rerun the complete verifier and all catches;
- require the recomputed anchor labels to be exactly one each of the three preregistered motifs;
- require all residuals, counts, stage gates, source hashes, and catches to continue passing.

No production result, scientific classification, threshold, candidate, source, or stage gate may
change under this correction.
