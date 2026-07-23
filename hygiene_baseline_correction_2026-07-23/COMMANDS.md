# Commands

```bash
python3 hygiene_baseline_correction_2026-07-23/verify_hygiene_correction.py
python3 hygiene_baseline_correction_2026-07-23/run_full_tests.py
python3 hygiene_baseline_correction_2026-07-23/build_manifest.py
python3 hygiene_baseline_correction_2026-07-23/verify_repository_gates.py
sha256sum -c hygiene_baseline_correction_2026-07-23/MANIFEST.sha256
```

All computations are CPU-only. The independent verifier copies only the 70 covered documents and
the hygiene-test controls into disposable temporary directories, applies four registered
mutations, and confirms that the actual pytest test turns red. It never modifies the source
documents.
