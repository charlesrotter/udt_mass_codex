# G312 run record

Date: 2026-09-01
Device: CPU
Arithmetic: Python standard-library exact `Fraction`
GPU: not used
Long solve: none

Commands:

```bash
python3 -S derive_response_constitution.py
python3 -S verify_response_constitution_independent.py
python3 -S run_catch_proofs.py
```

Results:

- production: 4,690 exact checks;
- independent: 4,824 exact checks;
- semantic regression catches: 6/6;
- common landing: `TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED`.
