# G337 registered commands

Run from repository root:

```bash
python3 -B -S udt_g337_double_silent_third_normal_ownership_2026-09-03/build_source_manifest.py
python3 -B -S udt_g337_double_silent_third_normal_ownership_2026-09-03/derive_double_silent_third_response.py --output udt_g337_double_silent_third_normal_ownership_2026-09-03/DERIVATION_RESULT.json
python3 -B -S udt_g337_double_silent_third_normal_ownership_2026-09-03/verify_double_silent_third_response_independent.py --output udt_g337_double_silent_third_normal_ownership_2026-09-03/INDEPENDENT_VERIFICATION.json
python3 -B -S udt_g337_double_silent_third_normal_ownership_2026-09-03/run_catch_proofs.py --output udt_g337_double_silent_third_normal_ownership_2026-09-03/CATCH_PROOF_RESULT.json
python3 -B -S udt_g337_double_silent_third_normal_ownership_2026-09-03/verify_package.py --output udt_g337_double_silent_third_normal_ownership_2026-09-03/PACKAGE_VERIFICATION_RESULT.json
```
