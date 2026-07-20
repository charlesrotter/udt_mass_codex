# Commands and environment

All calculations were run from repository root on CPU only.

```text
python3 c2_intrinsic_angular_product_selector_2026-07-20/derive_product_background.py
python3 c2_intrinsic_angular_product_selector_2026-07-20/derive_product_twist.py
python3 c2_intrinsic_angular_product_selector_2026-07-20/analyze_product_branches.py
python3 c2_intrinsic_angular_product_selector_2026-07-20/verify_intrinsic_product.py
python3 c2_intrinsic_angular_product_selector_2026-07-20/verify_package.py
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

The first symbolic twist gate and constant-zero numerical diagnostic are preserved in
`FIRST_TWIST_GATE_CORRECTION.md` and `VERIFIER_ZERO_MODE_CORRECTION.md`. The action-density premise
correction is preserved in `ACTION_DENSITY_CORRECTION.md`. All occurred before banking a verdict.
