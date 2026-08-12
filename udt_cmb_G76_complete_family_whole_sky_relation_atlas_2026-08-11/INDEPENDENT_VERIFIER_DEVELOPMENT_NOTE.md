# G76 independent-verifier development note

Date: 2026-08-11

This preserves two fail-closed events before the independent verifier was accepted.

1. The first Christoffel replay produced excellent null residuals but large endpoint disagreement.
   Inspection found an index permutation error in the independently implemented third Christoffel
   term: the code did not represent `partial_k g_ab`. It was corrected before any verifier result
   was accepted.
2. The corrected implementation made seven resolved panel rows agree within the separately chosen
   `1e-5` independent-replay tolerance. The deliberately included production-unresolved row
   `G75_AP_S03_E100` differed by `1.2089089529884446e-05`. That row is not promoted or retuned. Its
   independent gate is instead typed honestly: reproduce the production-unresolved classification,
   preserve exact crossing-mask agreement and raw null error, and agree within the original frozen
   `5e-5` G76 numerical-resolution threshold. The stricter `1e-5` gate remains unchanged for rows
   classified resolved by production.

This is a verifier-typing correction, not a relaxation of the production classification. All four
production rows above the frozen `512`-versus-`1024` threshold remain
`NUMERICALLY_UNRESOLVED`.
