# G245 repair-strategy correction preregistration

Date: 2026-08-24

The first repair preregistration selected the external reviewer's option to include
`verify_current_scientific_premises.py` in the sealed intake. Before any follow-up review, the fresh
29-file intake was replayed exactly. The verifier exited at its first transitive repository
dependency (`G196 evidence missing: AUDIT_REPORT.md`). It is intentionally a repository-wide audit,
not a standalone registry checker.

Do not widen the bounded G245 intake into the full repository merely to make that command run.
Adopt the reviewer's other explicitly allowed repair:

1. Remove `verify_current_scientific_premises.py` from the sealed evidentiary command block.
2. List both the premise verifier and `pytest -q` as repository-only gates that passed before
   sealing but are not replay commands inside the bounded intake.
3. Remove the verifier from `SOURCE_MANIFEST.tsv` and restore the package's exact source count to
   five.
4. Include this correction record in the new sealed intake.
5. Require all four G245 no-write commands to replay exactly in the sealed root.

No scientific output, theorem, classification, source authority, or observational boundary may
change. The repair-only follow-up remains limited to command-list self-containment and the unchanged
bounded landing.
