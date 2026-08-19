# G181 review execution boundary

The reviewer may inspect only the sealed intake defined by `REVIEW_SCOPE.json`. It may run
read-only checks with scratch output outside the intake. It must not edit the intake, continue the
research, use the internet, inspect the repository, or access protected packages.

The intended launch uses a read-only intake mount, isolated writable runtime and scratch, a
separate return mount, system runtime and resolver files, and an explicitly authorized read-only
authentication file. The repository and protected packages are not mounted.
