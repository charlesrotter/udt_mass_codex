# External-review repair preregistration

Date: 2026-08-01  
Base outcome preregistration: commit `9c50c53`  
Accepted external-review file SHA-256: `a6d8801337c9090f2fc139c6ab80ff0de6c1c1de18ead5dd369f815ca9843345`  
External verdict before repair: `PASS-WITH-REQUIRED-REPAIRS`

## Exact repair authorized by the review

The only mandatory repair is to distinguish the frozen primary SymPy 1.14.0 run from the external
reviewer's own replay environment. In `AUDIT_REPORT.md`, replace the evidence bullet

```text
24/24 exact SymPy 1.14.0 checks;
```

with wording that says the frozen `RESULT.json` records that run, that its replay requires the pinned
SymPy 1.14.0 dependency, and that the external reviewer independently replayed the non-importing
verifier and scratch algebra under its available environment.

## Permitted closure edits

After applying that exact repair:

- mark the fresh external semantic review complete while retaining the bounded caveats;
- record the external verdict, independent witnesses, environment mismatch, and accepted repair in
  the audit report, status ledger, and machine-readable result/verification records;
- extend the verifier with fail-closed checks for the reviewer SHA-256, repaired wording, retained
  scientific maximum, and absence of a stronger native carrier/action claim;
- add a package manifest and deterministic manifest verifier after all evidence files are final;
- update live startup/navigation controls only after the repaired evidence package passes every gate.

No equation, identity, candidate ruling, premise status, source classification, carrier/action
status, or proposed next scientific test may change. Any additional mathematical or scientific
repair requires a new preregistration.
