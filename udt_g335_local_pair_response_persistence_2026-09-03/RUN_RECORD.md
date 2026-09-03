# G335 run record

Date: 2026-09-03

```text
python3 -B -S derive_local_pair_persistence.py --output DERIVATION_RESULT.json
171124 exact checks over 13728 response cases

python3 -B -S verify_local_pair_persistence_independent.py --output INDEPENDENT_VERIFICATION.json
4448 checks; PASS

python3 -B -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
12 hostile mutations caught; PASS
```

Fresh external `gpt-5.4` review authenticated the 32-payload manifest, replayed all 78 aggregate
gates, and returned `ACCEPT__G335_BOUNDED_LOCAL_PAIR_PERSISTENCE_RETAINED` with no repairs.
