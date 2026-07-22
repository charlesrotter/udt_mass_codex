# Repository-link gate correction preregistration

Date: 2026-07-22

After the final clean-archive `PASS-WITH-CAVEATS`, the repository gate failed on Markdown links in
the preserved external-review returns. Those immutable reviews contain auditor-generated absolute
citations of the form:

`/tmp/<historical-clean-worktree>/repo/<repository-relative-path>:<line>`

The generic inherited checker treats the historical temporary path plus line suffix as a current
filesystem target. The linked repository artifacts are present; the ephemeral worktree path is not.

Before mutation, the registered correction is:

1. preserve every external-review raw return and transcript byte-for-byte;
2. reproduce the current-path and frontier-target gates exactly;
3. for an absolute `/tmp/.../repo/<path>:<line>` citation only, strip the historical worktree prefix
   and numeric line suffix, then require `<repository root>/<path>` to exist;
4. retain normal handling for relative links, anchors, and web/mail links;
5. fail closed if the mapped repository path is absent;
6. add an exercised catch that maps such an archival citation to a nonexistent target.

No scientific evidence, package result, navigation control, prior verifier, or historical review may
change. This is a path-resolution correction for immutable provenance citations only.
