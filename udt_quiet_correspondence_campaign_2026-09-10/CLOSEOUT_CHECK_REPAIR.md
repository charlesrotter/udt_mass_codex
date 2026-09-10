# Packaging-only status-enumeration correction

The first closeout_check.py run failed, honestly, before its manifest checks:
51 recursively enumerated unrelated untracked file entries were compared with
the baseline's46 DEFAULT-status entries (which can include directory entries).
This was an inconsistent enumeration, not evidence of changed payloads.
The failed final_preservation_checks.{json,stdout,stderr} remains intact.

Original script SHA256:
1f77278b5772375f626620e0246261fd13d70b3ce8be44f4667d261d4e0d2261.
The sole correction removes the extra enumeration flag to match baseline:

```diff
-status = git("status", "--short", "--untracked-files=all").splitlines()
+status = git("status", "--short").splitlines()
```

Reversing that one line reconstructs the complete initial script exactly.
No expected hash/count, payload, scientific check, candidate, test or guard
was changed. The corrected run uses a new final_preservation_checks_corrected
output stem; the original failed receipt is not overwritten. This is packaging
maintenance, not a second scientific repair of QC1 or a QC2 premise change.
Both versions inspect status names only, never protected payload contents.
