G245_REPAIR_FOLLOWUP_ACCEPTED

- `REVIEW_SCOPE.json` declares `29` scoped files excluding the scope file; I recomputed all `29` SHA-256 hashes and found `0` mismatches.
- `COMMANDS.md` now contains exactly four self-contained G245 `--no-write` replay commands, and it clearly labels `python3 verify_current_scientific_premises.py` plus `python3 -m pytest -q` as repository-only gates, not bounded sealed replay.
- I replayed all four registered commands with bytecode writes disabled. All exited successfully.
- The replay matched the saved bounded outputs: production exact, independent exact, and catch exact. `verify_package.py --no-write` returned `PASS` with `source_count: 5`, unchanged classification, `production_cases: 1024`, `independent_cases: 5000`, and `hostile_catches: 12`.
- `REVIEW_REPAIR_EXECUTION_NOTE.md` records the same five-source authority set and states that no production result, independent result, hostile catch, theorem, classification, or observational boundary changed; the successful exact replays are consistent with that bounded landing.
- Remaining defect: none.
