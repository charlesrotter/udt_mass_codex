# G238 registered checks

## Repository production

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

The final premise-verifier command is repository-wide and is not part of the sealed external
replay.

## Sealed external replay

The sealed intake itself is read-only. Copy it to a disposable directory, make only that copy
writable, and run the registered checks from its root:

```bash
g238_runtime="$(mktemp -d)"
cp -a /path/to/sealed-intake/. "$g238_runtime"/
chmod -R u+w "$g238_runtime"
cd "$g238_runtime"
python3 -m py_compile \
  udt_g238_bao_heldout_query_typing_2026-08-23/derive_query_typing.py \
  udt_g238_bao_heldout_query_typing_2026-08-23/verify_query_typing_independent.py \
  udt_g238_bao_heldout_query_typing_2026-08-23/verify_package.py \
  udt_g238_bao_heldout_query_typing_2026-08-23/run_catch_proofs.py
python3 udt_g238_bao_heldout_query_typing_2026-08-23/derive_query_typing.py --write
python3 udt_g238_bao_heldout_query_typing_2026-08-23/verify_query_typing_independent.py
python3 udt_g238_bao_heldout_query_typing_2026-08-23/verify_package.py
python3 udt_g238_bao_heldout_query_typing_2026-08-23/run_catch_proofs.py
```

Do not invoke `verify_current_scientific_premises.py` inside the sealed intake; it is deliberately
outside that bounded review payload.
