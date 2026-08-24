# G245 append-only banking integration preregistration

Date: 2026-08-24

## Trigger

G245 was preregistered, derived, sealed, and externally accepted against the exact 227-row premise
registry whose SHA-256 is frozen in `SOURCE_MANIFEST.tsv`:

```text
bb2bbc2c3574dc0c10845c4472d00b10f64459bddc990859b8b830857c92deb1
```

Banking the accepted result requires one append-only `G245` row at the head of the live registry.
That live 228-row registry must coexist with exact verification of the frozen pre-G245 source bytes.

## Authorized mechanical integration

The G245 verifier and intake builder may recover their preregistration registry as follows:

1. require the header and exactly one `G245` row;
2. treat rows before `G245` as later append-only descendants;
3. reconstruct the historical registry from the header plus every row after `G245` in unchanged
   byte order;
4. require that reconstruction to hash to the frozen digest above.

The same suffix rule may replace G244's one-self-row helper so G244 continues to reconstruct its
exact pre-G244 registry after G245 and later rows are banked. The live premise verifier separately
guards the exact row count, unique IDs, current rows, startup surface, and every load-bearing G245
artifact; the package helpers do not authorize arbitrary live rows.

The live verifier and startup surface may then advance from 227 to 228 rows and G166--G244 to
G166--G245. They must guard the exact bounded landing, external repair-only acceptance, local cone
typing, G188/G244 induction, full-phase caustic boundary, no-fit/outcome boundary, and next gate.

## Forbidden changes

This integration may not change any saved scientific result, classification, theorem, witness,
tolerance, earlier registry row, historical source digest, or observational boundary. It may not
select a ray, source, endpoint, observer population, global branch, detector, or physical metric
history.

Maximum conclusion: append-only premise/startup integration and exact historical provenance remain
valid. No scientific claim is strengthened.
