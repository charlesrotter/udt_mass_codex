# ECS1 initial source-first check record

The source argument and independent code were frozen by INITIAL_FREEZE.sha256
at the UTC recorded in FREEZE_UTC.txt before the first run and before parent
candidate exposure. All three frozen hashes and all SOURCE_PINS hashes were
checked after the run and matched.

The parent's explicit serial CPU grant covered the one run:

    python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_echo_consistency_2026-10-01/math/source_first_run python3 udt_echo_consistency_2026-10-01/math/check_source_first.py

Result: PASS,47 exact symbolic checks, Python3.10.12/SymPy1.13.1,
0.458476149 seconds,48,300KiB maxRSS,2,147,483,648-byte virtual-address cap,
no wall or CPU timeout, empty stderr. Original stdout, stderr and capture
receipt are preserved as source_first_run.stdout/.stderr/.json. No failed
scientific run preceded this output. The CPU slot was explicitly released.

The checks concern original metric Christoffels, clock/preparation properties,
both affine null ray directions and measured frequency, product curvature,
Jacobi/sign equations, the finite-branch ratio algebra, and exact interior
counterexamples to reciprocal-q and total-as-leg confusions. Domain and
nonuniqueness conclusions are analytic arguments in SOURCE_FIRST, not inferred
from the assertion count. No independent numerical integration, generic metric
classification, field-sector admissibility or observed-physics confirmation
was performed.

After freezing/running the above and still before parent-candidate exposure, I
read FPC1 INITIAL_CANDIDATE and math/DERIVATION to assess the requested existing
Kasner control. Its directional log series imply, on the stated local positive-L
branches, D=log q-log[p/(2-p^2)]=-16L^3/27+O(L^4) on r=-1/3 and
D=8L^3/27+O(L^4) on each r=2/3 axis. The analytic remainder argument from that
source justifies a failure for sufficiently small positive L, without a finite
threshold. I have not independently replayed that whole Kasner construction.
This is a source-based algebraic consequence, not new source-blind evidence.

Candidate review and final integration attestation remain outstanding.
