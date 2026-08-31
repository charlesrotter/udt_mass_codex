# G307 registered commands

## Sealed package replays

Run from this package directory with no third-party package import. In a sealed layout, run from a
writable copy so the first three commands can regenerate their registered outputs:

```bash
python3 -S derive_directed_member_reconstruction.py
python3 -S verify_directed_member_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
python3 -S build_review_intake.py
python3 -S verify_repair_portability.py
```

## Repository-only gates

Run the current premise audit and repository regression only from the complete repository root:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

The first three sealed commands write only their registered JSON/TSV outcome files inside this
package. `verify_package.py` is a no-write check. The intake builder writes only a new sealed
directory under `/tmp` and resolves either repository or sealed `frozen_*` layouts uniquely. The
whole-repository premise verifier and pytest are recorded gates, not self-contained sealed replays.
