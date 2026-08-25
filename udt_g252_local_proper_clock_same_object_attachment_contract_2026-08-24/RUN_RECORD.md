# G252 run record

Date: 2026-08-24

All scientific scripts were run with `PYTHONDONTWRITEBYTECODE=1`. They write only when an explicit
output path is supplied.

- Production: 4,096 exact rational cases; 18,451 segment terms; 20,480 assertions; PASS.
- Independent: 12,000 exact rational cases; 60,000 assertions; 12,000 inconsistent second
  attachments rejected; PASS.
- Hostile: 20 of 20 executable mutations caught; PASS.
- Observational values read: 0.
- Fitted coefficients: 0.
- GPU: not used.
- Long solve/checkpoint: not applicable.

Fresh external review returned `ACCEPT_WITH_REPAIRS` because the original sealed intake relocated
sources under `sources/` while three verifiers searched only the repository layout. The scientific
landing was retained. The repair was preregistered at `80581067`, then implemented. A fresh 33-file
repair test intake replayed production, independent, hostile, and package commands successfully.
The current 234-row premise verifier also passed. External repair-only follow-up remains pending.
