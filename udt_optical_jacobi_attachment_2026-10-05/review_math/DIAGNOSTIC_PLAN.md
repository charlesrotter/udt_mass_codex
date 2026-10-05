# Finite failure diagnostic

Initial run completed30 passing original/Jacobi/neighbor ray cases and reached
the fourth optical case after its10 solves; its final neighbor assertion failed.
The initial code failed before serializing that local report; stdout/stderr,
three complete passing reports and initial code are preserved. Total attempted
ray integrations40, irrespective of the initial aggregate counter30.

Read solver-first protocol. No scientific equation has changed. Freeze one
repeat of the strong case with the same settings and tolerances, adding only
pre-assertion report serialization to expose actual errors and decide whether
finite-angle truncation or metric/Jacobi discrepancy is responsible. This adds
10 runs (cumulative50). A supported step-size repair and four planned actual
incidences may follow within the100 total budget. No failed case is dropped.
