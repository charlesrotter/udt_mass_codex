# G336 preregistration scope repair R1

Date: 2026-09-03
Timing: after the first production probe, before sealed external transmission
Type: `SCIENTIFIC_SCOPE_REPAIR__STRICT_STRATUM_VERSUS_CLOSURE_BOUNDARY`

## Error caught

The frozen preregistration asked for the vertical endpoint `mu=1` while also declaring the strict
two-branch G332 family. On the first-order-silent set,

```text
C=b(1-2mu),
(b+C)^2=4b^2(1-mu)^2.
```

For strict silent data `b!=0`. Therefore the G332 radicand is positive exactly when `mu<1`, and it
vanishes at `mu=1`. The vertical endpoint is the branch-meeting closure boundary, not a member of
the strict two-branch family.

## Frozen repair

1. The production census shall distinguish:
   - strict horizontal endpoint `mu=0`;
   - strict interior `0<mu<1`; and
   - vertical closure boundary `mu=1`, retained only as an algebraic continuity diagnostic.
2. `ENDPOINT_SILENT_SECOND_RESPONSE_CARRY_INDEPENDENT_AT_THIS_ORDER` is narrowed to
   `STRICT_HORIZONTAL_ENDPOINT_SECOND_RESPONSE_CARRY_INDEPENDENT_AT_THIS_ORDER`.
3. The vertical identity `s1=Lambda-2` may be reported only as a branch-meeting boundary identity.
4. Both G332 roots remain required on every strict control. They coincide at the vertical boundary,
   which must not be counted as two distinct branches.
5. Strict production counts, boundary counts, and landing language must be separated.

## What is unchanged

The ADM formula, all-weight Ricci formula, interior carry dependence, exact positive/zero/negative
triplet at `mu=1/2`, double-silent stratum, boost response, and all omitted physics remain exactly
as preregistered. No outcome was filtered or new physical premise introduced.

This repair supersedes only the affected endpoint scope in `PREREGISTRATION.md`. Git retains the
original timestamped contract at commit `eba7a42a`.
