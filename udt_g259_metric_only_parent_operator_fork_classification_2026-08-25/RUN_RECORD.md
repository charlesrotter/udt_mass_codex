# G259 run record

Date: 2026-08-25
Branch: `grok`
Preregistration commit: `a1fa9d7d`

## Commands

```bash
python3 derive_parent_operator_fork.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_dependency_free.py --write-result
python3 verify_package.py
```

## Results

- conditional four-dimensional Lovelock basis dimension: 2 (`g_ab`, `G_ab`);
- flat quiet-vacuum inclusion removes the metric/cosmological term;
- conditional nonzero vacuum operator has the Einstein zero set;
- spherical residual dependence and mass-aspect identities: exact;
- higher-order counterfamily: exact and nonidentity off the Ricci-flat branch;
- independent verification: 111 exact-rational assertions;
- hostile controls: 11/11;
- dependency-free replay: 139 exact standard-library assertions;
- fitted coefficients: zero;
- observational values: zero;
- GPU: not used;
- protected packages: not read.

Fresh external review returned `ACCEPT_WITH_REPAIRS`. The theorem-scope, zero-operator, and
dependency-free-replay repairs were implemented. The sealed repair-only follow-up returned
`ACCEPT_REPAIRS` after reproducing the 111-assertion independent replay, 139-assertion
dependency-free replay, and package integrity with all 11 catches.

## Repair catch proofs

- changing `locality` from `NEW_PREMISE_CANDIDATE` to `DERIVED` in an ephemeral copy makes
  `run_catch_proofs.py` exit `1`;
- admitting `a=0` as a physical Einstein-zero-set law in an ephemeral copy makes
  `verify_dependency_free.py` exit `1`;
- `python3 -m pytest tests/` exits `0` across 164 collected tests with one expected xfail;
- the 242-row current-premise verifier passes.
