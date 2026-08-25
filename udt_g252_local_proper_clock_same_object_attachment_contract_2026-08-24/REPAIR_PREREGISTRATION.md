# G252 repair preregistration — sealed-source relocation only

Date: 2026-08-24

## Frozen defect

The fresh external review retained the scientific theorem but found that three verifiers resolved
each `SOURCE_MANIFEST.tsv` entry only as `ROOT / relative`. The sealed intake lawfully relocates
those exact sources to `ROOT / sources / relative`, so production, independent, and package replays
failed before entering the scientific calculation.

## Authorized repair scope

R1. In `derive_local_proper_clock_attachment.py`, resolve each manifest entry against exactly the
repository-root and sealed-`sources/` candidates. Require exactly one existing candidate and the
registered SHA-256.

R2. Implement the same rule independently in
`verify_local_proper_clock_attachment_independent.py`, without importing production code.

R3. Apply the same exact uniqueness-and-hash rule in `verify_package.py`; add hostile package checks
that reject missing, ambiguous, and hash-mismatched relocated sources.

R4. Regenerate all saved replay JSON, run the premise verifier in the repository, build a fresh
sealed intake, and prove that all four registered no-write replays pass from that intake.

R5. Record the original failed-as-delivered gate state and change gates 3 and 4 back to PASS only
after the repaired sealed replay succeeds. Do not alter the bounded theorem or conclusion ceiling.

## Forbidden changes

- no scientific equation, premise status, attachment semantics, or landing change;
- no empirical value, fit, coefficient, new kernel mechanism, history selection, or observational
  outcome;
- no source-manifest membership or source-content change;
- no access to protected work;
- no unrelated cleanup or research continuation.

## Certification

The repair passes only if repository and fresh sealed-intake replays produce JSON identical to the
regenerated saved outputs; production and independent implementations still satisfy their case
floors; all 20 scientific hostile catches remain; missing/ambiguous/mutated source layouts are
rejected; and the external reviewer can reproduce the entire registered sealed chain.

## Maximum conclusion

At most: `G252_SCIENTIFIC_LANDING_UNCHANGED__SEALED_SOURCE_RELOCATION_REPAIRED__ALL_REGISTERED_REPLAYS_REPRODUCIBLE_IN_REPOSITORY_AND_FRESH_SEALED_INTAKE`.
