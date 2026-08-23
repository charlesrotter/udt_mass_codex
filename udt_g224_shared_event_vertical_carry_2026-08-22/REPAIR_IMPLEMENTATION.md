# G224 repair implementation

Date: 2026-08-22

## R1 — distinct-event wording

Implemented exactly as preregistered. `OBSERVATION.md` now says:

- local observer clocks define an abstract line normalization even at distinct events; and
- physical vertex composition still requires shared incidence.

The stale statement that abstract comparison requires transport was removed. No equation, result
payload, source, or landing changed.

## R2 — review-grade alignment

Updated the audit, evidence gates, status ledger, result payload, verifier, and catch proofs to
record:

```text
ACCEPT_WITH_REPAIRS
```

with scientific grade `A-` and repair-only follow-up still pending.

The verifier now rejects:

- reintroduction of the stale distinct-event sentence;
- deletion of the physical-composition boundary;
- a false clean-acceptance grade;
- a false external-follow-up acceptance; and
- any change to the accepted scientific landing.
