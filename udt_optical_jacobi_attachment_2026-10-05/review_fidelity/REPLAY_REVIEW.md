# Saved-quantity replay and clarification review

Verdict: VERIFIED-WITH-CAVEATS for the candidate plus CLARIFICATIONS.md,
pending final integration-byte review. Seven new cases were frozen and computed
at 60 digits before reading parent numerical output or implementation. The
independent code imports no parent/source computational module. Cumulative
executed finite cases: 23. There were no scientific failures, repairs or reruns.

The four actual histories (E=1 and10, R=10^3 and10^6) were independently solved
from original incidence using reciprocal-radius integration, then their signed
Jacobi components, J components, D_A, D_o, Z and emission time reconstructed.
All three frozen supplied-ray controls were independently recomputed as well.
Comparison with both 40/70-digit parent records gives 14 saved-value comparisons
with maximum scaled discrepancy 6.38320127530874919105425291674e-39, below the
frozen 1e-24 threshold. SAVED_COMPARISON.json binds both result artifacts.
This is floating-point agreement, not interval/global certification. The shared
mpmath library and common supplied equations limit implementation independence.

Exact commands, all with empty stderr and exit0:

    python3 udt_optical_jacobi_attachment_2026-10-05/review_fidelity/replay_saved.py > udt_optical_jacobi_attachment_2026-10-05/review_fidelity/replay.stdout 2> udt_optical_jacobi_attachment_2026-10-05/review_fidelity/replay.stderr
    python3 udt_optical_jacobi_attachment_2026-10-05/review_fidelity/compare_saved.py > udt_optical_jacobi_attachment_2026-10-05/review_fidelity/compare.stdout 2> udt_optical_jacobi_attachment_2026-10-05/review_fidelity/compare.stderr

The comparison script was preserved after an equivalent inline saved-value
comparison had already passed; executing it again compares existing records
only and is not a new physical case or independent numerical re-solve. Resource
controls are internal to the replay script; versions appear in the earlier
independent result. REPLAY_FREEZE.json records the pre-run code/plan hashes.

CLARIFICATIONS.md explicitly distinguishes J from J^{-1}, names the finite
map associated with its Hessian remainder, and prevents an angular-area
distance from being used as a universal directional size conversion. These
resolve the nonblocking wording points without changing equations or premises.
DESCENDANT_REVIEW.md correctly covers constructive and adverse uses and keeps
R14/R15, physical scale, source model and native metric admission open. The
initial candidate remains preserved. No omitted historical source check is
represented as newly rerun, and source/registry grades are unchanged.
