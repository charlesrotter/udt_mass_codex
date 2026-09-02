#!/usr/bin/env bash
set -euo pipefail

review_intake=/tmp/udt_g325_review_cy_73nsm
review_request="$review_intake/ADVERSARIAL_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g325_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g325_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g325_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g325_external_capture_XXXXXXXX)

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="Act as a fresh zero-context adversarial scientific reviewer. The sealed G325 intake is mounted read-only at /intake. First authenticate REVIEW_SCOPE.json, REVIEW_MANIFEST.tsv, REVIEW_MANIFEST.sha256, and every manifest payload. Inspect only /intake; do not edit evidence files or continue the research. Writable ephemeral checks may use /work. Network access exists solely for Codex API transport; web browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Do not access any repository or protected package. Independently attack mode completeness, constraint propagation, gauge classification, quotient periodicity, curvature witnesses, scalar-mode normalization, controlled-linearization scope, and native provenance. Run the four registered commands literally in a writable ephemeral copy. Write the detailed report to /return/EXTERNAL_REVIEW_RESPONSE.md and end it with exactly one allowed verdict token. In the final response state the token and report path.\n\n$(<"$review_request")"

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
  /opt/codex -a never exec --ephemeral --ignore-user-config --skip-git-repo-check -m gpt-5.4
  -c 'model_reasoning_effort="high"'
  -c 'web_search="disabled"'
  -s danger-full-access --color never
  -o /return/final_response.md
  "$review_prompt"
)
printf -v review_command '%q ' "${review_args[@]}"
exec script -q -e -f -c "$review_command" "$review_capture/external_review_transcript.txt"
