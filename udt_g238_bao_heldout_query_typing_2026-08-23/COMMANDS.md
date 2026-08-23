# G238 registered checks

```bash
python3 -m py_compile \
  udt_g238_bao_heldout_query_typing_2026-08-23/derive_query_typing.py \
  udt_g238_bao_heldout_query_typing_2026-08-23/verify_query_typing_independent.py \
  udt_g238_bao_heldout_query_typing_2026-08-23/verify_package.py \
  udt_g238_bao_heldout_query_typing_2026-08-23/run_catch_proofs.py
python3 udt_g238_bao_heldout_query_typing_2026-08-23/derive_query_typing.py --write
python3 udt_g238_bao_heldout_query_typing_2026-08-23/verify_query_typing_independent.py
python3 udt_g238_bao_heldout_query_typing_2026-08-23/verify_package.py
python3 udt_g238_bao_heldout_query_typing_2026-08-23/run_catch_proofs.py
python3 verify_current_scientific_premises.py
```
