# Final audit interrupted by server restart

The parent launched the declared normal full406 after-audit with the existing
900s/2GiB capture wrapper and output prefix checks/premise_after. The tool yielded
execution session98628. Before any completion receipt was returned, the server
restart interrupted the turn; recovery was explicitly requested by the user.

At recovery on2026-09-29T20:56:26UTC, HEAD/origin were still cffe75fa, all39
accepted integration file hashes matched, and the completed non-draft and31-test
receipts remained exit0. Resuming session98628 failed with “Unknown process id”.
The available /proc view showed no matching audit/capture Python process, and
no premise_after output/receipt artifacts existed. The available process view
alone is not an audit-completion certificate. No partial stdout/stderr could
be recovered from disk; none is invented. The interrupted attempt is UNVERIFIED,
not a pass or a scientific failure.

The parent reruns only this unfinished full audit using the same still-unused
prefix. The capture utility refuses to overwrite existing output files. The
subsequent actual receipt owns the rerun's duration, exit and output. Candidate,
reviews, fast checks and their sealed bytes are not regenerated.
