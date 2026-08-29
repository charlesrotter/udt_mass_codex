#!/usr/bin/env bash
set -euo pipefail

intake=/tmp/udt_g297_repair_followup_592rmkml
request="$intake/udt_g297_complete_pair_causal_dilation_equivalence_2026-08-29/REPAIR_FOLLOWUP_REQUEST.md"
codex_binary=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
auth_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g297_repair_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g297_repair_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g297_repair_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g297_repair_external_capture_XXXXXXXX)
mkdir -p "$review_home/.codex"

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

prompt="The sealed repair-only intake is mounted read-only at /intake. Writable ephemeral checks may use /work. Inspect only /intake; do not edit evidence files or continue the research.\n\n$(<"$request")"
args=(
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
  --ro-bind "$codex_binary" /opt/codex
  --bind "$review_home" /home/udt-admin
  --ro-bind "$auth_file" /home/udt-admin/.codex/auth.json
  --ro-bind "$intake" /intake
  --bind "$review_work" /work
  --bind "$review_return" /return
  --setenv HOME /home/udt-admin
  --setenv CODEX_HOME /home/udt-admin/.codex
  --chdir /return
  /opt/codex exec --ephemeral --ignore-user-config -m gpt-5.4
  -c 'model_reasoning_effort="high"'
  -c 'web_search="disabled"'
  --dangerously-bypass-approvals-and-sandbox --color never
  -o /return/final_response.md
  "$prompt"
)
printf -v command '%q ' "${args[@]}"
exec script -q -e -f -c "$command" "$review_capture/external_review_transcript.txt"
