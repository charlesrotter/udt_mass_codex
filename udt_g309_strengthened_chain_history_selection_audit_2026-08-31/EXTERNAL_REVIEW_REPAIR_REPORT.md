# G309 external-review repair report

Date: 2026-08-31
Preregistered at: `4280cb5d`
Status: `EXTERNAL_REPAIR_FOLLOWUP_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`

## Repair results

R1 passed. `derive_strengthened_history_audit.py` now uses only the Python standard library. Exact
integer-coefficient polynomial checks cover the trace-free numerator, scalar-curvature numerator,
hyperbolic reduction, flat-bump derivative polynomials through order four, normalized Hopf carry,
and conditional constant relation. `Decimal` at 90-digit working precision independently evaluates
the preregistered witness. The resulting JSON equals the previously reviewed JSON exactly: 13
checks, the same formulas, and the same 50-significant-digit values.

R2 passed. `verify_package.py` imports and executes the live production builder, then requires exact
dictionary equality with `DERIVATION_RESULT.json`. A stale or unreplayable saved production result
can no longer pass merely by existing.

R3 passed. `COMMANDS.md` registers all four package-local replays under `python3 -S`. It and
`RUN_RECORD.md` distinguish those sealed replays from the premise-registry and pytest provenance
gates, which require the repository and are not promised inside the bounded intake.

R4 passed. The first external response and transmission record are preserved. This report, the
repair preregistration, and the repair-only request are registered with the intake builder.

## Gates

- production replay: PASS, 13 checks, byte-equivalent structured result;
- independent replay: PASS, 28 checks;
- hostile mutations: PASS, four of four caught;
- live package verification: PASS;
- startup-surface boundedness: PASS after compactly restoring literal route guards exposed by the
  full suite; no scientific content changed;
- full repository suite: `199 passed, 1 xfailed in 136.86s`;
- full premise/startup verifier: PASS, 289-row registry and 754 historical dispositions.

No metric, kernel, formula, witness, premise grade, candidate-B landing, conditional-law status,
history, physical scale, or `X_max` claim changed.

## External closure

The repair-only reviewer ran the four registered `python3 -S` commands in a fresh ephemeral copy
and returned `G309_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`. See
`EXTERNAL_REVIEW_REPAIR_FOLLOWUP_RESPONSE.md` and
`EXTERNAL_REVIEW_REPAIR_FOLLOWUP_TRANSMISSION.md`.
