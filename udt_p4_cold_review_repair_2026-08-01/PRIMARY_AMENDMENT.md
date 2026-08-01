# Primary repair-verifier amendment

Date: 2026-08-01

Status: `AMENDED-PASS-PENDING-SAME-SECOND-VERIFIER-CLOSURE`

The initial primary repair report, verifier, raw record, result, and manifest remain unchanged as
historical evidence. The same second verifier accepted both repair data products but found that the
initial `catch_changed_review_tree` compared two constants instead of exercising the production
tree predicate. Its exact verdict is preserved in `SECOND_VERIFIER_REPORT.md`.

The amended verifier factors the production rule into:

```python
def review_tree_ok(candidate_tree: str, changed_review_paths: list[str]) -> bool:
    return candidate_tree == REVIEW_TREE and not changed_review_paths
```

The real repository tree and changed-path list pass through this predicate. The catch proof now
passes a wrong 40-hex tree through the same predicate and requires rejection. This converts the
catch census from 4 genuine + 1 tautological to 5 genuine mutation tests without changing the
headline, dependency freeze, review evidence, or any scientific result.

Amended verifier result: 12/12 PASS.

- `verify_repairs_amended.py` SHA-256:
  `ffe6d68af4c1983284b8b47920dccb629be994853ad4869d0d1458c5834f6bbc`.
- `AMENDED_REPAIR_VERIFIER_RAW.jsonl` SHA-256:
  `f1ad2f053416c8f7da3867a85ed603e4a14c6946687c7e4930e413300121ca8c`.
- `AMENDED_REPAIR_VERIFIER_RESULTS.json` SHA-256:
  `06c9f4a704edcaf05835ca66a7572c4b95595064b0ec31b9ead90e30ba52ec63`.

All previously verified repair facts and the maximum conclusion remain unchanged. This amendment
authorizes no T4, stability work, adoption, physics, canonization, GPU work, navigation edit, or
repository movement. Closure remains pending the same second verifier.
