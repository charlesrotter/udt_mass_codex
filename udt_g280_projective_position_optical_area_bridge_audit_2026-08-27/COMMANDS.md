# G280 commands

Preregistration phase only. No outcome command is authorized until this preregistration is banked.

Bounded replays:

```bash
python3 freeze_source_manifest.py
python3 derive_projective_optical_bridge.py
python3 verify_projective_optical_bridge_independent.py
python3 run_catch_proofs.py
python3 derive_projective_optical_bridge.py --no-write
python3 verify_projective_optical_bridge_independent.py --no-write
python3 run_catch_proofs.py --no-write
python3 verify_package.py
```

Repair-follow-up seal:

```bash
python3 build_review_intake.py --repair-followup
```
