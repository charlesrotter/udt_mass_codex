# G167 external adversarial review

Date: 2026-08-18

Model: external Codex `gpt-5.4`, high reasoning, fresh ephemeral context, web disabled,
read-only sealed intake.

Authorized sealed intake:

- path: `/tmp/udt_g167_pair_pullback_review_bwe2smyj`
- `REVIEW_SCOPE.json` SHA-256:
  `f95125e8828fdc3db51033ca13a07591c349db54d38ad24638d25b47968007c2`
- tree digest SHA-256:
  `8db8b346df164ab81e2a8decec1fcb6ba243492629425201f9738739d5d5f29a`

## Reviewer landing

```text
VERIFIED_WITH_CAVEATS__BOUNDED_PRIMARY_PAIR_PULLBACK__SOURCE_HASH_REPLAY_BROKEN
```

## Scientific findings

The reviewer independently reproduced the algebraic core:

1. `h=J^T g J` gives the stated arbitrary local rank-two pair metric.
2. The exact bounded identification
   `h=Y^T B^T eta_2 B Y + Z^T Q^T Q Z` holds for
   `B=diag(c_E exp(-phi),exp(phi))`, `Q=diag(r,r sin(theta))`, and `S=0`.
3. The nonradial rational witness reproduces
   `h=[[-391/100,9/50],[9/50,2]]`, `det(h)=-19631/2500`,
   `beta_pair=-18/391`, and `q_pair^2=152881/78524`.
4. Angular-coordinate covariance of the Gram term checks exactly.
5. The radial control returns `q_pair^2=exp(-4 phi)`.
6. The full query-live derivative checks as a directional derivative through the supplied static
   metric, not as ambient time evolution.
7. No fixed path, geodesic, action, source, `X_max`, observational result, GR field equation, or
   protected work was imported into the bounded terminal pair-metric claim.
8. Connection, Jacobi, normal-transport, and holonomy channels remain outside the terminal claim.

The reviewer judged the phrase “full general pair pullback” honest only with the package's bounded
scope: every local regular rank-two pair realization inside the declared static-spherical primary
metric and regular calibrated Lorentzian readout stratum. It is not a general nonspherical,
time-dependent, global, or complete-universe theorem.

The reviewer also accepted `h01` only as a calibrated, pair-chart-dependent shift state, not an
ambient shift field or invariant scalar. It accepted the `mu` conclusion only in the stated weak
form: no extra scalar `mu` is needed or presently owned in this bounded representation; no future
derived reduction rule is excluded.

## Mandatory repairs

1. The intake copied frozen sources under `sources/`, while the three package verifiers resolved
   manifest paths directly from the intake root. Consequently, source-hash and package replay were
   not runnable from the sealed intake as delivered. Correct the intake layout or resolution logic
   and regenerate all affected result artifacts.
2. Reconcile `EVIDENCE_GATES.md`: it simultaneously recorded completed gates and the stale grade
   `PREREGISTERED__NOT_YET_RUN`. Repository regression and premise-verifier evidence must either be
   sealed as replayable artifacts or clearly marked as repository-side external notes.

## Optional but adopted clarifications

- Restore missing visible plus signs in the displayed pullback formulas. The scripts contained the
  correct sums, so this was a typesetting defect rather than an algebra defect.
- Prefer wording that keeps “bounded primary-metric” attached to the general-pair claim wherever a
  title could otherwise be overread.

## Review disposition

The scientific result survived independent adversarial reconstruction. Banking remains paused
until the mandatory evidence repairs are registered, implemented, regenerated, and independently
rechecked in a fresh corrected sealed intake.
