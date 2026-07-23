# Fresh Adversarial Review

Date: 2026-07-23

Reviewer: `hygiene_adversary`, fresh zero-context, read-only

Verdict: `VERIFIED-WITH-CAVEATS`

The reviewer independently reproduced:

- 70 covered documents;
- 33 fully compliant documents;
- 37 exact registered backlog documents;
- 88 exact omissions;
- backlog SHA-256
  `a93c4148808d78cfba3171ee1ad00ff440e0909cbdcca00c2c07e47b27776312`;
- ordered path/hash identity SHA-256
  `7a1b9fece4c6aed810e7f29ac703e021ab22310097932092038109bd0fdc381a`;
- all 37 current and base-`9373c156` document hashes;
- three passing hygiene tests; and
- the green full baseline of 70 passed, one expected xfail, and zero failures.

Disposable-copy mutation tests confirmed that the actual pytest guard rejects:

- a new covered but unregistered incomplete document;
- changed bytes in a registered document;
- a duplicate backlog row;
- an enlarged backlog; and
- a corrected document left as a stale exception.

The guard is data-mutation fail-closed, not tamper-proof against deliberate code weakening. Co-editing
the test and all frozen constants can make any editable test accept a new policy. This package
therefore hash-gates the final test and current control files, while code review remains the
authority for an intentional policy change.

Two boundaries are deliberate: documents outside the declared root globs are not covered, and this
hygiene test does not freeze the scientific content of already compliant documents. Repository
scope, frozen manifests, and scientific-package gates perform those separate jobs.

The reviewer changed no repository file.
