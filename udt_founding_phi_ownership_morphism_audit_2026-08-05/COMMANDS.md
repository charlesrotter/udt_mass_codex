# Commands

```bash
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/freeze_sources.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/freeze_source_addendum.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/derive_founding_ownership.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/independent_founding_ownership.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/verify_audit.py --write
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/verify_audit.py
```

All derivation work is exact CPU rational/symbolic algebra. No GPU or long solve is used.

# Banking and preservation replay

```bash
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/derive_founding_ownership.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/independent_founding_ownership.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/verify_audit.py --write
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/verify_repository_gates.py
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/verify_package_manifest.py --write
python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/verify_package_manifest.py
```

`FRESH_ADVERSARIAL_REVIEW_RAW.txt` and `REVIEW_REPAIR_RAW.txt` preserve their PTY-captured bytes
exactly. The final staged whitespace check excludes only those two raw evidence streams.
