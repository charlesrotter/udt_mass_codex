# G263 repair result

Date: 2026-08-25

Repair contract: `REPAIR_PREREGISTRATION.md`, banked at `0ac8f0c5` before implementation.

## R1 — dependency-free sealed replay

`verify_sealed_replay.py` now recomputes the bounded G263 landing with the Python standard library
only. It imports neither SymPy nor production code and reads no saved result. The registered output
contains:

- 1,000 exact rational cases;
- 38,010 assertions;
- 421 negative-`phi`, 53 zero-`phi`, and 526 positive-`phi` cases;
- 1,000 shared scalar-inversion checks;
- 1,000 areal-sphere guards;
- 947 off-fixed-point metric separations;
- 577 nonquiet conjugate zero-tide witnesses;
- exact finite witnesses plus an explicit elementary-limit qualification for the scoped
  constant-jet end table.

`RUN_RECORD.md` now separates local SymPy/repository gates from the commands actually available in
the sealed repair intake.

## R2 — mutation escapes closed

`run_catch_proofs.py` now requires the exact complete 31-name symbolic-check list and exact
structured values for both operations, their shared/distinct separation, sphere guard, and scoped
constant-jet ends. The five reviewer probes are registered mutations. All 17/17 mutations are
caught.

`verify_repair_catches.py` additionally proves in disposable altered copies that all five reviewer
escapes now fail and that the package verifier rejects corrupted sealed-replay and mutation-result
evidence: 7/7 altered-copy catches.

## R3 — independence qualification retained

The sealed replay remains exact implementation-distinct algebra, not an independent physical
premise or valued-history derivation. No history, physical mass, source, dynamics, universal
loudness, or `X_max` result is promoted.

## Landing

```text
REPLAY_PORTABILITY_AND_MUTATION_GUARDS_REPAIRED
__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED
__EXTERNAL_REPAIR_FOLLOWUP_REQUIRED
```
