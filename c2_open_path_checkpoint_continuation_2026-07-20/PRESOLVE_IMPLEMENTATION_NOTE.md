# Presolve Implementation Note

Date: 2026-07-20

Committed before the official 22-path extension.

The implementation imports the frozen homotopy equation and corrector from the parent package and
adds only checkpoint restart, longer registered limits, complete state logging, and the preregistered
loop/safety classifications.  A disposable one-path, 60-second software pilot recomputed the first
checkpoint residual as `1.7286616582623537e-10`, below the inherited `1e-9` gate, and continued to a
new accepted state with homotopy residual `4.1603165357173566e-11`.  The pilot outcome is not part of
the official scientific census.

Eight CPU worker processes are isolated and restricted to one thread each.  No GPU, physical value,
equation, seed, endpoint tolerance, or branch-selection rule is added.
