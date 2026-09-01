# G311 repair ancestry

The scientific preregistration is commit `ab93cf6e`, whose parent is `8ec52db6`.

The fresh external review record and repair preregistration are frozen at commit `30070cb8`. That
commit precedes every R1--R3 implementation change.

Repository-side ancestry checks were run before building the repair follow-up intake. They are
upstream banking evidence, not part of the intake-self-contained registered replay:

```bash
git show --format= --name-only 30070cb8
git merge-base --is-ancestor ab93cf6e 30070cb8
git show 30070cb8:udt_g311_universal_reciprocity_full_covariant_response_2026-09-01/REPAIR_PREREGISTRATION.md
```

The sealed replay intentionally does not invoke these commands or access Git history.
