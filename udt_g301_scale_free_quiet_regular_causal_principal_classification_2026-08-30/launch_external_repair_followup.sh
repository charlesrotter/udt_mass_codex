#!/usr/bin/env bash
set -euo pipefail

intake=/tmp/udt_g301_repair_followup_flap4lt9
request="$intake/udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/EXTERNAL_REPAIR_FOLLOWUP_REQUEST.md"
codex_binary=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
auth_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g301_repair_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g301_repair_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g301_repair_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g301_repair_external_capture_XXXXXXXX)
mkdir -p "$review_home/.codex"

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

prompt="The sealed repair-follow-up intake is mounted read-only at /intake. Writable ephemeral checks may use /work. Verify only preregistered G301 repairs R1-R5 and the unchanged bounded scientific landing. Inspect only /intake; do not edit evidence files, continue the research, change the scientific question, access any repository or protected package, use web search or unsealed observations, or select a law, field equation, source, action, matter model, scale, history, or X_max. Begin with the G301 external repair-follow-up request and open only the exact intake files required to adjudicate it.\n\n$(<"$request")"
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
exec script -q -e -f -c "$command" "$review_capture/external_repair_followup_transcript.txt" >/dev/null
