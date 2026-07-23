# Reproduction commands

Run from repository root with Python 3.10 and the dependency pinned in `requirements.txt`.

```bash
python3 -m py_compile \
  udt_phi_causal_interface_atlas_2026-07-22/build_phi_causal_interface_atlas.py \
  udt_phi_causal_interface_atlas_2026-07-22/verify_phi_causal_interface_independent.py \
  udt_phi_causal_interface_atlas_2026-07-22/verify_package.py

python3 udt_phi_causal_interface_atlas_2026-07-22/build_phi_causal_interface_atlas.py
python3 udt_phi_causal_interface_atlas_2026-07-22/verify_phi_causal_interface_independent.py
python3 udt_phi_causal_interface_atlas_2026-07-22/verify_package.py
python3 udt_phi_causal_interface_atlas_2026-07-22/build_manifest.py
(cd udt_phi_causal_interface_atlas_2026-07-22 && sha256sum --check MANIFEST.sha256)

CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/
```

The documented repository test baseline is 69 passed, 1 xfailed, and 1 known hygiene-header
failure. No GPU process is authorized or used.
