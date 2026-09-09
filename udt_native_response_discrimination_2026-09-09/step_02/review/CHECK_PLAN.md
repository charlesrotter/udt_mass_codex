# Independent check refinement before execution

2026-09-09. SOURCE_FIRST.md remains frozen. Parent reported after receiving
the reviewer's source-first argument that its own prior exploration agreed;
this concurrence is exposure and will be recorded in direct review. No new
candidate/code/output has yet been read. Parent also reported it will use
Laurent-polynomial arithmetic. To strengthen the implementation difference,
the reviewer will instead compute the full 4D spherical metric's connection
and Ricci tensor using independently written SymPy coordinate contractions,
then differentiate the constructed Q and S tensors in a formal parameter.

This changes the implementation plan, not the mathematical scope. It does not
reuse the step 1 code or any author/source scientific module. Generic matrix
checks exercise arbitrary first metric and Ricci coefficients as algebraic
inputs; they do not claim those are globally realizable metric jets/curves.
Analytic closed-subspace and positivity arguments remain essential.

Parent approved one concurrent reviewer CPU slot. Existing capture utility,
one library thread, 512 MiB/60 seconds, no GPU, absolute review output stem.
If a missing dependency or resource failure occurs, preserve the failed run
and narrow/repair the check without changing candidate science.
