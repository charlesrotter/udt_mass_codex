# Commands

```bash
python3 udt_wrl_xmax_lightcone_frame_audit_2026-07-23/derive_wrl_xmax_lightcone_frame.py --write
python3 udt_wrl_xmax_lightcone_frame_audit_2026-07-23/verify_wrl_xmax_lightcone_frame_independent.py
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
```

Production uses pinned `sympy==1.13.1`. The independent route uses only the
Python standard library and does not import the production module.
