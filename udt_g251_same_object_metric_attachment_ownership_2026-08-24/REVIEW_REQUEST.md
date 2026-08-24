# G251 repair-only follow-up review request

Review only the sealed intake and do not continue the research.

## Question

Do the preregistered R1/R2 repairs close the two certification defects in the retained G251
scientific landing without changing its question, candidate census, sources, classifications, or
conclusion?

## Required checks

1. Verify the sealed scope and every payload hash.
2. Verify all 18 rows expose Boolean `E/I/C/W` fields plus nonblank exact source, locator, and
   evidence fields for all 72 legs.
3. Verify every locator resolves inside an exact source in `SOURCE_MANIFEST.tsv` and that the
   independent implementation rebuilds the byte-identical ledger digest without importing
   production code or output.
4. Run the registered production, independent, hostile, sealed-premise, and package no-write
   replays. Confirm the four new hostile ledger mutations are caught.
5. Verify the sealed premise-registry replay checks the exact 233-row registry and load-bearing
   G249/G250 rows, while `COMMANDS.md` accurately distinguishes it from the broader repository-only
   startup verifier.
6. Confirm the landing, 18/7/3/0 census, zero observational values, zero fitted coefficients, and
   no history/anchor selection are unchanged.

Review only R1/R2 and the retained bounded landing. Do not widen the scientific question or
continue the research. Return `REPAIRS_ACCEPTED`, `REPAIRS_INCOMPLETE`, or `REJECT`, with exact
remaining defects.
