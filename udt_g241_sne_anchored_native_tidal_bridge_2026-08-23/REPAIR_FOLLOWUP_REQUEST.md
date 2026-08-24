# G241 R4 repair-only follow-up request

The fresh external review returned:

```text
G241_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED
```

It independently reproduced the full-covariance degree-two through degree-four carrier census,
the derivative classifications, the exact radial-to-tidal identity, the absolute-scale
cancellation, and the outcome/provenance boundary. It found only two operational defects:

1. manifested source files were sealed under `sources/`, while replay scripts correctly resolve
   them at their repository-relative sibling paths;
2. `COMMANDS.md` presented two full-repository integration checks beside sealed commands even
   though the full verifier and test suite were not part of the intake.

R4 was preregistered in `CORRECTION_PREREGISTRATION.md` before implementation. Review only whether:

- the sealed source layout now preserves original repository-relative paths;
- `sources/` is absent and the frozen G237 state is present at its expected sibling path;
- `SEALED_REPLAY_RESULT.json` and an independent ephemeral replay show that all four registered
  no-write commands pass without relocation;
- `COMMANDS.md` clearly separates sealed replay from repository-only integration checks;
- no formula, source hash, covariance entry, candidate, threshold, fit, derivative classification,
  tidal value, premise status, outcome boundary, or scientific landing changed.

Do not continue the research, inspect BOSS outcomes, recommend a new carrier, or edit evidence.
Return exactly one of:

```text
G241_BOUNDED_NEGATIVE_ACCEPTED__RADIAL_TO_TIDAL_IDENTITY_RETAINED
G241_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED
G241_SCIENTIFIC_LANDING_REJECTED
```
