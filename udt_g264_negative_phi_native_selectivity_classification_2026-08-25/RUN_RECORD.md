# G264 run record

Date: 2026-08-25
Branch: `grok`
Preregistration commit: `8af24ad6aa54e9f69dbe0b00601464a1077c4589`

## Registered executions

```bash
python3 derive_selectivity.py --output DERIVATION_RESULT.json
python3 verify_metric_first.py --output METRIC_FIRST_VERIFICATION.json
python3 verify_independent.py --output INDEPENDENT_VERIFICATION.json
python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 verify_package.py --output VERIFICATION_RESULT.json
python3 verify_current_scientific_premises.py
pytest -q tests/
```

The direct derivation uses SymPy. The metric-first verifier and consistency replay use only the
Python standard library and do not import the production derivation or read its result.

Fresh external review returned `ACCEPT_WITH_REPAIRS`. The bounded scientific landing was accepted;
the independence-evidence repair was preregistered and implemented. Repair-only follow-up is
pending.

## Observed gates

- production symbolic derivation: `PASS`, 27 exact checks;
- independent metric-first tensor derivation: `PASS`, 250 cases and 1,000 exact assertions;
- implementation-distinct consistency replay: `PASS`, 12,000 exact plus 6,025 high-precision assertions;
- applied mutations: `PASS`, 18/18 caught;
- fail-closed package verifier: `PASS`;
- current scientific premise verifier: `PASS`, 245-row registry;
- repository tests before review: `167 passed, 1 xfailed in 64.30s`;
- registered repair metric-first derivation: `PASS`, 250 cases and 1,000 exact assertions;
- registered altered-copy repair catches: `PASS`, 10/10 caught;
- post-repair package verifier: `PASS`;
- post-repair premise verifier: `PASS`, 245-row registry;
- post-repair repository tests: `167 passed, 1 xfailed in 64.32s`.

## First repair follow-up and packaging repair

The first repair-only external follow-up returned `REJECT_REPAIR` solely because the sealed repaired
subtree omitted `SOURCE_MANIFEST.tsv`. It independently accepted R1--R3, reran the metric-first and
consistency checks, caught bounded altered-copy attacks, and left the scientific landing unchanged.

The packaging repair was preregistered before implementation. The corrected seal reconstructs a
repository-shaped `replay_root/` with all seven frozen sources. In a fresh copy:

- all six scientific/evidence commands passed with their unchanged registered counts;
- `verify_package.py` passed and resolved seven sources inside the seal;
- `verify_packaging_catches.py` caught 3/3 missing-manifest, altered-source, and missing-source
  attacks.

Final packaging-repair-only external follow-up returned `ACCEPT_PACKAGING_REPAIR`. The reviewer
verified the 133-file seal, all 131 manifest payloads, seven source resolutions without Git, R1--R3
byte continuity, unchanged scientific and ownership documents, and 3/3 packaging attacks. Its
isolated runtime lacked SymPy, so the production symbolic command was not rerun externally. That
environment qualification is retained; the same sealed command passed locally and the external
dependency-free metric-first verifier passed 1,000 exact assertions.
