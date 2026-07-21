# Commands and environment

Successful CPU commands from repository root:

```text
python3 c2_transverse_coframe_closure_2026-07-20/derive_gauge_structure.py
python3 c2_transverse_coframe_closure_2026-07-20/derive_transverse_background.py
python3 c2_transverse_coframe_closure_2026-07-20/verify_transverse_coframe.py
python3 c2_transverse_coframe_closure_2026-07-20/analyze_closure.py
python3 c2_transverse_coframe_closure_2026-07-20/verify_package.py
```

The exact general twist command was stopped after ten minutes with exit `130` and no result:

```text
python3 c2_transverse_coframe_closure_2026-07-20/derive_transverse_twist.py
```

Environment:

```text
Python 3.10.12
SymPy 1.13.1
Torch 2.5.1+cu121
Torch dtype float64
device CPU
```

The Torch build includes CUDA support, but every tensor was created on CPU and no GPU process ran.
All pre-bank corrections and the timeout are preserved in named records.
