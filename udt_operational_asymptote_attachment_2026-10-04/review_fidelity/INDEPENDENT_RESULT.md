# Independent source-first numerical return

Repaired run PASS:56 finite cases,340 checks at45/75 decimal digits. Initial
failed run remains preserved (13 attempted cases);69 attempted cases in total.
The early R=60 case for the second fixed history remains outside the checked
branch and is not silently treated as a pass. REPAIR_FREEZE.md owns the exact
scope reduction. No tolerance or physical preparation was changed.

Actual maximum original incidence residual1.572e-39, differentiated arrival
ratio relative error6.919e-11, and two-precision relative discrepancy6.564e-39.
Direct regular-coordinate null norm error<5.474e-48; receiver norm error<1.752e-46.
At R=60000, H*d_o=0.99886764659549 and0.99817324743413 in the two respective
fixed histories, with Z=1518.6248226432 and673.95594806270. These are finite
sanity checks of the analytic asymptote, not interval certification or proof
that arbitrary finite histories are monotone. Raw numbers are in the JSON.

The auxiliary static radar controls increase64.4335,116.4630,167.6670 as the
outer root is approached, while the selected static-slice lengths increase
51.3845,65.6730,70.1480 below their finite endpoint integral. This is a different
query from the circular source. Flat endpoint-boost controls also pass; their
distance changes are ordinary observer dependence, not a preferred-observer
counterexample. No scalar beam/luminosity-distance formula was tested.

Frequency contractions and actual incidence differentiation use independent
quantities. d_e/d_o=Z by definition is an algebraic identity, and is not counted
as independent physical validation. The geometric two-way obstruction remains
an analytic causal argument, not a finite numerical search.

Command for both preserved initial run and repaired run:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_operational_asymptote_attachment_2026-10-04/review_fidelity/check_independent.py > udt_operational_asymptote_attachment_2026-10-04/review_fidelity/stdout.txt 2> udt_operational_asymptote_attachment_2026-10-04/review_fidelity/stderr.txt

Initial code/output was copied into initial_attempt before the active checker
was repaired. Both runs used Python3.10.12/mpmath1.3.0, CPU only,2GiB address
space, one BLAS thread and no wall/CPU timeout. Repaired stderr is empty and
exit code0 was directly observed. Review payload currently<150KiB. This record
precedes any OAA candidate exposure and supplies no native/empirical admission.
