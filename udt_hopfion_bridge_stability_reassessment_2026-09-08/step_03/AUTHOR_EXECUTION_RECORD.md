# HB3 author execution and limits

Parent supplied scope before computation in QUESTION.md after reading the
complete HB2 mathematical review. The final review's later operational append
and the two failed stale-pin checks are preserved and explained in
DEPENDENCY_HASH_FINALIZATION.md; initial author/review history is unchanged.

Exact common launch form from the repository root:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py ABS_STEM /home/udt-admin/udt_mass_codex python3 -B SCRIPT

ABS_STEM is this step's absolute path plus the indicated stem. Actual child
argv/cwd/start/duration/exit/timeout/RSS are in each automatic JSON; separate
stdout/stderr survive. Existing inspected capture utility sets512MiB AS/60s
CPU/wall; one child in this context, BLAS/OMP/MKL threads1. Python3.10.12,
SymPy1.13.1 already installed. No GPU, field grid, install or evolution solve.

| Stem | Script relative to this step | Actual outcome |
|---|---|---|
| author_check_initial | check_orbits.py, bytes retained as check_orbits_initial_pin.py | exit1 at source-hash gate;0.1634822729974985s,54084KiB; NOT_PASS |
| author_check_complete | SAME original checker bytes, despite intended patch | exit1 at SAME source gate;0.16043165398878045s,54140KiB; NOT_PASS despite stem name |
| author_check_final_pin | check_orbits.py, only final HB2 review hash substituted | exit0,0.3984070190053899s,49588KiB; first completed mathematical check, empty stderr |
| parent_independent_replay | review/independent_ratio_check.py | exit0,0.29503554198890924s,45524KiB; empty stderr, saved independent output reproduced byte-for-byte |

The independent replay output SHA-256 is
`500755176bff9e2b5f6bd0850d1df608a5a723a80b4e96c09f21e1291c94d52f`.
The main author read that implementation and its analytic reconstruction only
after freezing the initial HB3 candidate/code. Replaying a fresh reviewer's
script is reproducibility, not another independent context or general proof.

The algebra supports inverse-metric contraction, normalized ratio, polynomial
nonconstancy, exact saved HB2 quantities and finite controls. The actual local
development, retained symmetries, fixed-point/time quantifier argument and
torus orbit classification require their stated analytical reasoning and
fresh adversarial review. No finite fixture proves them. Equal-weight
preservation needs full-pair U(2) symmetry, not merely a zero initial derivative.

Global strict root and simple gap, positive unscaled weights, compact/local
domain, supplied marked normal slices and imported smooth Cauchy/isometry
method are retained. Spatial line leaves are not physical time trajectories.
There is no new carrier action, physical content, scale or stability adoption.
