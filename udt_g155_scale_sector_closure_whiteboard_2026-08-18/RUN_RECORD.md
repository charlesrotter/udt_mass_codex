# Run record

Date: 2026-08-18

Working directory: `/home/udt-admin/udt_mass_codex`

Preregistration commit: `2f5cf474`

Environment:

- Python `3.10.12`;
- SymPy `1.13.1`;
- CPU/symbolic only; no GPU process and no long solve.

Commands:

```bash
python3 -m py_compile \
  udt_g155_scale_sector_closure_whiteboard_2026-08-18/derive_scale_sector_closure.py \
  udt_g155_scale_sector_closure_whiteboard_2026-08-18/verify_scale_sector_independent.py \
  udt_g155_scale_sector_closure_whiteboard_2026-08-18/run_catch_proofs.py
python3 udt_g155_scale_sector_closure_whiteboard_2026-08-18/derive_scale_sector_closure.py
python3 udt_g155_scale_sector_closure_whiteboard_2026-08-18/verify_scale_sector_independent.py
python3 udt_g155_scale_sector_closure_whiteboard_2026-08-18/run_catch_proofs.py
```

Observed results:

- production exact checks: `9/9`;
- frozen sources: `41/41`;
- equation-role rows: `41/41`;
- independent numerical conformal trials: `500/500`;
- independent three-observer conformal triangle trials: `500/500`;
- mutation catches: `6/6`;
- active physical-history common-scale equations: `0`;
- common-scale physical-history principal rank: `0`;
- landing: `RANK_ZERO`.

Load-bearing SHA-256 after the verified run:

```text
99a1f8b79cfbbdc6ede68df8066521235ffb44533832b49d0bb427277d170fc0  DERIVATION_RESULT.json
915e059e15a267ab4796dc250daa4775850843db9f947ec4babb6619b6a355a9  INDEPENDENT_RESULT.json
f1b2745a96d9adcb69a198be41093f857ce62ec48c716a3adc112a58988c93a9  CATCH_PROOF_RESULT.json
02cf55ad80b219c5caa5c00e1406290fdace3b5efb1239669f3676c29f6db65e  EQUATION_ROLE_LEDGER.tsv
d27e51d86901580a6b2dca26900347da8694301378fec3eacd35c60f1b4c82fa  VERIFICATION_RESULT.json
```
