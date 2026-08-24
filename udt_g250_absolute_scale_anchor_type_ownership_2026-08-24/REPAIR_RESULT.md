# G250 repair result

Date: 2026-08-24

Status:

```text
R1_R2_R3_IMPLEMENTED_AND_EXTERNALLY_ACCEPTED__NO_REMAINING_REPAIR_DEFECT
```

## R1 — sealed source-path contract

`verify_package.py` now resolves every manifest source through exactly one of two explicit layouts:
the repository root or the sealed `sources/` relocation root. SHA-256 remains mandatory. Three new
hostile cases reject absent, ambiguous, and hash-mutated sources.

## R2 — command-scope contract

`COMMANDS.md` now separates the four sealed-intake replays from the repository-only current-premise
gate. The absent repository verifier is no longer represented as a sealed replay.

## R3 — source-backed provenance certification

Production and independent implementations now resolve and hash the frozen manifest sources before
parsing:

- G236 and G237 zero-point-removal ledger rows;
- G99's P1, external `M_B`, and imported-transfer rows;
- G132 and G202's exact attachment-law boundaries.

The old literal-`True` independent checks and nonempty-set G99 hostile check are gone. The hostile
suite now requires the exact source-backed facts.

## Internal replay

- production: `PASS`, 10/10 exact checks, 4,096 cases and 8,192 sampled assertions;
- independent: `PASS`, 12,000 cases, 24,010 assertions, five exact provenance sources;
- hostile: `PASS`, 23/23 catches;
- package verifier: `PASS`, 26/26 checks;
- current 232-row pre-banking premise verifier: `PASS`;
- repository suite: 153 passed, one registered XFAIL.

External repair-only follow-up independently reran the sealed package and accepted R1--R3 with no
remaining defect. The scientific landing remained unchanged.

No observational value, fitted coefficient, anchor instance, scale, branch population, or history
was introduced. The scientific landing is unchanged.
