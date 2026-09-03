# G337 external review transmission

Date: 2026-09-03

Charles authorized the sealed 35-file intake at `/tmp/udt_g337_review_ntppktls` for fresh,
read-only external `gpt-5.4` adversarial review, including read-only authentication-file use and
network access solely to launch it.

Authenticated before launch:

```text
REVIEW_SCOPE.json     bf75aba718e6da0cc2f47375cdb9d0b156c5b6bb922f598a773f16bab05d7413
REVIEW_MANIFEST.tsv   d22dd082c4158a2300de5e9dbe80472c6c0f0e968f1a5a16ca11719ca1b99f54
detached seal         608a085c51929ad2505c1de5d89d693f30838209a5ed3bb3b6d09dd313f7cccb
manifest payloads     33 PASS
```

The intake and authentication file were mounted read-only. The reviewer had writable ephemeral
work and return directories, no repository or protected-package mount, and web search disabled.
It authenticated the exact file set and independently rederived the bounded mathematics.

Returned verdict:

```text
ACCEPT_WITH_REPAIRS__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED
```

The mathematical landing was retained. The sole finding was a sealed-replay path-layout defect:
the builder placed frozen sources under `sources/`, while `verify_package.py` expected them at the
copied root and otherwise fell back to unavailable Git history. The reviewer confirmed the same
aggregate verifier passed unchanged after manually restoring that expected layout.
