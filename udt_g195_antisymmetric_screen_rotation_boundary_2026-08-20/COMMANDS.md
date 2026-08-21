# G195 commands

Run from the package directory unless stated otherwise.

```bash
python3 derive_antisymmetric_screen_rotation.py
python3 verify_antisymmetric_screen_rotation_independent.py
python3 run_catch_proofs.py
python3 build_source_manifest.py
python3 verify_package.py
G195_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 verify_package.py --no-write
```

The repair-frozen stdout from that exact command is preserved as
`NO_WRITE_REPLAY_RESULT.json`. The ordinary writable package summary remains a distinct artifact
and therefore truthfully records `no_write_replay: false`.

Repository gates run from the repository root:

```bash
python3 verify_current_scientific_premises.py
pytest -q
git diff --check
```
