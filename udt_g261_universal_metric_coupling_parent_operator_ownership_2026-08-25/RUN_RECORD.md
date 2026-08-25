# G261 run record

Date: 2026-08-25

No long solve, GPU process, observation, fit, or protected input was used.

Commands, run from this package:

```bash
python3 -m py_compile derive_w4_ownership.py verify_independent.py run_catch_proofs.py
python3 derive_w4_ownership.py
python3 verify_independent.py
python3 run_catch_proofs.py
```

Expected durable outputs:

- `DERIVATION_RESULT.json`
- `OWNERSHIP_ATLAS.tsv`
- `INDEPENDENT_VERIFICATION.json`
- `CATCH_PROOF_RESULT.json`

The first unfinished independent harness contained a tautological jet assertion and the first
hostile harness expected an absent `NOT_ADOPTED` marker. Both were repaired before the evidence was
banked; neither repair changed the preregistered question, controls, landings, or conclusion ceiling.
