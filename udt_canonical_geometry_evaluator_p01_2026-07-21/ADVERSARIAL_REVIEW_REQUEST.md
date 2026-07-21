# Fresh adversarial review request

Review only the P01 package `udt_canonical_geometry_evaluator_p01_2026-07-21` in the current
repository. Do not edit files, run network searches, or inspect unrelated scientific packages except
the exact sources named by this package when needed to test a status claim.

Independently audit:

1. whether the metric, derivative-of-connection, Riemann, Ricci, scalar, spin-connection, first
   Cartan, and second Cartan index/sign conventions are mutually correct;
2. whether the conditional ten-slot `2+2` forward map, reverse map, block inverse, determinant, and
   value/first/second-channel coverage are actually complete inside a supplied split;
3. whether the coframe local-Lorentz and linear-coordinate reconstruction tests could pass
   circularly or omit a load-bearing transformation;
4. whether the CSN constant weights and variable connection transformation are correct;
5. whether `verify_p01_evaluator.py` is genuinely independent where claimed and whether any shared
   code could hide an error;
6. malformed, singular, symmetry, signature, and mutation catches;
7. any imported action, GR equation, preferred `phi` join, selected reciprocal plane, desired-result
   leakage, or conclusion/status overstatement; and
8. whether the evidence supports at most
   `GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED`.

You may run the two bounded CPU scripts and small independent calculations. Report exact file/line
locations for defects. Distinguish a blocking correctness failure from a coverage caveat or optional
improvement. End with exactly one verdict:

- `PASS`
- `PASS_WITH_CAVEATS`
- `FAIL_BLOCKING`

Do not propose physics, an action, P02 execution, an ODE/PDE, or a selector.
