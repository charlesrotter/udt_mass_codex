# Commands and environment

All calculations were CPU-only from repository root.

```text
python3 c2_coupled_reciprocal_twist_onshell_2026-07-20/derive_background_bach.py
python3 c2_coupled_reciprocal_twist_onshell_2026-07-20/analyze_background_branches.py
python3 c2_coupled_reciprocal_twist_onshell_2026-07-20/verify_background_bach.py
python3 c2_coupled_reciprocal_twist_onshell_2026-07-20/verify_package.py
```

Environment:

```text
Python 3.10.12
SymPy 1.13.1
Torch 2.5.1+cu121
Torch dtype float64
device CPU
```

The Torch build tag includes CUDA support, but the verifier creates only CPU tensors and no GPU
process was launched. `requirements.txt` pins the public package versions.

The two pre-bank branch-harness stops are preserved in `PRESOLVE_CHECK_CORRECTION.md`. They were a
symbolic expression-tree comparison and JSON boolean-serialization issue; neither wrote an outcome
or changed any equation, profile, branch, tolerance, or conclusion.
