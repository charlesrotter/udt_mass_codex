# G284 repair preregistration

Date: 2026-08-27

External verdict: `ACCEPT-WITH-REPAIRS`; bounded scientific landing accepted unchanged.

## Frozen repairs

### R1 — dependency-free symbolic replay

Replace the registered SymPy-dependent production command with a dependency-free standard-library
exact derivation that checks the same 20 claims on the full arbitrary smooth symmetric `T(u)`
coefficient class. Retain the original SymPy script only as a supplemental development control, not
as the durable sealed replay.

Acceptance:

- no third-party imports;
- all three functions `T_xx(u)`, `T_xy(u)`, and `T_yy(u)` remain algebraically live;
- determinant, inverse, central metric/first jet/connection, `c_E` coordinate cone, central clock
  state, neighboring nullness/Hessian, curvature/Jacobi sign, Hamiltonian generator, and constant
  homothety checks remain exact;
- output landing and 20/20 claim results remain unchanged.

### R2 — executable replay certification

Regrade `verify_package.py` explicitly as a fail-closed package-and-replay verifier. It must construct
an ephemeral copy containing the package plus exactly the frozen source-manifest files, execute the
four registered dependency-free recomputations there, require zero exit codes, and then validate the
saved artifacts and wording gates. A saved passing JSON file alone must no longer suffice.

Acceptance:

- the verifier runs `verify_preregistration.py`, the R1 derivation, `verify_independent.py`, and
  `run_catch_proofs.py` in an ephemeral copy;
- every replay command exits zero and emits the expected status token;
- the verifier records the four command names and exit codes;
- an in-memory mutation that breaks any replay command is caught;
- no source, premise, witness, tolerance, scientific question, or landing changes.

## Scientific boundary

These are reproducibility repairs only. They may not add a field equation, source, action, matter
model, observation, fit, scale, operational distance, history, population, `X_max`, or new causal
principle. The accepted landing remains:

```text
EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_TIDAL_HISTORY
```
