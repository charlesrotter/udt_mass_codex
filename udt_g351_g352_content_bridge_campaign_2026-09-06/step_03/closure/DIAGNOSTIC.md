# Bounded closure-check diagnostic

The first check reached pinned archived blob reads, then Git failed to map a
pack file under the inherited 512 MiB address-space cap. It exited 128; the
check wrapper exited 1. Original code and raw stdout/stderr/metadata are saved.
This is a resource/configuration failure, not a hash or mathematical mismatch.

Before replay, retain the same 512 MiB/60 s limits and all exact comparison
targets. Add only per-command Git settings core.packedGitWindowSize=1m and
core.packedGitLimit=64m to bound mapping windows. No repository or persistent
Git configuration is changed. Rerun the same complete membership/byte check.
