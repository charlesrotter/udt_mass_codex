# G306 repair-only external follow-up request

Review only the sealed intake. Verify only repairs R1--R4 preregistered in
`REPAIR_PREREGISTRATION.md` and whether the bounded G306 scientific landing is unchanged. Do not
edit evidence files or continue the research.

## Required checks

1. Confirm that `COMMANDS.md` explicitly separates the four self-contained sealed commands from
   the two repository-only regression gates, and that every sealed command runs under `python3 -S`
   from a writable ephemeral copy.
2. Inspect `verify_package.py`. Confirm that each source resolves uniquely in repository-root or
   sealed `frozen_sources/` layout, that all 15 hashes pass, and that missing and ambiguous layouts
   are rejected by `verify_repair_portability.py`.
3. Inspect and run the repaired `derive_intrinsic_hopf_section.py`. Confirm that it has no SymPy or
   other external dependency, performs exact integer/rational/polynomial checks, retains 172
   production assertions, and produces byte-identical `DERIVATION_RESULT.json` and
   `CANDIDATE_CENSUS.tsv`.
4. Run the independent verifier, hostile controls, package verifier, and portability verifier.
   Confirm 22,237 independent checks, 17 hostile direct mutations, 15 source hashes, and four
   passing sealed commands.
5. Confirm that no metric, kernel, scientific question, family census, ownership grade, or bounded
   landing changed and that no physical member, population, target, action, history, magnitude,
   mass, scale, or physical `X_max` was added.

The repository-wide premise verifier and pytest suite are recorded pre-seal repository gates. They
are not part of the bounded intake and must not be reported as failed sealed commands.

## Allowed landings

- `G306_REPAIRS_ACCEPTED`
- `G306_REPAIRABLE_DEFECTS_REMAIN`
- `G306_SCIENTIFIC_LANDING_CHANGED`

Return exact defects with file and line references. Do not select or propose a field equation,
action, source, matter model, physical field population, scale, fit, mass law, history, or physical
`X_max`.
