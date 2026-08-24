# G244 append-only banking integration preregistration

Date: 2026-08-24

## Trigger

G244 was preregistered, derived, sealed, and externally accepted against the exact 226-row premise
registry whose SHA-256 is frozen in `SOURCE_MANIFEST.tsv`:

```text
1cad6bf0a437157a87013f0ac718a6e54213f093a6088670ed5ad7e233668126
```

Banking the accepted result now requires one append-only `G244` row in that registry. The package
must continue to verify its historical source bytes after its own row is present.

## Authorized mechanical integration

The G244 package verifier and review-intake builder may treat
`CURRENT_SCIENTIFIC_PREMISES.tsv` specially:

1. read the current registry bytes without editing them;
2. require exactly one row beginning `G244\t` after banking;
3. remove exactly that one row in memory;
4. require the resulting bytes to hash to the frozen preregistration digest above;
5. fail closed on every other registry difference.

Before the row is appended, the exact current registry hash must continue to pass directly. This
permits the same code to verify both the preregistration state and the append-only banked state.

The live premise verifier and bounded startup surface may then be updated from 226 to 227 rows and
from G166--G243 to G166--G244. They must add exact G244 guards for:

- the externally accepted conditional area/shape theorem;
- the orientation-line parity correction;
- zero fitted angular coefficients;
- closed BOSS/CMB outcomes;
- the source/catalogue/history ceiling;
- package replay and evidence presence.

## Forbidden changes

This integration may not change:

- any G244 saved scientific result, formula, witness, tolerance, or classification;
- any earlier premise row;
- the historical source manifest;
- observational-outcome access;
- the physical-history, source, detector, transfer, critical, or `X_max` ceilings.

Maximum conclusion: append-only premise/startup integration and exact historical provenance remain
valid. No scientific claim is strengthened.
