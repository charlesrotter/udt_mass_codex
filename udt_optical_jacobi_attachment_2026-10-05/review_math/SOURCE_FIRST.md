# Sealed source-first return

VERIFIED-WITH-CAVEATS for the independent conditional derivation in
SOURCE_FIRST_DERIVATION.md. The full two-dimensional map is essential; affine
and angular distance are not generally equal. The actual b*=0 limiting
preparation preserves the1/H angular endpoint and the stated clock-pole residue
on its eventual caustic-free tail. Generic b* has the separate M5 factor and
possible caustics. This is not physical adoption, empirical evidence or canon.

Parent OJM1 candidate/code has not been read. After my derivation and numerical
plan were saved, parent sent matching formulas/basis and an original-metric
check request; this exposure is disclosed. Fresh context, independent hand
argument, and implementation-distinct original-metric coordinate Jacobi plus
neighboring-ray checks are present; different-model independence is untested.
The parent and reviewer use common mathematical sources and numerical libraries.

Independent numerical evidence consists of original full4D metric Christoffels
and their coordinate derivatives, integrated coordinate Jacobi fields, and
exact-null fixed-frequency neighboring sky rays. No parent code is imported.
Closed-form quadratures serve as the comparison, not the Jacobi ODE definition.
For the four finite optical cases, tight original-metric Jacobi errors are
2.631e-14,1.326e-12,7.482e-12 and1.933e-11. Norm/energy checks pass their frozen
tolerances. Final neighboring-ray errors are1.783e-8,2.090e-8,7.448e-8 and
3.145e-7, all below the unchanged2e-5 acceptance bound. Off-diagonal elements
are included in the full matrix error.

The strong case has P=5.646688777589277>pi, B_parallel=371.07789558786857,
B_perp=-3.647597165879074: one conjugate crossing has occurred. Its angular
distance18.312990152360758 differs from affine6.595602714185797. This is a
finite conditional counterexample to universal affine=angular, and to a
universal angular ceiling1/H across all these branches.

The strong-case finite-angle test initially failed:1e-4 and5e-5 angles gave
relative errors.0133767 and.00322250. Original metric/Jacobi agreement already
passed. A frozen diagnostic repeat retained the same failure and exposed
quadratic truncation. The same-equation, unchanged-tolerance repair used
1e-6 and5e-7 angles, obtaining1.276e-6 and3.145e-7. Initial code/output and
diagnostic output remain intact. This emphasizes the lack of an unqualified
finite-source approximation near a strongly focusing preparation.

Four actual b*=0 incidences have nonzero b(R) at all sampled finite R. The
independent incidence residual is at most3.594e-15. At R=10^6, D_A=
49.99720013999665 tends toward1/H=50, and Z(50-D_A)=79.190934767022 versus
the analytic residue79.19595949289332 (relative discrepancy6.345e-5).
Discrepancy decreases at every frozen radius. These are finite float64 checks,
not interval/asymptotic proof; the smooth-tail argument supplies the limit.

Actual cumulative case/run count is64:40 initial optical geodesic solves,
10 diagnostic-repeat solves,10 repaired strong-case solves and4 incidence
cases. The per-attempt JSON counters count completed records only; the failed
strong case's10 solves are explicitly included here. There remain36 cases
under the100-case ceiling for exposed saved-quantity replay/repairs.

Commands, all from the repository root, were:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 bash -c 'ulimit -v 2097152; python3 udt_optical_jacobi_attachment_2026-10-05/review_math/check_original_metric.py > udt_optical_jacobi_attachment_2026-10-05/review_math/stdout.txt 2> udt_optical_jacobi_attachment_2026-10-05/review_math/stderr.txt'

The diagnostic run changed only the output names to diagnostic_stdout.txt and
diagnostic_stderr.txt; the repair run used repaired_stdout.txt and
repaired_stderr.txt. INITIAL_check_original_metric.py and
DIAGNOSTIC_check_original_metric.py preserve the exact earlier scripts.
PRE_RUN_FREEZE.json and REPAIR_FREEZE.json bind the pre-execution source
versions. CPU only,2GiB virtual-memory limit, one thread, no timeout; Python
3.10.12, NumPy2.2.6, SciPy1.15.3, SymPy1.13.1. No external literature used.

SOURCE_FIRST_MANIFEST.json binds this return and all current reviewer files;
the manifest is documentary correspondence, not an external chronology stamp.
Full old-package replays, physical source modeling, global image classification,
observational inference and different-model review were not performed.
