# Gradient-Incidence Precision Correction

Date: 2026-07-21

Status: `PREREGISTERED_BEFORE_WORDING_AND_CONTRACT_CORRECTION`

During the fresh review's raw-row inspection, the aggregate 7,840
`SPLIT_ACROSS_BOTH_PLANES` family incidences was decomposed by original numeric status:

- 7,839 `NUMERIC_CLASSIFIED`;
- 1 `NUMERIC_UNCERTAIN` (`V007_MA_B2_P2`, `M01_R`);
- 0 `WHOLLY_IN_ONE_PLANE`;
- 0 `WHOLLY_IN_COMPLEMENT`.

The aggregate census and every raw scientific row are correct. However, `AUDIT_REPORT.md` currently
calls all 7,840 incidences certified, and `INTERACTION_RULE_LEDGER.tsv` associates the 7,840 count
with “registered classified cases.” Those phrases overstate one retained margin.

Correction contract:

1. preserve every scientific artifact and the fresh review unchanged;
2. state 7,839 classified split-across incidences plus one retained uncertain split-across incidence;
3. keep the zero wholly-contained counts;
4. extend the package contract to enforce the 7,839/1 decomposition;
5. do not alter the bounded observation that every classified incidence crosses both sides.
