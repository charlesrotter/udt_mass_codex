# Bounded read-only Git resource diagnostic

The first review child `git diff --check c92588ad31f3fd79868378e6e3a318af2de1235f`
returned 128 under the unchanged 512 MiB/60-second resource ceiling. Its stderr:
`fatal: unable to create threaded lstat: Resource temporarily unavailable`.
No diff conclusion follows from that failed invocation.

Retry once with command-local `core.preloadIndex=false` and `index.threads=1`,
under the same cap and with no persistent Git configuration or source edits.
The question is whether the serial read-only check completes and finds whitespace
errors. Success supports that bounded alternative, not a unique causal diagnosis
of the resource failure. Preserve the initial streams and all retry output.
Stop after the retry if it fails; no system tuning, process termination or broader
resource expansion is authorized. The clean full premise audit is not duplicated.
