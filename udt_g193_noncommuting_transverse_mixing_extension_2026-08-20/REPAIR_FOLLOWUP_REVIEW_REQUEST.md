# G193 repair-only external follow-up request

## Scope

Verify only the preregistered R1/R2 repairs in `REVIEW_REPAIR_PREREGISTRATION.md` and confirm that
the already accepted bounded scientific landing is unchanged.  Do not extend the research.

## R1 replay gate

Run exactly the command in `REVIEW_SCOPE.json`.  Confirm:

1. all evidence files are physically read-only;
2. `.review_runtime` is the only writable intake directory;
3. the verifier rejects missing, redirected, or pre-populated runtime paths;
4. the exact no-write replay completes;
5. `.review_runtime` is empty afterward; and
6. no package evidence file changes.

## R2 wording gate

Confirm that the packet now describes the numerical work as:

```text
independent metric-jet/Riemann spot checks plus a separately implemented
formula-driven matrix-IVP replay
```

and expressly does **not** call it end-to-end metric-derived Jacobi propagation over the interval.
The numerical artifacts, counts, ceilings, hostile catches, theorem, family, and maximum conclusion
must remain unchanged.

## Required return

Return exactly one:

- `G193_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED`
- `G193_REPAIRS_INCOMPLETE`
- `G193_BOUNDED_LANDING_REOPENED`

State the replay result and any remaining defect.  Do not continue to another family.
