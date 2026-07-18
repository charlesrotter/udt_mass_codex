# Repository test audit

**Date:** 2026-07-18

**Execution:** CPU only; GPU visibility disabled; Python bytecode disabled

## Required full run

```text
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/
```

```text
collected 71 items
69 passed
1 xfailed
1 failed
```

The expected xfail is
`tests/test_solution_space_gate.py::test_no_habit_pins`, whose repository reason says the known
HABIT pins remain until the matter sector is freed or justified to theory.

The failure is
`tests/test_hygiene_header.py::test_covered_results_have_hygiene_header`. It reports missing hygiene
markers or an out-of-vocabulary build-on grade in unchanged legacy files matching
`simple_metric_*_results.md`, including the EOS, GR-mine, HL, L/P, WR-L-center, BAO, dS, kaleidoscope,
local-cavity, and time-live families. The test did not name the preregistration or any file in the
final-adjudication package.

`git status` before and after the run shows those legacy result files are not modified by this task.
The failure is therefore disclosed as a pre-existing repository hygiene debt, not repaired inside a
native-action adjudication and not hidden by narrowing the required run.

## Scoped confirmation

```text
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ --ignore=tests/test_hygiene_header.py
```

```text
collected 68 items
67 passed
1 xfailed
0 failed
```

This scoped run covers branch/operator, N5D, action-operator, solution-space, and solver-integrity
tests. It does not convert the full-suite hygiene failure into a pass.

## Disposition

- Preserve the failure in this package.
- Do not edit unrelated historical headers or reorganize the repository.
- Do not weaken the final physics statuses because of an unrelated documentation-hygiene failure.
- Do not claim the repository-wide suite is green.
