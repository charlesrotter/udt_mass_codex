# G256 fresh external adversarial review — gpt-5.4

Original sealed intake: `/tmp/udt_g256_review_l9c4sh0p`  
Original `REVIEW_MANIFEST.tsv` SHA-256:
`bed3e5d67f9cf64732a8e1a3c0fca3a94d5ff53c60774f11d23efe899b92d45a`  
Returned response SHA-256:
`1cf75ca12cfc1c8ceb1e698cfa3813b22a4da6244c9c443bd1a683b0de4bb6bc`

## Grade

`G256_REPAIR_REQUIRED`

## Finding 1 — sealed replay was not self-contained

The sealed package failed its registered `verify_package.py --no-write` command because that script
invoked `/intake/verify_current_scientific_premises.py`, which was not included in the intake. The
builder copied the package and exact 18 scientific sources, but not that repository-wide verifier.

## Retained scientific conclusion

The reviewer directly verified all `43/43` review-manifest payload hashes and all `18/18` source
hashes. The independent exact-Fraction replay passed with anchored rank `N-1`, 220 cycle checks, 100
angular trials, and 14 Hermite trials. All seven hostile mutations were caught.

The reviewer reported no successful refutation of:

- the graph-rank result;
- the angular-tomography classification;
- the arbitrary-`N` Hermite realization argument;
- the owner-bounded conclusion;
- the solver gate.

It found no hidden independent angular condition, circular graph-rank argument, invalid
arbitrary-`N` proof, missed value-law owner within the inspected manifest sources, or overclaim
beyond the stated bounded universe.

## Required repair

Make the sealed replay self-contained by either including the repository-wide verifier and its
dependencies or removing that subprocess from the package verifier. Then distinguish the local
repository premise gate from what is replayable inside the sealed intake and obtain repair-only
follow-up review.
