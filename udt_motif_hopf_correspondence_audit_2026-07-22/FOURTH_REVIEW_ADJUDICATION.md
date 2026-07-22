# Fourth fresh-review adjudication

Date: 2026-07-22

The fourth fresh `FAIL` is accepted in full. The reviewer confirmed the repaired scientific
validator, exact toric/seed witness, all 29 attacks, premise boundaries, and `LEAD` grade. It
rejected immutable package closure because the generated raw evidence had not yet been committed and
because the production builder still rewrote the corrected ten-source lineage as the older
eight-source table.

| blocker | repair | result |
|---|---|---|
| committed tree omitted raw/generated evidence | freeze the complete registry, raw compressed ledgers, results, transcripts, reports, and manifest | clean archive contains every input required by `verify_package.py` |
| builder emitted stale eight-source lineage | add the two direct production source manifests and their exact roles to the builder | builder-generated and current ten-row lineage tables are identical |
| passing transcript lacked immutable raw hashes | generate and replay `SHA256SUMS.txt` over the complete package | raw ledgers and every load-bearing package file are authenticated |

This is an evidence-closure correction only. No raw row, count, scientific premise, status,
tolerance, or maximum conclusion changed.
