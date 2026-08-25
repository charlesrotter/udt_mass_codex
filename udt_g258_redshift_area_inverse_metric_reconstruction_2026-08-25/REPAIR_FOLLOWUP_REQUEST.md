# G258 R1 repair-only follow-up request

Review only the sealed intake. Verify only the repair preregistered in
`REPAIR_PREREGISTRATION.md` and the unchanged bounded G258 scientific landing. Do not change the
scientific question, edit evidence files, or continue the research. Run registered checks only in
the supplied writable ephemeral copy.

Required checks:

1. Confirm that `verify_package.py` and `build_review_intake.py` no longer delete, filter, or
   rewrite registry rows to manufacture a historical hash.
2. Confirm that the included `CURRENT_SCIENTIFIC_PREMISES.tsv` is verified byte-for-byte against
   `SOURCE_MANIFEST.tsv` inside the sealed intake.
3. Confirm that live-repository compatibility is limited to exact retrieval of Git object
   `a9f96360:CURRENT_SCIENTIFIC_PREMISES.tsv`.
4. Run `verify_repair.py` and all four unchanged scientific replays.
5. Confirm that the five load-bearing generated scientific artifacts retain their prerepair hashes
   and that a one-byte premise-source mutation is rejected.
6. Confirm that no scientific result, premise grade, numerical value, or conclusion ceiling changed.

Return `REPAIRS_ACCEPTED` or `REPAIRS_REJECTED` with exact findings.
