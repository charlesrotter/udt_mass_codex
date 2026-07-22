# Commands

```bash
python3 udt_local_selector_holonomy_closure_2026-07-22/build_atlas.py
python3 udt_local_selector_holonomy_closure_2026-07-22/verify_atlas.py
python3 udt_local_selector_holonomy_closure_2026-07-22/freeze_manifest.py
python3 udt_local_selector_holonomy_closure_2026-07-22/verify_repository_gates.py
(cd udt_local_selector_holonomy_closure_2026-07-22 && sha256sum --check MANIFEST.sha256)
```

The first unoptimized build was interrupted before output after it redundantly ran full commutant
classification on already-full and exactly-flat rows. The retained production build uses the same
space and thresholds, with exact stopping rules before expensive subspace classification.

Two verifier development failures are preserved in `PRE_VERIFIER_SCOPE_WORDING_FAILURE.txt` and
`PRE_CATCH_C14_FALSE_PASS.txt`.

