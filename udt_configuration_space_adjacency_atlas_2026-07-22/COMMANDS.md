# Commands

CPU-only environment:

```bash
python3 --version
python3 -c 'import numpy, mpmath, sympy; print(numpy.__version__, mpmath.__version__, sympy.__version__)'
python3 udt_configuration_space_adjacency_atlas_2026-07-22/build_configuration_adjacency_atlas.py
python3 udt_configuration_space_adjacency_atlas_2026-07-22/verify_adjacency_independent.py
python3 udt_configuration_space_adjacency_atlas_2026-07-22/verify_package.py
python3 udt_configuration_space_adjacency_atlas_2026-07-22/replay_and_capture.py
python3 udt_configuration_space_adjacency_atlas_2026-07-22/build_manifest.py
python3 udt_configuration_space_adjacency_atlas_2026-07-22/verify_repository_gates.py
```

The repository test gate uses the inherited full test command and retains the documented baseline:
69 passed, 1 expected xfail, and 1 known hygiene-header failure.
