# G305 final R3-completion external follow-up request

Review only the sealed intake. Verify only the exact direct-field-mutation repair preregistered in
`R3_COMPLETION_PREREGISTRATION.md`, the retained R1/R2 acceptances, and whether the bounded
scientific landing is unchanged. Do not edit evidence files or continue the research.

## Required checks

1. Inspect and run `run_global_hopf_catches.py` in a writable ephemeral copy. Confirm there is no
   `promotions` set or label-only catch.
2. Confirm each of the ten hostile cases directly changes the exact computed-evidence or
   required-premise fields frozen in the R3 completion preregistration.
3. Confirm every case records its mutation path and distinct before/after values, then triggers its
   preregistered named failure. Confirm the clean baseline passes and the corrupted baseline fails.
4. Run `verify_package.py` and the independent standard-library replay. Confirm retained R1 and R2,
   11 source hashes, 687 independent checks, 11 hostile evidence mutations, 77 production
   assertions, Hopf integer `-1`, and unchanged metric, kernel, topology census, and landing.

## Allowed landings

- `R3_COMPLETION_ACCEPTED`
- `R3_REPAIRABLE_DEFECTS_REMAIN`
- `SCIENTIFIC_LANDING_CHANGED`

Return exact defects with file and line references. Do not select or propose a field equation,
action, source, matter model, physical history, scale, mass law, fit, or physical `X_max`.
