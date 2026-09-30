# Final integration check plan

Independently verify the332 accepted hashes in the dispatched integration freeze,
first rejecting all four protected prefixes and out-of-root/symlink targets.
Compare the prior261-map with the current map: eight changed,253 identical,
71 new; compare the changed list to git diff. Parse old/new graph and require
all old node meanings, edges and source bindings remain, apart from explicit
additions. Independently walk graph descendants of the TRI1 sources and require
both positive/adverse PRI1 contexts while excluding original R6/R7/R9 and CCR1
proofs. Verify generated startup text correspondence and actual repair/source
pins. Run only the three new targeted maintenance tests as regression/catch
checks; do not replay the historical corpus or full406. No synthetic reviewer
fixture from those tests is evidence of actual scientific review.

One CPU process/thread for each capture,60 seconds512 MiB, stdout/stderr retained
in review/math. No GPU/grid, no source edits. Code and plan sealed before run.
