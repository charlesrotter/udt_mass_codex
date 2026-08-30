# G305 repair-only external follow-up request

Review only the sealed intake. Verify only preregistered repairs R1--R4 in
`REPAIR_PREREGISTRATION.md` and whether the bounded scientific landing is unchanged. Do not edit
evidence files or continue the research.

## Required checks

1. Run `verify_package.py` from a writable ephemeral copy and confirm all eleven source hashes
   resolve in the sealed layout with no missing or ambiguous path.
2. Inspect and run `verify_global_hopf_bridge_independent.py`. Confirm it imports no production code
   and now independently covers ambient constraints, positive chart overlap, negative global
   pullback/relation, computed topology witnesses, Hopf normalization, scale/time independence, and
   null optical controls.
3. Inspect and run `run_global_hopf_catches.py`. Confirm its ten catches mutate computed evidence,
   return named failures, validate the clean baseline, and detect a corrupted baseline.
4. Confirm the production result remains 77 assertions with Hopf integer `-1`, and that no metric,
   kernel, premise, topology class, or scientific landing changed.

## Allowed landings

- `REPAIRS_ACCEPTED`
- `REPAIRABLE_DEFECTS_REMAIN`
- `SCIENTIFIC_LANDING_CHANGED`

Return exact defects with file and line references. Do not select or propose a field equation,
action, source, matter model, physical history, scale, mass law, fit, or physical `X_max`.
