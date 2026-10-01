# TPS1 finite engineering check before production

Same supplied N8 engineering initial g/v and mathematical controls as TPP1,
with wall_seconds:null and new workspace/signatures. No automatic timeout.
Run two-case pause/resume/idempotent completion and third-case actual SIGTERM/
resume, all to t1.1. Compare final fields and saved selected frames to the
unchanged TPP1 engineering evidence; actual original constraints are checked by
the worker and independently in the parent/reviewer checks. Preserve receipts,
source hashes, failures and readable checkpoint/extraction outputs. Use oneGPU,
float64,8GiB allocated cap,16MiB per run and64MiB total smoke area.

Signal when the first COMMITTED artifact appears; stop at a finite case count,
never because elapsed time expired. Parent can manually interrupt on a real
problem. Dedicated runtime CPU guards exercise synthetic elapsed time far past
all former deadlines and confirm ordinary diagnostics/memory/output controls
remain. This is finite operational regression; first3 actual production cases
still need independent original-equation/refinement gates.
