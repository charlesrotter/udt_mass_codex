# G337 external-review repair preregistration R1

Date: 2026-09-03
Timing: after fresh sealed external review, before changing the reviewed evidence
Type: `SEALED_REPLAY_SOURCE_LAYOUT_REPAIR_ONLY`

## External finding

The external reviewer retained the bounded G337 mathematics and returned
`ACCEPT_WITH_REPAIRS__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED`. It found one packaging defect:
the intake builder places frozen dependencies under `sources/<registered-path>`, whereas
`verify_package.py` resolves each registered path from the copied intake root. A direct aggregate
replay therefore falls back to unavailable Git history and fails, although the unchanged verifier
passes after a reviewer manually reconstructs the expected root layout.

## Frozen repair

1. Make `verify_package.py` resolve a frozen source from either the repository-root location or the
   sealed `sources/<registered-path>` location, with the same path-containment, byte-count, and
   SHA-256 requirements.
2. Keep the Git fallback only for repository replay at the preregistration commit; sealed replay
   must succeed without Git history.
3. Add a registered direct sealed-copy aggregate replay that proves the builder's produced layout
   works without manual restaging.
4. Preserve every mathematical formula, numerical result, premise stamp, and bounded scientific
   landing unchanged.
5. Preserve the external response verbatim and register the review transmission details.
6. Re-run production, independent, hostile, aggregate, intake, premise, and repository tests.

## Acceptance contract

The repair passes only if:

- a newly built sealed intake authenticates exactly;
- `verify_package.py` passes directly from the copied sealed package with sources still under
  `sources/`, without a repository or manual root-layout reconstruction;
- the production, independent, and hostile JSON outputs remain byte-identical;
- all registered G337 and repository gates pass; and
- the package remains `ACCEPT_WITH_REPAIRS` pending an authorized repair-only external follow-up.

This preregistration authorizes no new derivation and no change to the scientific question.
