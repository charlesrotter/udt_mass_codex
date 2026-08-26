# G275 run record

Date: 2026-08-26

Environment: repository Python 3, SymPy production algebra, Python standard-library `Fraction`
independent arithmetic. CPU only; no GPU process or long solve.

Production:

```bash
python3 udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/derive_projective_scale_attachment.py
```

Independent:

```bash
python3 udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/verify_scale_attachment_independent.py
```

Hostile catches:

```bash
python3 udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/run_catch_proofs.py
```

Result: production PASS, independent PASS, hostile catches PASS.
