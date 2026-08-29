# G294 commands

```bash
python3 udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/derive_copresence_architecture.py \
  --output udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/DERIVATION_RESULT.json

python3 udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/verify_copresence_independent.py \
  --output udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/INDEPENDENT_VERIFICATION.json

python3 udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/run_catch_proofs.py \
  --package udt_g294_nonsignalling_copresence_network_architecture_2026-08-29 \
  --output udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/CATCH_PROOF_RESULT.json

python3 udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/freeze_source_manifest.py

python3 udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/verify_package.py \
  --package udt_g294_nonsignalling_copresence_network_architecture_2026-08-29 \
  --output udt_g294_nonsignalling_copresence_network_architecture_2026-08-29/PACKAGE_VERIFICATION_RESULT.json

python3 verify_current_scientific_premises.py
```
