# Same-second-verifier report — P4 cold-review forward repair

Date: 2026-08-01

Verdict: **AMENDMENT-REQUIRED**

The two repair data products satisfy the preregistered contract exactly.  Closure is withheld
only because the primary verifier's fifth claimed mutation proof is a tautology rather than a
changed-review-tree candidate passed through the production tree gate.

## Independently closed repair facts

1. Preregistration commit `9089c0fcfd3bd8cfaa0121afb42d343593d7bca6` has parent
   `c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c` and adds only `PREREGISTRATION.md`,
   `PREREG_SNAPSHOT.json`, `REPAIR_SCOPE.tsv`, and `verify_preregistration.py`.  At that
   commit the summary still has base SHA-256
   `db004cbc5c72c8cdf1f784a1b514ab95ec94db34205e4283ebcba31a96c1e31b`;
   the repair mutation is a later worktree change.
2. Relative to `c9c8b38`, every changed or untracked path is either
   `P4_ARC_SUMMARY_2026-07-31.md` or inside this repair package.  No producer, navigation,
   canon, registry, evidence, or cold-review-package path changed.
3. The corrected summary is byte-for-byte the base summary with exactly one substitution:
   `K₄ = real points of the gauge-spent screen U(1)` is replaced by
   `the screen-character image {+1,-1}, not K₄ itself, is the real two-torsion of the
   gauge-spent screen U(1)`.  The old phrase now occurs zero times and the new phrase once.
   Corrected SHA-256:
   `85f5b9e7ce6619ba0b286c71291a3eaee61779fcdb81980c0241d0e24a3b2bb8`.
4. The forward freeze exactly reproduces all 13 overlay identities and required fields,
   classified **7 LOAD_BEARING + 6 SUPPORTING**.  Every current path and its blob at review
   base `2e93a621aeeee0a0844543068363d0ba94094357` independently hash to the recorded value.
   Freeze SHA-256:
   `e74b025264d7f1d4bea3dbb383280bcaba76ea113d83114e507e498318f354ac`;
   13-path manifest SHA-256:
   `58cf2290cf5e4add8597592a17bd7d188c0b4666c694f2a2ee83bac9fccdf6bb`.
5. All 13 rows say `FORWARD_CORRECTION_FREEZE_2026-08-01` and
   `DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED`.  The repair record explicitly says it does
   not rewrite the original 311-path preregistration; no retroactive-freeze claim was found.
6. The cold-review tree remains
   `d1254e1e018d55ead4b57696629163c3d0006db5` at both base and HEAD, with no worktree change.
   Its original inventory and manifest remain, respectively,
   `a7032b94d91218e64ebfb40d0d31375cdfd75cc297aafabcf33d6617f12a199e`
   and `f150650c940e2d942a455234726ad3e3ce72b20bd175573a65ca0aeea34e8d85`;
   all 311 manifest rows validate against the review-base bytes.
7. The saved primary record contains 12/12 PASS and its 12-file primary manifest validates.
   Four catch proofs are genuine: old headline, missing dependency, changed dependency hash,
   and retroactive-promotion mutations are all fed through their actual predicates and rejected.
8. Scientific-premise gates pass: 18 premise guards, 9 startup controls, 754 candidate
   dispositions, corrected DOF semantics.  Tests pass **70**, with **1 expected xfail**.
   Status after testing contains no path outside the authorized summary and repair package.

## Exact blocker

The primary `catch_changed_review_tree` record is implemented as:

```python
record(checks, "catch_changed_review_tree", "0" * 40 != REVIEW_TREE,
       "wrong tree rejected by exact equality gate")
```

This compares two constants.  It does not construct a changed tree candidate, invoke the
production `git rev-parse`/tree-equality path, or pass the candidate through a shared predicate.
Therefore the primary statement that five mutation catches were exercised is false: the exact
census is **4 genuine + 1 tautological**.  An independent wrong-tree comparison confirms that
the intended exact-equality rule would reject a bad tree, but that cannot retroactively turn the
primary assertion into a real catch proof.

Required amendment: factor or expose the production review-tree equality predicate, pass an
in-memory wrong 40-hex tree candidate through that same predicate, require rejection, rerun the
primary verifier, and rebuild its manifest.  Do not alter the corrected summary, dependency
freeze, original review package, or any scientific result.  Then return to this same verifier.

## Second-verifier machine record

The independent checker records **11 PASS / 1 FAIL**:

- `SECOND_VERIFIER_CHECK.py`:
  `b2f5e39a50dabeac086503cee18ffb6a6aa6d6563ca08348a69df50e5509420f`
- `SECOND_VERIFIER_RAW.jsonl`:
  `8d470e7645bbd51a4c41ebad66b9ba4d623e8b2d102b8c6128f1286355aafc9b`
- `SECOND_VERIFIER_RESULTS.json`:
  `a92dddead5dfc1b7a1806f87c14ee67e1987c27fdbd4656324b722d2d881b28f`

Maximum conclusion: the headline correction and forward 13-dependency freeze are byte-sound,
but the repair evidence package is not second-verifier closed until the fifth primary catch is
real.  No T4, stability work, new science, GPU action, adoption, navigation, git mutation,
physics claim, or canon change is authorized.
