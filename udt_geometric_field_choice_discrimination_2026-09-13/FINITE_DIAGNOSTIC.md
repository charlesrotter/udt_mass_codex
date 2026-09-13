# NR2 finite diagnostic — coincident-sample symbolic failure

Initial capture candidate_exact returned exit1, 49/50 checks. Its only failure
was `coincident_samples_rank_loss`, residual `nan` from substituting t=1 into
SymPy's unevaluated-form determinant. Preserve original code, freeze, output
and capture. This is not yet a passing check or a changed scientific claim.

Before the diagnostic run, freeze this finite comparison: reconstruct the
original signed two-sample matrix from the explicit q/r solution, substitute
t=1 BEFORE taking its determinant and rank, inspect entry finiteness, and
compare the unsimplified determinant with its cancelled form and its limit.
Expected rank2 follows from identical first/second measurement rows. Check
the declared determinant factor away from the possible removable expression
singularity. Distinguish an expression-evaluation defect from a map defect.
CPU, one thread/process,180s/2048MiB, exact arithmetic; no new physical premise.
If the matrix is finite rank2 with zero determinant, repair only evaluation
order and add original-matrix rank/equality checks in a separate script;
otherwise retain an unresolved mathematical objection and stop that claim.
