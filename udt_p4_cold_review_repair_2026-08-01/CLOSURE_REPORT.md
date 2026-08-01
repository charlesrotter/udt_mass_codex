# Same-second-verifier closure — amended P4 cold-review repair

Date: 2026-08-01

Verdict: **CLOSED-PASS**

The amendment closes the sole defect in the preserved `AMENDMENT-REQUIRED` report.  The two
forward repair products were already byte-sound; the amended primary verifier now supplies the
missing genuine changed-review-tree catch without altering any original primary or second-
verifier record.

## Exact amended-verifier result

`verify_repairs_amended.py` defines one production predicate:

```python
def review_tree_ok(candidate_tree: str, changed_review_paths: list[str]) -> bool:
    return candidate_tree == REVIEW_TREE and not changed_review_paths
```

Independent AST and runtime checks confirm both uses of that exact function:

1. The production gate passes the actual HEAD review tree
   `d1254e1e018d55ead4b57696629163c3d0006db5` and the actual empty changed-path list.
2. The mutation passes `0000000000000000000000000000000000000000` and `[]` through the
   same function and requires rejection.

The saved amended emission records both argument sets and passes **12/12**.  All five mutation
proofs are now genuine: old headline, missing dependency, changed dependency hash, retroactive
promotion, and changed review tree.

## Retained repair gates

- The headline remains exactly the base summary with the false K4 phrase replaced once by the
  screen-character-image `{+1,-1}`/U(1) real-two-torsion wording.  SHA-256:
  `85f5b9e7ce6619ba0b286c71291a3eaee61779fcdb81980c0241d0e24a3b2bb8`.
- The dependency freeze remains **13 = 7 LOAD_BEARING + 6 SUPPORTING**.  Every current and
  review-base byte matches.  Freeze SHA-256:
  `e74b025264d7f1d4bea3dbb383280bcaba76ea113d83114e507e498318f354ac`;
  dependency-manifest SHA-256:
  `58cf2290cf5e4add8597592a17bd7d188c0b4666c694f2a2ee83bac9fccdf6bb`.
- The cold-review tree remains
  `d1254e1e018d55ead4b57696629163c3d0006db5`.  The original 311 inventory and manifest remain
  `a7032b94d91218e64ebfb40d0d31375cdfd75cc297aafabcf33d6617f12a199e`
  and `f150650c940e2d942a455234726ad3e3ce72b20bd175573a65ca0aeea34e8d85`.
- The primary, second-verifier, amended-repair, and 13-dependency manifests all validate.
  Original primary and second-verifier records retain their recorded hashes.
- Changed paths remain confined to `P4_ARC_SUMMARY_2026-07-31.md` and this repair package.
  Scientific-premise guards pass; tests are **70 passed, 1 expected xfail**; no outside
  mutation occurred.
- The forward freeze still says `DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED`.  No retroactive
  preregistration, T4, stability work, new science, GPU action, adoption, navigation, git,
  physics, or canon change is introduced.

## Closure records

The independent closure checker passes **11/11**:

- `CLOSURE_VERIFIER_CHECK.py`:
  `326d81b03b4e177b68749908f02b4dbe051fd305320c328347446441cb29a3c9`
- `CLOSURE_VERIFIER_RAW.jsonl`:
  `10ce6bbbf02875f6dc56afa0a305f283a39b7b60401052fe480965f78f7044ad`
- `CLOSURE_VERIFIER_RESULTS.json`:
  `ba98fcdb048864a471ebb13827dac3261ddc4854d29a4ab39760925ce920c255`

Amended primary hashes:

- `verify_repairs_amended.py`:
  `ffe6d68af4c1983284b8b47920dccb629be994853ad4869d0d1458c5834f6bbc`
- `AMENDED_REPAIR_VERIFIER_RAW.jsonl`:
  `f1ad2f053416c8f7da3867a85ed603e4a14c6946687c7e4930e413300121ca8c`
- `AMENDED_REPAIR_VERIFIER_RESULTS.json`:
  `06c9f4a704edcaf05835ca66a7572c4b95595064b0ec31b9ead90e30ba52ec63`
- `AMENDED_REPAIR_MANIFEST.sha256`:
  `ad3bb083ef94ac76236e9c4ad1b9ad3640f5371abb75c5b456e97c65ede2bd04`

Maximum conclusion: the two preregistered cold-review presentation/provenance repairs are
second-verifier closed.  The underlying P4 arc remains premise-scoped formal response/census
evidence; no response law, action, carrier, mass, coupling, solution, or physical branch is
selected.
