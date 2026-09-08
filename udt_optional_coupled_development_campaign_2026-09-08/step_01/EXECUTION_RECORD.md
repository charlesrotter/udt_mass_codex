# CD1 author execution and freeze

Question recorded before computation in ../CD1_QUESTION.md; explored symbolic
argument then initial candidate/checker frozen unchanged. Initial hashes in
INITIAL_SHA256SUMS. No failed author run or repair so far.

Executed from repository root:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_optional_coupled_development_campaign_2026-09-08/step_01/author_initial /home/udt-admin/udt_mass_codex python3 -B udt_optional_coupled_development_campaign_2026-09-08/step_01/check_initial_data.py

Actual initial run12:48:37.726282UTC, exit0,17 exact identity/anchor groups,
five actual nonzero wrong-substitution controls;0.351814s, maxRSS51596KiB,
empty stderr,512MiB AS/60s CPU/wall limits. Python3.10.12, SymPy1.13.1.
Raw stdout/stderr/JSON preserved. Full intrinsic metric and K calculation,
not an independent reviewer; counts are diagnostics, not proof of ODE existence.

Fresh reviewer /root/cd1_data_review is source-first before target intake.
Review not yet complete; no downstream use until its actual verdict is read.
