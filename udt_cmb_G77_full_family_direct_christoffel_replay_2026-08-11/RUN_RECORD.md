# G77 run record

Date: 2026-08-11

Preregistration commit: `0d376014`

Working directory:

```text
/home/udt-admin/udt_mass_codex/udt_cmb_G77_full_family_direct_christoffel_replay_2026-08-11
```

Commands, in order:

```bash
python3 -m py_compile run_direct_christoffel_replay.py
python3 run_direct_christoffel_replay.py --max-new-profiles 0
python3 run_direct_christoffel_replay.py --max-new-profiles 1
script -q -e -c "python3 run_direct_christoffel_replay.py" PRODUCTION_TRANSCRIPT.txt
python3 -m py_compile verify_artifacts_independent.py verify_panel_scipy_independent.py run_catch_proofs.py
python3 verify_artifacts_independent.py
python3 run_catch_proofs.py
script -q -e -c "python3 verify_panel_scipy_independent.py" INDEPENDENT_PANEL_TRANSCRIPT.txt
```

The first bounded invocation created and validated the restartable zero-row checkpoint. The second
computed profile `001/591`. The preserved production transcript contains profiles `002/591`
through `591/591`, the four refinement rows, and the final machine-readable result. Raw checkpoint
arrays preserve all 591 rows, including the first.

Runtime reported by the completed production invocation:

```text
Python 3.10.12
NumPy 2.2.6
SciPy 1.15.3
CPU float64
elapsed_seconds_this_invocation = 2525.6971683502197
```

One CPU process was used. No GPU work ran. Runtime was not a scientific acceptance condition.
