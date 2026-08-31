# G306 command environments

## Self-contained package and sealed-intake replay

From the repository root or a writable copy of the sealed intake root:

```bash
python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/derive_intrinsic_hopf_section.py
python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/verify_intrinsic_hopf_section_independent.py
python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/run_catch_proofs.py
python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/verify_package.py
```

These four commands use only Python's standard library and files included in the sealed intake.
They are the complete registered sealed replay.

The repair meta-certificate copies the package and frozen sources into a fresh temporary layout,
runs those four commands, compares production outputs byte-for-byte, and tests missing/ambiguous
source rejection:

```bash
python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/verify_repair_portability.py
```

## Repository-only gates

The following commands test the surrounding repository and are intentionally not claims about a
bounded intake's contents:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```

They must pass in the repository before a follow-up intake is built. Their exact counts are recorded
in `PACKAGE_VERIFICATION_RESULT.json` and `EVIDENCE_GATES.md`; they are regression evidence, not
self-contained sealed replay commands.

The repository-only follow-up intake builder is:

```bash
python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/build_repair_followup_intake.py
```
