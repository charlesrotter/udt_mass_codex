# SM3 review execution record

Reviewer `/root/sm3_interface_review`; baseline grok
cc71a324a61bf2711a4b52c8ebee8a8e4d9b8269;2026-09-08 UTC.
All writes were restricted to this step_03/review directory. Exact source
hashes and exposure history are recorded in SOURCE_FIRST_REQUIREMENTS.md
and ADVERSARIAL_REVIEW_INITIAL.md. No candidate or author source was edited.

Independent exact rational jet/frame diagnostic, started02:07:45.431515UTC:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_03/review/independent_checks_initial /home/udt-admin/udt_mass_codex python3 -B udt_source_metric_connection_campaign_2026-09-08/step_03/review/independent_interface_check.py
```

Exit0;56/56 exact diagnostics;7 matching RED mutation paths; duration
0.074535748019116seconds; maximum child RSS11520KiB; stderr0bytes.
Python3.10.12; standard-library fractions.Fraction arithmetic. Capture:
independent_checks_initial.stdout/.stderr/.json. Controls include4 full
metric event jets and4 Lorentz-frame parameter cases; no sampled convergence,
floating-point certification or scientific solve is claimed.

Unchanged author replay, started02:09:19.843684UTC:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_03/review/author_replay_initial /home/udt-admin/udt_mass_codex python3 -B udt_source_metric_connection_campaign_2026-09-08/step_03/check_interface.py
```

Exit0;17/17; duration0.49620163498912007seconds; maximum child RSS49124KiB;
stderr0bytes. Python3.10.12; SymPy1.13.1. Capture:
author_replay_initial.stdout/.stderr/.json. This is shared-code regression.

Both numerical runs were sequential with512MiB address-space and60s CPU/wall
limits from the inspected capture utility. The utility refuses overwrites.
No resources were increased. Matching REDs are deliberate actual caught
AssertionErrors and their exact residuals are retained in independent stdout.

Correspondence check:

```sh
cmp udt_source_metric_connection_campaign_2026-09-08/step_03/review/author_replay_initial.stdout udt_source_metric_connection_campaign_2026-09-08/step_03/author_checks_initial.stdout
```

Exit0; byte-identical. Independent and replay stderr were each0bytes by wc.
Actual branch/HEAD were rechecked afterward and still match the baseline.
No review repair was necessary. All counts are finite diagnostic/regression
evidence, not analytic proof, trusted chronology or scientific promotion.
