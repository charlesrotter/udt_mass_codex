# G271 external repair-only follow-up

Reviewer: external Codex `gpt-5.4`

Date: 2026-08-26

Sealed intake: `/tmp/udt_g271_repair_followup_64hcy5t2`

`REVIEW_SCOPE.json` SHA-256:
`a69a8f6c1037390a1528e4bf24d24be6d370721756f1c7d61bcc1ffccb010ca7`

`REVIEW_MANIFEST.tsv` SHA-256:
`842b75d0568212cf56a8084a23036e497712016f6c9f2e2705556da1a5210940`

Raw response SHA-256:
`fc2ff0a6df5c02712b91cab95e0c5956dcbbc62f5f3ab4a860c3fda9096a035a`

## Landing

`ACCEPT_REPAIRS_AND_CLOSE`

## R1 — source-path containment

Accepted. The reviewer confirmed all five `SOURCE_MANIFEST.tsv` targets resolve under
`SCOPE_ROOT`, that `path.is_relative_to(SCOPE_ROOT)` is enforced before access, and that the replayed
result records both `source_rows=5` and `source_paths_within_scope_root=5`.

## R2 — spherical-isometry coverage

Accepted. The reviewer confirmed that the explicit `SO(3)` reduction preserves the metric,
`phi(r)`, static clock, radial acceleration, Levi-Civita transport, jets, norm split, and
radial/quiet strata. The equatorial calculation therefore represents every regular finite-radius
null germ modulo exact metric isometry.

## Replay

The reviewer ran the registered command exactly. It exited zero with:

- package status `PASS`;
- three nested no-write replays;
- 30 production checks;
- 20,000 independent exact-fraction cases;
- six implementation mutations caught;
- six textual scope-regression catches passed.

## Scientific grade

The scientific conclusion did not change. G271 remains a bounded theorem on a supplied arbitrary
smooth primary static reciprocal family. It does not select a profile, finite path, physical
history, distance, branch population, or `X_max`.

Final package grade:
`EXTERNALLY_REVIEWED_BOUNDED_LEAD__REPAIRS_ACCEPTED`.
