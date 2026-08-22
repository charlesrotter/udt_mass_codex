# G210 run record

Date: 2026-08-21

## Environment

- repository: `/home/udt-admin/udt_mass_codex`
- branch: `grok`
- preregistration commit: `d1458d37`
- computation: CPU, exact SymPy/Fraction plus 120-digit `mpmath`
- GPU: not used

## Commands

```bash
python3 udt_g210_g205_spatial_volume_robustness_2026-08-21/derive_spatial_volume.py
python3 udt_g210_g205_spatial_volume_robustness_2026-08-21/verify_spatial_volume_independent.py
python3 udt_g210_g205_spatial_volume_robustness_2026-08-21/run_boundary_diagnostics.py
```

## Initial results

- production assertions: 24 after the disclosed structural-simplification repair
- independent exact cases: 10,000
- independent assertions: 250,001
- high-precision profiles: 4 at 120 digits
- hostile catches: 25
- source hashes: 9/9 passed in live repository context
- byte-stable registered no-write replay: passed

The first production run stopped closed on a SymPy structural-equality mismatch. The comparison
was repaired by simplifying the exact difference to zero without changing the formula or expected
result. A mixed-case landing-token typo was also corrected before package assembly.

## External review

- sealed intake: `/tmp/udt_g210_review_e7hcvu9c`
- scope SHA-256: `a24c576e2deddfa0531bbb8645f92d2e31c002799b9a31616e69e22119c463a0`
- tree SHA-256: `316bc5cb513911595a9b8903d3d48af0ac40c962183019dc22669776ec44f16e`
- payload hashes: 35/35 passed
- registered no-write replay: passed
- reviewer grade: `VERIFIED_WITH_CAVEATS`
- required repairs: none
- scientific landing: unchanged
