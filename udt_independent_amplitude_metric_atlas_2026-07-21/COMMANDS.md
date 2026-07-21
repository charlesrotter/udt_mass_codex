# Reproduction commands

Run from repository root in the documented CPU environment:

```bash
python3 udt_independent_amplitude_metric_atlas_2026-07-21/build_independent_amplitude_atlas.py
python3 udt_independent_amplitude_metric_atlas_2026-07-21/verify_independent_amplitude_atlas.py
```

The builder regenerates the registered configuration evidence. The verifier is separately written,
does not import the builder, reconstructs the load-bearing rank structurally and symbolically, and
exercises corruption catches.
