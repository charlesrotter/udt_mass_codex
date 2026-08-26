# G265 repair-only external follow-up request

Date: 2026-08-26
Original disposition: `ACCEPT_WITH_REPAIRS`

Inspect only the sealed follow-up intake and verify only the repairs preregistered at commit
`51601515`.

## R1 — replay/result alignment

Confirm that `derive_closure.py` emits a JSON object exactly equal to `DERIVATION_RESULT.json`,
including every field and the complete bounded landing. Confirm that no formula, symbolic check,
profile, numerical result, or scientific ceiling changed.

## R2 — fail-closed verifier

Confirm that `verify_package.py` compares the complete replayed and recorded results and rejects the
registered in-memory altered-landing control. Run only registered no-write replays or bounded checks
in a writable ephemeral copy.

## R3 — premise-status wording

Confirm that the repaired derivation, audit, lay report, evidence gates, and status ledger preserve
the following distinctions:

- infinite bare `c`: proposed provenance interpretation, not adopted value law;
- signed/even channel distinction: bounded derived algebra;
- `sech(delta)`: candidate physical projection, not founded readout;
- mutual-distance ownership: proposed and open;
- no startup semantic regrade, canonization, selected profile, infinite physical signalling, or
  full time-live no-go.

## Required return

Return `REPAIRS_ACCEPTED` or `REPAIRS_REJECTED`. State whether R1--R3 close the original review
defects while leaving the bounded G265 scientific landing unchanged. Do not continue the research,
adopt either proposed premise, or widen the conclusion.
