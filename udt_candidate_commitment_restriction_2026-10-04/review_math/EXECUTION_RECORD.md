# Independent mathematical check execution

Commands, from repository root (no wall or CPU timeout):

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_candidate_commitment_restriction_2026-10-04/review_math/independent_check.py > udt_candidate_commitment_restriction_2026-10-04/review_math/initial_stdout.txt 2> udt_candidate_commitment_restriction_2026-10-04/review_math/initial_stderr.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 CPR_REVIEW_RADII=1000,10000,100000,1000000 CPR_REVIEW_OUTPUT=results.json python3 udt_candidate_commitment_restriction_2026-10-04/review_math/independent_check.py > udt_candidate_commitment_restriction_2026-10-04/review_math/stdout.txt 2> udt_candidate_commitment_restriction_2026-10-04/review_math/stderr.txt
```

Initial attempt exit 1; domain/continuation failure preserved with pre-repair
freeze and reasoning in NUMERICAL_REPAIR.md. Tail run exit 0, 24 actual incidence
solve attempts, 8 central records at 40/70 decimal digits; 25 attempts total.
Python 3.10.12, mpmath 1.3.0. Address-space limit 2 GiB, one BLAS thread,
CPU only. Tail run took 4.57 seconds. Results own exact reported resource values.

The independent check evaluates the outgoing-chart metric, derives its connection
from metric derivatives, and contracts original circular/free/null geodesic equations.
It solves actual nonradial incidence for fixed emitter and receiver histories,
then compares endpoint contractions to finite differences of proper arrival.
The wrong differentiation with b held fixed fails by several percent. This is a
concrete sensitivity check, not a substitute for a full generic mutation census.
The endpoint product H Z (tau_e* - tau_e) approaches one in the retained tail.
No parent implementation or its outputs were imported or replayed.

All assertions passed at the declared thresholds. Finite high precision and
step-size checks are not interval certification, genericity or proof of limits.
The analytic hypotheses and proof in SOURCE_FIRST.md own the asymptotic statement.
No empirical bound, physical X_max, native Lambda selection, full angular map,
global branch uniqueness, matter model, or whole-postulate insufficiency is claimed.
