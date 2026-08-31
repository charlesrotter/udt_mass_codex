# G309 external-review repair preregistration

Date: 2026-08-31
Frozen reviewed parent: `7d72de0d`
External verdict: `G309_ACCEPTED_WITH_STATED_CAVEATS`

## Discovery

The fresh external reviewer found no scientific defect in the bounded G309 landing and independently
reproduced its load-bearing curvature and residual witnesses. It found one medium evidence defect:
the command registered as the production no-write replay imports SymPy, which was not present in the
sealed review runtime. The independent verifier, hostile checks, and saved-result package verifier
all replayed successfully, but the production derivation itself did not.

The reviewer also recorded that the two commands explicitly labelled `Repository-only gates` were
not included in the sealed intake and therefore remained reported provenance rather than reviewer-
replayed evidence.

## Exact bounded repairs

R1. Replace the SymPy-dependent production derivation with a Python-standard-library implementation
that checks the same exact algebraic identities, flat-join polynomial structure, conditional
constant relation, and numerical deformation witness. It must preserve the 13-check count, output
schema, premise ownership, and scientific landing.

R2. Strengthen `verify_package.py` so it executes the live dependency-free production builder and
requires equality with `DERIVATION_RESULT.json`, rather than checking the saved JSON alone.

R3. Amend `COMMANDS.md` and `RUN_RECORD.md` to state precisely that the package-local commands are
sealed replays, while the premise-registry and repository pytest commands are repository-only
provenance gates and are not promised as sealed-intake replays.

R4. Preserve the external final response and a concise transmission record in the G309 package.
Update the package builder and evidence ledger to include the registered repair artifacts.

## Forbidden changes

No formula, witness, candidate-B landing, premise grade, conditional-law status, metric, reciprocal
kernel, history selection, physical scale, or `X_max` claim may change. The repair may not add a
source, action, matter model, field equation, observational result, or protected-package input.

## Acceptance gates

- all four package-local commands run under `python3 -S` in a fresh writable copy;
- the live production result equals the saved production result exactly;
- the independent verifier still reports 28 checks;
- all four hostile mutations remain caught;
- the package verifier passes without SymPy or third-party imports;
- repository premise verification and pytest remain unchanged and pass locally;
- a fresh repair-only sealed intake is built only after all gates pass.
