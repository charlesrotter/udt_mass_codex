# G263 run record

Date: 2026-08-25

Question: metric-led exact parity classification, not a solve.

Local production and repository-gate commands:

```bash
python3 derive_parity.py --output DERIVATION_RESULT.json
python3 derive_parity.py
python3 verify_independent.py --output INDEPENDENT_VERIFICATION.json
python3 verify_independent.py
python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 run_catch_proofs.py
python3 verify_repair_catches.py --output REPAIR_CATCH_RESULT.json
python3 verify_repair_catches.py
python3 verify_package.py --output VERIFICATION_RESULT.json
python3 verify_package.py
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```

Self-contained sealed repair replay:

```bash
python3 verify_sealed_replay.py --output SEALED_REPLAY_RESULT.json
python3 verify_sealed_replay.py
python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 run_catch_proofs.py
python3 verify_package.py --output VERIFICATION_RESULT.json
python3 verify_package.py
```

The repository premise verifier and `pytest tests/` are local repository gates, not commands that
can be rerun from a sealed intake unless those repository files are explicitly included. The
dependency-free sealed replay uses Python's standard library only. `derive_parity.py` remains the
local SymPy production derivation and is not misreported as dependency-free.

Runtime: CPU algebra only; no GPU process and no long solve.

Inputs: the exact ten-source `SOURCE_MANIFEST.tsv`; no protected package, observation, fit, source,
action, or imported field equation.

Outputs are overwritten only by their registered producer commands. Fresh adversarial review is
required before the repaired provisional grade can close.
