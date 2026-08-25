# G252 external review

Date: 2026-08-24

Fresh external Codex `gpt-5.4` returned `ACCEPT_WITH_REPAIRS`.

The reviewer found no load-bearing scientific defect and retained the bounded conditional theorem.
It found one evidence-packaging defect: the three source verification paths worked in the
repository but did not accept the sealed `sources/` relocation. Consequently the two scientific
replays and package verifier failed inside the original sealed intake, although all 28 payload
hashes matched and the hostile replay passed.

As originally delivered, gates 3 and 4 failed for the sealed relocation. The scientific landing
remained retained while the evidence repair was preregistered and implemented.

## Repair state

The repair was preregistered at `80581067` and implemented. All four commands pass in a fresh sealed
intake, including exact-source relocation and hostile layout checks. A fresh external repair-only
review then verified every registered payload, replayed all four commands, independently regenerated
the scientific artifacts, and returned `REPAIRS_ACCEPTED`. The original failed-as-delivered record
remains preserved in `EXTERNAL_REVIEW_RAW.md`.
