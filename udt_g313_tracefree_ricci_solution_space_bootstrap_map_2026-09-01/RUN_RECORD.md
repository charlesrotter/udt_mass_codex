# G313 run record

Date: 2026-09-01
Preregistration commit: `e0b6e478`

## Registered commands

```text
python3 -S derive_solution_space.py --output DERIVATION_RESULT.json
python3 -S verify_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -S verify_package.py
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

## Outcomes

- production exact assertions: `72`, all pass;
- independent exact assertions: `58`, all pass;
- hostile semantic mutations: `8/8` caught;
- dependency-free aggregate replay: `PASS`;
- exact 295-row premise/startup verifier: `PASS` through G312;
- full repository suite: `213 passed, 1 known matter-sector xfailed in 139.34s`;
- `git diff --check`: `PASS`.

No GPU, network, observation, fit, source, action, matter, mass, calibrated scale, physical
`X_max`, or protected input was used.

## Preregistered external-review repairs

The fresh reviewer retained the landing and returned four evidence defects. Their exact repair-only
scope was committed and pushed at `6fcbeb36` before implementation.

Repair outcomes:

- R1: 25 exact evaluations of `Q[a]=a*a''-(a')^2-1` across five scales and five points, with the
  constant mutation rejected;
- R2: 12 independent explicit-coordinate product-metric Ricci reconstructions plus a separate
  compact-Cauchy proof;
- R3: production and independent exhaustive eight-selector/four-response-map type censuses;
- R4: direct G307 and G308 audit reports added to source scope and the corrected intake;
- repaired production: 181 assertions, all pass;
- repaired independent route: 357 assertions, all pass;
- repaired hostile controls: 12/12 caught;
- aggregate dependency-free repair replay: `PASS`.
- exact 295-row premise/startup verifier after repair: `PASS`;
- full repository regression after repair: `213 passed, 1 known matter-sector xfailed in 139.46s`.

External repair-only follow-up reran the four registered commands in a writable ephemeral copy and
returned `G313_REPAIRS_R1_R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`. No repair-scope defect remains.
