# A2 INFLIGHT STATE (advances at every pipeline step; model-handoff safety)

Contract: PREREGISTRATION.md (frozen). Staged banking order TP2-1 -> TP2-2 -> TP2-3 -> TP2-4.

- [x] TP2-1 BANKED (P1a-P1j; phi-forcing MODE-UNIFORM INTACT; full D_x + D_y operators; mirror layer)
- [x] TP2-2 BANKED (P2a-P2k; R_m survives coordinate / chart-slack projected; reading-independence; P2h fork composition)
- [x] TP2-3 BANKED (P3a-P3g; embedding EXACT at banked layers; P3b mirror reaches mode zero; identity verbatim; EH placement)
- [x] TP2-4 BANKED (C1a/C1b/C1c/C2a + coverage; C-1 PASS, C-2 PASS, F-P7 not fired)
- [x] derive_angular_A2.py: 38/38 (27 SUBSTANTIVE + 11 GUARD), exit 0, deterministic (verified), < 4 s CPU
- [x] EXACT_DERIVATION.md complete; ANGULAR_A2_LEDGER.tsv (19 COMPONENT + 5 CONSTRAINT + 2 ALPHABET rows);
      angular_A2_results.json; DERIVATION_STDOUT.txt; DECISION_SURFACE_UPDATE.md; AUDIT_REPORT.md (verifier OPEN)
- [x] Final derivation report delivered (<= 50 lines)
- [ ] NEXT PIPELINE STEP (driver): blind adversarial verifier (zero-context; phi-forcing + R_m survivals HARDEST;
      C-1 with own parser); then amendments + SAME-verifier closure; then four-check -> bank + push. DO NOT COMMIT before that.

Outcome class: OA2-1. Falsifier events: none fired (F-P7 not fired; G4 F-P1 scan clean).
