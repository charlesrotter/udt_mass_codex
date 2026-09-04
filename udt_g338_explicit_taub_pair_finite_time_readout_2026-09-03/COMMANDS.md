# G338 commands

Run from the package directory with no site packages:

```bash
python3 -S derive_explicit_taub_pair_readout.py
python3 -S verify_explicit_taub_pair_readout_independent.py
python3 -S run_catch_proofs.py
```

The scripts write only their registered JSON result beside themselves. They require only the Python
standard library and do not use a GPU, network, observations, or repository-global imports.
