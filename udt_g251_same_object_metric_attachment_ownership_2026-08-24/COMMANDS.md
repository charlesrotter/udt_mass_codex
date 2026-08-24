# G251 registered commands

Set `PYTHONDONTWRITEBYTECODE=1` for every replay.

## Scientific no-write replays

```bash
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/derive_attachment_ownership.py --cases 4096
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/verify_attachment_ownership_independent.py --cases 12000
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/run_catch_proofs.py
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/verify_sealed_premise_registry.py
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/verify_package.py
```

These scripts write only when an explicit output path is supplied.

## Repository-only full startup and premise gate

```bash
python3 verify_current_scientific_premises.py
```

The sealed `verify_sealed_premise_registry.py` replay is self-contained and checks the exact frozen
233-row registry plus the load-bearing G249/G250 rows. The repository-wide command additionally
checks the entire startup surface and its broad historical dependency closure; it is run before
banking but is intentionally not misrepresented as self-contained inside the 12-source intake.
