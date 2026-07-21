# Commands

Executed from the clean worktree root on 2026-07-21.

## Map verifier

```bash
python3 -m py_compile udt_complete_metric_solution_space_map_2026-07-21/verify_complete_metric_solution_space_map.py
python3 udt_complete_metric_solution_space_map_2026-07-21/verify_complete_metric_solution_space_map.py --output udt_complete_metric_solution_space_map_2026-07-21/VERIFICATION_RESULT.json --transcript udt_complete_metric_solution_space_map_2026-07-21/VERIFICATION_TRANSCRIPT.txt
```

The verifier is standard-library only. It executes no scientific equation solve.

## Repository gates

```bash
python3 udt_complete_metric_solution_space_map_2026-07-21/build_manifest.py
python3 udt_complete_metric_solution_space_map_2026-07-21/verify_repository_gates.py
```

The repository verifier replays the map verifier, all prior scientific-package manifests, six frozen manifests, navigation/frontier/current-path checks, the documented test baseline, and metadata-only preservation of the original dirty checkout.
