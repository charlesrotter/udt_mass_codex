# G275 final R4 repair-only follow-up review

Date: 2026-08-26

Reviewer: external Codex `gpt-5.4`, fresh ephemeral context

Authorized sealed intake:
`/tmp/udt_g275_review_7bhim5jc`

- `REVIEW_SCOPE.json` SHA-256:
  `97be9f8576231dd4fb46427f1b268232b69dfda091a58d104e607d020303e357`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `4e6e724c01662c76a3509d8f251b457c6357eb2c07f1a99b2c704b256e70dc93`
- saved raw reviewer output SHA-256:
  `da9a7fdd40a04638a9df92d949baa960af43e418611cee5596a35e3b02ec40b1`

## Verdict

`R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`

The reviewer independently verified the exact intake hashes, 41 physical files, and 40-row
nonrecursive manifest. It ran both registered no-write replays successfully. It then built a
bounded pseudo-repository wholly from sealed-intake files to exercise the repository-mode branch:
the registered repair command returned zero and the fake-Git marker remained absent.

Every preregistered R4 gate passed:

1. sealed builder resolution is package-local first and fail-closed;
2. sealed builder and verifier cannot reach live paths or Git fallback;
3. the repair verifier recognizes and reuses an existing sealed root;
4. repository-only fallback remains available outside sealed mode;
5. repository mode launches the registered command from a fresh sealed root;
6. the fake-Git tripwire remains untouched;
7. clean replay and all three tamper rejections pass;
8. the bounded G275 scientific landing, scope, and open boundaries are unchanged.

No blocking defect was found within R4 scope. The reviewer did not access the real repository,
protected packages, observational outcomes, or continue the research. A byte comparison after the
review found no change to any evidence file; only ephemeral Codex runtime metadata appeared in the
writable review copy.

## Reviewer response with ephemeral line links omitted

`R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`

`REVIEW_SCOPE.json` matched
`97be9f8576231dd4fb46427f1b268232b69dfda091a58d104e607d020303e357`,
`REVIEW_MANIFEST.tsv` matched
`4e6e724c01662c76a3509d8f251b457c6357eb2c07f1a99b2c704b256e70dc93`, the intake contained
exactly 41 physical files, and the manifest had exactly 40 data rows excluding itself and did not
self-list.

1. Gate 1 passed. Sealed builder resolution is package-local first and fail-closed, and sealed
   verifier source resolution is likewise package-local only.

2. Gate 2 passed. In sealed mode, both builder and verifier stop before any live-path or Git
   fallback. I reran `python3 .../verify_review_repairs.py --no-write`; it exited `0`, and the
   recorded result still states `sealed_git_fallback_invoked: false` and
   `sealed_builder_git_fallback_invoked: false`.

3. Gate 3 passed. The repair verifier detects an existing sealed root and reuses it as the immutable
   source instead of rebuilding from a repository root.

4. Gate 4 passed. Repository-mode fallback was retained, not removed: after the sealed fail-closed
   branch, the builder still falls back to the repository-relative source and then `git show` only
   when not sealed. I did not exercise real repository history because the review scope forbids
   outside-repository access.

5. Gate 5 passed. The registered repo-mode path that launches
   `verify_review_repairs.py --no-write` from the fresh sealed intake is implemented. To avoid
   touching the real repository, I additionally ran that exact registered command in a bounded
   `/tmp` pseudo-repository assembled only from intake files; it returned `0`.

6. Gate 6 passed. The fake-Git tripwire is created and checked around the sealed-source,
   sealed-builder, and sealed-entrypoint replays. In both the sealed-intake rerun and the bounded
   repo-mode simulation, the marker stayed absent.

7. Scientific landing unchanged. `verify_package.py --no-write` exited `0`. The exact landing
   string, 26 production checks, and unchanged open scope remain. The independent replay still
   shows `observations_used: false`, `history_selected: false`, and `X_max_selected: false`; the
   eight hostile catches still pass.

No blocking defect was found within R4 scope.
