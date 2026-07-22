# Repository-gate archival-link correction preregistration

Date: 2026-07-22

The first final repository-gate run failed only its Markdown-link check. The preserved fresh-review
return contains three absolute citations of the form `/tmp/<immutable-archive>/<repository-path>`.
The checker already normalizes the older `/tmp/.../repo/<repository-path>` form, but not the direct
archive-root form. The cited current repository targets exist; the disposable archive does not.

Before mutation, the correction is frozen as follows:

- preserve the raw review and failed gate transcript byte-identically;
- normalize either disposable-archive spelling to the repository-relative suffix;
- require the normalized target to exist in the clean worktree;
- retain the existing deliberately broken archival-link catch;
- do not weaken checks for ordinary relative links, current paths, or frontier targets;
- do not change scientific results, evidence tables, sources, or maximum conclusion.

The correction passes only if the real archival citations resolve, the deliberately nonexistent
archival citation is still rejected, and every other repository gate remains unchanged.
