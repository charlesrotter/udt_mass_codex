# Reproduction commands

Run from repository root in the documented CPU environment:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_amplitude_volume_metric_atlas_2026-07-21/build_amplitude_volume_atlas.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -B udt_amplitude_volume_metric_atlas_2026-07-21/verify_amplitude_volume_atlas.py
```

The builder regenerates the preregistered raw volume evidence. The verifier does not import that
builder; it independently reconstructs the design and reconciles every saved configuration and
radial edge.

