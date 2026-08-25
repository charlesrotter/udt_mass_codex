# G260 external-review repair preregistration

Date: 2026-08-25

The fresh external `gpt-5.4` reviewer returned `ACCEPT_WITH_REPAIRS`. It accepted the bounded
scientific landing and identified one replay-portability defect with two equivalent remedies. This
document freezes the chosen repair before implementation.

## Frozen repair R1 — dependency-free production replay

Replace the registered SymPy-dependent production replay with a Python-standard-library-only
production replay that recomputes the same load-bearing G260 identities from source. The repair
must cover at least:

- the full four-dimensional spherical Einstein residuals;
- the isolated two-dimensional Einstein-tensor vacuity control;
- the flat-screen corruption and its exact unit residual on `f=1+C/r`;
- `A_parallel+A_perp=E1-E0`;
- nonzero cancelling angular amplitudes on the nonflat vacuum family;
- the complete trace-balanced family `f=1+a*r^2+b/r` and `E0=E1=3*a*r^2`;
- the mass-aspect rewrite;
- the nonradial angular-Gram witness.

The replay may use exact rational arithmetic and symbolic coefficient algebra from the Python
standard library. It must not import SymPy, production results, or the independent verifier. It
must write only the already registered `DERIVATION_RESULT.json` when explicitly run.

The richer SymPy implementation may be retained as an optional development cross-check, but it
must no longer be required by the registered sealed replay or package verifier.

## Wording and package alignment

After the dependency-free replay passes, retain the accurate wording `production full-metric
derivation: PASS` and identify it explicitly as dependency-free. Register the runtime requirement,
command, evidence hash, and replay result in the run record, package verifier, source manifest,
review request, and repaired sealed intake.

## Certification contract

1. The dependency-free production replay must run in a stock Python environment without SymPy.
2. It must reproduce the existing `DERIVATION_RESULT.json` exactly, not merely a subset of it.
3. The independent verifier must remain independent: it may not import production code or read the
   production result.
4. All 10,044 independent assertions and all eight hostile catches must remain unchanged and pass.
5. Full package verification, the current-premise verifier, and the repository test suite must pass.
6. The bounded scientific landing and all premise grades must remain unchanged.
7. A new sealed intake must pass its scope/manifest checks and registered dependency-free replays
   before repair-only follow-up review is requested.

## Forbidden during repair

- changing any G260 equation, coefficient, sign, family, or scientific conclusion;
- promoting the imported quiet Einstein comparator into a UDT law;
- adding a source, history law, loud-regime extension, observation, fit, or `X_max` claim;
- modifying protected or unrelated work.

Maximum repair conclusion:

```text
G260_R1_DEPENDENCY_FREE_PRODUCTION_REPLAY_REPAIRED
__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED
__EXTERNAL_REPAIR_ONLY_FOLLOWUP_REMAINS_OPEN
```
