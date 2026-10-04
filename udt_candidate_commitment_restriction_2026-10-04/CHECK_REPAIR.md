# Original residual caught a prematurely stopped root solve

The first parent check passed original-coordinate symbolic checks and its40-digit
finite pass, then stopped at the70-digit central E=1,R=1e6 case. No numerical
result file was written; the initial stdout/stderr/receipt and INITIAL_CHECK.py
are retained. Those partial outputs are not a substitute for saved quantities.

The Newton stopping threshold was10^(-dps+10), ten times looser than the
original-incidence acceptance threshold10^(-dps+9). The independently evaluated
incidence residual4.0998519464711163e-61 passed the internal1e-60 stop but failed
the required1e-61 acceptance. This is a checker convergence defect, not an
equation, asymptotic argument or physical failure. Repair tightens only the
internal stop to10^(-dps+7). All original acceptance tolerances remain unchanged.

A frozen first-case diagnostic passed five E1,R1000 incidences. A second frozen
diagnostic recomputed only central cases: first three passed and R1e6 reproduced
the failure. The exact initial order therefore comprised40 successful40-digit
cases plus15 successful70-digit cases and one failed central case:56 attempts.
Diagnostics add5+4. This reconstructs the execution count from deterministic
code/receipts; it is not a newly recovered raw numerical dump of the first pass.

To respect the <=100-case budget including repeats and failures, the repaired
run narrows to E1,R1000 and1e6, plus E10,R100, with five incidences each at40/70
digits:30 more,95 total. The previously failing case remains included. This
retains an asymptotic trend and finite static/continued examples, but does not
numerically track one history continuously through its horizon or densely
sample intermediate radii. Exact regular-chart algebra owns horizon crossing.
The original candidate remains unchanged; reviewers inspect the repair and
coverage loss before final banking. No new parameter, physical assumption,
relaxed test, fit or additional resource is introduced.
