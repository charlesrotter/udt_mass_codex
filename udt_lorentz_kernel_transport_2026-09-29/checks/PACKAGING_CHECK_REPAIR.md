# Git mapping resource repair

The full normal premise audit passed before this packaging check. The first
completion check failed while Git read an old source blob: the large packfile
could not be mapped under the declared512MiB address-space limit. This is a Git
mapping-resource failure, not a source mismatch or failed scientific assertion.
The original script is preserved as check_completion_initial.py; the exact
failed command, stderr and receipt remain completion_final.*.

The only script repair adds per-command Git core.packedGitWindowSize=16m and
core.packedGitLimit=64m. No repository config, scientific source, test assertion,
accepted integration byte or resource ceiling changes. Re-run uses a fresh
completion_repair output prefix and the same60s/512MiB capture. Its actual
receipt determines success. This is packaging-only repair, not a scientific
repair/re-review cycle or a reason to repeat the successful full premise audit.
