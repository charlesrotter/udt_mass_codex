# G275 external adversarial review

Reviewer: external Codex `gpt-5.4`, high reasoning, fresh ephemeral read-only intake

Date: 2026-08-26

Sealed intake: `/tmp/udt_g275_review_w3q1dmp3`

`REVIEW_SCOPE.json` SHA-256:
`ad7ba5aba15a8a256c238b2fb8f06528c274428ab77e2c4a4b8bd3e5f43bfac8`

`REVIEW_MANIFEST.tsv` SHA-256:
`920a438f67eef0d65a247175a4c0b30b24fe3a150ebe1b678ce324fefb877957`

Final response SHA-256:
`2f1adb5949bd92c2d099df7b113b96dbd6ad91a491476a0d58733d4fdfaa46fd`

## Verdict

`ACCEPT_WITH_REPAIRS`

The reviewer reran all four registered no-write commands. All passed. It found no scientific defect
in the bounded G275 landing and retained it exactly:

```text
W5_PROJECTIVE_POSITION_IS_HOMOTHETY_INVARIANT
__ONE_MATCHED_NONZERO_WEIGHT_ANCHOR_FIXES_ONE_DIMENSIONAL_SCALE
__DIMENSIONFUL_REPRESENTATIVE_RETAINS_FULL_FRAME_CARRY
__XMAX_EQUALS_SCALE_ONLY_AFTER_SEPARATELY_OWNED_POPULATED_BOUNDARY_COMPLETION
```

## Required repairs

1. Make the review-manifest convention explicit and mechanically prove the physical file count,
   listed-payload count, path containment, no extras, and all listed hashes. The original 34-file
   intake contained 33 listed files plus the manifest itself but did not state that nonrecursive
   convention clearly enough.
2. In a sealed intake, make `verify_package.py` fail closed if a frozen source is absent or changed;
   it must never fall back to `git show` or any path outside the intake.
3. Replace tautological catch predicates and the `len([]) == 0` empty-population check with genuine
   executable mutation/scope tests, and align the certification wording with what those tests prove.

These are certification repairs. The reviewer explicitly retained the scientific landing.
