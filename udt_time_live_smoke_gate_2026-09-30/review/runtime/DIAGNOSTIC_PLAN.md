# Runtime review diagnostic freeze

Scope: adversarial CPU-only review of SMK1 checkpoint persistence and runner
control flow. Parent owns GPU checks. Parent startup is attributed in
INITIAL_SOURCE_BINDING.json; reviewer independently observed grok at
622d1700d91705320ee17e79ed5fd92bc174d752 and existing unrelated untracked files.
Those payloads were neither read nor changed.

Question: can a malformed committed record, interrupted marker publication, or
constraint-rejected endpoint bypass the stated restart controls? Examine actual
save/load and runner paths, using preserved source snapshots and tiny synthetic
float64 arrays. These are engineering fixtures, not admitted scientific data.

Checks: save/load identity; partial later directory ignored; payload and metadata
corruption rejected; spec mismatch rejected; nonfinite state rejected; tiny output
budget rejected; overwrite and cooperative lock rejected; simulate SIGKILL after
the COMMITTED file is created but before its write; resume a finite but
constraint-violating endpoint using explicitly mocked CUDA entry points mapped to
CPU tensors. The latter is a control-flow counterexample, not CUDA numerics.

Maximum 180 seconds and 2 GiB working data for this diagnostic; no GPU, no installs,
no changes outside review/runtime. Preserve all fixtures, stdout/stderr, exact
command, version and hashes. Stop when these finite checks complete or hit budget.
Maximum conclusion is a concrete operational defect or scoped reviewed engineering
readiness after repair. No scientific result, accepted premise or broader solver
certification follows.
