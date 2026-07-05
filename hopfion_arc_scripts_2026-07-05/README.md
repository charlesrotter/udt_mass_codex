# Hopfion-arc scripts (2026-07-05 session) — provenance for the node_*/F4/H3 results

Working scripts from the 2026-07-05 hopfion arc (moved out of the session scratchpad so the next session
can rerun/verify). Field checkpoints (*.npz, 50–98 MB each) were NOT committed — regenerate them.

- **H3 hopfion solver (the top next-session item = precision closure reruns THIS):** `fs_hopfion.py`
  (Faddeev–Skyrme energy E=∫[(ξ/2)|∂n|²+(κ/4)F²] + Whitehead-integral Q_H), drivers `drive_ckpt.py`,
  `drive_stereo.py`, `drive_val.py`, analysis `analyze_final.py`. See `node_H3_hopfion_solve_results.md`
  + `H3_hopfion_solve_preregistration.md`. NEXT: finer grid (N≳256) to close the ~16% energy gap +
  certify integer Q_H on the relaxed field, then bank clean-A or D.
- F4 (fixed-background Jacobi/Derrick, ILL-POSED per verifier): `f4_test.py`, `wide.py`, `fd.py`,
  `ergo_check.py` → `node3_f4_test_results.md`.
- CAS armchair checks: `armchair_check.py`,`L4.py`,`framedrag.py` (node23), `wcheck.py` (p16), `crux.py`,
  `prof2.py`,`diag.py`,`drive*.py`.
