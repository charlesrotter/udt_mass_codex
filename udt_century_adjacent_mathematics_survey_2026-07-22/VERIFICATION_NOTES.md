# Verification Notes

The first manual manifest replay was invoked from repository root even though `MANIFEST.sha256`
contains package-local basenames. `sha256sum` therefore reported 18 files as unreadable. This was an
invocation-path error, not a hash mismatch.

The registered command was corrected to run inside the package directory. The repository-gate
verifier also runs replay with the package as its working directory. That replay passed all entries.

A second correction attempt entered the package directory but retained repository-relative Python
script paths. Those three Python invocations therefore did not execute; the following stale-manifest
replay correctly reported the edited `COMMANDS.md` as mismatched. The build, survey verifier, and
manifest builder were then rerun from repository root, followed by a package-directory hash replay.
All 20 final manifest entries passed.

Both failed invocations are retained here rather than omitted from the audit history.
