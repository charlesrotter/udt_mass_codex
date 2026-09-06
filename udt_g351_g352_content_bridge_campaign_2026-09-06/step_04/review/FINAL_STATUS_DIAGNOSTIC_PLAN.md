# Final status diagnostic, before retry

The first bounded final git status command exited 128 with exact stderr:
`fatal: unable to create threaded lstat: Resource temporarily unavailable`.
No mathematical check failed. It ran under the generic 512 MiB/60-second
child wrapper. No evidence identifies a scientific, source or repository defect.

Bounded diagnostic: disable only Git's in-memory parallel index preloading
for one read-only status command using command-line -c core.preloadindex=false
and -c index.threads=1. Keep the same address-space/time limits and preserve
the failed command/streams. Do not change Git configuration, stage files,
expand resources, retry numerical work or touch unrelated payloads. If the
retry fails, final status remains unverified by this check.

Maximum conclusion: an operational status-read failure and successful or
unsuccessful serial alternative. Success does not establish exact causal
attribution of the initial system resource error. The solver-first protocol's
finite diagnostic discipline is used; no scientific repair is proposed.
