# G171 sealed-review packaging repair preregistration

Date: 2026-08-19
Trigger: first fresh external review

## Retained scientific landing

The external reviewer independently retained the pair-germ-relative network, same-pair reversal,
three-pair defect identity, exact angular witness, matched-readout subfamily, pair-rechart formula,
and absence of load-bearing G142--G160 scaffolding.

No scientific formula or boundary will be changed by this repair.

## Registered packaging defect

The reviewer treated `verify_package.py` and `VERIFICATION_RESULT.json` as a sealed-intake replay.
That verifier is the repository outer gate: it intentionally checks the preregistration commit and
the repository-wide premise verifier. The intake instead contains `verify_sealed_intake.py`, which
independently validates the sealed tree, copies it to isolated scratch, and replays the three
load-bearing scripts without writing the seal. The first request did not make this distinction
explicit enough, and the intake omitted its own builder even though the outer verifier lists that
builder among repository-required files.

## Frozen repairs

1. Add an explicit two-gate execution boundary distinguishing repository verification from sealed
   replay.
2. Include `build_review_intake.py` in the corrected seal and make it source-path safe when copied.
3. Make the outer result state its repository-only gate type.
4. Make the sealed verifier report its own gate type, source count, and replay counts.
5. Direct a repair-only reviewer to run `verify_sealed_intake.py` from the corrected seal.

## Certification

The corrected intake must pass its own sealed verifier, retain the exact scientific landing, and
receive a fresh repair-only external review. A reviewer finding a mathematical change or a failed
sealed replay blocks closure.
