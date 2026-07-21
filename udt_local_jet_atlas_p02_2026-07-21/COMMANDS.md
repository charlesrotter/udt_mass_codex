# Commands

Run from the clean repository root with the pinned requirements.

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_local_jet_atlas_p02_2026-07-21/run_p02_local_jet_atlas.py

PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B \
  udt_local_jet_atlas_p02_2026-07-21/verify_p02_local_jet_atlas.py
```

Both commands use exact SymPy algebra plus fixed float64 P01 regression. They execute no equation of
motion, parameter sweep, ODE, PDE, GPU process, or physical comparison.

After the scientific package is complete:

```bash
python3 udt_local_jet_atlas_p02_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  udt_local_jet_atlas_p02_2026-07-21/verify_repository_gates.py
```

The repository gate replays P02, all prior scientific-package manifests, six frozen manifests,
navigation/frontier/current-path checks, the documented test baseline, and metadata-only preservation
of the original dirty checkout.
