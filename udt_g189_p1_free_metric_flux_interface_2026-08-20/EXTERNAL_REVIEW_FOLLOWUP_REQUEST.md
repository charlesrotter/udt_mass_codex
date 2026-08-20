# G189 repair-only external follow-up request

Review only the two repairs preregistered in `EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md` after the
fresh review returned `G189_ACCEPTED_WITH_REPAIRS`.

## Exact checks

1. Confirm that the DES entries in `SOURCE_MANIFEST.tsv` are logical `external_data/...` paths and
   that the production and intake-builder code resolve them only through the explicitly supplied
   `G189_DES_ROOT` environment variable. No executable G189 source may retain a host-default data
   path.
2. Confirm that `verify_p1_free_flux_independent.py` does not read `PRODUCTION_RESULT.json`, imports
   no production implementation, and derives its own result from the sealed raw data.
3. Confirm that `verify_package.py`, rather than the second implementation, owns the explicit
   production-versus-independent comparison.
4. Run the sealed replay below and verify the registered science outputs are unchanged.
5. Do not reopen, extend, or continue the scientific investigation.

## Required landing

Return exactly one:

```text
G189_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
G189_REPAIRS_REQUIRE_FURTHER_MECHANICAL_WORK
G189_REPAIRS_CHANGE_SCIENTIFIC_LANDING
```

## Sealed replay

From the intake root:

```bash
G189_DES_ROOT="$PWD/external_data" \
python3 udt_g189_p1_free_metric_flux_interface_2026-08-20/verify_package.py
```

The review is read-only. Inspect only the sealed intake. Do not edit files or continue the
research.
