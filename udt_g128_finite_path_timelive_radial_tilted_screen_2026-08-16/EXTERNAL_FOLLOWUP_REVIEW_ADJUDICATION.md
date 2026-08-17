# G128 corrected follow-up review adjudication

Date: 2026-08-16

Sealed intake: `/tmp/udt_g128_review_cz3sd51x`

`REVIEW_SCOPE.json` SHA-256:
`03e4faa83e16f9ba659fd86828172ae000949ace55da408c65d82659920bff7e`

Reviewed commit: `b61402ab7d096fbdf37cff684d70b26381d97b1a`

External verdict: `FOLLOWUP_FAIL`.

## Adjudication

The failure is confined to certification coverage. The reviewer verified that both registered
repairs are implemented in the solvers, that the preregistered `h=2e-4` replay passes, and that the
original bounded landing remains supported. It found no changed history, equation, interval,
tolerance, candidate landing, or maximum conclusion.

The package verifier exercised the radius and pole events and nonfinite-state rejection, but did not
separately force either `N` or `L` to the nonpositive branch. The verifier now supplies finite test
jets that make exactly one exponential scale underflow to zero while the other remains one, and
requires rejection independently in both production and independent implementations.

The stale rounded maximum in the first adjudication is also corrected from `1.263e-11` to the banked
`1.330e-11`; both values were far inside the preregistered `2e-7` independent agreement gate, so this
does not alter the result.

## Current status

The scientific landing remains:

`FINITE_PATH_SAME_HISTORY_EMERGENCE_OBSERVED`.

The external certification status remains failed until a new sealed reviewer confirms the added
positive-scale coverage. No stronger scientific conclusion is authorized.
