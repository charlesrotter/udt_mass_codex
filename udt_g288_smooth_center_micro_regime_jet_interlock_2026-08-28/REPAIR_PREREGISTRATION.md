# G288 external-review repair preregistration

Date: 2026-08-28
State: frozen before repair implementation
Scientific landing: unchanged

## Repair-only scope

R1. Replace the independent verifier's hard-coded coefficient table and closed-form random-case
comparator with coefficient data obtained from its own full tensor reconstruction on exact monomial
germs.  The repaired route must still cover both signs of `c2`, `c4=0`, and `c4!=0`.

R2. Preserve `run_catch_proofs.py` only as a saved-artifact and semantic-regression guard.  Add a
separate dependency-free hostile harness whose geometric mutations are rejected by fresh tensor
recomputation, not JSON-string comparison.

R3. Reclassify `verify_package.py` explicitly as an integrity/provenance aggregator.  It may require
the scientific replays to pass, but it must not be described as an independent derivation.

R4. Register the standard-library exact tensor route as the self-contained scientific replay.  Keep
the SymPy production route as a separately useful dependency-declared derivation, not a replay that
is guaranteed in a minimal reviewer environment.

R5. State that the exact quadratic family has sectional curvature `K=-C` in the registered
curvature convention.

## Falsification and ceiling

The repair fails if it changes the scientific equations, weakens exact arithmetic, imports an older
audit, or permits a Planck-scale, physical-mass, history, source, observation, or `X_max` promotion.
The maximum return is repair-only certification of the already accepted bounded G288 landing.
