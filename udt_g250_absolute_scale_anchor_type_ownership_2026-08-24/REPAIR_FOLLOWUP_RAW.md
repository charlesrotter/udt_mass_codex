# G250 repair-only external follow-up — exact final response

Date: 2026-08-24

Reviewer: external Codex `gpt-5.4`, high reasoning, web disabled, sealed read-only intake.

## Findings

No remaining repair defect was found within the sealed review scope. R1--R3 are repaired, and the
bounded G250 landing is unchanged.

R1 is satisfied by unique root-or-`sources/` resolution plus SHA-256 enforcement in the package,
production, independent, and hostile checks. The bounded manifest check found all nine exact
sources present only under `sources/`, each with exactly one valid candidate and matching SHA-256.

R2 is satisfied: the sealed replay list is exactly four commands, while
`verify_current_scientific_premises.py` is separately and truthfully labeled repository-only.

R3 is source-backed in production, independent, hostile, and package checks. G236, G237, G99, G132,
and G202 facts are read from exact manifest sources rather than truth constants.

## Replay results

- production, 4,096 cases: `PASS`; 18 candidate classes; zero fitted coefficients and zero
  observational values;
- independent, 12,000 cases: `PASS`; 24,010 assertions; five provenance sources;
- hostile: `PASS`; 23/23 caught, including missing, ambiguous, and hash-mutated sealed sources;
- package verifier: `PASS`; no failures; saved and live replays match exactly;
- bounded intake check: 38/38 payload hashes and 9/9 manifest relocations pass.

## Maximum unchanged scientific conclusion

At most: one matched nonzero-homothety-weight direct anchor conditionally fixes the single G249
scale; additional independent anchors test consistency of the supplied dimensionless history
rather than adding scale parameters; `c_E`, `G_obs`, reciprocal redshift, and the relative SNe state
do not fix absolute scale; mass/density/energy composites remain dimensional candidates pending a
metric-attachment law; historical G99 `X_eff` remains a conditional external cross-check, not a
native G249 input; no anchor value, fitted coefficient, observational outcome, history, or profile
is selected.
