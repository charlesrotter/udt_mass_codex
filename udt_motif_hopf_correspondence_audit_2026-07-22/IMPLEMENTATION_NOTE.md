# Implementation note — deterministic compressed ledgers

Date: 2026-07-22

Before the complete coherent-path/stencil census was launched, a one-identity smoke run showed the
implementation was computationally viable. An output-code review then found that repeated
`gzip.open(..., "at")` calls would create timestamped gzip members and prevent byte-identical clean
replay even when every scientific row was unchanged.

The production writer was changed before the full census to keep one gzip stream open per ledger,
set `mtime=0`, use an empty stored filename, and write every row through that stream. No path,
family, stencil, threshold, classifier, or scientific premise changed. The one-identity smoke output
was printed only to stdout and did not create a package ledger.
