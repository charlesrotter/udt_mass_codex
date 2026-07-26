# Commands

Run from the repository root in a clean CPU environment:

```bash
python3 udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/run_isolated_replay.py
python3 udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/run_adversarial_replay.py
python3 udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/build_manifest.py
python3 udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26/verify_repository_gates.py
```

The launcher copies the exact pinned SymPy and mpmath package trees into a
fresh temporary directory, then invokes Python with `-I -S` and only that
temporary dependency directory added to `sys.path`. It records dependency-tree
hashes and the raw replay streams before deleting the temporary environment.
The second command preserves two genuinely different reconstructions: a
Koszul/noncoordinate-frame route and an all-sector coordinate-metric route.

No GPU process, PDE solve, relaxation, time evolution, or density sweep is
part of this package.
