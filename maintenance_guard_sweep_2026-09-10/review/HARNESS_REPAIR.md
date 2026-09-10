# Reviewer harness repair history

The first independent probe command failed before executing a guard because the
reviewer assumed the exact registry header was `id`; its actual header is
`premise_id`. The failure stdout/stderr/command are preserved in
`g349_independent_probes.{stdout,stderr,json}`. This is a reviewer fixture defect,
not a candidate defect or scientific failure.

Initial harness SHA-256:
`2e4fecace572dffa74099c6c5d310126fb066fd823639e351b9b3b08357739e7`.
Its exact source is reconstructable from the repaired harness by replacing the
single expression `row["premise_id"] == "G349"` with `row["id"] == "G349"`.
No other source change was made between this first failed invocation and the
repaired probe run. The repaired invocation has a distinct output prefix so
the failed evidence is not overwritten.
