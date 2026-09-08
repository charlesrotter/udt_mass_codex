# Reviewer Git mapping diagnostic and bounded repair

The initial independent fidelity child, `independent_fidelity.*`, exited1
after0.152024065s with empty stdout. Its stderr records `git show` exit128:
the original campaign's empty `full356.stderr` blob could not be mapped from
a large Git pack under the declared512MiB address-space cap. This occurred
before completing the original71-blob loop or running hostile fixtures.
The diagnostic is a resource/mapping failure, not a corrupted source or a
failed scientific claim. No PASS is inferred for the unfinished checks.

Keep the initial script and receipt unchanged. A small wrapper changes only
the review helper's Git invocation in memory to set per-process
`core.packedGitWindowSize=16m` and `core.packedGitLimit=64m`. No persistent Git
configuration, resource cap, expected value, source file, fixture, guard or
scientific statement changes. This bounded mapping control is a numerical
implementation choice, not a physical premise. Replay must actually finish
under the original512MiB/60s child limits; otherwise report the remaining
check as unverified. No larger memory allowance is requested or used.
