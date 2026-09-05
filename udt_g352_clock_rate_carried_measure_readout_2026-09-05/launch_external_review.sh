#!/usr/bin/env bash
set -euo pipefail

review_intake=${1:?usage: launch_external_review.sh /tmp/udt_g352_review_PATH}
review_request="$review_intake/udt_g352_clock_rate_carried_measure_readout_2026-09-05/ADVERSARIAL_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g352_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g352_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g352_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g352_external_capture_XXXXXXXX)
mkdir -p "$review_home/.codex"

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a zero-context adversarial mathematical-relativity, null-phase, geometric-measure, functional-equation, and evidence-integrity reviewer. The sealed G352 intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, the exact file set, and every payload. Inspect only /intake; do not edit evidence files, access a repository or protected packages, change the scientific question, or continue the research. Copy the complete intake into /work before running checks. Network access exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Independently reconstruct the exact bounded G352 claim rather than treating executable counts as proof. Attack the supplied phase-admitting fixed-increment and product-crossing-measure assumptions, the repaired sign, phase normalization, observer covariance, p=1 versus universal p, sewing/reversal, and the frequency-integrable caustic measure statement. Do not identify the crossings with light, photons, energy, detector response, distance, source, population, history, matter, scale, X_max, or canon. Run the registered dependency-free checks only in /work. Write the detailed report to /return/EXTERNAL_REVIEW_RESPONSE.md. End it with exactly one token: ACCEPT_G352_BOUNDED_CLOCK_RATE_READOUT, REPAIR_G352_BOUNDED_CLOCK_RATE_READOUT, or REJECT_G352_BOUNDED_CLOCK_RATE_READOUT. In the final response state the token and report path.

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
