# Preregistration commit proof

The data-suitability contract was frozen and pushed before the official DR2 numerical vector was
inspected in this audit.

Exact Git object:

```text
commit 1ed1a3a0001ac9fa99ced02bd422b53c86ef6460
tree f55f3364821ea9b932b095628a43acae8a5c96e6
parent 965906fb042c87c4af272646e23e48bba8eead9f
author Charles Rotter <charles@charlesrotter.com> 1786568213 -0400
committer Charles Rotter <charles@charlesrotter.com> 1786568213 -0400

Preregister BAO data suitability reset

Freeze provenance, covariance, observable-typing, fiducial-map, and no-fit gates before inspecting
the official DESI DR2 measurement vector.
```

The commit contains exactly these six newly added files:

```text
09f0e9942aadac6c3821ec78c5077348180114de  CANDIDATE_LEDGER.tsv
e5e2a8813a66de5a3f045bc43692b48db80be72c  PREREGISTRATION.md
f356ab74ce246d9d8a55ecd7f88ddcc6d21cbdca  SOURCE_MANIFEST.tsv
284e64700fe4749ac2ef887c74b3053d73459d00  STATUS_LEDGER.tsv
a45770afc757288415c52e89d24b0fcc2feaea34  SUITABILITY_GATES.tsv
878e2bb66b6edb91ba9ef9ced6c9bd47327caea6  verify_preregistration.py
```

At the post-review provenance check, the remote returned:

```text
1ed1a3a0001ac9fa99ced02bd422b53c86ef6460  refs/heads/grok
```

The commit and tree hashes make the frozen contents immutable under Git's object identity. The Git
author/committer time is repository provenance, not a separately signed third-party timestamp; this
document does not promote it to one. Its role is to close the review intake's omission of the actual
commit object and remote containment evidence.
