# G263 repair-only external follow-up request

Verify only repairs R1–R3 in `REPAIR_PREREGISTRATION.md` and the unchanged bounded G263 scientific
landing. Do not continue the research or alter the scientific question.

Required checks in the writable ephemeral copy:

```bash
python3 udt_g263_pair_reversal_profile_sign_parity_2026-08-25/verify_sealed_replay.py
python3 udt_g263_pair_reversal_profile_sign_parity_2026-08-25/run_catch_proofs.py
python3 udt_g263_pair_reversal_profile_sign_parity_2026-08-25/verify_repair_catches.py
python3 udt_g263_pair_reversal_profile_sign_parity_2026-08-25/verify_package.py
```

Also perform altered-copy probes for the five registered reviewer escapes and for corrupted sealed
replay evidence. Return `ACCEPT_REPAIR`, `REPAIR_INCOMPLETE`, or `REJECT_REPAIR`, with exact defects.
