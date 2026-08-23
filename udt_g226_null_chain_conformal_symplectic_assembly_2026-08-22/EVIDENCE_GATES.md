# G226 evidence gates

Date: 2026-08-22

| Gate | Status | Evidence |
|---|---|---|
| Preregistered before computation | PASS | commit `1f60deb0` |
| Exact bounded regime declared | PASS | `MAP.md`, `PREMISE_LEDGER.tsv` |
| Production algebra | PASS | 28 exact checks in `DERIVATION_RESULT.json` |
| Independent implementation | PASS | 20,000 exact-Fraction chains; 200,007 assertions |
| Hostile catches | PASS | 8/8 in `CATCH_PROOF_RESULT.json` |
| Caustic-safe full phase | PASS | singular position block, full determinant one control |
| Middle-screen gauge covariance | PASS | independent incoming/outgoing middle gauges cancel |
| Affine-generator covariance | PASS | exact cancellation under constant positive rescaling |
| No-persistent-output package replay | PASS_REPAIRED | `/dev/null` component replay compares exact stdout JSON and leaves package and sources byte-identical |
| Frozen source hashes | PASS | 13-source manifest verified with path containment |
| Fresh adversarial review | ACCEPTED_WITH_REPAIRS | no scientific defect; two evidence-layer repairs only |
| Repair-only follow-up | PENDING | must verify R1/R2 before final banking |
| Premise audit | PASS_BOUNDED | no fit, profile, `X_max`, transfer, source, or protected input |

Current maximum grade:
`DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED__PACKAGING_REPAIRS_PENDING_FOLLOWUP`.

The aggregate verifier is a bounded mechanical gate. It checks enumerated counters, exact replay
equality, required evidence presence, selected scope tokens, source hashes, and evidence-byte
nonmutation; it is not a semantic proof of every narrative sentence.
