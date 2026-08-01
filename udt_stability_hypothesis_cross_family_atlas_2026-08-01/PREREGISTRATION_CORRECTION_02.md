# Preregistration correction 02 — load-bearing source admission

Date: 2026-08-01

The original preregistration at `3ae58ba` and family-partition correction 01 at `aa8413d` remain
unchanged. A fresh cold audit found that three records cited as controlling anchors in the primary
atlas were absent from the frozen 1,466-path source universe:

- `PONDER_MATH_ELEGANCE_2026-07-31.md` — original hypothesis formulation;
- `udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md` — ring/completion adjudication;
- `udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv` — machine-readable ring-family ledger.

Using any of those records load-bearingly without admitting and hashing it violates the source
freeze, even if the record is tracked and its claim is reported correctly. Before changing the
source inventory or any result record, this additions-only correction therefore freezes those exact
three paths as a third source layer named `CONTROLLING_ANCHOR_ADDITION_CORRECTION_02`.

The effective source universe becomes exactly **1,469 sorted unique paths**:

- 1,424 inherited parent-audit sources;
- 42 complete parent-package paths;
- 3 controlling-anchor additions named above.

The verifier must require all 18 controlling anchors to occur in the effective source universe with
matching Git blobs and SHA-256 values. It must reject a missing or extra addition, overlap between
source layers, a count other than 1,469, or any attempt to hide this post-preregistration repair.

This correction changes no family, premise, claim, outcome label, algebra, source meaning, or
conclusion ceiling. If adding the three records changes the primary outcome, exposes a conflicting
source, or fails independent semantic review, the allowed result is
`SOURCE_CONFLICT_OR_SCOPE_BROKEN`, not the currently proposed atlas outcome.
