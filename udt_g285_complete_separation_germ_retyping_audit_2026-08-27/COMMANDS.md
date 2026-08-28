# G285 registered commands

Run from repository root after the preregistration commit:

```bash
python3 -S udt_g285_complete_separation_germ_retyping_audit_2026-08-27/verify_preregistration.py
python3 -S udt_g285_complete_separation_germ_retyping_audit_2026-08-27/derive_complete_separation_retyping.py
python3 -S udt_g285_complete_separation_germ_retyping_audit_2026-08-27/verify_independent.py
python3 -S udt_g285_complete_separation_germ_retyping_audit_2026-08-27/run_catch_proofs.py
python3 -S udt_g285_complete_separation_germ_retyping_audit_2026-08-27/verify_package.py
```

All production scripts are standard-library only. They write no repository files; stdout is captured
into immutable evidence artifacts only after the preregistration is banked.
