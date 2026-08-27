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

External review retained the scientific landing and requested certification repairs R1--R3.
Those repairs were preregistered at commit `18f84136`. The corrected run adds an exact sealed-root
manifest verifier, fail-closed sealed-source resolution, three ephemeral tamper checks, and a real
eight-entry mutation/scope ledger. No scientific formula or landing changed.

The first repair-only follow-up retained the science but found the repair harness was not replayable
from inside the sealed intake. R4, preregistered at `a16436e3`, adds package-local frozen-source
resolution, sealed-entrypoint detection, a sealed builder replay, and a fake-Git tripwire.

The final repair-only `gpt-5.4` follow-up used the authorized 41-file intake and returned
`R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`. It reran the sealed harness and an intake-only bounded
repository-mode simulation; both passed and the fake-Git marker remained absent.
