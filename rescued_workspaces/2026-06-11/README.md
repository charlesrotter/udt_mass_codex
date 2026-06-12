# Rescued /tmp workspaces — provenance repair (2026-06-11)

During the W1 push (w_stiffness_push_declaration.md), all three route
agents independently found that the scripts backing the two 2026-06-11
THEOREMS — pde_p1_results.md ({f spherical, q=0, w arbitrary}, 61/61)
and nonstationary_opener_results.md (fate polynomial f_T-free,
VN-ruled) — were never committed: the docs say "new files only" but
commits 039a0df / 548114d carried only the .md files. The workspaces
lived in /tmp, one reboot from loss. This directory is a verbatim
rescue (rsync, __pycache__ excluded) of:

- pde_p1/ — the P1 static classification derivation + validations
  (derive_system.py defines the exact P1 metric class).
- nonstat_n1/, nonstat_n2/ — the nonstationary opener arms.
- verify_pde/, verify_nonstat/ — the blind verifier workspaces
  (VP1, VN).
- verify_angular, verify_ens, verify_mass, verify_mf, verify_s2,
  verify_blind, verify_x1, verify_n_adjudication — earlier-session
  verifier workspaces found alongside them.
- tmp_loose_scripts/ — every loose *.py verifier/audit script found in
  /tmp at rescue time (sweep insurance; some may duplicate properly
  committed scripts).

These are PROVENANCE ARTIFACTS, not canonical audit scripts: they are
committed as found, unreviewed, and inherit the append-never-edit rule.
Where a rescued script conflicts with a committed results doc, the doc
plus its recorded verifier pass remains authoritative; flag the
conflict, don't silently prefer either.

Process fix going forward (binding on the driver): a results doc may
not be committed unless its scripts are in the same commit. Recorded
in HANDOFF at next session close.
