#!/usr/bin/env bash
set -euo pipefail

review_intake=${1:?usage: launch_repair_followup.sh /tmp/udt_g352_repair_followup_PATH}
review_request="$review_intake/udt_g352_clock_rate_carried_measure_readout_2026-09-05/REPAIR_FOLLOWUP_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g352_r2_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g352_r2_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g352_r2_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g352_r2_external_capture_XXXXXXXX)
mkdir -p "$review_home/.codex"

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a zero-context repair-only mathematical-relativity, null-phase, geometric-measure, functional-equation, and evidence-integrity reviewer. The sealed G352 R2 follow-up intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, the exact file set, and every payload. Inspect only /intake; do not edit evidence, access a repository or protected packages, change the scientific question, or continue the research. Copy the complete intake into /work before running checks. Network exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Verify only the preregistered R2 continuous-versus-atomic, nonnegative product-measure, explicit-factorization, domain, and evidence-grading repairs and the unchanged conditional R A^-1 landing. Do not promote the chosen realization or owner premise to derived/canon, universalize p=1, suppress p=0 or the atomic/other readouts, or select light, energy, detector, distance, source, population, history, matter, mass, scale, X_max, or canon. Run registered dependency-free checks only in /work. Write the detailed report to /return/EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md. End it with exactly one token: ACCEPT_G352_R2_REPAIR_COMPLETION, REPAIR_G352_R2_REPAIR_COMPLETION, or REJECT_G352_R2_REPAIR_COMPLETION. In the final response state the token and report path.

$(<"$review_request")"

review_args=(
  bwrap --die-with-parent --unshare-all --share-net
  --ro-bind /usr /usr
  --ro-bind /bin /bin
  --ro-bind /lib /lib
  --ro-bind /lib64 /lib64
  --ro-bind /etc /etc
  --ro-bind /run/systemd/resolve /run/systemd/resolve
  --proc /proc
  --dev /dev
  --tmpfs /tmp
  --dir /opt
  --ro-bind "$codex_executable" /opt/codex
  --bind "$review_home" /home/udt-admin
  --ro-bind "$authentication_file" /home/udt-admin/.codex/auth.json
  --ro-bind "$review_intake" /intake
  --bind "$review_work" /work
  --bind "$review_return" /return
  --setenv HOME /home/udt-admin
  --setenv CODEX_HOME /home/udt-admin/.codex
  --chdir /return
  /opt/codex -a never exec --ephemeral --ignore-user-config --skip-git-repo-check -m gpt-5.6-sol
  -c 'model_reasoning_effort="high"'
  -c 'web_search="disabled"'
  -s workspace-write --add-dir /work --color never
  -o /return/final_response.md
  "$review_prompt"
)
printf -v review_command '%q ' "${review_args[@]}"
exec script -q -e -f -c "$review_command" "$review_capture/external_review_transcript.txt"
