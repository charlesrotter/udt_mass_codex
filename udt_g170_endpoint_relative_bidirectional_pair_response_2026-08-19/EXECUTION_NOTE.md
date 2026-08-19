# G170 execution note

Date: 2026-08-19

Commands:

```bash
python3 udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/derive_endpoint_relative_response.py
python3 udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/verify_endpoint_relative_independent.py
python3 udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/run_catch_proofs.py
```

Observed outputs:

```text
production: 40/40
independent: 21,600/21,600 over 1,200 channel and 1,200 regular angular trials
angular generation: 1,213 attempts for 1,200 accepted regular trials
angular shift live: 1,200/1,200
angular readout changed: 1,200/1,200
mutation catches: 13/13
```

CPU-only exact algebra. No long process or GPU solve was launched.

The first sealed intake's package verifier depended on repository Git history and the outer
premise verifier. After external review, `verify_sealed_intake.py` was added to verify copied source
hashes and replay calculations in a writable temporary copy without modifying or reading outside
the corrected sealed intake. The first repair-only follow-up found that the minimal external
sandbox did not expose SymPy, so the sealed verifier now reruns only the standard-library
independent and mutation implementations. It hash-verifies the stored SymPy result; the SymPy
controller and repository premise verifier remain separate outer banking gates.

Corrected sealed replay observed:

```text
PASS__SEALED_STDLIB_REPLAY__SYMPY_ARTIFACT_HASHED__OUTER_GATES_SEPARATE
12 frozen sources; independent 21,600/21,600; mutation catches 13/13;
saved SymPy production artifact hash-verified at 40/40 but not rerun in the sealed sandbox
```

Dependency-minimal replay command:

```bash
python3 -S /path/to/sealed-intake/udt_g170_endpoint_relative_bidirectional_pair_response_2026-08-19/verify_sealed_intake.py
```

This command passes with environment site packages disabled.
The sealed wrapper also passes `-S` explicitly to both replay children, so the dependency boundary
is enforced end to end rather than inferred from their current imports.
