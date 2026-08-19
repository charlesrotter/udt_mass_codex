# G178 review execution boundary

The reviewer may inspect only the sealed intake defined by `REVIEW_SCOPE.json`. It may execute
read-only checks with scratch output outside the intake. It must not edit files, continue the
research, use the internet, inspect the repository, or access protected packages.

The intake contains the complete banked G176 and G177 packages plus only their exact declared
upstream sources. One historical `AGENTS.md` blob is intentionally taken from commit
`1dadbb04`, exactly as recorded by G177's source-scope clarification; all other banked evidence is
taken from the registered commits listed in `SOURCE_MANIFEST.tsv`.
