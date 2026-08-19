# G180 review execution boundary

The reviewer could inspect only the sealed intake defined by `REVIEW_SCOPE.json`. It could run
read-only checks with scratch output outside the intake. It could not edit the intake, continue the
research, use web search, inspect the repository, or access protected packages.

The successful run used a read-only intake mount, isolated writable runtime and scratch, a separate
return mount, system runtime and resolver files, and the previously authorized authentication file
mounted read-only. The repository and protected packages were not mounted.
