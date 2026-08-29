# G293 registered commands

Run from the repository root.

```bash
python3 -m py_compile \
  udt_g293_history_law_architecture_constraint_funnel_2026-08-29/derive_history_architecture_funnel.py \
  udt_g293_history_law_architecture_constraint_funnel_2026-08-29/verify_history_architecture_independent.py \
  udt_g293_history_law_architecture_constraint_funnel_2026-08-29/run_catch_proofs.py \
  udt_g293_history_law_architecture_constraint_funnel_2026-08-29/freeze_source_manifest.py \
  udt_g293_history_law_architecture_constraint_funnel_2026-08-29/verify_package.py

python3 udt_g293_history_law_architecture_constraint_funnel_2026-08-29/derive_history_architecture_funnel.py \
  --output udt_g293_history_law_architecture_constraint_funnel_2026-08-29/DERIVATION_RESULT.json

python3 udt_g293_history_law_architecture_constraint_funnel_2026-08-29/verify_history_architecture_independent.py \
  --output udt_g293_history_law_architecture_constraint_funnel_2026-08-29/INDEPENDENT_VERIFICATION.json

python3 udt_g293_history_law_architecture_constraint_funnel_2026-08-29/run_catch_proofs.py \
  --package udt_g293_history_law_architecture_constraint_funnel_2026-08-29 \
  --output udt_g293_history_law_architecture_constraint_funnel_2026-08-29/CATCH_PROOF_RESULT.json

python3 udt_g293_history_law_architecture_constraint_funnel_2026-08-29/freeze_source_manifest.py

python3 udt_g293_history_law_architecture_constraint_funnel_2026-08-29/verify_package.py \
  --package udt_g293_history_law_architecture_constraint_funnel_2026-08-29 \
  --output udt_g293_history_law_architecture_constraint_funnel_2026-08-29/PACKAGE_VERIFICATION_RESULT.json

python3 verify_current_scientific_premises.py
```
