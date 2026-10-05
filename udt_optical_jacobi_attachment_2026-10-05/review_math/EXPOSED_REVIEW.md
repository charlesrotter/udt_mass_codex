# Exposed mathematical review

Verdict: VERIFIED-WITH-CAVEATS / ACCEPT_WITH_LIMITS for INITIAL_CANDIDATE.md
as scoped by CLARIFICATIONS.md. No unresolved mathematical defect or required
scientific repair. This verdict does not adopt the supplied metric, identify a
physical ruler/population, establish an additional UDT effect or confer canon.

Reviewed candidate, numerical freeze/implementation, clarifications, premise
ledger, descendant review and method attribution. Source-first derivation and
failure/repair history remain unchanged. External paper itself was not inspected
by this reviewer; its geometry is not a proof dependency of this review.

The exact two-dimensional Jacobi factors follow from original null geodesic
variations. Their diagonal curvature signs, source vertex slopes, endpoint
quotient/rest-screen isometries and observing-frequency normalization are
correct. The observed sky sign in equation3 is consistent with the opposite
future propagation direction. J maps angle to source displacement; J inverse
maps source size to angle only at rank two. The clarification correctly restricts
the supplied Taylor/Hessian bound to the forward finite map and does not claim
an inverse-map error bound. No source-frequency factor belongs in J.

The caustic criterion, simple perpendicular zero, phase regularity, and strictly
smaller pre-caustic area distance for mb!=0 are correct. The general endpoint
need not equal1/H and can be rank deficient. For the actual b*=0 preparation,
uniform even-in-b small-ray estimates and CPR1's b(R)=O(1/R) preserve the first
deficit and clock-pole residue. Candidate statements retain eventual-tail and
physical-admission restrictions; no frozen radial family replaces actual
incidence. Analytic arguments, rather than finite numerics, own these claims.

Independent saved-result replay completed after the freeze in
EXPOSED_REPLAY_FREEZE.md. All8 saved70-digit incidence records were reconstructed
with SciPy Brent/quadratures, with maximum scaled discrepancy
3.798183989545123e-12 across b,t_e,tail,P,U,I,L,A,omega_e,Z,both Jacobi widths,
both angular length factors,D_A,D_o,area/affine and shear ratios,pole ratio.
Direct original-radius quadrature independently recomputed affine L.

Two full original4D metric coordinate-Jacobi integrations used the reviewer's
sealed implementation, not parent quadrature code. For E1,R1000 the full matrix
error was4.0939958498007134e-12; for E10,R1e6 it was2.970474969312744e-11.
Maximum scaled null residual2.909e-14 and energy residual8.882e-15 passed the
unchanged bounds. The full matrices include off-diagonal components. The common
minus sign relative to candidate J is the explicitly different future-tangent
variation convention; it leaves singular values/determinants unchanged.

The replay read CONSTRUCTION_RESULT.json at the hash preserved in
SAVED_REPLAY_RESULT.json and writes no parent artifact. Exact command:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 bash -c 'ulimit -v 2097152; python3 udt_optical_jacobi_attachment_2026-10-05/review_math/replay_saved.py > udt_optical_jacobi_attachment_2026-10-05/review_math/replay_stdout.txt 2> udt_optical_jacobi_attachment_2026-10-05/review_math/replay_stderr.txt'

Cumulative usage74/100 finite cases, including every failed/diagnostic/repaired
run; no GPU,2GiB virtual-memory cap,one BLAS/OMP thread,no timeout. Distinct code
and argument do not mean distinct premises or a different model. Float64 replay
is not interval certification. Initial finite-source failure remains evidence
that a infinitesimal map alone does not control a finite object near focusing.

Central integration/final binding and parent's final normal/full406 checks are
not yet attested by this exposed-stage review. Review does not replay the full
historical packages or review the entire corpus. An immutable source-first
manifest and a separate exposed-stage binding retain the review boundaries.
