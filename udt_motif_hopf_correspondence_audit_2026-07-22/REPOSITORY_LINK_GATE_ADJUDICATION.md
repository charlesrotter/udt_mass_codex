# Repository-link gate adjudication

Date: 2026-07-22

The initial repository gate failure is accepted as a checker path-resolution defect, not dismissed.
The preserved external-review returns contain absolute citations into their historical temporary
clean worktrees. Their target repository artifacts still exist, but the ephemeral prefixes do not.

The corrected package-local repository verifier:

- preserves every historical review byte-for-byte;
- maps only `/tmp/.../repo/<repository-path>:<numeric-line>` citations to the corresponding current
  repository path;
- retains exact 1,114-current-path and 306-row/101-target frontier gates;
- requires every mapped target to exist; and
- exercises a nonexistent archival-target catch.

Final repository gate: `PASS`. It reports 3,072 identities, 1,618,944 family rows, 143,487
distribution rows, 67,456 covariance comparisons, 63,438 eligible edge comparisons, six frozen
manifests with 127 entries/133 paths, 69 prior packages with 1,864 entries, the documented test
baseline `69 passed / 1 known failed / 1 xfailed`, and the unchanged 54-path dirty metadata hash
`4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c`.
