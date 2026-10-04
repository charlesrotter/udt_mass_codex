# Preserved source-first numerical-domain failure

The initial frozen script failed to locate a direct real incidence at R=25 for the
single source phase chosen from the asymptotic b*=2 endpoint. Full initial result,
stdout and stderr are retained. This is a failed solve, not proof that the metric
or a physical class lacks incidence. The analytic theorem is local near R=infinity;
it does not imply its branch extends back to R=25 through the same winding choice.
The rapidly changing orbital source phase makes that omitted global-continuation
hypothesis substantive. No equation, tolerance or desired physical conclusion changes.

Bounded repair: retain identical script bytes and fixed source/receiver histories;
sample R=1000,10000,100000,1000000 instead, with their same relative centered
increments and both frozen precisions. Preserve this repair before execution.
At most 25 incidence solve attempts including initial failure, below 100 total.
No earlier failed sample is presented as a passing branch. This tests the analytic
tail statement and makes no global existence or uniqueness claim. Environment
CPR_REVIEW_RADII supplies the new frozen radii; CPR_REVIEW_OUTPUT preserves the
initial artifact. Source-first analytical discussion and original numerical freeze
remain unchanged.
