# G304 repair preregistration

Date: 2026-08-30
Trigger: fresh external `gpt-5.4` verdict `VERIFIED_WITH_CAVEATS`

## Frozen repair scope

### R1 — sealed source-root resolution

`verify_package.py` currently resolves each `SOURCE_MANIFEST.tsv` path against the repository root.
That is correct in the live repository but fails in the sealed layout, where the same frozen files
are rooted under `/intake/frozen_sources`.

Repair: resolve every manifest row against exactly one of two declared layouts:

1. repository root `HERE.parent`;
2. sealed root `HERE.parent/frozen_sources`.

The verifier must fail if neither or both layouts resolve a row, and it must still check the exact
registered SHA-256. No source path, source hash, or scientific assertion may change.

### R2 — command-scope precision

`COMMANDS.md` lists the repository-wide `verify_current_scientific_premises.py`, but that file was
not included in the source-bounded review intake.

Repair: split commands into:

- sealed-intake replay commands that are actually present;
- repository-only banking gates, explicitly labelled unavailable inside the intake.

No new scientific checker or dependency is introduced.

## Frozen conclusion

The landing, 65 production assertions, 55 independent assertions, 10 hostile checks, eight domain
rows, 14 source hashes, exact formulas, and all scientific scope statements remain unchanged.

## Repair certification

1. local repository replay must pass;
2. a rebuilt sealed intake copied to a writable ephemeral directory must pass `verify_package.py`
   under `python3 -S` without access to the repository;
3. all 14 source hashes must resolve only under `frozen_sources` in the sealed layout;
4. the command list must name the premise verifier only as a repository-only gate;
5. a repair-only external follow-up must confirm R1 and R2 before external-verification status.
