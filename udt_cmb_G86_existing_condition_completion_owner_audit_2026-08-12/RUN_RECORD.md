# G86 run record

Date: 2026-08-12
Branch: `grok`
Base: `b8875ccffaaa422e3447c58895017e475202a804`
Preregistration: `2778b16ee8a2f034670d90e3ddc6c8d853706320`
Python: `3.10.12`
Hardware: CPU only

## Commands

```text
python3 udt_cmb_G86_existing_condition_completion_owner_audit_2026-08-12/derive_owner_atlas.py
python3 udt_cmb_G86_existing_condition_completion_owner_audit_2026-08-12/verify_independent.py
python3 udt_cmb_G86_existing_condition_completion_owner_audit_2026-08-12/run_catch_proofs.py
python3 udt_cmb_G86_existing_condition_completion_owner_audit_2026-08-12/verify_repository_gates.py
python3 -m pytest -q tests/
```

## Output identities before navigation edits

```text
11054c9fd3d0444d711bfa94699cbbba5a44f4d136761540b9b8e49dced26e65  CONDITION_OWNER_ATLAS.tsv
a3e88831e461a792031c25c235249b1d908de2456a94713804a90e16c42b68ac  FAMILY_CONDITION_MATRIX.tsv
8f5a8aad6b32c7038f5c3cd116df9599f4f3dbfb872a6343894d7d152d4bb95c  CONDITIONAL_SELECTOR_ATLAS.tsv
b1a07337b8ec449fdf702b78bd95d9fb3c1266d7d2034a0b330360409612abe6  DERIVATION_RESULT.json
d80a099706fca36a7de8fb2b0cba7ab3e37dbfb1690dc81619bc4167e9998e8c  INDEPENDENT_VERIFICATION.json
5c60f1d4ef54a47a91e967376db93b29609d465f55eb908be0fe5dd1817bcce9  CATCH_PROOF_RESULT.json
613a3121cdf6cba1d5edab6d01f028387c414451b6a08a431530c92d0b779829  REPOSITORY_GATES.json
```

The independent replay returns `VERIFIED_WITH_CAVEATS`; all `12/12` hostile mutations are caught.
Repository gates return `PASS`, including tests `103 passed, 1 xfailed`. No GPU or observational fit
was run. The protected stopped draft remained seven untracked paths and its contents were unread.
