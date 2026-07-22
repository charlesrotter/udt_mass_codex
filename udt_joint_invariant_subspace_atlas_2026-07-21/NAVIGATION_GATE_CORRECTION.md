# Preregistered Navigation-Gate Correction

Date: 2026-07-21

The first post-Jordan repository-gate run completed the scientific replay, frozen-manifest replay,
and prior-package replay, then stopped at `NAVIGATION: markdown-link`.

The only Markdown link tokens in this package occur in the byte-preserved failed external review.
That review used the workspace renderer's absolute `path:line` target convention.  The inherited
generic navigation checker interprets the trailing `:line` as part of the filesystem filename and
therefore rejects an existing file such as `verify_joint_atlas.py:202`.

The preserved external review must not be rewritten.  Before changing the gate implementation, this
correction registers a package-local navigation validator that retains the inherited 1,114-current-
path and 306-frontier-row checks, scans every package Markdown link, and recognizes a trailing
decimal `:line` suffix only when the underlying target path exists.  It must still reject every
genuinely missing target.  The current/frontier negative controls remain exercised.

No scientific classifier, output row, tolerance, count, premise, or conclusion may change.  The
package manifest and complete repository gate must be rebuilt and rerun after the correction.
