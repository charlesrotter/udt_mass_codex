# Bounded packaging follow-up

2026-09-27, `/root/archive_review`; same separate, source-exposed context as the
maintenance review. No new scientific review or different-model claim.

**VERIFIED-WITH-CAVEATS for the reviewed packaging scope after two repairs.**
The new README, repair/scope record and source-read ledger distinguish source
exposure, provisional scientific meaning, review limitations and archival
preservation. No additional scientific or permission strengthening was found
in those packaging descriptions. Parent/scientific reviewer read-depth claims
remain attributed; I did not replay their entire source reads.

The initial static review identified two narrow false-pass routes in
`check_integrity.py`, retained in `PACKAGING_INITIAL_REVIEW.json`:

1. **PKG1:** the archive manifest's `source_commit` field was unchecked even
   though blob retrieval used the baseline commit. A wrong per-row provenance
   value could coexist with a PASS. The repair asserts equality to BASELINE HEAD.
2. **PKG2:** a header-only source-pin table could skip every source check and
   still return PASS. The repair requires 41 pins with 41 unique paths for this
   fixed source snapshot.

I inspected the repaired implementation, then ran the actual checker against
isolated copies of its metadata. ROOT and PREFIX remained the real repository
values; only PACKET was redirected to the temporary fixture. Each of the three
negative cases was preceded by a successful positive run using restored original
metadata. Results:

| Injected defect | Actual result |
|---|---|
| Wrong archive source commit | Rejected: `archive source commit mismatch` |
| Empty source-pin table | Rejected: `source pin count mismatch` |
| Duplicate source path, retaining 41 rows | Rejected: `duplicate source pin path` |

All positive controls passed; the source fixtures in the authoritative packet
remained byte-identical. These are maintenance fault controls through the actual
checker, not an independent scientific calculation. The test took less than one
second, used no GPU/scientific subprocess, and did not mutate root sources or
protected payloads. The isolated fixture path and observed Python version are
retained in `PACKAGING_NEGATIVE_CONTROLS.json`. Code, exact command, exit status,
stdout and empty stderr are saved beside this review. Preserve the empty stderr
as a committed artifact rather than relying on filesystem-only presence.

Reviewed packaging hashes:

| Path within continuation | SHA-256 |
|---|---|
| `README.md` | `cd5010b3ebb1363e43e88f51d49f36d1756d20fd0b429dd0f78cb3e3747a698e` |
| `REPAIR_AND_SCOPE.md` | `ef225c671e31da58f1b38e37d26e391498930f00736e86f4c63347a1d6c9fab2` |
| `SOURCE_READ_LEDGER.tsv` | `7c292df5e50e121dc365d6536e316ce2ed97468073e17c4234bf2760da9770a4` |
| `check_integrity.py` | `cd8607d865609de8fa9c8ac993e2a1e8f7febaa0e1c233bbce7a92e7b38dfe68` |

The checker verifies its declared saved paths/bytes and status metadata; it does
not establish scientific truth, complete protected-work backups, every possible
reference, or validity of every old frozen script in a relocated worktree. Its
status parsing is suitable for the present unstaged snapshot and clean committed
form; staged rename porcelain is not a promised execution state. That limitation
does not affect these observed controls or the parent's separate publication
check.

After the initial packaging read, CLOSEOUT was created and the parent's final
full406 run completed. I read the closeout, observed exit `0`, empty stderr and
the `PASS: 406-row premise registry` stdout receipt, and checked every Markdown
link in README/CLOSEOUT. `PACKAGING_LINK_RECEIPT.json` records those observations
and the exact closeout hash. The execution remains attributed to the parent,
not a reviewer rerun. The reported startup result of 371 passed/1 deselected
likewise remains parent evidence.

The final SHA256SUMS manifest and commit/push correspondence remain parent
construction/publication gates. README's manifest description is not evidence
that publication already occurred. The closeout accurately separates its
snapshot from the later external publication receipt. No final publication or
universal archive-readiness claim is made here.
