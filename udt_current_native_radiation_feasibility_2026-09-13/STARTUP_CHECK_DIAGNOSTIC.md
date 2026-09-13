# NR1 startup test-launch diagnostic

The initial startup_active capture exited4 before collection: the repository's
global tests/conftest.py imports torch and CUDA shared libraries, and libcublasLt
could not map inside NR1's2048MiB address-space limit. No startup test ran; no
scientific candidate failure or PASS is inferred. Preserve stdout/stderr/metadata.

Bounded repair: reuse the established SD1 startup command with --noconftest and
exclude the one full-premise nested test, because NR1 already ran the actual
full406 separately in its900s envelope. The startup tests do not need the global
P1/grid/torch fixtures. Do not raise resources, edit runtime configuration,
load a GPU workload or change tests/science. Capture the result, and stop with
a precise infrastructure obstruction if that command also cannot run.
