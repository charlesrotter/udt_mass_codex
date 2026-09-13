# Administrative seal assertion and exact correction

The initial seal command was `PYTHONDONTWRITEBYTECODE=1 python3 udt_signal_chain_banking_2026-09-13/review/seal_final_review.py`.
It exited1 before producing a final receipt:

```
Traceback (most recent call last):
  File "udt_signal_chain_banking_2026-09-13/review/seal_final_review.py", line 21, in <module>
    assert sha(V / 'INITIAL_FINAL_CLOSEOUT.md') == amend['old_closeout_sha256']
AssertionError
```

The assertion incorrectly assumed the reviewer copy preceded the parent amendment.
Actual bytes prove that INITIAL_FINAL_CLOSEOUT.md matches the amended closeout
3c07593ead187cbbc4ab434e23fbed7d3ce86f0b51b725ff68a44f7288987f5b.
The parent's CLOSEOUT_BEFORE_COUNT_CLARIFICATION.md preserves the initial bytes
2ba1044ba3aada8d513e946824f389704c54c65d1b684620ab398ae7b579c5f6,
matching the unchanged original intake. Both copies are preserved as found.
INITIAL_SEAL_SCRIPT.py preserves the failed assertion. The correction checks
these actual correspondences and attributes the reviewer copy to the amended
state. The report is corrected before its first final seal. No scientific,
guard, input, test or source change follows; this is an administrative timing
assumption failure. This command is not an additional scientific capture.
