# G123 evidence gates

1. **Preregistered:** yes — commit `41aa54b6` preceded theorem reduction and witness evaluation.
2. **Scope complete:** yes for the declared regular common-event overlap. Regular multiple
   preimages are retained as separate graph branches; nontransverse fibers are retained but remain
   an unclassified stratified relation.
3. **Independent verification:** yes — 12/12 exact Fraction checks pass without importing
   production code.
4. **Premise audit:** the pre-G123 109-row verifier passed before preregistration; the final
   G123-extended 110-row registry and startup verifier pass.

Blind review: `PASS_WITH_REPAIRS`; both implementations reproduced exactly. Repairs are registered
in `CORRECTION_RECORD.md`. Bounded follow-up returned `PASS_REPAIRS_VERIFIED`; fresh replays were
byte-identical.

Current maximum status: `BLIND_VERIFIED_WITH_REPAIRS`.
