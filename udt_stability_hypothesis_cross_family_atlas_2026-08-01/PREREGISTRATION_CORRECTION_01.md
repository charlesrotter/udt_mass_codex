# Preregistration correction 01 — effective family partition

Date: 2026-08-01

The committed preregistration at `3ae58ba` is preserved unchanged. During mechanical assembly, its
broad F01 wording (“S-i massive ... cells and chains”) was found to overlap F06's explicitly frozen
empty massive closed postures. That conflicts with the same preregistration's no-double-count rule.

The effective partition is therefore narrowed before banking:

- **F01:** only nonempty or conditionally nonempty mixed/open `S-i` branches on which a stability
  form is evaluated. Massive cyclic one-cell and double-crease empty postures are excluded.
- **F06:** only the exact empty massive cyclic-one-cell and double-crease postures. They are
  existence controls and never stability-tested survivors.
- **F05:** massless cyclic rings and conditional multi-cell mixed-sign ring closure; the F06 empty
  massive one-cell posture is excluded.

No family is added or removed. No source, outcome label, premise, conclusion ceiling, or favorable
result changes. `FAMILY_PARTITION_LEDGER.tsv` is the machine-readable effective partition. The
verifier must reject any repeated partition key or any return of F06 empty postures to F01/F05.
