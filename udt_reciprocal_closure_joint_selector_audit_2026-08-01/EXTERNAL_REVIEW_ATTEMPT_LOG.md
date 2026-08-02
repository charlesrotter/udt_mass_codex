# External-review attempt log

Date: 2026-08-01

Only `EXTERNAL_ADVERSARIAL_REVIEW.md` is accepted review evidence.

- An initial full-repository attempt was rejected because it spent its context on startup/history
  and did not return a target verdict.
- A first minimal-payload attempt was rejected because it drifted into an unrelated prior package
  and did not produce the designated output file.
- The accepted attempt used only this package and the exact 24 hash-frozen sources copied to a
  temporary read-only payload. It returned the preserved byte-exact verdict with SHA-256
  `a6d8801337c9090f2fc139c6ab80ff0de6c1c1de18ead5dd369f815ca9843345`.

The rejected attempts supplied no scientific ruling and were not used to repair or grade the audit.
