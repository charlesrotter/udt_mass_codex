# Phase R1B audit index

Phase R1B archives only preregistered, superseded pre-2026-07-01 root Markdown. It does not authorize active-lane migration or any physics, Python, data, manifest, or hard-frozen change.

## Audit order

1. [`R1B_PREREGISTRATION.md`](R1B_PREREGISTRATION.md) and [`PREREGISTERED_CANDIDATES.tsv`](PREREGISTERED_CANDIDATES.tsv) freeze the 99-file universe at `4b22647`.
2. [`base_census/`](base_census/) and [`base_forensic_census/`](base_forensic_census/) hold the corrected inbound-source and dependency evidence.
3. [`adjudication/PREMOVE_ADJUDICATION_REPORT.md`](adjudication/PREMOVE_ADJUDICATION_REPORT.md) gives all 99 individual rulings and the safety-stop result.
4. [`migration/`](migration/) records two R100 moves, one exact path substitution, one intentionally unchanged co-located reference, tests, and fail-closed verification.
5. [`postmove_forensic_census/`](postmove_forensic_census/) and [`postmove_operational_census/`](postmove_operational_census/) keep the two dependency views separate.
6. [`R1B_AUDIT_REPORT.md`](R1B_AUDIT_REPORT.md) and `FINAL_VERIFY_RESULT.json` are the final audit surface.

Generated R1B records did not participate in candidate selection or adjudication.
