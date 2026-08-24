# G242 append-only banking replay

Date: 2026-08-24

After appending the externally accepted G242 row alongside the already banked G243 row in the live
premise registry, the corrected lineage helper removed exactly those two rows in memory and
reconstructed the preregistered 224-row digest. A fresh repository-relative sealed copy then ran
`verify_package.py --no-write` successfully with bytecode writes disabled.

```text
intake=/tmp/udt_g242_review_c6tf9xez
files_including_scope=25
scope_sha256=e787f563e662f4f5b439d69abba2c54697ffe58f135f68be6c6aca2308997aa3
package_status=PASS
classification=EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN
```

The sealed tree contains exactly the 24 files enumerated by `REVIEW_SCOPE.json` plus the scope file,
with no `__pycache__` directory. This is banking-lineage evidence only and changes no scientific
result. The original externally reviewed intake remains recorded in `TRANSMISSION_RECORD.md`.
