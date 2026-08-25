# G260 run record

Date: 2026-08-25
Branch: `grok`
Preregistration commit: `0857c2a2`

## Registered commands

```bash
python3 derive_angular_nondiscard.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

## Current results

- production full-metric dependency-free exact derivation: PASS;
- third-party production dependencies: none;
- repaired production result SHA-256: `ddc9b6f0ef357cf433d171472e51d49ca7c87352d5464ec4cf2d3349aa429248`
  (byte-identical to the prerepair manifested result);
- independent exact-rational reconstruction: PASS;
- arbitrary metric-jet cases: `700`;
- nonflat vacuum-family cases: `446`;
- trace-balanced cases: `267`;
- independent assertions: `10044`;
- observational values and fit coefficients: zero;
- GPU: not used;
- protected packages: not read.

Fresh external review: `ACCEPT_WITH_REPAIRS`; bounded mathematics accepted and one production-replay
portability defect registered. R1 dependency-free replay repair: PASS. External repair-only
follow-up remains open.
