# LG1 reviewer evidence record

Reviewer context `/root/lg1_review` is fresh and source-first. Exact model UNKNOWN;
different-model independence UNTESTED. Source-first proof is an independent local
adjoint PDE argument, not a rerun of the parent candidate or NR1/NR2 code.
Only the shared capture wrapper is reused unchanged. Both check scripts were
independently written before parent candidate exposure.

SOURCE_FIRST.md was saved by 2026-09-09 17:25:28 UTC and its SHA-256 sent to parent.
The first check began 17:27:15.093549 UTC, took 0.27130 seconds, and peaked at
47,904 KiB. The second began 17:29:08.026088 UTC, took 0.27999 seconds, and peaked
at 45,232 KiB. Both exited zero; stdout, empty stderr, and JSON capture receipts
are retained. No GPU. One reviewer check at a time; 512 MiB address-space and
60 second CPU/wall caps; library thread variables set to one.

Exact commands, from `/home/udt-admin/udt_mass_codex`:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_localized_geometry_campaign_2026-09-09/step_01/review/source_first_check /home/udt-admin/udt_mass_codex python3 udt_localized_geometry_campaign_2026-09-09/step_01/review/check_source_first.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_localized_geometry_campaign_2026-09-09/step_01/review/adjoint_constraint_check /home/udt-admin/udt_mass_codex python3 udt_localized_geometry_campaign_2026-09-09/step_01/review/check_adjoint_from_constraints.py
```

Results: exact no-lapse coefficient `-8/(9*T**3)`; forbidden rotation rank two;
the nonlinear momentum-density divergence identity has exact zero residual for
arbitrary first-jet symbols at a nonsingular positive metric. The second script
reconstructs all three momentum variations by varying the mixed-index divergence,
then formally integrates by parts to recover both adjoint tensor coefficients.
It also differentiates the Hamiltonian inverse-metric contractions directly.
These are symbolic identities on the stated background/jet domain, not numerical
approximation, PDE certification, or a nonlinear gluing proof.

Three meaningful mutation controls reject a missing connection term, an x-y
rotation, and the directional-derivative-only treatment of tensor rotation.

Reporting defect retained and EXCLUDED: the second check's hard-coded
`zero_residuals: 18` summary is not a computed check count (the stated component
identities total 3+6+6+1=16). That field supplies no evidence. The individual
symbolic identities, source, output, and independent analytic argument remain
available; no pass-count claim uses it. This is reviewer metadata, not a defect
in the parent candidate. No failed run has been deleted or overwritten.

Primary public methods read through the browser: Chrusciel--Delay,
gr-qc/0301073v2, equation (2.4), Section 3 projection discussion and Theorem 8.15;
Chrusciel--Isenberg--Pollack, gr-qc/0403066v2 (16 June 2005), equations (1.1),
(1.2), (1.6) and Theorem 1.1, including the preceding definition of the neck
construction. These sources were not downloaded by this reviewer; no PDF byte
hash or full-paper verification is claimed. Their no-local-KID hypothesis is
explicit, and their topology-changing construction is not applied here.

The parent owns synchronization, exact registry audit, campaign finalization,
and any candidate commit. The historical full365 G325 failure is not waived.
