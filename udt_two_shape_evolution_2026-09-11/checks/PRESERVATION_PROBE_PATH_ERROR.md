# Initial parent preservation probe — metadata failure retained

An inline Python metadata probe at approximately 14:17 UTC incorrectly used the TI2 package
as the path base for PRECOMPUTATION_FREEZE.json. That older freeze's keys are repository-relative;
the later CANDIDATE_FREEZE.json keys are package-relative. The candidate's 33 pins checked first,
then the probe failed on all seven precomputation paths without reaching any precomputation-file byte comparison.
No preservation receipt was written, no mismatch of existing file bytes was established, and
no candidate, source, manifest or scientific implementation was repaired.

The exact failing lookup was `q=base/f`, with the incorrect tuple
`('PRECOMPUTATION_FREEZE.json', p)` where p is the TI2 package. The correction is the
repository root for that explicitly repository-relative record. The same base correction
does not apply to the candidate freeze. The successful separately saved preservation capture
uses explicit path bases for each record.

Actual tool returned exit 1 and this final exception (transcribed from the tool output):

```
AssertionError: ('PRECOMPUTATION_FREEZE.json', ['udt_two_shape_evolution_2026-09-11/FRAME_AND_DISCOVERY.md', 'udt_two_shape_evolution_2026-09-11/initial_rate.py', 'udt_ti1_banking_2026-09-11/WORK_ORDER.md', 'udt_ti1_banking_2026-09-11/BANKING_RECORD.md', 'udt_two_shape_nonlinear_interaction_2026-09-11/INITIAL_CANDIDATE.md', 'udt_two_shape_nonlinear_interaction_2026-09-11/review/REVIEW.md', 'udt_two_shape_nonlinear_interaction_2026-09-11/review/FINAL_FIDELITY.md'])
```

This is a path-namespace error in a late metadata probe, not a failed scientific check.
