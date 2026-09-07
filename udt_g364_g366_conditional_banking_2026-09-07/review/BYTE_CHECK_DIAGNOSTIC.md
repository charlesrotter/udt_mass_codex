# Finite independent-byte-check execution diagnostic

The initial read-only byte check passed registry-byte comparison then failed
when git diff returned128. A separate captured reproduction identifies
`fatal: unable to create threaded lstat: Resource temporarily unavailable`.
The failure is in Git's index preload, not a failed scientific or preservation
assertion. Initial code and complete failed capture streams remain preserved.

Bounded correction: disable Git index preloading for read-only subprocesses
with `-c core.preloadIndex=false`, keeping the512MiB/60-second CPU/wall caps,
same exact comparisons, original files and baseline. Rerun once. No source,
registry, scientific equation, tolerance or assertion is changed. If this
still fails, report the dependent scope check unavailable; no cap increase.
