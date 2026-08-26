# G265 external-review repair preregistration

Date: 2026-08-26
External disposition: `ACCEPT_WITH_REPAIRS`
Status: evidence and wording repair only; bounded scientific result frozen

## Trigger

The fresh sealed GPT-5.4 reviewer verified all 28 payload hashes and reproduced the bounded result
with `18/18` symbolic checks, `63/63` independent numerical assertions, and `8/8` mutation catches.
It found no fatal mathematical defect. It identified one material replay-alignment defect and one
premise-status wording defect.

## Frozen scientific content

The following may not change during this repair:

- the static-radial metric, profile arena, and separating controls;
- the optical, slice-proper, endpoint-clock, local-speed, and coordinate-speed formulas;
- the constant-lapse/flatness result for the stronger all-subinterval distance equality;
- the signed-arrow reversal and exact even/odd reciprocal decomposition;
- the `p=-2/9` local candidate and its fourth-order failure coefficient `7/13122`;
- the conclusion that infinite bare `c` is nonselective as a static value law;
- the conclusion that `sech(delta)` and mutual-distance ownership remain proposed, not adopted;
- every numerical count and the bounded static-radial conclusion ceiling.

Any change to those objects invalidates this repair path and requires a new preregistration.

## R1 — exact replay/result alignment

Make `derive_closure.py` emit the same landing and result fields as `DERIVATION_RESULT.json`. The
repair may reconcile metadata only; it may not alter formulas, checks, counts, or scientific scope.

## R2 — fail-closed package verification

Strengthen `verify_package.py` to require exact equality between the live `derive_closure.py` result
and the recorded `DERIVATION_RESULT.json`, rather than accepting a common landing prefix. Retain the
existing source-resolution, independent-replay, mutation-catch, and premise-status gates.

Add a bounded verifier mutation test proving that a changed recorded landing or result field is
rejected. The test may operate only on in-memory data or an ephemeral copy and must not mutate the
evidence package.

## R3 — premise-status wording

Tighten the public summary and ownership wording so that:

- infinite bare `c` is a proposed provenance interpretation, not an adopted law;
- the signed/even channel distinction is derived algebraically;
- `sech(delta)` is only a candidate physical projection;
- mutual-distance ownership is proposed and remains open;
- no startup semantic regrade, canonization, selected profile, infinite physical signalling, or
  time-live no-go is implied.

## R4 — preserve the external record and repair ledger

Bank the exact fresh external report and add a concise repair implementation record. Update the
package evidence/status files only enough to state `ACCEPT_WITH_REPAIRS__REPAIR_FOLLOWUP_PENDING`.
Do not promote G265 into startup authority until a fresh repair-only follow-up accepts R1--R3.

## Certification contract

The repaired package passes only if:

1. the scientific formulas, result counts, and bounded landing remain unchanged;
2. the live exact result equals the recorded result as a complete JSON object;
3. the verifier rejects a deliberately altered result object;
4. all registered no-write checks pass from the repaired package;
5. proposed premise statuses remain explicit in the derivation, lay report, ledgers, and verifier;
6. unrelated and protected local work remains untouched; and
7. the grade remains `ACCEPT_WITH_REPAIRS__REPAIR_FOLLOWUP_PENDING` until external follow-up.

