# Publication gate supplemental review

Verdict: the repaired `verify_publication.py` passed the bounded delivery review. This supplement preserves the earlier construction review and seal; it does not replace them or supply scientific evidence.

Reviewer context: `/root/cleanup_dependency_review`, separate from the implementing parent, GPT-6 family (precise runtime identifier not exposed). This reviewer read the implementation before devising the scratch cases. Tests deliberately execute the production verifier with its root redirected to owned temporary repositories; they are adversarial regression checks, not a different implementation or an independent scientific argument. Parent startup and prior reviews remain attributed as documented in `../FINAL_DIRECT_REVIEW.md`.

## Initial finding and repair

The first static inspection found that the publication scope could omit an archive destination while still accepting deletion of its original. Merely matching the deletion list to the archive manifest did not require delivering the archived bytes. Mandatory manifest/verifier interfaces and all owned packet artifacts were also not enforced, regular non-executable file types were not required, and checking only `commit^` could accept a merge with additional parents. These findings were reported to the parent before publication.

The repaired code now requires every unique archive row's exact prefixed destination to be published, the five maintained navigation files and publication interfaces to be present, and the scope to match the owned packet/archive files (excluding `__pycache__`). It requires Git mode `100644`, a regular non-executable working file, exact delivered bytes and SHA-256 membership, and exactly one commit parent equal to the baseline. Duplicate paths and unexpected staged changes are rejected.

The parent repaired the code before the local source capture completed. `REPAIRED_CAPTURE_verify_publication.py` therefore records the repaired version, not the initial faulty implementation. Its SHA-256, also measured on the actual production file before and after the test, is `54dc5bd25b78b24072c11b7a0f4658ebb2e9fa7f84bf09506eba0b82cd2c2ba6`.

## Direct checks

Command: `python3 udt_repository_cleanup_2026-09-27/review/dependencies/publication_gate/check_scratch_git.py`. The script uses real local Git in owned `/tmp/cleanup_publication_real_git_*` fixtures. It does not stage, commit, or alter the index in the actual repository, read protected work, use remote access, or launch scientific checks. Exact results are in `SCRATCH_GIT_RESULT.json`; stdout and empty stderr are retained.

Both healthy states passed: a staged index and a single-parent commit, each delivering twelve fixture files and deleting one original. All fifteen faults were rejected:

- Missing archive destination, missing scope delivery, or omitted owned artifact.
- Wrong archive destination, duplicate archive row, or duplicate required file.
- Executable index mode or a same-byte working symlink.
- Wrong manifest hash or incomplete manifest membership.
- Working bytes changed after staging, an extra staged path, or an original still in the index.
- Wrong sole parent or a merge whose first parent matches the expected baseline.

A final read-only observation found actual repository HEAD `8aac11e13a2311347771e11f507f4f2042ea02a2` and no staged paths. No unresolved defect was found within this bounded publication task.

## Limits and remaining handoff

The gate compares delivery to the sealed working files and exact declared membership. This is correspondence evidence, not external trust, scientific validity, or proof that an arbitrary scope is substantively correct; the independent construction and inventory reviews supply the earlier scope checks. The scratch matrix is targeted, not exhaustive.

Finalize packet reports and closeout before generating `PUBLICATION_SCOPE.json` and `SHA256SUMS.txt`: exact owned-file membership means later packet additions require regenerating the manifests. Run the verifier on the actual staged index and final commit before claiming publication. Parent reports that the full 406-row premise verifier and 384 relevant tests passed; this context did not repeat those runs. Actual staging, commit, and remote verification remain parent responsibilities. Earlier review artifacts and seals are preserved unchanged.
