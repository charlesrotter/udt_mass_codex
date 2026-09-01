#!/usr/bin/env bash
set -euo pipefail

review_intake=/tmp/udt_g311_review_mw9zyh9c
review_request="$review_intake/udt_g311_universal_reciprocity_full_covariant_response_2026-09-01/EXTERNAL_REVIEW_REQUEST.md"
codex_executable=/home/udt-admin/.codex/packages/standalone/releases/0.144.5-x86_64-unknown-linux-musl/bin/codex
authentication_file=/home/udt-admin/.codex/auth.json

review_home=$(mktemp -d /tmp/udt_g311_external_home_XXXXXXXX)
review_work=$(mktemp -d /tmp/udt_g311_external_work_XXXXXXXX)
review_return=$(mktemp -d /tmp/udt_g311_external_return_XXXXXXXX)
review_capture=$(mktemp -d /tmp/udt_g311_external_capture_XXXXXXXX)

printf 'review_home=%s\nreview_work=%s\nreview_return=%s\nreview_capture=%s\n' \
  "$review_home" "$review_work" "$review_return" "$review_capture"

review_prompt="The sealed G311 intake is mounted read-only at /intake. Writable ephemeral checks may use /work. Inspect only /intake; do not edit evidence files or continue the research. Network access is authorized only for Codex API transport. Internet browsing, web search, downloads, package installation, curl, wget, and network-capable Python calls are prohibited. Independently rederive the result and run registered checks only in a writable ephemeral copy. Do not access the repository or protected packages, use unsealed observations, or select or canonize a response law, history, scale, or X_max.\n\n$(<"$review_request")"

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
