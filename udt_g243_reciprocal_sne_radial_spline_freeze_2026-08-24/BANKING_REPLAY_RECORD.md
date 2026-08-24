# G243 append-only banking replay

Date: 2026-08-24

After appending the externally accepted G243 row to the premise registry, the corrected intake
builder reconstructed the preregistration registry bytes by removing exactly that one row in
memory. It then ran all four registered no-write commands successfully in a fresh sealed copy.

```text
intake=/tmp/udt_g243_review_g7ccqxuo
files_including_scope_and_manifest=35
scope_sha256=ea9ae685ba72be3395f3f8e2407e3af27ca0ff9ec14ad393fdd668921987a380
manifest_sha256=f7f17f7e9212611db886a515a03b6040344d3d59b63de155a70bce8dd498cedd
```

This is banking-lineage evidence only. It changes no scientific result and does not replace the
original externally reviewed intake recorded in `TRANSMISSION_RECORD.md`.
