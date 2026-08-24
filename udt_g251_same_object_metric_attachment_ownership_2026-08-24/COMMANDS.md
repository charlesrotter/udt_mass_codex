# G251 registered commands

Set `PYTHONDONTWRITEBYTECODE=1` for every replay.

## Scientific no-write replays

```bash
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/derive_attachment_ownership.py --cases 4096
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/verify_attachment_ownership_independent.py --cases 12000
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/run_catch_proofs.py
```

These scripts write only when an explicit output path is supplied.

## Repository-only gate

```bash
python3 verify_current_scientific_premises.py
```
