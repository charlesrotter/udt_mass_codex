# Final verification

Date: 2026-08-10

## Scientific and adversarial gates

- preregistration commit: `1e070e76`
- external-failure/correction preregistration commit: `a589f0a7`
- first external verdict: `TYPE_FAILURE` (accepted and preserved)
- corrected external verdict: `ACCEPT_BRANCH_CONDITIONAL_OWNER_ONLY`
- exact branch-family coverage: 24 by five = 120 unique cells
- complete physical owner rows: zero
- branch-conditional endpoint clock-magnitude owners: R17 and R18 only
- catch proofs: 17/17

## Exact hashes

```text
SOURCE_MANIFEST.tsv                 ebb96da73ffa2a3fbeb081ad1c90a874ef5b2b93a6f4080553c46ddbce3ced3c
DERIVATION_RESULT.json              5c2f5402bbb36c2badbdf1852c795a2860ffb800e7d8100f5a7e89ade61c7926
INDEPENDENT_VERIFICATION_RESULT     7092006cbfeb809e6e15276b20760d0bf6e710bad34e2cb012a950f22800cc76
MAGNITUDE_OWNER_ATLAS.tsv           09beed81dedc8a474d19aecf2894582efe5638309e1d71637095bc928eb31af7
CATCH_PROOFS.tsv                    462aac3a55381869cb9babefb21b7baad7e774fdec84b5d2ace068e745482856
REPOSITORY_GATES.json               18563c511ae887188abb9303e7f0862014ea63e4ad0e83c4f802aa2282c981a8
first external raw output            3d905a6509364044e7a24aef34c26c5d1d9bd790f3da5dcda3921cb0096bdf18
corrected external raw output        4abbac5da08a5310632e54b8494110aaef76a9c8de9ab4cdb8b19103a87f64bd
final sealed-intake tree pre/post     41b4d03f5dafa9e57519d56b4ea022ed9a3124c6086657babda314a310e779bb
```

## Repository gates

- 45/45 current premise guards
- six frozen manifests, 127 members, 133 package paths unchanged
- 1,114 current artifact paths resolve uniquely
- 306 frontier rows / 101 unique targets resolve
- Markdown links checked
- tests: 88 passed, one expected xfail
- protected curvature-atlas contents unread and untouched

The maximum conclusion remains `VERIFIED-WITH-CAVEATS` within the frozen identity/family/regular-
stratum scope. No action, source, matter, bootstrap law, universal `c_eff`, `X_max` value, CMB
spectrum, or GPU work follows.
