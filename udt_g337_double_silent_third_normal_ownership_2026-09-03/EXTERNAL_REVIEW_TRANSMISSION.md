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

## R1 repair-only follow-up

Charles then authorized the corrected sealed 41-file intake at
`/tmp/udt_g337_repair_followup_p89zzicn` for repair-only review.

Authenticated before launch:

```text
REVIEW_SCOPE.json     7619ac2a92041cc8e6a68af022cdbde7f7bbf93b027694f396bdbc81fcde4c53
REVIEW_MANIFEST.tsv   248232c3534f1dc2fe06d329e352af8e7eee61cb3f2b4089eeb29232bbe44238
detached seal         739620b82134601676f1c4f8ff62c8d06f82a54f2753758377a5c5909a7b4f80
manifest payloads     39 PASS
exact files           41 PASS
```

The external reviewer authenticated the exact intake, ran the direct sealed replay from a clean
writable copy with `git` unavailable, obtained 69/69 aggregate gates, and reproduced the 149-check
production, 26-check independent, 17-mutation hostile, and aggregate outputs byte-for-byte.

Returned verdict:

```text
REPAIRS_ACCEPTED__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED
```

The returned report is preserved byte-exact as `EXTERNAL_REPAIR_FOLLOWUP.md`, SHA-256
`f6e5fd6b862c27c7945e39b93e1cb043a09342bf31e5a345147629b1b8b30d2d`.
